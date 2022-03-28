"""File manager package URL."""
from django.urls import path

from .views import FileAPIView

urlpatterns = [
    path("<path:path>", FileAPIView.as_view()),
    path("", FileAPIView.as_view()),
]
