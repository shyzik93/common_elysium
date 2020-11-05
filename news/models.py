from django.db import models


class NewsArticle(models.Model):
    date_create = models.DateTimeField(auto_now_add=True)
    date_modify = models.DateTimeField(auto_now_add=True)
    #created_by = None
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=512)
    article = models.TextField(max_length=40960)
    main_image_link = models.IntegerField(null=True, blank=True)
    active = models.IntegerField(default=1, blank=True)
