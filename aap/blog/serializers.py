"""Blog serializers."""
from django.db.models import Avg
from rest_framework import serializers

from account.serializers import UserSerializer
from .models import Post, Tag, Star, Category, Comment


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
        )


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""

    # url = relations.NestedHyperlinkedIdentityField(
    #     view_name="blog:post-comment-detail",
    #     parent_lookup_kwargs={"post_pk": "post__pk"}
    # )

    class Meta:
        model = Comment
        read_only_fields = ("is_approved",)
        fields = (
            # "url",
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


class CategorySerializer(serializers.ModelSerializer):
    """Bookmark serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="blog:category-detail")

    class Meta:
        model = Category
        fields = (
            "url",
            "id",
            "name",
            "parent",
        )


class PostSerializer(serializers.ModelSerializer):
    """Post serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="blog:post-detail")
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    stars_average = serializers.SerializerMethodField()
    bookmarks_count = serializers.SerializerMethodField()
    publisher = serializers.PrimaryKeyRelatedField(source="user", read_only=True)

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
            "publisher",
            "visited",
        )

    def get_comments_count(self, obj):
        """Get post's comment count."""
        return obj.comments.count()

    def get_stars_average(self, obj):
        """Get post's star average."""
        if obj.stars.all().aggregate(Avg("star"))["star__avg"]:
            return obj.stars.all().aggregate(Avg("star"))["star__avg"]
        else:
            return 0

    def get_bookmarks_count(self, obj):
        """Get post's bookmarks count."""
        return obj.bookmarks.count()

    def to_representation(self, instance):
        """Override tag IDs with tag details."""
        serialized_data = super().to_representation(instance)
        serialized_data["tags"] = TagSerializer(instance=instance.tags, many=True).data
        return serialized_data
