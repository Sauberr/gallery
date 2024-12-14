from http import HTTPStatus
from unittest.mock import patch, Mock
from decimal import Decimal

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from subscriptions.models import SubscriptionPlan, UserSubscription
from subscriptions.services.paypal import (
    get_paypal_headers,
    get_access_token,
    cancel_subscription_paypal,
    update_subscription_paypal,
    get_current_subscription
)


def create_test_user(
        email: str = "test@test.com",
        password: str = "testPass123!"
) -> get_user_model():
    """Create a test user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


def create_test_subscription_plan(
        name: str = "Premium",
        description: str = "Premium Plan",
        cost: Decimal = Decimal("9.99"),
        paypal_plan_id: str = "P-123",
        has_thumbnail_400px: bool = True,
        has_original_photo: bool = True
) -> SubscriptionPlan:
    """Create test subscription plan"""
    return SubscriptionPlan.objects.create(
        name=name,
        description=description,
        cost=cost,
        paypal_plan_id=paypal_plan_id,
        has_thumbnail_400px=has_thumbnail_400px,
        has_original_photo=has_original_photo
    )


def create_test_user_subscription(
        user: get_user_model(),
        plan: SubscriptionPlan,
        paypal_subscription_id: str = "S-123",
        is_active: bool = True
) -> UserSubscription:
    """Create test user subscription"""
    return UserSubscription.objects.create(
        user=user,
        plan=plan,
        paypal_subscription_id=paypal_subscription_id,
        is_active=is_active
    )


class PayPalServiceTests(TestCase):
    def setUp(self) -> None:
        """Set up test data"""
        self.user = create_test_user()
        self.plan = create_test_subscription_plan()
        self.subscription = create_test_user_subscription(
            user=self.user,
            plan=self.plan
        )
        self.access_token = "test_access_token"

    def test_get_paypal_headers(self) -> None:
        """Test PayPal headers generation"""
        headers = get_paypal_headers(self.access_token)

        self.assertEqual(
            headers,
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.access_token}",
            }
        )

    @patch('requests.post')
    def test_get_access_token(self, mock_post: Mock, requests=None) -> None:
        """Test getting PayPal access token"""
        mock_response = Mock()
        mock_response.json.return_value = {"access_token": self.access_token}
        mock_post.return_value = mock_response

        token = get_access_token()
        self.assertEqual(token, self.access_token)

        mock_post.side_effect = requests.exceptions.RequestException()
        token = get_access_token()
        self.assertIsNone(token)

    @patch('requests.post')
    def test_cancel_subscription_paypal(self, mock_post: Mock, requests=None) -> None:
        """Test cancelling PayPal subscription"""
        cancel_subscription_paypal(self.access_token, "S-123")
        mock_post.assert_called_once()

        mock_post.side_effect = requests.exceptions.RequestException()
        result = cancel_subscription_paypal(self.access_token, "S-123")
        self.assertIsNone(result)

    @patch('requests.post')
    def test_update_subscription_paypal(self, mock_post: Mock, requests=None) -> None:
        """Test updating PayPal subscription"""
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {
            "links": [
                {"rel": "approve", "href": "http://approve.url"}
            ]
        }
        mock_post.return_value = mock_response

        result = update_subscription_paypal(
            self.access_token,
            "S-123",
            "Premium"
        )
        self.assertEqual(result, "http://approve.url")

        result = update_subscription_paypal(
            self.access_token,
            "INVALID",
            "Premium"
        )
        self.assertIsNone(result)

        mock_post.side_effect = requests.exceptions.RequestException()
        result = update_subscription_paypal(
            self.access_token,
            "S-123",
            "Premium"
        )
        self.assertIsNone(result)

    @patch('requests.get')
    def test_get_current_subscription(self, mock_get: Mock, requests=None) -> None:
        """Test getting current subscription details from PayPal"""
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = {"plan_id": "P-123"}
        mock_get.return_value = mock_response

        result = get_current_subscription(self.access_token, "S-123")
        self.assertEqual(result, "P-123")

        mock_response.status_code = HTTPStatus.NOT_FOUND
        result = get_current_subscription(self.access_token, "S-123")
        self.assertIsNone(result)

        mock_get.side_effect = requests.exceptions.RequestException()
        result = get_current_subscription(self.access_token, "S-123")
        self.assertIsNone(result)


class SubscriptionViewsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = create_test_user()
        self.client.login(email='test@test.com', password='testpass123')
        self.plan = create_test_subscription_plan()
        self.subscription = create_test_user_subscription(
            user=self.user,
            plan=self.plan
        )

    def test_create_subscription(self):
        """Test create subscription view"""
        self.subscription.delete()

        url = reverse('subscriptions:create_subscription',
                      kwargs={'subscription_id': 'S-NEW', 'plan': 'Premium'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'subscriptions/create_subscription.html')

        subscription = UserSubscription.objects.get(paypal_subscription_id='S-NEW')
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertTrue(subscription.is_active)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @patch('subscriptions.views.get_access_token')
    @patch('subscriptions.views.update_subscription_paypal')
    def test_update_subscription(self, mock_update, mock_token):
        """Test update subscription view"""
        mock_token.return_value = 'test-token'
        mock_update.return_value = 'http://approve.url'

        url = reverse('subscriptions:update_subscription',
                      kwargs={'subscription_id': 'S-123', 'new_plan': 'Premium'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response.url, 'http://approve.url')

        url = reverse('subscriptions:update_subscription',
                      kwargs={'subscription_id': 'INVALID', 'new_plan': 'Premium'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_confirm_delete_subscription(self):
        """Test confirm delete subscription view"""
        url = reverse('subscriptions:confirm_delete_subscription',
                      kwargs={'subscription_id': 'S-123'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'subscriptions/confirm_delete_subscription.html')

    @patch('subscriptions.views.get_access_token')
    @patch('subscriptions.views.cancel_subscription_paypal')
    def test_delete_subscription(self, mock_cancel, mock_token):
        """Test delete subscription view"""
        mock_token.return_value = 'test-token'
        mock_cancel.return_value = None

        url = reverse('subscriptions:delete_subscription',
                      kwargs={'subscription_id': 'S-123'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'subscriptions/delete_subscription.html')

        self.assertFalse(
            UserSubscription.objects.filter(paypal_subscription_id='S-123').exists()
        )

    def test_paypal_update_subscription_confirmed(self):
        """Test PayPal update subscription confirmed view"""
        url = reverse('subscriptions:paypal_update_subscription_confirmed')

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            'subscriptions/paypal_update_subscription_confirmed.html'
        )

    @patch('subscriptions.views.get_access_token')
    @patch('subscriptions.views.get_current_subscription')
    def test_django_update_subscription_confirmed(self, mock_current, mock_token):
        """Test Django update subscription confirmed view"""
        mock_token.return_value = 'test-token'
        mock_current.return_value = 'P-123'

        url = reverse('subscriptions:django_update_subscription_confirmed',
                      kwargs={'subscription_id': 'S-123'})

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            'subscriptions/django_update_subscription_confirmed.html'
        )

        url = reverse('subscriptions:django_update_subscription_confirmed',
                      kwargs={'subscription_id': 'INVALID'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_login_required(self):
        """Test that views require login"""
        self.client.logout()
        urls = [
            reverse('subscriptions:create_subscription',
                    kwargs={'subscription_id': 'S-NEW', 'plan': 'Premium'}),
            reverse('subscriptions:update_subscription',
                    kwargs={'subscription_id': 'S-123', 'new_plan': 'Premium'}),
            reverse('subscriptions:confirm_delete_subscription',
                    kwargs={'subscription_id': 'S-123'}),
            reverse('subscriptions:delete_subscription',
                    kwargs={'subscription_id': 'S-123'}),
            reverse('subscriptions:paypal_update_subscription_confirmed'),
            reverse('subscriptions:django_update_subscription_confirmed',
                    kwargs={'subscription_id': 'S-123'})
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, HTTPStatus.FOUND)


class UserSubscriptionTests(TestCase):
    def setUp(self) -> None:
        """Set up test data"""
        self.user = create_test_user()
        self.plan = create_test_subscription_plan()
        self.subscription = create_test_user_subscription(
            user=self.user,
            plan=self.plan
        )

    def test_user_subscription_creation(self) -> None:
        """Test UserSubscription model creation"""
        self.assertEqual(self.subscription.user, self.user)
        self.assertEqual(self.subscription.plan, self.plan)
        self.assertEqual(self.subscription.paypal_subscription_id, "S-123")
        self.assertTrue(self.subscription.is_active)

    def test_user_subscription_str(self) -> None:
        """Test UserSubscription string representation"""
        expected_str = f"Subscription {self.subscription.paypal_subscription_id} for {self.user.email}"
        self.assertEqual(str(self.subscription), expected_str)

    def test_unique_active_subscription(self) -> None:
        """Test that user can't have multiple active subscriptions"""
        with self.assertRaises(Exception):
            create_test_user_subscription(
                user=self.user,
                plan=self.plan,
                paypal_subscription_id="S-456",
                is_active=True
            )

    def test_multiple_inactive_subscriptions(self) -> None:
        """Test that user can have multiple inactive subscriptions"""
        self.subscription.is_active = False
        self.subscription.save()

        new_subscription = create_test_user_subscription(
            user=self.user,
            plan=self.plan,
            paypal_subscription_id="S-456",
            is_active=True
        )
        self.assertTrue(new_subscription.is_active)

    def test_subscription_deactivation(self) -> None:
        """Test subscription deactivation"""
        self.subscription.is_active = False
        self.subscription.save()
        self.assertFalse(self.subscription.is_active)

    def test_subscription_plan_change(self) -> None:
        """Test changing subscription plan"""
        new_plan = create_test_subscription_plan(
            name="Basic",
            description="Basic Plan",
            cost=Decimal("4.99"),
            paypal_plan_id="P-456"
        )
        self.subscription.plan = new_plan
        self.subscription.save()
        self.assertEqual(self.subscription.plan, new_plan)