"""Slider serializers."""
from rest_framework import serializers

from .models import Slide


class SlideSerializer(serializers.ModelSerializer):
    """Slide serializer."""

    class Meta:
        model = Slide
        read_only_fields = ("is_approved",)
        fields = (
            "title",
            "content",
            "image",
            "is_draft",
            # "visited",
            "order",
            "link",
            "created_at",
            "modified_at",
            "is_approved",
            "start_time",
            "expire_time",
        )
