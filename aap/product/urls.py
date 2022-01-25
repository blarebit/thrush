"""Product URLs."""
from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from .views import (
    AudioBookViewSet,
    AudioIndexViewSet,
    AudioTypeViewSet,
    BookAuthorViewSet,
    AudioBookBookmarkViewSet,
    PaperBookBookmarkViewSet,
    BookSpeakerViewSet,
    CategoryViewSet,
    CompatibleDeviceViewSet,
    PublisherViewSet,
    TagViewSet,
    PaperBookViewSet,
)

router = routers.DefaultRouter()
router.register("tags", TagViewSet, basename="tag")
router.register("categories", CategoryViewSet, basename="category")
router.register("audio_book_bookmarks", AudioBookBookmarkViewSet, basename="audio_book_bookmark")
router.register("paper_book_bookmarks", PaperBookBookmarkViewSet, basename="paper_book_bookmark")
router.register("audio_types", AudioTypeViewSet, basename="audio_type")
router.register("book_speakers", BookSpeakerViewSet, basename="book_speaker")
router.register("publishers", PublisherViewSet, basename="publisher")
router.register("audio_books", AudioBookViewSet, basename="audio_book")
router.register("paper_books", PaperBookViewSet, basename="paper_book")
router.register("audio_indices", AudioIndexViewSet, basename="audio_index")
router.register("book_authors", BookAuthorViewSet, basename="book_author")
router.register(
    "compatible_devices", CompatibleDeviceViewSet, basename="compatible_device"
)

# Nested router.
category_router = nested_routers.NestedDefaultRouter(
    router, "categories", lookup="category"
)
category_router.register("audio_books", AudioBookViewSet, basename="audio_books")

tag_router = nested_routers.NestedDefaultRouter(router, "tags", lookup="tags")
tag_router.register("audio_books", AudioBookViewSet, basename="audio_books")

compatible_device_router = nested_routers.NestedDefaultRouter(
    router, "compatible_devices", lookup="compatible_devices"
)
compatible_device_router.register(
    "audio_books", AudioBookViewSet, basename="audio_books"
)

publisher_router = nested_routers.NestedDefaultRouter(
    router, "publishers", lookup="publishers"
)
publisher_router.register("audio_books", AudioBookViewSet, basename="audio_books")

book_author_router = nested_routers.NestedDefaultRouter(
    router, "book_authors", lookup="book_authors"
)
book_author_router.register("audio_books", AudioBookViewSet, basename="audio_books")

book_speaker_router = nested_routers.NestedDefaultRouter(
    router, "book_speakers", lookup="book_speakers"
)
book_speaker_router.register("audio_books", AudioBookViewSet, basename="audio_books")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(category_router.urls)),
    path("", include(tag_router.urls)),
    path("", include(compatible_device_router.urls)),
    path("", include(publisher_router.urls)),
    path("", include(book_author_router.urls)),
    path("", include(book_speaker_router.urls)),
]
