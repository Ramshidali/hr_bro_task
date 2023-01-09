from django.urls import path, include, re_path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home_product/$', views.home_products, name='home_products'),
    re_path(r'^product/$', views.product_view, name='product_view'),

    re_path(r'^add-cart/(?P<pk>.*)/(?P<qty>.*)/$', views.add_cart, name='add_cart'),
    re_path(r'^remove-from-cart/(?P<pk>.*)/$', views.remove_from_cart, name='remove_from_cart'),
    re_path(r'^increment-cart/(?P<pk>.*)/$', views.increment_cart, name='increment_cart'),
    re_path(r'^decrement-cart/(?P<pk>.*)/$', views.decrement_cart, name='decrement_cart'),
    re_path(r'^cart/$', views.cart, name='cart'),

    re_path(r'^add-address/$', views.add_address, name='add_address'),
    re_path(r'^create-order/$', views.create_order, name='create_order'),
    re_path(r'^payment-gateway/(?P<order_id>.*)/$', views.payment_gateway, name='payment_gateway'),

    re_path(r'^payment-response/(?P<order_id>.*)/$', views.payment_response, name="payment_response"),
    re_path(r'^payments/$',views.payments,name='payments'),
    re_path(r'^payment/(?P<pk>.*)/$',views.payment,name='payment'),
    re_path(r'^payment-success/(?P<order_id>.*)/$', views.payment_success, name="payment_success"),
    re_path(r'^payment-failed/$', views.payment_failed, name="payment_failed"),

    re_path(r'^invoice/(?P<order_id>.*)/$', views.invoice, name="invoice"),

    path('logout/', views.customer_logout, name='logout'),
]