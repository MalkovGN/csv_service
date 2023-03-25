from django.urls import path

from import_api import views


urlpatterns = [
    path('upload_file/', views.UploadView.as_view()),
    path('files_info/', views.AllFilesView.as_view()),
    path('file/<int:pk>/', views.FileInfoView.as_view()),
]
