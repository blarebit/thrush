"""Cart serializers."""
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from .models import Cart
from shop.product.models import Product, AudioBook, PaperBook
from shop.product.serializers import ProductSerializer, PaperBookSerializer, AudioBookSerializer


class ProductGeneralInfoSerializer(serializers.ModelSerializer):
    """Product's public info serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="product:product-detail")

    class Meta:
        model = Product
        readonly_fields = (
            # "__all__"
            "url",
            "id",
            "name",
            # "first_name",
            # "last_name",
            # "is_active",
        )


# class AudioBookReadonlySerializer(serializers.ModelSerializer):
#     """Audio book serializer."""
#
#     url = serializers.HyperlinkedIdentityField(view_name="product:audio_book-detail")
#     bookmarks_count = serializers.SerializerMethodField()
#
#     class Meta:
#         model = AudioBook
#         read_only_fields = [
#             "name",
#             "description",
#             "product_code",
#             "image",
#             "inventory",
#             "buy_price",
#             "sel_price",
#             "extra",
#             "seller",
#             "category",
#             "intro",
#             "authors",
#             "speakers",
#             "translators",
#             "book_publisher",
#             "audio_publisher",
#             "indices",
#             "published_year",
#             "audio_type",
#             "compatible_devices",
#             "is_downloadable",
#             "tags"
#         ]
#         exclude = ["bookmarks"]
#
#     # def get_bookmarks_count(self, obj):
#     #     """Get product's bookmarks count."""
#     #     return obj.bookmarks.count()
#
#
# class PaperBookReadonlySerializer(serializers.ModelSerializer):
#     """Paper book serializer."""
#
#     url = serializers.HyperlinkedIdentityField(view_name="product:paper_book-detail")
#     # bookmarks_count = serializers.SerializerMethodField()
#
#     class Meta:
#         model = PaperBook
#         read_only_fields = [
#             "name",
#             "description",
#             "product_code",
#             "image",
#             "inventory",
#             "buy_price",
#             "sel_price",
#             "extra",
#             "seller",
#             "category",
#             "intro",
#             "authors",
#             # "speakers",
#             "translators",
#             "book_publisher",
#             # "audio_publisher",
#             # "indices",
#             "published_year",
#             # "audio_type",
#             # "compatible_devices",
#             # "is_downloadable",
#             "tags"
#         ]
#         exclude = ["bookmarks"]
#         # fields = "__all__"
#
#     # def get_bookmarks_count(self, obj):
#     #     """Get product's bookmarks count."""
#     #     return obj.bookmarks.count()


# class CartPolymorphicSerializer(PolymorphicSerializer):
class ProductPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        # Project: ProjectSerializer,
        # ArtProject: ArtProjectSerializer,
        # ResearchProject: ResearchProjectSerializer
        Product: ProductSerializer,
        PaperBook: PaperBookSerializer,
        AudioBook: AudioBookSerializer,
        # Cart: CartSerializer
    }


class CartSerializer(serializers.ModelSerializer):
    """Cart serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="cart:cart-detail")
    # total_price = serializers.SerializerMethodField()
    # products = ProductSerializer(many=True, read_only=True, source="cart_product")
    # products = ProductGeneralInfoSerializer(many=True, read_only=True)
    # products = ProductPolymorphicSerializer(many=True, read_only=True, source="cart:cart-detail")
    # products = ProductPolymorphicSerializer(many=True, read_only=True, source="cart_product")
    products = ProductPolymorphicSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = (
            "url",
            "id",
            "user",
            "product",
            # "delivery_address",
            # "content",
            "quantity",
            "products",
            # "price",
            # "final_price",
            # "invoice_number",
        )
        # read_only_fields = ("invoice_number",)
        ref_name = "cart"


    # def get_total_price(self, obj):
    #     """Get post's star average."""
    #     if obj.price.all().aggregate(Avg("star"))["star__avg"]:
    #         return obj.stars.all().aggregate(Avg("star"))["star__avg"]
    #     else:
    #         return 0


# class CartPolymorphicSerializer(PolymorphicSerializer):
# # class ProductPolymorphicSerializer(PolymorphicSerializer):
#     model_serializer_mapping = {
#         # Project: ProjectSerializer,
#         # ArtProject: ArtProjectSerializer,
#         # ResearchProject: ResearchProjectSerializer
#         Product: ProductSerializer,
#         PaperBook: PaperBookSerializer,
#         AudioBook: AudioBookSerializer,
#         Cart: CartSerializer
#     }
