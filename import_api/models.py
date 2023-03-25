from django.db import models


class FileModel(models.Model):
    file = models.FileField(upload_to='media', null=True, blank=True)

    def __str__(self):
        return str(self.file).split('/')[-1]


class FileInfo(models.Model):
    name = models.CharField(max_length=64)
    columns = models.JSONField(null=True, blank=True)
    file = models.ForeignKey(FileModel, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
