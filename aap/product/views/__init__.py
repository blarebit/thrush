"""Product views."""
from .audio_book import (
    AudioBookViewSet,
    AudioIndexViewSet,
    AudioTypeViewSet,
    BookAuthorViewSet,
    BookSpeakerViewSet,
    CompatibleDeviceViewSet,
    PublisherViewSet,
)
from .Paper_book import PaperBookViewSet
from .product import AudioBookBookmarkViewSet, PaperBookBookmarkViewSet, CategoryViewSet, TagViewSet

__all__ = (
    "AudioTypeViewSet",
    "TagViewSet",
    "CategoryViewSet",
    "PublisherViewSet",
    "AudioBookBookmarkViewSet",
    "PaperBookBookmarkViewSet",
    "AudioBookViewSet",
    "PaperBookViewSet",
    "AudioIndexViewSet",
    "BookAuthorViewSet",
    "BookSpeakerViewSet",
    "CompatibleDeviceViewSet",
)
