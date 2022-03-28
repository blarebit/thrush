"""Price URLs."""
from django.urls import include, path
from rest_framework import routers

from .views import PriceViewSet

router = routers.DefaultRouter()
router.register("", PriceViewSet, basename="price")

urlpatterns = [
    path("", include(router.urls)),
]
