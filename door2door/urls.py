from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^edit_campaign/(?P<pk>[0-9]+)$', views.edit_campaign, name='edit_campaign'),
    url(r'^edit_campaign/$', views.edit_campaign, name='add_campaign'),
    url(r'^save_campaign/$', views.save_campaign, name='save_campaign'),
    url(r'^select_campaign/$', views.select_campaign, name='door2door'),

    url(r'^edit_street/(?P<campaign_pk>[0-9]+)/(?P<pk>[0-9]+)$', views.edit_street, name='edit_street'),
    url(r'^edit_street/(?P<campaign_pk>[0-9]+)/$', views.edit_street, name='add_street'),
    url(r'^save_street/$', views.save_street, name='save_street'),
    url(r'^select_street/(?P<campaign_pk>[0-9]+)$', views.select_street, name='select_street'),

    url(r'^edit_house/(?P<street_pk>[0-9]+)/(?P<pk>[0-9]+)$', views.edit_house, name='edit_house'),
    url(r'^edit_house/(?P<street_pk>[0-9]+)/$', views.edit_house, name='add_house'),
    url(r'^save_house/$', views.save_house, name='save_house'),
    url(r'^select_house/(?P<street_pk>[0-9]+)$', views.select_house, name='select_house'),

    url(r'^edit_flat/(?P<street_pk>[0-9]+)/(?P<house_pk>[0-9]+)/(?P<pk>[0-9]+)$', views.edit_house, name='edit_flat'),
    url(r'^edit_flat/(?P<street_pk>[0-9]+)/(?P<house_pk>[0-9]+)$', views.edit_house, name='add_flat'),
    url(r'^save_flat/$', views.save_house, name='save_flat'),
    url(r'^select_flat/(?P<street_pk>[0-9]+)/(?P<house_pk>[0-9]+)$', views.select_house, name='select_flat'),

    url(r'^reaction/(?P<pk>[0-9]+)$', views.reaction, name='reaction'),
]