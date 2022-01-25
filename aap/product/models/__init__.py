"""Product models."""
from .audio_book import (
    AudioBook,
    AudioIndex,
    AudioType,
    Author,
    Speaker,
    CompatibleDevice,
    Publisher,
)
from .paper_book import PaperBook
# from .product import Category, Product, Tag
# from .product import Product

__all__ = (
    # "Tag",
    # "Category",
    # "Product",
    "Publisher",
    "AudioType",
    "AudioBook",
    "PaperBook",
    "Author",
    "AudioIndex",
    "Speaker",
    "CompatibleDevice",
)
