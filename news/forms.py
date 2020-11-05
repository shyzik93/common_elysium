from django.forms import ModelForm

from news.models import NewsArticle


class NewsForm(ModelForm):
    
    class Meta:
        model = NewsArticle
        fields = ['title', 'description', 'article', 'main_image_link']