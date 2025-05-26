from django.urls import path
from . import views

urlpatterns = [
    path('admin/download/<int:pk>/', views.admin_download_file, name='admin_download_file'),
]
