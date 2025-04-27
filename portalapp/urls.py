#Updated UI for notice and login error message box and updating in this file by Chetan Kumar

from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('post_notice/', views.post_notice_view, name='post_notice'),
    path('register/', views.register_view, name='register'),
    path('edit_notice/<int:notice_id>/', views.edit_notice_view, name='edit_notice'),
    path('delete_notice/<int:notice_id>/', views.delete_notice_view, name='delete_notice'),
]
