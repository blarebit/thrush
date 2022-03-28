"""Account tests."""
from unittest.mock import patch

from base.tests import BaseAPITestCase
from django.urls import reverse
from parameterized import parameterized


class AccountTest(BaseAPITestCase):
    def test_user_registration(self):
        response = self.client.post(
            reverse("account:register"),
            {"mobile": "123", "username": "user1", "password": "user-password1"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(
            response.json(), {"mobile": "123", "username": "user1", "email": ""}
        )

    @parameterized.expand(
        [
            (
                {"mobile": "123", "password": "user-password1"},
                {"username": ["This field is required."]},
            ),
            (
                {"username": "user1", "password": "user-password1"},
                {"mobile": ["This field is required."]},
            ),
            (
                {"mobile": "123", "username": "user1"},
                {"password": ["This field is required."]},
            ),
            (
                {},
                {
                    "mobile": ["This field is required."],
                    "password": ["This field is required."],
                    "username": ["This field is required."],
                },
            ),
            (
                {"mobile": "", "username": "", "password": ""},
                {
                    "mobile": ["This field may not be blank."],
                    "password": ["This field may not be blank."],
                    "username": ["This field may not be blank."],
                },
            ),
        ],
    )
    def test_invalid_user_registration(self, payload, expected_response):
        response = self.client.post(
            reverse("account:register"),
            payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), expected_response)

    @parameterized.expand(
        [
            (
                {"mobile": "321", "username": "user1", "password": "user-password1"},
                {"username": ["A user with that username already exists."]},
            ),
            (
                {"mobile": "123", "username": "user2", "password": "user-password1"},
                {"mobile": ["user with this mobile already exists."]},
            ),
            (
                {"mobile": "123", "username": "user1", "password": "user-password1"},
                {
                    "username": ["A user with that username already exists."],
                    "mobile": ["user with this mobile already exists."],
                },
            ),
        ],
    )
    def test_exists_user_registration(self, payload, expected_response):
        self.fake_user()
        response = self.client.post(
            reverse("account:register"),
            payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), expected_response)

    def test_user_authentication(self):
        self.fake_user()
        response = self.client.post(
            reverse("account:login"),
            {"username": "user1", "password": "user-password1"},
        )
        self.assertEqual(response.status_code, 200)
        resp_json = response.json()
        self.assertIsInstance(resp_json, dict)
        self.assertTrue(resp_json["token"])

    def test_user_logout(self):
        self.fake_user()
        response = self.client.get(reverse("account:profile"))
        self.assertEqual(response.status_code, 200)

        self.client.get(reverse("account:logout"))

        response = self.client.get(reverse("account:profile"))
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(response.json(), {"detail": "Invalid token."})

    def test_user_change_password(self):
        self.fake_user()
        response = self.client.patch(
            reverse("account:password"),
            {"old_password": "user-password1", "new_password": "user-password2"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {"message": "password has been updated"})

        self.logout()

        # Test old password.
        response = self.client.post(
            reverse("account:login"),
            {"username": "user1", "password": "user-password1"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(), {"message": "invalid username or password"}
        )

        # Test new password.
        response = self.client.post(
            reverse("account:login"),
            {"username": "user1", "password": "user-password2"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["token"])

    def test_user_profile_view(self):
        self.fake_user()
        response = self.client.get(reverse("account:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(
            {
                "id": 1,
                "username": "user1",
                "mobile": "123",
                "email": "",
                "first_name": "",
                "last_name": "",
                "groups": [1],
                "addresses": [],
                "permissions": [],
                "is_active": True,
                "last_login": None,
            },
            response.json(),
        )
        self.assertTrue(response.json()["date_joined"])

    def test_user_profile_edit(self):
        self.fake_user()
        response = self.client.patch(
            reverse("account:profile"), {"first_name": "first", "last_name": "user"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictContainsSubset(
            {
                "id": 1,
                "username": "user1",
                "mobile": "123",
                "email": "",
                "first_name": "first",
                "last_name": "user",
                "groups": [1],
                "addresses": [],
                "permissions": [],
                "is_active": True,
                "last_login": None,
            },
            response.json(),
        )

    def test_activate_user(self):
        with patch("account.models.send_verification_code") as mocked_fn:
            self.fake_user(activate_user=False)

            # Test the user (should get invalid auth due to not being activated).
            response = self.client.post(
                reverse("account:login"),
                {"username": "user1", "password": "user-password1"},
            )
            self.assertEqual(response.status_code, 401)
            self.assertTrue(response.json(), {"message": "user is not activated yet"})

            # Activate the user.
            verification_code = mocked_fn.call_args.args[2]
            response = self.client.get(
                reverse("account:verification") + f"?code={verification_code}"
            )
            self.assertEqual(response.status_code, 200)
            self.assertDictEqual(
                response.json(), {"message": "user has been successfully activated"}
            )

        # Test the user (should be able to login).
        response = self.client.post(
            reverse("account:login"),
            {"username": "user1", "password": "user-password1"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["token"])

    def test_activate_user_invalid_verification_code(self):
        self.fake_user(activate_user=False)

        # Test the user (should get invalid auth due to not being activated).
        response = self.client.post(
            reverse("account:login"),
            {"username": "user1", "password": "user-password1"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.json(), {"message": "user is not activated yet"})

        # Try invalid codes.
        response = self.client.get(reverse("account:verification") + "?")
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {"message": "verification code is empty"})

        response = self.client.get(
            reverse("account:verification") + "?code=invalid-verification-key"
        )
        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(response.json(), {"message": "invalid verification code"})

        # Test the user (should get invalid auth due to not being activated).
        response = self.client.post(
            reverse("account:login"),
            {"username": "user1", "password": "user-password1"},
        )
        self.assertEqual(response.status_code, 401)
        self.assertTrue(response.json(), {"message": "user is not activated yet"})
