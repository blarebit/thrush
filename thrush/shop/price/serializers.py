"""Price serializers."""
from rest_framework import serializers

from .models import Price


class PriceSerializer(serializers.ModelSerializer):
    """Price serializer."""

    class Meta:
        model = Price
        # readonly_fields = ["inventory"]
        fields = (
            "id",
            "product",
            "inventory",
            "price",
            "discount",
            "start",
            "end",
        )

