from rest_framework import serializers

from . import models


class UploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = models.FileModel
        fields = ('file',)


class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FileInfo
        fields = ('name', 'columns')
