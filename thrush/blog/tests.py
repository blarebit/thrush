"""Blog tests."""
from aap.tests import BaseAPITestCase
from django.urls import reverse


class PostTest(BaseAPITestCase):
    """Test post endpoints."""

    def setUp(self):
        self.register_and_login("admin", "admin@dev.local", "admin")

    def test_new_post(self):
        response = self.client.post(reverse("blog:category-list"), {"name": "cat1"})
        print(response.json())
        self.assertEqual(response.json()["name"], "cat1")
