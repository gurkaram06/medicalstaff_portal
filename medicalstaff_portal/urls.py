# URL Configuration for Medical Staff Noticeboard Portal - Updated by Tarun

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portalapp.urls')),
]
