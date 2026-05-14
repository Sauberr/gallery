from http import HTTPStatus
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from account.tests.common_test import CommonTest


class TestRegistrationUser(CommonTest):
    path_name: str = "account:registration"
    template_name: str = "registration/registration.html"
    title: str = "Registration"

    def setUp(self) -> None:
        super().setUp()
        self.client = Client()
        self.data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "example@gmail.com",
            "phone_number": "+12125552368",
            "password1": "TestPassword123!",
            "password2": "TestPassword123!",
            "captcha": "PASSED",
        }

    def test_common(self):
        self.common_test()

    @patch("django_recaptcha.fields.ReCaptchaField.validate")
    def test_user_registration_post_success(self, mock_validate):
        mock_validate.return_value = None
        email = self.data["email"]
        self.assertFalse(get_user_model().objects.filter(email=email).exists())

        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("account:login"))
        self.assertTrue(get_user_model().objects.filter(email=email).exists())

    def test_user_registration_post_error(self):
        get_user_model().objects.create(email=self.data["email"])
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "User with this Email address already exists.", html=True)
