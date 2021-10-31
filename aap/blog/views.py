"""Blog views."""

from rest_framework import permissions, generics, status
from rest_framework.response import Response

from base.views import BaseViewSet
from .models import Post, Tag, Star, Category, Comment
from .serializers import (
    PostSerializer,
    TagSerializer,
    StarSerializer,
    CategorySerializer,
    CommentSerializer,
    BookmarkSerializer,
)


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


class CategoryViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Category view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Category.objects.filter(is_deleted=False)
    serializer_class = CategorySerializer
    alternative_lookup_field = "name"


class PostViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Post view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        """DRF built-in method.

        Attach user ID into a request.
        """
        request.data["user"] = self.request.user.id
        return super().create(request, *args, **kwargs)


class CommentViewSet(
    BaseViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """Comment view set."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.filter(is_deleted=False, is_approved=True)
    serializer_class = CommentSerializer

    def get_queryset(self):
        """DRF built-in method.

        Only fetch post-related comments.
        """
        return Comment.objects.filter(post=self.kwargs["post_pk"])

    def create(self, request, *args, **kwargs):
        """DRF built-in method.

        Attach user ID and post ID into a request.
        """
        request.data["user"] = self.request.user.id
        request.data["post"] = kwargs.pop("post_pk")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """DRF built-in method.

        Attach user ID and post ID into a request.
        """
        request.data["user"] = self.request.user.id
        request.data["post"] = kwargs.pop("post_pk")
        return super().update(request, *args, **kwargs)


class StarViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
):
    """Star view set."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = Star.objects.all()
    serializer_class = StarSerializer

    def create(self, request, *args, **kwargs):
        """DRF built-in method.

        Attach user ID into a request. Also, handle updating a star.
        """
        request.data["user"] = self.request.user.id
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
        """DRF built-in method.

        Only fetch bookmark-related posts.
        """
        return Post.objects.filter(bookmarks=self.request.user)

    def create(self, request, *args, **kwargs):
        """DRF built-in method.

        Attach user ID into a request.
        """
        request.data["user"] = self.request.user.id
        try:
            self.get_queryset().get(id=request.data["post"])
            return Response(
                data={"message": "the post already bookmarked."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Post.DoesNotExist:
            post = Post.objects.get(id=request.data["post"])
            post.bookmarks.add(self.request.user)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        """DRF built-in method."""
        try:
            post = Post.objects.get(id=kwargs["pk"])
        except Post.DoesNotExist:
            return Response(
                data={"message": "post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if post.bookmarks.filter(bookmarks__bookmarks=self.request.user).exists():
            post.bookmarks.remove(self.request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            data={"message": "bookmark not found"}, status=status.HTTP_404_NOT_FOUND
        )
