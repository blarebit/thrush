"""Payment views."""
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from .serializers import PaymentSerializer, OrderSerializer
from .models import Payment, Order
from base.views import BaseViewSet
from rest_framework import permissions, generics

from account.models import Address
from shop.product.models import Product
from shop.cart.models import Cart
from shop.payment.models import Payment


class OrderViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
):
    """Order view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Order.objects.filter(is_deleted=False)
    serializer_class = OrderSerializer
    alternative_lookup_field = "invoice_number"


class PaymentViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveAPIView,
    generics.UpdateAPIView,
):
    """Order view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Payment.objects.filter(is_deleted=False)
    serializer_class = PaymentSerializer
    # alternative_lookup_field = "invoice_number"

    def fill_payment(self, request, *args):
        # user = self.request.user
        # carts = Cart.objects.filter(is_deleted=False, user=user)
        total_price = 0
        discount = 0
        for item in args[1]:
            product = Product.objects.get(id=item.product_id)
            if product.discount:
                if not product.end or datetime.utcnow <= product.end:
                    if not product.start or datetime.utcnow >= product.start:
                        discount = product.discount

            total_price += (item.quantity * (product.sel_price - discount))

        payment = Payment.objects.create(
            user=args[0],
            total_payment=total_price,
            payment_type=request.data["payment_type"] if request.data["payment_type"] else '',
            status=request.data["status"] if request.data["status"] else '',
            # bank_response =
            bank_id=request.data["bank_id"] if request.data["bank_id"] else '',
            # batch_number =
        )
        # carts.delete()
        return Response({
            "invoice_number": payment.id,
            "total_payment": total_price
        })

    def fill_order(self, request):
        user = self.request.user
        carts = Cart.objects.filter(is_deleted=False, user=user)
        total_price = 0
        discount = 0
        if carts:
            payment = self.fill_payment(request, user, carts)
            for item in carts:
                product = Product.objects.get(id=item.product_id)
                if product.discount:
                    if not product.end or datetime.utcnow <= product.end:
                        if not product.start or datetime.utcnow >= product.start:
                            discount = product.discount

                total_price = (item.quantity * (product.sel_price - discount))
                Order.objects.create(
                    user=item.user,
                    delivery_address=Address.objects.filter(is_deleted=False, user=user).first(),
                    product=item.product,
                    quantity=item.quantity,
                    total_price=total_price,
                    invoice_number=payment.data['invoice_number'],
                )

            # Add any more information to payment.data here
            # payment.data.append(.....)

            carts.delete()
            return Response(payment.data, status=status.HTTP_200_OK)
        return Response({"Failed": True, "Message": "Cart had not any products."}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        return self.fill_order(request)
        # return super().create()
