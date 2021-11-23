"""SlideShow URLs."""
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from .views import GroupSlideShowViewSet, SlideShowViewSet

router = routers.DefaultRouter()
router.register("groups", GroupSlideShowViewSet, basename="group")

group_router = nested_routers.NestedDefaultRouter(router, "groups", lookup="group")
group_router.register("slideshows", SlideShowViewSet, basename="slideshow")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(group_router.urls)),
]
