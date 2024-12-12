from http import HTTPStatus
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from images.models import Images
from subscriptions.models import SubscriptionPlan, UserSubscription


IMAGES_URL = reverse("images:images")


def create_user_with_email(email="user@example.com", password="TestPassword123!"):
    return get_user_model().objects.create_user(email=email, password=password)


def create_admin_user_with_email(email="admin@example.com", password="TestPassword123!", is_staff=True):
    return get_user_model().objects.create_superuser(email=email, password=password, is_staff=is_staff)


def create_subscription_plan(
        name="Premium",
        description="Premium Plan",
        cost=Decimal("9.99"),
        paypal_plan_id="P-123",
        has_thumbnail_400px=True,
        has_original_photo=True
):
    return SubscriptionPlan.objects.create(
        name=name,
        description=description,
        cost=cost,
        paypal_plan_id=paypal_plan_id,
        has_thumbnail_400px=has_thumbnail_400px,
        has_original_photo=has_original_photo
    )


def create_user_subscription(user, plan, paypal_subscription_id="S-123", is_active=True):
    return UserSubscription.objects.create(
        user=user,
        plan=plan,
        paypal_subscription_id=paypal_subscription_id,
        is_active=is_active
    )


def create_images(
        title="Image 1",
        author="Author 1",
        description="Description 1",
        subscription_plans="Premium",
        image="images/image1.jpg",
):
    return Images.objects.create(
        title=title,
        author=author,
        description=description,
        subscription_plans=subscription_plans,
        image=image
    )


class ImagesListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.images = Images.objects.all()
        self.user = create_user_with_email()
        self.admin_user = create_admin_user_with_email()

        self.subscription_plan = create_subscription_plan()

        self.user_subscription = create_user_subscription(
            user=self.user,
            plan=self.subscription_plan
        )

        self.image1 = create_images(
            title="Image 1",
            author="Author 1",
            description="Description 1",
            subscription_plans="Premium",
            image="images/image1.jpg",
        )
        self.image2 = create_images(
            title="Image 2",
            author="Author 2",
            description="Description 2",
            subscription_plans="Premium",
            image="images/image2.jpg",
        )

    def test_images_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("user_subscription", response.context_data)
        self.assertIn("images", response.context_data)

    def test_images_anonymous_user(self):
        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_images_admin_user(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_images_pagination(self):
        self.client.force_login(self.user)
        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("custom_range", response.context_data)
        self.assertEqual(list(response.context_data["object_list"]), list(self.images[:2]))

    def test_images_cache(self):
        self.client.force_login(self.user)
        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("images", response.context_data)
        self.assertEqual(list(response.context_data["object_list"]), list([self.image1, self.image2]))

    def test_user_subscription_properties(self):
        self.assertEqual(self.user_subscription.subscriber_name, self.user.get_full_name())
        self.assertEqual(self.user_subscription.subscription_plan, "Premium")
        self.assertEqual(self.user_subscription.subscription_cost, Decimal("9.99"))

    def test_inactive_subscription(self):
        self.user_subscription.is_active = False
        self.user_subscription.save()
        self.client.force_login(self.user)
        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)