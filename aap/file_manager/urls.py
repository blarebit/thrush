from django.urls import path

from file_manager import FileManager

urlpatterns = [
    path("<path:url_path>", FileManager.as_view()),
    path("", FileManager.as_view()),
]
