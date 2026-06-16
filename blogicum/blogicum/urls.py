"""Главные URL-маршруты проекта."""

from django.contrib import admin
from django.urls import include, path


admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Блогикум'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('blog.urls', namespace='blog')),
]
