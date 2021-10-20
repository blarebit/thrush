"""Blog URLs."""
from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import (
    posts_list,
    post_detail,
    CategoriesList,
    category_detail,
    user_stars,
    comment_approve,
)
from .views import (
    TagsList,
    tag_detail,
    comment_detail,
    tag_posts,
    new_post_star,
    post_bookmark,
)
from .views import (
    new_post_tag,
    delete_post_tag,
    post_comment,
    new_comment_reply,
    user_bookmarks,
)

router = routers.DefaultRouter()
# List all categories, or create a new category.
router.register("categories/", CategoriesList, basename="categories")
# List all tags, or create a tag.
router.register("tags/", TagsList, basename="tags")

urlpatterns = [
    # Retrieve, update or delete a category <id | name>.
    path("categories/<uuid:category_id_or_name>", category_detail),
    path("categories/<str:category_id_or_name>", category_detail),
    # Retrieve a tag <id | name>.
    path("tags/<uuid:tag_id_or_name>", tag_detail),
    path("tags/<str:tag_id_or_name>", tag_detail),
    # List all posts with one tag <id | name>.
    path("tags/<uuid:tag_id_or_name>/posts", tag_posts),
    path("tags/<str:tag_id_or_name>/posts", tag_posts),
    # List all posts, or create a new post.
    path("posts/", posts_list),
    # Retrieve, update or delete a post <id | title>.
    path("posts/<uuid:post_id_or_title>", post_detail),
    path("posts/<str:post_id_or_title>", post_detail),
    # Bookmark a post <id | title> or Delete bookmark.
    path("posts/<uuid:post_id_or_title>/bookmarks/", post_bookmark),
    path("posts/<str:post_id_or_title>/bookmarks/", post_bookmark),
    # Create a new tag for a post <id | title>.
    path("posts/<uuid:post_id_or_title>/tags/", new_post_tag),
    path("posts/<str:post_id_or_title>/tags/", new_post_tag),
    # Delete a tag <id | name> from a post <id | title>.
    path("posts/<uuid:post_id_or_title>/tags/<uuid:tag_id_or_name>", delete_post_tag),
    path("posts/<str:post_id_or_title>/tags/<uuid:tag_id_or_name>", delete_post_tag),
    path("posts/<uuid:post_id_or_title>/tags/<str:tag_id_or_name>", delete_post_tag),
    path("posts/<str:post_id_or_title>/tags/<str:tag_id_or_name>", delete_post_tag),
    # Create a new star for a post <id | title>.
    path("posts/<uuid:post_id_or_title>/stars/", new_post_star),
    path("posts/<str:post_id_or_title>/stars/", new_post_star),
    # Retrieve all comments or Create a new comment for a post <id | title>.
    path("posts/<uuid:post_id_or_title>/comments/", post_comment),
    path("posts/<str:post_id_or_title>/comments/", post_comment),
    # Create a new comment's reply for a post <id | title>.
    path("posts/<uuid:post_id_or_title>/replies/<uuid:comment_id>", new_comment_reply),
    path("posts/<str:post_id_or_title>/replies/<uuid:comment_id>", new_comment_reply),
    # Retrieve or delete a comment
    path("comments/<uuid:comment_id>", comment_detail),
    # Approve or disapprove a comment for a post
    path("comments/<uuid:comment_id>/approve/", comment_approve),
    # Retrieve all stars who a user <user-id> gives.
    path("stars", user_stars),
    # Retrieve all user's <user-id> bookmarks.
    path("bookmarks/", user_bookmarks),
    path("", include(router.urls)),
]
