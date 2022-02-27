"""Blog URLs."""
from django.urls import path, include
from rest_framework import routers
# from rest_framework_nested import routers as nested_routers

from .views import (
    TagViewSet,
    CategoryViewSet,
)

router = routers.DefaultRouter()
router.register("tags", TagViewSet, basename="tag")
router.register("categories", CategoryViewSet, basename="category")

# # Category nested router.
# category_router = nested_routers.NestedDefaultRouter(
#     router, "categories", lookup="category"
# )
# category_router.register("posts", PostViewSet, basename="post")
#
# # Post nested router.
# post_router = nested_routers.NestedDefaultRouter(
#     category_router, "posts", lookup="post"
# )
# post_router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    # path("", include(category_router.urls)),
    # path("", include(post_router.urls)),
]
