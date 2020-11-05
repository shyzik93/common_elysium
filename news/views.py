from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from utils.utils import get_success, get_error, get_absent_fields_list
from news.forms import NewsForm
from news.models import NewsArticle


def view_news(request, pk):
    news = get_object_or_404(NewsArticle, pk=pk, active=1)
    context = {
        'page_title': news.title,
        'description': news.description,
        'keywords': 'новости, события',
        'news': news,
        'is_admin': True,
    }
    return render(request, 'news/news.html', context)


def view_all_news(request):    
    newses = NewsArticle.objects.filter(active=1).order_by('-date_create')
    
    context = {
        'page_title':'Статьи',
        'description': 'статьи',
        'keywords': 'статьи,новости, события',
        'newses': newses,
        'is_admin': True,
    }
    
    return render(request, 'news/index.html', context)


def view_edit_news(request, pk=''):
    news = NewsArticle.objects.get(pk=pk) if pk else NewsArticle()
    context = {
        'news': news,
        'page_title': '{} статьи'.format('Редактирование' if news.pk else 'Добавление'),
        'description': '',
        'keywords': '',
    }
    return render(request, 'news/edit.html', context)


@csrf_protect
@require_POST
def view_save_news(request):
    pk = request.POST.get('id')
    try:
        news_article = NewsArticle.objects.get(pk=pk) if pk else None
    except NewsArticle.DoesNotExist as err:
        return HttpResponse(get_error('Новость не существует!'))
    form_news = NewsForm(request.POST, instance=news_article)
    
    if form_news.is_valid():
        form_news.save()
        new_pk = form_news.instance.pk
        current_site = get_current_site(request)
        view_url = '{}://{}{}'.format(settings.SCHEMA, current_site.domain, reverse('view_news', args=[new_pk]))
        answer = get_success(
            'Статья {}'.format('обновлена' if pk else 'добавлена'),
            {'data': {'view_url': view_url, 'id': new_pk}}
        )
    else:
        absent_fields, msg_err = get_absent_fields_list(form_news)
        answer = get_error('Ошибка: {}'.format(msg_err), {'absent_fields': absent_fields})

    return HttpResponse(answer)
