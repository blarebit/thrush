"""Product URLs."""
from django.urls import include, path
from rest_framework import routers

from .views import OrderViewSet, PaymentViewSet

router = routers.DefaultRouter()
# router.register("orders", OrderViewSet, basename="order")
router.register("payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]
