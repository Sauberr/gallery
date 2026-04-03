from http import HTTPStatus
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class VerifyMfaTests(TestCase):
	def setUp(self):
		self.url = reverse("account:verify_mfa")
		self.user = get_user_model().objects.create_user(
			email="mfa-user@example.com",
			password="TestPassword123!",
			is_active=True,
		)

	@patch("account.views.verify_2fa_otp", return_value=True)
	def test_verify_mfa_valid_otp_redirects_to_profile(self, _mock_verify):
		response = self.client.post(
			self.url,
			{
				"user_id": str(self.user.id),
				"otp_code": "123456",
			},
		)

		self.assertEqual(response.status_code, HTTPStatus.FOUND)
		self.assertEqual(response.url, reverse("account:profile"))

	@patch("account.views.verify_2fa_otp", return_value=False)
	def test_verify_mfa_invalid_otp_redirects_to_profile(self, _mock_verify):
		response = self.client.post(
			self.url,
			{
				"user_id": str(self.user.id),
				"otp_code": "000000",
			},
		)

		self.assertEqual(response.status_code, HTTPStatus.FOUND)
		self.assertEqual(response.url, reverse("account:profile"))

