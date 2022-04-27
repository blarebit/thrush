"""Blog tests."""
from base.tests import BaseAPITestCase
from django.urls import reverse


class PostTest(BaseAPITestCase):
    """Test post endpoints."""

    def test_new_tag(self):
        self.fake_user()
        response = self.client.get(reverse("blog:tag-list"))
        self.assertEqual(response.json()["count"], 0)

        response = self.client.post(reverse("blog:tag-list"), {"name": "python"})
        breakpoint()

    # def test_new_post(self):
        # self.fake_user()
        # response =self.client.post(reverse("blog:category-list"), {"name": "cat1"})
        # print(response.json())
        # self.assertEqual(response.json()["name"], "cat1")
