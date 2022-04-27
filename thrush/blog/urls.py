"""Blog URLs."""
from django.urls import include, path
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from .views import (
    BookmarkViewSet,
    CategoryViewSet,
    CommentViewSet,
    PostViewSet,
    StarViewSet,
    TagViewSet,
)

router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("stars", StarViewSet, basename="star")
router.register("bookmarks", BookmarkViewSet, basename="bookmark")
router.register("categories", CategoryViewSet, basename="category")
router.register("tags", TagViewSet, basename="tag")

# Category nested router.
category_router = nested_routers.NestedDefaultRouter(
    router, "categories", lookup="category"
)
category_router.register("posts", PostViewSet, basename="post")

# Tag nested router.
tag_router = nested_routers.NestedDefaultRouter(router, "tags", lookup="tag")
tag_router.register("posts", PostViewSet, basename="post")

# Post nested router.
post_router = nested_routers.NestedDefaultRouter(
    category_router, "posts", lookup="post"
)
post_router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(category_router.urls)),
    path("", include(post_router.urls)),
    path("", include(tag_router.urls)),
]
