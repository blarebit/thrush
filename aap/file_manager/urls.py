"""File manager package URL."""
from django.urls import path

from .views import FileManager

urlpatterns = [
    path("media/", FileManager.as_view()),
    path("media/<path:path>", FileManager.as_view()),
]
