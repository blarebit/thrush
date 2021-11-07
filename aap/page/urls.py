"""Page URLs."""
from django.urls import path, include
from rest_framework import routers

from .views import (
    PageViewSet, GroupMenuViewSet, MenuViewSet
)

router = routers.DefaultRouter()
router.register("pages", PageViewSet, basename="page")
router.register("group_menus", GroupMenuViewSet, basename="group_menu")
router.register("menus", MenuViewSet, basename="menu")

urlpatterns = [
    path("", include(router.urls)),
]
