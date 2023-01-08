from django.contrib import admin
from django.views.static import serve
from django.urls import include, path, re_path
from django.contrib.auth.views import LogoutView

from mechion_test import settings
from main import views as general_views
from web import views as web_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/accounts/', include('registration.backends.default.urls')),

    # admin panel
    path('admin-panel/',include(('main.urls'),namespace='main')),
    path('app/',general_views.app,name='app'),

    path('product/',include(('product.urls'),namespace='product')),

    # web
    path('', web_views.home, name='home'),
    path('web/',include(('web.urls'),namespace='web')),
    path('login/', web_views.customer_join, name='login'),

    path('social-auth/', include('social_django.urls', namespace='social')),
    # path('logout/', LogoutView.as_view()),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
