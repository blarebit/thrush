"""Payment serializers."""
from rest_framework import serializers
from .models import Payment, Order


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="payment:payment-detail")

    class Meta:
        model = Payment
        # readonly = ("delivery_address",)
        fields = (
            "url",
            "id",
            "user",
            "payment_type",
            "status",
            "total_payment",
            "bank_id",
            "batch_number",
            # "invoice_number",
        )
        ref_name = "payment"

    # def get_total_price(self, obj):
    #     """Get post's star average."""
    #     if obj.price.all().aggregate(Avg("star"))["star__avg"]:
    #         return obj.stars.all().aggregate(Avg("star"))["star__avg"]
    #     else:
    #         return 0


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="payment:payment-detail")

    class Meta:
        model = Order
        fields = (
            "url",
            "id",
            "user",
            "delivery_address",
            "product",
            "quantity",
            "total_price",
            "invoice_number",
        )
        ref_name = "order"

    # def get_total_price(self, obj):
    #     """Get post's star average."""
    #     if obj.price.all().aggregate(Avg("star"))["star__avg"]:
    #         return obj.stars.all().aggregate(Avg("star"))["star__avg"]
    #     else:
    #         return 0
