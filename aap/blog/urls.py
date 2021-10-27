"""Blog URLs."""
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from .views import (
    TagViewSet,
    PostViewSet,
    CategoryViewSet,
    StarViewSet,
    CommentViewSet,
    BookmarkViewSet,
)

router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("tags", TagViewSet, basename="tag")
router.register("categories", CategoryViewSet, basename="category")
router.register("stars", StarViewSet, basename="star")
router.register("bookmarks", BookmarkViewSet, basename="bookmark")

post_router = nested_routers.NestedDefaultRouter(router, "posts", lookup="post")
post_router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(post_router.urls)),
]
