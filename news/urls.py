from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^edit/(?P<pk>[0-9]+)$', views.view_edit_news, name='edit_news'),
    url(r'^edit/$', views.view_edit_news, name='add_news'),
    url(r'^save/$', views.view_save_news, name='save_news'),
    url(r'^(?P<pk>[0-9]+)$', views.view_news, name='view_news'),
    url(r'^$', views.view_all_news, name='all_news'),
]