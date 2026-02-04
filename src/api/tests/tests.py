from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from images.models import Images
from subscriptions.models import SubscriptionPlan, UserSubscription


def create_test_user(email="test@example.com", password="TestPass123!"):
    """Create a test user"""

    return get_user_model().objects.create_user(
        email=email,
        password=password,
    )


def create_test_admin(email="admin@example.com", password="AdminPass123!", is_staff=True):
    """Create a test admin user"""

    return get_user_model().objects.create_superuser(email=email, password=password, is_staff=is_staff)


def create_test_subscription_plan(
    name="Premium",
    description="Premium Plan",
    cost=Decimal("9.99"),
    paypal_plan_id="P-123",
    has_thumbnail_400px=True,
    has_original_photo=True,
):
    """Create a test subscription plan"""
    return SubscriptionPlan.objects.create(
        name=name,
        description=description,
        cost=cost,
        paypal_plan_id=paypal_plan_id,
        has_thumbnail_400px=has_thumbnail_400px,
        has_original_photo=has_original_photo,
    )


def create_test_user_subscription(user, plan, paypal_subscription_id="S-123"):
    """Create a test user subscription"""
    return UserSubscription.objects.create(
        user=user,
        plan=plan,
        paypal_subscription_id=paypal_subscription_id,
        is_active=True,
    )


def create_test_image(
    title="Test Image",
    author="Test Author",
    description="Test Description",
    subscription_plans="Premium",
    image="test_images/test.jpg",
):
    """Create a test image"""
    return Images.objects.create(
        title=title,
        author=author,
        description=description,
        subscription_plans=subscription_plans,
        image=image,
    )


class APITests(APITestCase):
    def setUp(self):
        """Set up test data"""

        self.user = create_test_user()
        self.admin = create_test_admin()

        response = self.client.post(
            reverse("api:token_obtain_pair"),
            {"email": "test@example.com", "password": "TestPass123!"},
        )
        self.token = response.data["access"]

        response = self.client.post(
            reverse("api:token_obtain_pair"),
            {"email": "admin@example.com", "password": "AdminPass123!"},
        )
        self.admin_token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.plan = create_test_subscription_plan()
        self.subscription = create_test_user_subscription(self.user, self.plan)
        self.image = create_test_image()

    def test_images_viewset(self):
        """Test images ViewSet"""
        list_url = reverse("api:images-list")
        detail_url = reverse("api:images-detail", kwargs={"pk": self.image.pk})

        self.client.credentials()
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.image.title)

        search_url = f"{list_url}?search={self.image.title}"
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        ordering_url = f"{list_url}?ordering=title"
        response = self.client.get(ordering_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            list_url,
            {
                "title": "New Image",
                "author": "New Author",
                "description": "New Description",
                "subscription_plans": "Premium",
                "image": "test.jpg",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(detail_url, {"title": "Updated Title"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscriptions_viewset(self):
        """Test subscription plans ViewSet"""
        list_url = reverse("api:subscriptions-list")
        detail_url = reverse("api:subscriptions-detail", kwargs={"pk": self.plan.pk})

        self.client.credentials()
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.plan.name)

        search_url = f"{list_url}?search={self.plan.name}"
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        ordering_url = f"{list_url}?ordering=cost"
        response = self.client.get(ordering_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            list_url,
            {"name": "New Plan", "description": "New Description", "cost": "19.99"},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(detail_url, {"name": "Updated Plan"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_subscriptions_viewset(self):
        """Test user subscriptions ViewSet"""
        list_url = reverse("api:user-subscriptions-list")
        detail_url = reverse("api:user-subscriptions-detail", kwargs={"pk": self.subscription.pk})

        self.client.credentials()
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], self.user.email)

        search_url = f"{list_url}?search={self.user.email}"
        response = self.client.get(search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

        ordering_url = f"{list_url}?ordering=create_datetime"
        response = self.client.get(ordering_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(list_url, {"user": self.user.id, "plan": self.plan.id})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(detail_url, {"is_active": False})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get(reverse("api:health"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("status", response.data)
        self.assertIn("version", response.data)
        self.assertIn("dependencies", response.data)
        self.assertIn("timestamp", response.data)

    def test_token_endpoints(self):
        """Test JWT token endpoints"""
        response = self.client.post(
            reverse("api:token_obtain_pair"),
            {"email": "test@example.com", "password": "TestPass123!"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        refresh_token = response.data["refresh"]
        response = self.client.post(reverse("api:token_refresh"), {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

        access_token = response.data["access"]
        response = self.client.post(reverse("api:token_verify"), {"token": access_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
