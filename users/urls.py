from django.urls import path
from .views import (
    login,google_callback,
    upload_file_google_drive,list_drive_files,
    download_drive_file,
)

urlpatterns =[
    path("auth/login/",login,name="google_login"),
    path("auth/callback/",google_callback,name="google_callback"),
    path("upload/",upload_file_google_drive,name="upload_file"),
    path("list_drive_files/",list_drive_files,name="list_google_drive_files"),
    path("download_drive_file/<str:file_id>/",download_drive_file,name="download_file"),
]