"""Base serializers."""
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Tag, Category


class ContentTypeLinkModelSerializer(serializers.ModelSerializer):
    """ContentTypeLink model serializer implementation."""

    link_details = serializers.SerializerMethodField()

    def get_link_details(self, obj):
        """Serialize link details based on loaded serializers."""
        instance = obj.link_type.model_class().objects.get(id=obj.link)
        instance_serializer_name = f"{instance.__class__.__name__}Serializer"
        if instance_serializer_name in settings.SERIALIZERS:
            instance_serializer = settings.SERIALIZERS[instance_serializer_name]
            return instance_serializer(
                instance=instance, context={"request": self.context["request"]}
            ).data
        return obj.link


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:category-detail")

    class Meta:
        model = Category
        fields = (
            "url",
            "id",
            "name",
            "parent",
        )
        ref_name = "category"


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
        )
        ref_name = "tag"
