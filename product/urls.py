from django.urls import path, re_path
from . import views

app_name = 'product'

urlpatterns = [
    path('brand/', views.brands, name='brand'),
    re_path(r'^create-brand/$', views.create_brand, name='create_brand'),
    re_path(r'^edit-brand/(?P<pk>.*)/$', views.edit_brand, name='edit_brand'),
    re_path(r'^delete-brand/(?P<pk>.*)/$', views.delete_brand, name='delete_brand'),

    path('product-list/', views.product_list, name='product_list'),
    re_path(r'^product-details/(?P<pk>.*)/$', views.product_details, name='product_details'),
    re_path(r'^create-product/$', views.create_product, name='create_product'),
    re_path(r'^edit-product/(?P<pk>.*)/$', views.edit_product, name='edit_product'),
    re_path(r'^delete-product/(?P<pk>.*)/$', views.delete_product, name='delete_product'),
]