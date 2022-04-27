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
        response = self.client.get(
            reverse("blog:post-detail", kwargs={"pk": "1"})
        )
        self.assertDictEqual(
            response.json(),
            expected_result
        )

        # Update a post
        response = self.client.patch(
            reverse("blog:post-detail", kwargs={"pk": "1"}),
            {"title": "Multi-threading in Python", "tags": [tags_and_categories["tags"][0]]},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_expected_result = expected_result.copy()
        new_expected_result["title"] = "Multi-threading in Python"
        new_expected_result["tags"] = [{"url": "http://testserver/blog/tags/1/", "id": 1, "name": "Python"}]
        self.assertDictEqual(
            response.json(),
            new_expected_result
        )

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
