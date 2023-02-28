from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^campaign/edit/(?P<pk>[0-9]+)$', views.edit_campaign, name='edit_campaign'),
    url(r'^campaign/edit$', views.edit_campaign, name='add_campaign'),
    url(r'^campaign/save$', views.save_campaign, name='save_campaign'),
    url(r'^campaign/$', views.select_campaign, name='door2door'),

    url(r'^campaign-(?P<campaign_pk>[0-9]+)/street/edit/(?P<pk>[0-9]+)$', views.edit_street, name='edit_street'),
    url(r'^campaign-(?P<campaign_pk>[0-9]+)/street/edit$', views.edit_street, name='add_street'),
    url(r'^campaign/street/save$', views.save_street, name='save_street'),
    url(r'^campaign-(?P<campaign_pk>[0-9]+)/street$', views.select_street, name='select_street'),

    url(r'^campaign/street-(?P<street_pk>[0-9]+)/building/edit/(?P<pk>[0-9]+)$', views.edit_house, name='edit_house'),
    url(r'^campaign/street-(?P<street_pk>[0-9]+)/building/edit/$', views.edit_house, name='add_house'),
    url(r'^campaign/street/building/save$', views.save_house, name='save_house'),
    url(r'^campaign/street-(?P<street_pk>[0-9]+)/building$', views.select_house, name='select_house'),

    url(r'^campaign/street-(?P<street_pk>[0-9]+)/building-(?P<house_pk>[0-9]+)/flat/edit/(?P<pk>[0-9]+)$', views.edit_house, name='edit_flat'),
    url(r'^campaign/street-(?P<street_pk>[0-9]+)/building-(?P<house_pk>[0-9]+)/flat/edit/$', views.edit_house, name='add_flat'),
    url(r'^campaign/street/building/flat/save/$', views.save_house, name='save_flat'),
    url(r'^campaign/street-(?P<street_pk>[0-9]+)/building-(?P<house_pk>[0-9]+)/flat$', views.select_house, name='select_flat'),

    url(r'^reaction/(?P<pk>[0-9]+)$', views.reaction, name='reaction'),
    url(r'^reaction/save_comment/(?P<pk>[0-9]+)$', views.save_reaction_comment, name='save_reaction_comment'),
    url(r'^reaction/save_reaction/(?P<pk>[0-9]+)$', views.save_reaction, name='save_reaction'),
]