"""Slideshow views."""
from rest_framework import permissions, generics, viewsets

from .models import SlideShow, GroupSlideShow
from .serializers import SlideShowSerializer, GroupSlideShowSerializer


class GroupSlideShowViewSet(
    viewsets.GenericViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveUpdateDestroyAPIView,
):
    """GroupSlideShow view set."""

    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    queryset = GroupSlideShow.objects.filter(is_deleted=False)
    serializer_class = GroupSlideShowSerializer


class SlideShowViewSet(
    viewsets.GenericViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveUpdateDestroyAPIView,
):
    """SlideShow view set."""

    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = SlideShowSerializer

    def get_queryset(self):
        return SlideShow.objects.filter(is_deleted=False, group_slideshow=self.kwargs["group_pk"])

    def perform_create(self, serializer):
        """Override group_slideshow value."""
        group_slideshow = GroupSlideShow.objects.get(id=self.kwargs["group_pk"])
        serializer.save(group_slideshow=group_slideshow)
