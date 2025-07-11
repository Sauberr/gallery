from http import HTTPStatus

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from account.tests.common_test import CommonTest


def create_user_with_email(email="user@example.com", password="TestPassword123!"):
    return get_user_model().objects.create_user(email=email, password=password)


def create_admin_user_with_email(
    email="admin@example.com", password="TestPassword123!", is_staff=True
):
    return get_user_model().objects.create_superuser(
        email=email, password=password, is_staff=is_staff
    )


def create_user_with_phone_number(
    phone_number="+12125552368", password="TestPassword123!"
):
    return get_user_model().objects.create_user(
        email=f"user_{phone_number}@example.com",
        phone_number=phone_number,
        password=password,
    )


def create_admin_user_with_phone_number(
    phone_number="+12125552367", password="TestPassword123!", is_staff=True
):
    return get_user_model().objects.create_superuser(
        email=f"admin_{phone_number}@example.com",
        phone_number=phone_number,
        password=password,
        is_staff=is_staff,
    )


class TestAuthUser(CommonTest):
    path_name: str = "account:login"
    template_name: str = "registration/login.html"
    title: str = "Login"

    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.user_email = create_user_with_email()
        self.admin_email = create_admin_user_with_email()
        self.user_phone_number = create_user_with_phone_number()
        self.admin_phone_number = create_admin_user_with_phone_number()

    def test_common(self):
        self.common_test()

    def test_login_with_invalid_email(self):
        response = self.client.post(
            self.path, {"username": "user@example.com", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_login_with_valid_email(self):  # 1
        response = self.client.post(
            self.path, {"username": "user@example.com", "password": "TestPassword123!"}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_login_with_invalid_phone_number(self):
        response = self.client.post(
            self.path, {"username": "+12125552368", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_login_with_valid_phone_number(self):  # 2
        response = self.client.post(
            self.path, {"username": "+12125552368", "password": "TestPassword123!"}
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_user_access_with_email(self):
        self.client.force_login(self.user_email)
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_access_admin_panel_with_email(self):
        self.client.force_login(self.user_email)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_admin_access_admin_panel_with_email(self):
        self.client.force_login(self.admin_email)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_access_with_phone_number(self):
        self.client.force_login(self.user_phone_number)
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_access_admin_panel_with_phone_number(self):
        self.client.force_login(self.user_phone_number)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_admin_access_admin_panel_with_phone_number(self):
        self.client.force_login(self.admin_phone_number)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
