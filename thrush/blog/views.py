"""Blog views."""
from base.views import BaseViewSet
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

from base.permissions import ThrushDjangoModelPermissions

from .models import Category, Comment, Post, Star, Tag
from .serializers import (
    BookmarkSerializer,
    CategorySerializer,
    CommentSerializer,
    PostSerializer,
    StarSerializer,
    TagSerializer,
)


class PostViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Post view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    filterset_fields = ("title", "slug", "tags", "is_draft")

    def perform_create(self, serializer):
        """Override post value."""
        if self.kwargs.get("category_pk"):
            category = Category.objects.get(id=self.kwargs["category_pk"])
            serializer.save(category=category, user=self.request.user)
        else:
            serializer.save(user=self.request.user)


class CommentViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Comment view set."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.filter(is_deleted=False, is_approved=True)
    serializer_class = CommentSerializer
    filterset_fields = ("user", "is_approved", "post")

    def get_queryset(self):
        """Only fetch post-related comments."""
        return Comment.objects.filter(post=self.kwargs["post_pk"])

    def perform_create(self, serializer):
        return serializer.save(post=serializer.post, user=self.request.user)


class StarViewSet(BaseViewSet, generics.ListCreateAPIView):
    """Star view set."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        """Attach user ID into a request. Also, handle updating a star."""
        current_star = Star.objects.filter(
            user=self.request.user, post=request.data["post"]
        ).first()
        if not current_star:
            return super().create(request, *args, **kwargs)

        current_star.star = request.data["star"]
        current_star.save()
        return Response(StarSerializer(instance=current_star).data)


class BookmarkViewSet(BaseViewSet, generics.ListCreateAPIView, generics.DestroyAPIView):
    """Bookmark view set."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all().only("id", "bookmarks")
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        """Only fetch bookmark-related posts."""
        return Post.objects.filter(bookmarks=self.request.user)

    def create(self, request, *args, **kwargs):
        """Attach user ID into a request."""
        try:
            self.get_queryset().get(id=request.data["post"])
            return Response(
                data={
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "code": status.HTTP_400_BAD_REQUEST,
                    "detail": "The post already bookmarked.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Post.DoesNotExist:
            post = Post.objects.get(id=request.data["post"])
            post.bookmarks.add(self.request.user)
        return Response(
            data={
                "status_code": status.HTTP_201_CREATED,
                "code": status.HTTP_201_CREATED,
                "detail": "Bookmark created.",
            },
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs):
        """DRF built-in method."""
        try:
            # FIXME: maybe it's needed to make it more consistent, like 'post' instead of 'pk'?
            post = Post.objects.get(id=kwargs["pk"])
        except Post.DoesNotExist:
            return Response(
                data={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "code": status.HTTP_404_NOT_FOUND,
                    "detail": "Post not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if post.bookmarks.filter(post_bookmarks__bookmarks=self.request.user).exists():
            post.bookmarks.remove(self.request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            data={
                "status_code": status.HTTP_404_NOT_FOUND,
                "code": status.HTTP_404_NOT_FOUND,
                "detail": "Bookmark not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class MyBookmarkViewSet(viewsets.ReadOnlyModelViewSet):
    """User bookmarks viewset."""

    permission_classes = [permissions.IsAuthenticated, ThrushDjangoModelPermissions]
    queryset = Post.objects.all().only("id", "bookmarks")
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.queryset.filter(bookmarks=self.request.user)

    def get_object(self):
        """DRF built-in method.

        Only return the current logged-in user object.
        """
        return self.request.user


class TagViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Tag view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Tag.objects.filter(is_deleted=False)
    serializer_class = TagSerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)


class CategoryViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Category view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    alternative_lookup_field = "name"
    filterset_fields = ("name",)
