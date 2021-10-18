"""Blog URLs."""
from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import (
    posts_list,
    post_detail,
    categories_list,
    category_detail,
    user_stars,
    comment_approve,
)
from .views import (
    tags_list,
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

urlpatterns = [
    # List all categories, or create a new category.
    path("categories/", categories_list),
    # Retrieve, update or delete a category <id | name>.
    path("categories/<uuid:val>", category_detail),
    path("categories/<str:val>", category_detail),
    # List all tags, or create a tag.
    path("tags/", tags_list),
    # Retrieve a tag <id | name>.
    path("tags/<uuid:val>", tag_detail),
    path("tags/<str:val>", tag_detail),
    # List all posts with one tag <id | name>.
    path("tags/<uuid:val>/posts", tag_posts),
    path("tags/<str:val>/posts", tag_posts),
    # List all posts, or create a new post.
    path("posts/", posts_list),
    # Retrieve, update or delete a post <id | title>.
    path("posts/<uuid:val>", post_detail),
    path("posts/<str:val>", post_detail),
    # Bookmark a post <id | title> or Delete bookmark.
    path("posts/<uuid:val>/bookmarks/", post_bookmark),
    path("posts/<str:val>/bookmarks/", post_bookmark),
    # Create a new tag for a post <id | title>.
    path("posts/<uuid:val>/tags/", new_post_tag),
    path("posts/<str:val>/tags/", new_post_tag),
    # Delete a tag <id | name> from a post <id | title>.
    path("posts/<uuid:val1>/tags/<uuid:val2>", delete_post_tag),
    path("posts/<str:val1>/tags/<uuid:val2>", delete_post_tag),
    path("posts/<uuid:val1>/tags/<str:val2>", delete_post_tag),
    path("posts/<str:val1>/tags/<str:val2>", delete_post_tag),
    # Create a new star for a post <id | title>.
    path("posts/<uuid:val>/stars/", new_post_star),
    path("posts/<str:val>/stars/", new_post_star),
    # Retrieve all comments or Create a new comment for a post <id | title>.
    path("posts/<uuid:val>/comments/", post_comment),
    path("posts/<str:val>/comments/", post_comment),
    # Create a new comment's reply for a post <id | title>.
    path("posts/<uuid:val1>/replies/<uuid:val2>", new_comment_reply),
    path("posts/<str:val1>/replies/<uuid:val2>", new_comment_reply),
    path("posts/<uuid:val1>/replies/<str:val2>", new_comment_reply),
    path("posts/<str:val1>/replies/<str:val2>", new_comment_reply),
    # Retrieve or delete a comment
    path("comments/<uuid:val>", comment_detail),
    # Approve or disapprove a comment for a post
    path("comments/<uuid:val>/approve/", comment_approve),
    # Retrieve all stars who a user <user-id> gives.
    path("stars", user_stars),
    # Retrieve all user's <user-id> bookmarks.
    path("bookmarks/", user_bookmarks),
    path("", include(router.urls)),
]
