"""Product views."""
from .audio_book import (
    AudioBookViewSet,
    AudioIndexViewSet,
    AudioTypeViewSet,
    BookSpeakerViewSet,
    CompatibleDeviceViewSet,
)
from .product import (
    BookAuthorViewSet,
    PublisherViewSet,
    TranslatorViewSet,
)
from .Paper_book import PaperBookViewSet
from .product import (
    AudioBookBookmarkViewSet,
    PaperBookBookmarkViewSet,
    CategoryViewSet,
    TagViewSet,
    ProductViewSet,
)

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
    "TranslatorViewSet",
    "ProductViewSet"
)
