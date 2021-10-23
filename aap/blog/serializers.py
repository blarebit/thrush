"""Blog serializers."""

from rest_framework import serializers
from django.db.models import Avg

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


class PostSerializer(serializers.ModelSerializer):
    """Post data serializer."""

    comments = CommentSerializer(many=True, read_only=True)
    stars = StarSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    stars_avg = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "created_at",
            "modified_at",
            "category",
            "title",
            "brief",
            "slug",
            "bookmark",
            "tags",
            "comments_count",
            "comments",
            "stars",
            "stars_avg",
            "is_deleted",
            "content",
            "image",
            "is_draft",
            "previous",
            "publisher",
            "visited",
        ]

    def get_comments_count(self, obj):
        """Get post's comment count."""
        return obj.comments.all().count()

    def get_stars_avg(self, obj):
        """Get post's star average."""
        if obj.stars.all().aggregate(Avg("star"))["star__avg"]:
            return obj.stars.all().aggregate(Avg("star"))["star__avg"]
        else:
            return 0
