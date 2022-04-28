"""Blog tests."""
from django.urls import reverse
from rest_framework import status
from freezegun import freeze_time
from base.tests import BaseAPITestCase


class BlogTest(BaseAPITestCase):
    """Test blog endpoints."""

    def test_tag(self):
        self.fake_user()

        # Should have an empty list
        response = self.client.get(reverse("blog:tag-list"))
        self.assertEqual(response.json()["count"], 0)

        # Create
        response = self.client.post(reverse("blog:tag-list"), {"name": "Python"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.json(),
            {"id": 1, "name": "Python", "url": "http://testserver/blog/tags/1/"},
        )

        # Check by a GET request
        response = self.client.get(reverse("blog:tag-list"))
        self.assertEqual(response.json()["count"], 1)

        # Check by URL
        response = self.client.get(reverse("blog:tag-detail", kwargs={"pk": "Python"}))
        self.assertDictEqual(
            response.json(),
            {"id": 1, "name": "Python", "url": "http://testserver/blog/tags/1/"},
        )

        # Check update
        response = self.client.put(
            reverse("blog:tag-detail", kwargs={"pk": "Python"}), {"name": "Server"}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Check delete
        response = self.client.delete(
            reverse("blog:tag-detail", kwargs={"pk": "Python"})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category(self):
        self.fake_user()

        # Should have an empty list
        response = self.client.get(reverse("blog:category-list"))
        self.assertEqual(response.json()["count"], 0)

        # Create
        response = self.client.post(
            reverse("blog:category-list"), {"name": "Python", "parent": ""}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.json(),
            {
                "id": 1,
                "name": "Python",
                "parent": None,
                "url": "http://testserver/blog/categories/1/",
            },
        )

        # Check by a GET request
        response = self.client.get(reverse("blog:category-list"))
        self.assertEqual(response.json()["count"], 1)

        # Check by URL
        response = self.client.get(
            reverse("blog:category-detail", kwargs={"pk": "Python"})
        )
        self.assertDictEqual(
            response.json(),
            {
                "id": 1,
                "url": "http://testserver/blog/categories/1/",
                "name": "Python",
                "parent": None,
            },
        )

        # Check parent
        response = self.client.post(
            reverse("blog:category-list"), {"name": "DevOps", "parent": 1}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.json(),
            {
                "id": 2,
                "name": "DevOps",
                "parent": 1,
                "url": "http://testserver/blog/categories/2/",
            },
        )

        # Update a category
        response = self.client.put(
            reverse("blog:category-detail", kwargs={"pk": "DevOps"}),
            {"name": "Server", "parent": 1},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                "id": 2,
                "name": "Server",
                "parent": 1,
                "url": "http://testserver/blog/categories/2/",
            },
        )

        # Check delete
        response = self.client.delete(
            reverse("blog:category-detail", kwargs={"pk": "DevOps"})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @freeze_time("2022-04-27T20:59:07.483327Z")
    def test_post(self):
        self.fake_user()
        tags_and_categories = self.fake_tag_and_category()

        # Should have an empty list
        response = self.client.get(reverse("blog:post-list"))
        self.assertEqual(response.json()["count"], 0)

        # Create
        response = self.client.post(
            reverse("blog:post-list"),
            {
                "title": "Threading in Python",
                "brief": "How to use Thread in Python",
                "content": "import threading",
                "slug": "threading-in-python",
                "tags": tags_and_categories["tags"],
                "category": tags_and_categories["categories"][0],
                "image": "http://127.0.0.1/file/1/1.jpg",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        expected_result = {
            "url": "http://testserver/blog/posts/1/",
            "id": 1,
            "created_at": "2022-04-27T20:59:07.483327Z",
            "modified_at": "2022-04-27T20:59:07.483327Z",
            "category": {
                "url": "http://testserver/blog/categories/1/",
                "id": 1,
                "name": "Development",
                "parent": None,
            },
            "title": "Threading in Python",
            "brief": "How to use Thread in Python",
            "slug": "threading-in-python",
            "tags": [
                {"url": "http://testserver/blog/tags/1/", "id": 1, "name": "Python"},
                {"url": "http://testserver/blog/tags/2/", "id": 2, "name": "C++"},
            ],
            "comments_count": 0,
            "stars_average": 0,
            "bookmarks_count": 0,
            "content": "import threading",
            "image": "http://127.0.0.1/file/1/1.jpg",
            "is_draft": False,
            "previous": None,
            "visited": 0,
            "publisher": {
                "id": 2,
                "first_name": "",
                "last_name": "",
                "is_active": True,
            },
        }
        self.assertDictEqual(response.json(), expected_result)

        # Check by a GET request
        response = self.client.get(reverse("blog:post-list"))
        self.assertEqual(response.json()["count"], 1)

        # Check by URL
        response = self.client.get(reverse("blog:post-detail", kwargs={"pk": "1"}))
        self.assertDictEqual(response.json(), expected_result)

        # Update a post
        response = self.client.patch(
            reverse("blog:post-detail", kwargs={"pk": "1"}),
            {
                "title": "Multi-threading in Python",
                "tags": [tags_and_categories["tags"][0]],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_expected_result = expected_result.copy()
        new_expected_result["title"] = "Multi-threading in Python"
        new_expected_result["tags"] = [
            {"url": "http://testserver/blog/tags/1/", "id": 1, "name": "Python"}
        ]
        self.assertDictEqual(response.json(), new_expected_result)

        # Check delete
        response = self.client.delete(
            reverse("blog:category-detail", kwargs={"pk": "DevOps"})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymouse_user(self):
        self.fake_user()

        tags_and_categories = self.fake_tag_and_category()

        # Should have an empty list
        response = self.client.get(reverse("blog:post-list"))
        self.assertEqual(response.json()["count"], 0)

        # Create
        response = self.client.post(
            reverse("blog:post-list"),
            {
                "title": "Threading in Python",
                "brief": "How to use Thread in Python",
                "content": "import threading",
                "slug": "threading-in-python",
                "tags": tags_and_categories["tags"],
                "category": tags_and_categories["categories"][0],
                "image": "http://127.0.0.1/file/1/1.jpg",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check anonymous access
        self.logout()
        response = self.client.get(reverse("blog:post-list"))
        self.assertEqual(response.json()["count"], 1)

    def test_star(self):
        self.fake_user()

        tags_and_categories = self.fake_tag_and_category()

        # Create a post
        response = self.client.post(
            reverse("blog:post-list"),
            {
                "title": "Threading in Python",
                "brief": "How to use Thread in Python",
                "content": "import threading",
                "slug": "threading-in-python",
                "tags": tags_and_categories["tags"],
                "category": tags_and_categories["categories"][0],
                "image": "http://127.0.0.1/file/1/1.jpg",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_id = response.json()["id"]

        # Star a post
        response = self.client.post(
            reverse("blog:star-list"), {"star": 3, "post": post_id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {"star": 3, "post": post_id})

        # Call again (should be updated)
        response = self.client.post(
            reverse("blog:star-list"), {"star": 4, "post": post_id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.json(), {"star": 4, "post": post_id})

        # Star by a different user
        self.fake_user(username="user2", mobile="111")
        response = self.client.post(
            reverse("blog:star-list"), {"star": 8, "post": post_id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {"star": 8, "post": post_id})

        # Get post info and check the star number
        response = self.client.get(reverse("blog:post-detail", kwargs={"pk": post_id}))
        self.assertEqual(response.json()["stars_average"], 6.0)

    @freeze_time("2022-04-27T20:59:07.483327Z")
    def test_bookmark(self):
        self.fake_user()

        tags_and_categories = self.fake_tag_and_category()

        # Create a post
        response = self.client.post(
            reverse("blog:post-list"),
            {
                "title": "Threading in Python",
                "brief": "How to use Thread in Python",
                "content": "import threading",
                "slug": "threading-in-python",
                "tags": tags_and_categories["tags"],
                "category": tags_and_categories["categories"][0],
                "image": "http://127.0.0.1/file/1/1.jpg",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_id = response.json()["id"]

        # Bookmark the post
        response = self.client.post(reverse("blog:bookmark-list"), {"post": post_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.json(),
            {"code": 201, "detail": "Bookmark created.", "status_code": 201},
        )

        # Retry to get 400
        response = self.client.post(reverse("blog:bookmark-list"), {"post": post_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {"code": 400, "detail": "The post already bookmarked.", "status_code": 400},
        )

        # Check bookmark count on the post
        response = self.client.get(reverse("blog:post-detail", kwargs={"pk": post_id}))
        self.assertEqual(response.json()["bookmarks_count"], 1)

        # Bookmark with another user and check the bookmark count on the post
        self.fake_user(username="user2", mobile="111")
        response = self.client.post(reverse("blog:bookmark-list"), {"post": post_id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(
            response.json(),
            {"code": 201, "detail": "Bookmark created.", "status_code": 201},
        )
        response = self.client.get(reverse("blog:post-detail", kwargs={"pk": post_id}))
        self.assertEqual(response.json()["bookmarks_count"], 2)

        # Check the bookmark in my blog bookmarks
        response = self.client.get(reverse("blog:my_blog_bookmarks"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "url": "http://testserver/blog/posts/1/",
                        "id": 1,
                        "created_at": "2022-04-27T20:59:07.483327Z",
                        "modified_at": "2022-04-27T20:59:07.483327Z",
                        "category": {
                            "url": "http://testserver/blog/categories/1/",
                            "id": 1,
                            "name": "Development",
                            "parent": None,
                        },
                        "title": "Threading in Python",
                        "brief": "How to use Thread in Python",
                        "slug": "threading-in-python",
                        "tags": [
                            {
                                "url": "http://testserver/blog/tags/1/",
                                "id": 1,
                                "name": "Python",
                            },
                            {
                                "url": "http://testserver/blog/tags/2/",
                                "id": 2,
                                "name": "C++",
                            },
                        ],
                        "comments_count": 0,
                        "stars_average": 0,
                        "bookmarks_count": 2,
                        "content": "import threading",
                        "image": "http://127.0.0.1/file/1/1.jpg",
                        "is_draft": False,
                        "previous": None,
                        "visited": 0,
                        "publisher": {
                            "id": 2,
                            "first_name": "",
                            "last_name": "",
                            "is_active": True,
                        },
                    }
                ],
            },
        )

        # Remove bookmark
        response = self.client.delete(
            reverse("blog:bookmark-detail", kwargs={"pk": post_id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check bookmarks count on the post
        response = self.client.get(reverse("blog:post-detail", kwargs={"pk": post_id}))
        self.assertEqual(response.json()["bookmarks_count"], 1)

    @freeze_time("2022-04-27T20:59:07.483327Z")
    def test_comment(self):
        self.fake_user()

        tags_and_categories = self.fake_tag_and_category()

        # Create a post
        response = self.client.post(
            reverse("blog:post-list"),
            {
                "title": "Threading in Python",
                "brief": "How to use Thread in Python",
                "content": "import threading",
                "slug": "threading-in-python",
                "tags": tags_and_categories["tags"],
                "category": tags_and_categories["categories"][0],
                "image": "http://127.0.0.1/file/1/1.jpg",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_id = response.json()["id"]

        # Check comments list should be empty
        response = self.client.get(
            reverse(
                "blog:comment-list",
                kwargs={
                    "category_pk": tags_and_categories["categories"][0],
                    "post_pk": post_id,
                },
            )
        )
        self.assertEqual(response.json()["count"], 0)

        # Add a new comment
        response = self.client.post(
            reverse(
                "blog:comment-list",
                kwargs={
                    "category_pk": tags_and_categories["categories"][0],
                    "post_pk": post_id,
                },
            ),
            {"message": "first comment"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_json = response.json()
        self.assertDictEqual(
            response_json,
            {
                "id": 1,
                "message": "first comment",
                "reply_to": "",
                "is_approved": False,
                "user": {"id": 2, "email": "", "first_name": "", "last_name": ""},
            },
        )
        comment_id = response_json["id"]

        # Login by another user to reply to the previous comment
        self.fake_user(username="user2", mobile="111")
        response = self.client.post(
            reverse(
                "blog:comment-list",
                kwargs={
                    "category_pk": tags_and_categories["categories"][0],
                    "post_pk": post_id,
                },
            ),
            {"message": "first comment", "reply_to": comment_id},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update the comment
        response = self.client.patch(
            reverse(
                "blog:comment-detail",
                kwargs={
                    "category_pk": tags_and_categories["categories"][0],
                    "post_pk": post_id,
                    "pk": response.json()["id"],
                },
            ),
            {"message": "second comment", "reply_to": comment_id},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                "id": 2,
                "message": "second comment",
                "reply_to": comment_id,
                "is_approved": False,
                "user": {"id": 3, "email": "", "first_name": "", "last_name": ""},
            },
        )

        # Delete the comment
        response = self.client.delete(
            reverse(
                "blog:comment-detail",
                kwargs={
                    "category_pk": tags_and_categories["categories"][0],
                    "post_pk": post_id,
                    "pk": response.json()["id"],
                },
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Logout and check the comment by anonymous user
        self.logout()

        response = self.client.get(
            reverse(
                "blog:comment-list",
                kwargs={
                    "category_pk": tags_and_categories["categories"][0],
                    "post_pk": post_id,
                },
            )
        )
        self.assertEqual(response.json()["count"], 1)
