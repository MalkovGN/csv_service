from django.contrib import admin

from . import models


admin.site.register(models.FileModel)

admin.site.register(models.FileInfo)
