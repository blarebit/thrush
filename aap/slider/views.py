"""Slider views."""
from rest_framework import permissions, generics

from base.views import BaseViewSet
from .models import Slide
from .serializers import SlideSerializer


class SliderAPIView(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Slide view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Slide.objects.filter(is_deleted=False)
    serializer_class = SlideSerializer
    alternative_lookup_field = "title"
