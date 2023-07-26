import csv
import pandas as pd

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from . import serializers, models
from csv_import import settings


class UploadView(generics.ListCreateAPIView):
    serializer_class = serializers.UploadSerializer

    def list(self, request, *args, **kwargs):
        return Response(
            'You can attach a file below. '
            'Choose an HTML form to have a select button.'
        )

    def create(self, request, *args, **kwargs):
        uploaded_csv = request.FILES['file']
        content_type = uploaded_csv.content_type
        file_name = str(uploaded_csv).split('/')[-1]
        extension = file_name.split('.')[-1]
        if extension != 'csv':
            return Response(
                f'You can upload only csv files. The file format you uploaded is .{extension}',
                status=status.HTTP_400_BAD_REQUEST,
            )
        file = models.FileModel.objects.create(
            file=uploaded_csv,
        )
        file.save()
        models.FileInfo.objects.create(
            name=file_name,
            file_id=file.pk,
        ).save()
        return Response(f'You uploaded a {content_type} file', status=status.HTTP_201_CREATED)


class AllFilesView(generics.GenericAPIView):
    serializer_class = serializers.FileInfoSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]

    def get(self, request, *args, **kwargs):
        response = []
        files = models.FileModel.objects.all()
        for file in files:
            file_name = file.file.name
            with open(f"{settings.MEDIA_ROOT}/{file_name}", 'r') as new_file:
                csv_reader = csv.reader(new_file)
                columns = next(csv_reader)
                response.append(
                    {
                        'id': file.pk,
                        'name': file_name.split('/')[-1],
                        'columns': columns,
                    }
                )
        return Response({'files': response})


class FileInfoView(generics.GenericAPIView):
    serializer_class = serializers.FileInfoSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request, pk):
        file = models.FileModel.objects.get(pk=pk)
        file_name = file.file.name
        column_info = {}
        query_param = self.request.query_params.get('columns')
        if query_param is not None:
            query_list = query_param.split(',')
            df = pd.read_csv(f'{settings.MEDIA_ROOT}/{file_name}')
            sorted_df = df.sort_values(by=query_list)
            sorted_df.to_csv(f'{settings.MEDIA_ROOT}/{file_name}', index=False)
        with open(f"{settings.MEDIA_ROOT}/{file_name}", 'r') as f:
            csv_reader = csv.reader(f)
            for idx, row in enumerate(csv_reader):
                if idx == 0:
                    columns = row
                    counter = 0
                    while counter < len(columns):
                        column_info[f'{columns[counter]}'] = []
                        counter += 1
                else:
                    data = row
                    counter = 0
                    while counter < len(data):
                        column_info[f'{columns[counter]}'].append(
                            {
                                'row': idx,
                                'value': data[counter]
                            }
                        )
                        counter += 1

        return Response(
            {
                'name': file_name.split('/')[-1],
                'data': column_info,
            }
        )

    def delete(self, request, pk):
        file = models.FileModel.objects.get(pk=pk)
        file_name = file.file.name
        file.delete()
        return Response(f'File {file_name.split("/")[-1]} was deleted successfully!')
