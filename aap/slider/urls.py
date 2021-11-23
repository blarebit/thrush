"""Slider URLs."""
from django.urls import path

from .views import SliderAPIView

urlpatterns = [
    path("", SliderAPIView, name="slide"),
]
