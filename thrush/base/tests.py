"""Base tests."""
from django.urls import reverse
from rest_framework.test import APITestCase
from account.models import User


class BaseAPITestCase(APITestCase):
    """Base API test case class.

    All tests should be derived from this class.
    """

    def _register_and_login(self, username, mobile, password, activate_user):
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

        response = self.client.post(
            reverse("account:login"), {"username": username, "password": password}
        )
        self.assertEqual(response.status_code, 200)
        token = response.json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        return username

    def fake_user(self, username="user1", activate_user=True):
        return self._register_and_login(username, "123", "user-password1", activate_user)

    def fake_admin(self, activate_user=True):
        return self._register_and_login("admin1", "321", "admin-password1", activate_user)

    def logout(self):
        self.client.get(reverse("account:logout"))
        self.client.credentials()
