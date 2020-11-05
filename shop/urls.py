from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<product_id>[0-9]+)-(?P<title_code>[0-9a-z-]+)$', views.view_product, name='shop-product'),
    url(r'', views.view_products, name='shop'),
]