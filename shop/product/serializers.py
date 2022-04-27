"""Product serializers."""
from rest_framework import serializers
# from base.models import Tag, Category
from shop.product.models import (
    AudioType,
    # AudioBook,
    Publisher,
    Author,
    AudioIndex,
    Speaker,
    CompatibleDevice,
    Translator,
    # Tag,
    # Category,
    Product,
    AudioBook,
    PaperBook,
)


class PublisherSerializer(serializers.ModelSerializer):
    """Publisher serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:publisher-detail")

    class Meta:
        model = Publisher
        fields = (
            "url",
            "id",
            "name",
        )


class TranslatorSerializer(serializers.ModelSerializer):
    """Publisher serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:book_translator-detail")

    class Meta:
        model = Translator
        fields = (
            "url",
            "id",
            "name",
        )


class BookAuthorSerializer(serializers.ModelSerializer):
    """Book author serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:book_author-detail")

    class Meta:
        model = Author
        fields = (
            "url",
            "id",
            "name",
        )


class BookSpeakerSerializer(serializers.ModelSerializer):
    """Book speaker serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:audio_speaker-detail")

    class Meta:
        model = Speaker
        fields = (
            "url",
            "id",
            "name",
        )


class AudioTypeSerializer(serializers.ModelSerializer):
    """Audio type serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:audio_type-detail")

    class Meta:
        model = AudioType
        fields = (
            "url",
            "id",
            "name",
        )


class CompatibleDeviceSerializer(serializers.ModelSerializer):
    """Compatible device serializer."""

    url = serializers.HyperlinkedIdentityField(
        view_name="product:compatible_device-detail"
    )

    class Meta:
        model = CompatibleDevice
        fields = (
            "url",
            "id",
            "name",
            "version",
        )


class AudioIndexSerializer(serializers.ModelSerializer):
    """Audio index serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:audio_index-detail")

    class Meta:
        model = AudioIndex
        fields = (
            "url",
            "id",
            "title",
            "file",
            "duration",
            "is_downloadable",
        )


class ProductSerializer(serializers.ModelSerializer):
    """Product serializer."""

    # url = serializers.HyperlinkedIdentityField(view_name="product:paper_book-detail")
    # bookmarks_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # exclude = ["bookmarks"]
        fields = "__all__"

    # def get_bookmarks_count(self, obj):
    #     """Get product's bookmarks count."""
    #     return obj.bookmarks.count()


class AudioBookBookmarkSerializer(serializers.ModelSerializer):
    """Bookmark serializer."""

    product = serializers.PrimaryKeyRelatedField(source="id", read_only=True)

    class Meta:
        model = AudioBook
        fields = ("product",)
        ref_name = "product"


class PaperBookBookmarkSerializer(serializers.ModelSerializer):
    """Bookmark serializer."""

    product = serializers.PrimaryKeyRelatedField(source="id", read_only=True)

    class Meta:
        model = PaperBook
        fields = ("product",)
        ref_name = "product"


class AudioBookSerializer(serializers.ModelSerializer):
    """Audio book serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:audio_book-detail")
    bookmarks_count = serializers.SerializerMethodField()

    class Meta:
        model = AudioBook
        fields = "__all__"

    def get_bookmarks_count(self, obj):
        """Get product's bookmarks count."""
        return obj.bookmarks.count()


class PaperBookSerializer(serializers.ModelSerializer):
    """Paper book serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:paper_book-detail")
    bookmarks_count = serializers.SerializerMethodField()

    class Meta:
        model = PaperBook
        exclude = ["bookmarks"]
        # fields = "__all__"

    def get_bookmarks_count(self, obj):
        """Get product's bookmarks count."""
        return obj.bookmarks.count()
