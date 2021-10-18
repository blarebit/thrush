"""Blog serializers."""
from rest_framework import serializers

from .models import Post, Tag, Star, Category, Comment


class TagSerializer(serializers.ModelSerializer):
    """Tag data serializer."""

    class Meta:
        model = Tag
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Test data serializer."""

    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    """Post data serializer."""

    tags = TagSerializer(read_only=True, many=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = "__all__"


class StarSerializer(serializers.ModelSerializer):
    """Star data serializer."""

    class Meta:
        model = Star
        fields = "__all__"


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark data serializer."""

    class Meta:
        model = Post
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """Bookmark data serializer."""

    class Meta:
        model = Category
        fields = "__all__"
