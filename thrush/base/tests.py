"""Base tests."""
from typing import Dict, List

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.management.commands.init_group import Command
from account.models import User


class BaseAPITestCase(APITestCase):
    """Base API test case class.

    All tests should be derived from this class.
    """

    def setUp(self):
        Command().handle()

    def _register_and_login(self, username, mobile, password, activate_user, login=True):
        response = self.client.post(
            reverse("account:register"),
            {"mobile": mobile, "username": username, "password": password},
        )
        self.assertEqual(response.status_code, 201)

        if not activate_user:
            return username

        user = User.objects.get(username=username)
        user.is_active = True
        user.save()

        if not login:
            return username

        response = self.client.post(
            reverse("account:login"), {"username": username, "password": password}
        )
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        return username

    def fake_user(self, username="user1", mobile="123", activate_user=True, login=True):
        return self._register_and_login(
            username, mobile, "user-password1", activate_user, login
        )

    def fake_admin(self, activate_user=True, login=True):
        return self._register_and_login(
            "admin1", "321", "admin-password1", activate_user, login
        )

    def logout(self):
        self.client.get(reverse("account:logout"))
        self.client.credentials()

    def fake_tag_and_category(self) -> Dict[str, List[int]]:
        self.fake_admin()

        result = {"tags": [], "categories": []}

        # Tags
        response = self.client.post(reverse("blog:tag-list"), {"name": "Python"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result["tags"].append(response.json()["id"])
        response = self.client.post(reverse("blog:tag-list"), {"name": "C++"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result["tags"].append(response.json()["id"])

        # Category
        response = self.client.post(
            reverse("blog:category-list"), {"name": "Development", "parent": ""}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result["categories"].append(response.json()["id"])
        response = self.client.post(
            reverse("blog:category-list"), {"name": "Debug", "parent": ""}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result["categories"].append(response.json()["id"])

        return result
