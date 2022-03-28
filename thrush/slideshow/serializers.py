"""Slideshow serializers."""
from rest_framework import serializers

from base.serializers import ContentTypeLinkModelSerializer
from .models import SlideShow, GroupSlideShow


class GroupSlideShowSerializer(serializers.ModelSerializer):
    """GroupSlideShow serializer."""

    # url = serializers.HyperlinkedIdentityField(view_name="slideshow:group-detail")

    class Meta:
        model = GroupSlideShow
        exclude = ("is_deleted",)


class SlideShowSerializer(ContentTypeLinkModelSerializer):
    """SlideShow serializer."""

    # url = serializers.HyperlinkedIdentityField(view_name="slideshow:slideshow-detail")

    class Meta:
        model = SlideShow
        exclude = ("is_deleted", "group_slideshow")
