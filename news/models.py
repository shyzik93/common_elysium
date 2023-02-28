from django.db import models

from utils.models import StorageFile


class NewsArticle(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now_add=True)
    active = models.IntegerField(default=1, blank=True, verbose_name='Активна')
    #created_by = None
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    article = models.TextField(max_length=40960)
    main_image_link = models.ForeignKey(StorageFile, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Заглавная картинка')
