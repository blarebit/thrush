"""Product views."""
from product.serializers import CategorySerializer, TagSerializer, AudioBookBookmarkSerializer,\
    PaperBookBookmarkSerializer
from base.models import Tag, Category, Product
from product.models import PaperBook, AudioBook
from base.views import BaseViewSet
from rest_framework import permissions, generics, status
from rest_framework.response import Response


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


class AudioBookBookmarkViewSet(BaseViewSet, generics.ListCreateAPIView, generics.DestroyAPIView):
    """Bookmark view set."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = AudioBook.objects.all().only("id", "bookmarks")
    serializer_class = AudioBookBookmarkSerializer

    def get_queryset(self):
        """Only fetch bookmark-related posts."""
        return AudioBook.objects.filter(bookmarks=self.request.user)

    def create(self, request, *args, **kwargs):
        """Attach user ID into a request."""
        request.data["user"] = self.request.user.id
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
        except AudioBook.DoesNotExist:
            post = AudioBook.objects.get(id=request.data["post"])
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
            post = AudioBook.objects.get(id=kwargs["pk"])
        except AudioBook.DoesNotExist:
            return Response(
                data={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "code": status.HTTP_404_NOT_FOUND,
                    "detail": "Post not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if post.bookmarks.filter(bookmarks__bookmarks=self.request.user).exists():
            post.bookmarks.remove(self.request.user)
            return Response(
                data={
                    "status_code": status.HTTP_204_NO_CONTENT,
                    "code": status.HTTP_204_NO_CONTENT,
                    "detail": "Bookmark removed.",
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            data={
                "status_code": status.HTTP_404_NOT_FOUND,
                "code": status.HTTP_404_NOT_FOUND,
                "detail": "Bookmark not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )


class PaperBookBookmarkViewSet(BaseViewSet, generics.ListCreateAPIView, generics.DestroyAPIView):
    """Bookmark view set."""

    permission_classes = [permissions.IsAuthenticated]
    queryset = PaperBook.objects.all().only("id", "bookmarks")
    serializer_class = PaperBookBookmarkSerializer

    def get_queryset(self):
        """Only fetch bookmark-related posts."""
        return PaperBook.objects.filter(bookmarks=self.request.user)

    def create(self, request, *args, **kwargs):
        """Attach user ID into a request."""
        request.data["user"] = self.request.user.id
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
        except PaperBook.DoesNotExist:
            post = PaperBook.objects.get(id=request.data["post"])
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
            post = PaperBook.objects.get(id=kwargs["pk"])
        except PaperBook.DoesNotExist:
            return Response(
                data={
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "code": status.HTTP_404_NOT_FOUND,
                    "detail": "Post not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if post.bookmarks.filter(bookmarks__bookmarks=self.request.user).exists():
            post.bookmarks.remove(self.request.user)
            return Response(
                data={
                    "status_code": status.HTTP_204_NO_CONTENT,
                    "code": status.HTTP_204_NO_CONTENT,
                    "detail": "Bookmark removed.",
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            data={
                "status_code": status.HTTP_404_NOT_FOUND,
                "code": status.HTTP_404_NOT_FOUND,
                "detail": "Bookmark not found.",
            },
            status=status.HTTP_404_NOT_FOUND,
        )
