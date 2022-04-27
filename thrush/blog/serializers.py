"""Blog serializers."""
from account.serializers import UserPublicInfoSerializer, UserSerializer
from django.db.models import Avg
from rest_framework import serializers

from .models import Category, Comment, Post, Star, Tag


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""

    class Meta:
        model = Comment
        read_only_fields = ("is_approved",)
        fields = (
            "id",
            "user",
            "message",
            "reply_to",
            "post",
            "is_approved",
        )
        user_fields = ("id", "url", "email", "first_name", "last_name")

    def to_representation(self, instance):
        """DRF built-in method."""
        serialized_data = super().to_representation(instance)
        serialized_data["user"] = UserSerializer(
            instance=instance.user,
            many=False,
            context={"request": self.context["request"]},
        ).data
        for user_field in serialized_data["user"].copy():
            if user_field not in self.Meta.user_fields:
                del serialized_data["user"][user_field]
        return serialized_data


class StarSerializer(serializers.ModelSerializer):
    """Star serializer."""

    class Meta:
        model = Star
        fields = ("star", "user", "post")


class BookmarkSerializer(serializers.ModelSerializer):
    """Bookmark serializer."""

    post = serializers.PrimaryKeyRelatedField(source="id", read_only=True)

    class Meta:
        model = Post
        fields = ("post",)
        ref_name = "blog"


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="blog:category-detail")

    class Meta:
        model = Category
        fields = (
            "url",
            "id",
            "name",
            "parent",
        )
        ref_name = "blog"


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="blog:tag-detail")

    class Meta:
        model = Tag
        fields = (
            "url",
            "id",
            "name",
        )
        ref_name = "blog"


class PostSerializer(serializers.ModelSerializer):
    """Post serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    stars_average = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    user = UserPublicInfoSerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = (
            "url",
            "id",
            "created_at",
            "modified_at",
            "category",
            "title",
            "brief",
            "slug",
            "tags",
            "comments_count",
            "comments",
            "stars_average",
            "bookmarks_count",
            "content",
            "image",
            "is_draft",
            "previous",
            "user",
            "visited",
        )

    def get_comments_count(self, obj):
        """Get post's comment count."""
        return obj.post_comments.count()

    def get_stars_average(self, obj):
        """Get post's star average."""
        if obj.post_stars.all().aggregate(Avg("star"))["star__avg"]:
            return obj.post_stars.all().aggregate(Avg("star"))["star__avg"]
        else:
            return 0

    def get_bookmarks_count(self, obj):
        """Get post's bookmarks count."""
        return obj.bookmarks.count()

    def to_representation(self, instance):
        """Override tag IDs with tag details."""
        serialized_data = super().to_representation(instance)
        serialized_data["publisher"] = serialized_data.pop("user")
        serialized_data["tags"] = TagSerializer(
            instance=instance.tags,
            many=True,
            context={"request": self.context["request"]},
        ).data
        serialized_data["category"] = CategorySerializer(
            instance=instance.category,
            many=False,
            context={"request": self.context["request"]},
        ).data
        return serialized_data
