import os.path
import os
import hashlib

from django.db import models
from django.conf import settings


def md5_by_file_path(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def md5_by_file_object(file_object):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file_object.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def build_file_path(md5hash, ext, subdir=''):
    file_dir = os.path.join('storage_files', subdir, md5hash[:3], md5hash[3:6])
    #abs_file_dir = os.path.join(os.path.dirname(settings.BASE_DIR), settings.STATIC_URL, file_dir)
    abs_file_dir = os.path.join(settings.MEDIA_ROOT, file_dir)
    if not os.path.exists(abs_file_dir):
        os.makedirs(abs_file_dir)
    return os.path.join(file_dir, '{}.{}'.format(md5hash[6:], ext))


def save_uploaded_file(uploaded_instance, subdir=''):
    """
    :param uploaded_instance: объект InMemoryUploadedFile
    """
    name, ext = os.path.splitext(uploaded_instance.name)
    file = StorageFile(
        md5hash = md5_by_file_object(uploaded_instance),
        ext = ext.lower(),
        name = name,
        size = uploaded_instance.size,
        content_type = uploaded_instance.content_type
    )
    file.save()

    #new_file_path = os.path.join(settings.BASE_DIR, settings.STATIC_URL, build_file_path(file.md5hash, file.ext, subdir))
    new_file_path = os.path.join(settings.MEDIA_ROOT, build_file_path(file.md5hash, file.ext, subdir))
    with open(new_file_path, 'wb') as new_file_object:
        for chunk in uploaded_instance.chunks():#read(4096):
            new_file_object.write(chunk)

    return file


class StorageFile(models.Model):
    md5hash = models.CharField(max_length=32)
    ext = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    size = models.IntegerField()
    content_type = models.CharField(max_length=255)
    is_deleted = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['md5hash'])
        ]
        
    def __str__(self, subdir=''):
        file_path = build_file_path(self.md5hash, self.ext, subdir)
        return os.path.join(settings.MEDIA_URL, file_path)


class StorageImage(StorageFile):
    x = models.IntegerField()
    y = models.IntegerField()


class StorageAudio(StorageFile):
    duration = models.IntegerField()
