"""Cart views."""
import account.models
from .serializers import CartSerializer
from .models import Cart
# from shop.product.models import Product
# from shop.cart.serializers import CartPolymorphicSerializer
from base.views import BaseViewSet
from rest_framework import permissions, generics


class UserCartViewSet(
    BaseViewSet,
    # generics.ListCreateAPIView,
    # generics.RetrieveUpdateAPIView,
    generics.ListAPIView,
    # generics.UpdateAPIView,
    # generics.RetrieveAPIView,
):
    """Cart view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Cart.objects.filter(is_deleted=False)
    serializer_class = CartSerializer
    # alternative_lookup_field = "user_id"

    def get_queryset(self):
        """
        This view should return a list of all the cart
        for the currently authenticated user.
        """
        # user = self.request.user
        #
        # if account.models.User.is_superuser:
        #     return Cart.objects.all()
        # else:
        #     return Cart.objects.filter(user=user)

        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        # user_id = self.kwargs['users_pk']
        # return Cart.objects.filter(user=user_id)

        """Combine the above two parts"""
        user = self.request.user.id

        if account.models.User.is_superuser:
            user_id = self.kwargs['user_pk']
            return Cart.objects.filter(user=user_id)
        else:
            return Cart.objects.filter(user=user)

    # def list(self, request, *args, **kwargs):
    #     return print()


class CartViewSet(
    BaseViewSet,
    generics.ListCreateAPIView,
    generics.RetrieveUpdateAPIView,
    # generics.RetrieveAPIView,
    # generics.UpdateAPIView,
):
    """Cart view set."""

    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Cart.objects.filter(is_deleted=False)
    serializer_class = CartSerializer
    alternative_lookup_field = "id"

    def get_queryset(self):
        """
        This view should return a list of all the cart
        for the currently authenticated user.
        """
        user = self.request.user

        if account.models.User.is_superuser:
            return Cart.objects.all()
        else:
            return Cart.objects.filter(user=user)

    # def put(self, request, *args, **kwargs):
    # def perform_update(self, serializer):
    # def list(self, serializer):
    # def update(self, request, *args, **kwargs):
    #     print("test")
    #     print()
    #     return super(CartViewSet, self).update(request, *args, **kwargs)

# class CartViewSet(
#     BaseViewSet,
#     generics.ListCreateAPIView,
#     generics.RetrieveAPIView,
#     generics.CreateAPIView,
# ):
#     """Cart view set."""
#
#     permission_classes = [permissions.DjangoModelPermissions]
#     queryset = Cart.objects.all()
#     serializer_class = CartPolymorphicSerializer
#     # alternative_lookup_field = "product"
