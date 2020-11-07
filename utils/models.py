from django.db import models


class StorageImageModel(models.Model):
    md5hash = models.CharField(max_length=32)
    ext = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    local_name = models.CharField(max_length=255, default='')
    is_deleted = models.IntegerField(default=0)