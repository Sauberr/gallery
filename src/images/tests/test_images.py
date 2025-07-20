from decimal import Decimal
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from images.models import Images
from images.tests.common_test import CommonTest
from subscriptions.models import SubscriptionPlan, UserSubscription

IMAGES_URL = reverse("images:images")
IMAGE_DETAIL_URL = "images:image_detail"


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
    has_original_photo=True,
):
    return SubscriptionPlan.objects.create(
        name=name,
        description=description,
        cost=cost,
        paypal_plan_id=paypal_plan_id,
        has_thumbnail_400px=has_thumbnail_400px,
        has_original_photo=has_original_photo,
    )


def create_user_subscription(user, plan, paypal_subscription_id="S-123", is_active=True):
    return UserSubscription.objects.create(
        user=user,
        plan=plan,
        paypal_subscription_id=paypal_subscription_id,
        is_active=is_active,
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
        image=image,
    )


class ImagesListTests(CommonTest):
    path_name: str = "images:images"
    template_name: str = "images/images.html"
    title: str = "Gallery"

    def setUp(self):
        super().setUp()
        self.client = Client()
        self.images = Images.objects.all()
        self.user = create_user_with_email()
        self.admin_user = create_admin_user_with_email()
        self.subscription_plan = create_subscription_plan()
        self.user_subscription = create_user_subscription(user=self.user, plan=self.subscription_plan)
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

    def test_common(self):
        """Test common functionality from parent class"""
        self.common_test()

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

    def test_pagination_first_page(self):
        """Test first page pagination"""
        self.client.force_login(self.user)

        # Create more images for pagination
        for i in range(3, 7):  # Create 4 more images (total 6)
            create_images(
                title=f"Image {i}",
                author=f"Author {i}",
                description=f"Description {i}",
                image=f"images/image{i}.jpg",
            )

        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Check pagination data
        self.assertEqual(len(response.context_data["images"]), 4)  # 4 items per page
        self.assertEqual(response.context_data["custom_range"], range(1, 2))  # Only page 1
        self.assertTrue(response.context_data["images"].has_next())
        self.assertFalse(response.context_data["images"].has_previous())

    def test_pagination_middle_page(self):
        """Test middle page pagination"""
        self.client.force_login(self.user)

        # Create more images for pagination
        for i in range(3, 9):  # Create 6 more images (total 8)
            create_images(
                title=f"Image {i}",
                author=f"Author {i}",
                description=f"Description {i}",
                image=f"images/image{i}.jpg",
            )

        response = self.client.get(f"{IMAGES_URL}?page=2")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Check pagination data
        self.assertEqual(len(response.context_data["images"]), 4)
        self.assertEqual(response.context_data["custom_range"], range(1, 3))
        self.assertTrue(response.context_data["images"].has_next())
        self.assertTrue(response.context_data["images"].has_previous())

    def test_pagination_last_page(self):
        """Test last page pagination"""
        self.client.force_login(self.user)

        # Create more images for pagination
        for i in range(3, 9):  # Create 6 more images (total 8)
            create_images(
                title=f"Image {i}",
                author=f"Author {i}",
                description=f"Description {i}",
                image=f"images/image{i}.jpg",
            )

        response = self.client.get(f"{IMAGES_URL}?page=3")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Check last page data
        self.assertEqual(len(response.context_data["images"]), 2)  # Last page with remaining items
        self.assertEqual(response.context_data["custom_range"], range(1, 3))
        self.assertFalse(response.context_data["images"].has_next())
        self.assertTrue(response.context_data["images"].has_previous())

    def test_pagination_invalid_page(self):
        """Test pagination with invalid page number"""
        self.client.force_login(self.user)

        response = self.client.get(f"{IMAGES_URL}?page=999")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Should return last available page
        self.assertEqual(len(response.context_data["images"]), 2)  # Only 2 images in setup
        self.assertEqual(response.context_data["custom_range"], range(1, 2))

    def test_pagination_non_numeric_page(self):
        """Test pagination with non-numeric page parameter"""
        self.client.force_login(self.user)

        response = self.client.get(f"{IMAGES_URL}?page=abc")
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # Should return first page
        self.assertEqual(len(response.context_data["images"]), 2)
        self.assertEqual(response.context_data["custom_range"], range(1, 2))

    def test_allowed_plans_context(self):
        """Test allowed plans in context for different subscription levels"""
        # Test Premium subscription
        self.client.force_login(self.user)
        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data["allowed_plans"]["Premium"], ["Basic", "Premium"])

        # Test Basic subscription
        basic_plan = create_subscription_plan(
            name="Basic",
            description="Basic Plan",
            cost=Decimal("4.99"),
            paypal_plan_id="P-BASIC",
        )
        self.user_subscription.plan = basic_plan
        self.user_subscription.save()

        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.context_data["allowed_plans"]["Basic"], ["Basic"])

        # Test Enterprise subscription
        enterprise_plan = create_subscription_plan(
            name="Enterprise",
            description="Enterprise Plan",
            cost=Decimal("19.99"),
            paypal_plan_id="P-ENTERPRISE",
        )
        self.user_subscription.plan = enterprise_plan
        self.user_subscription.save()

        response = self.client.get(IMAGES_URL)
        self.assertEqual(
            response.context_data["allowed_plans"]["Enterprise"],
            ["Basic", "Premium", "Enterprise"],
        )

    def test_no_subscription_context(self):
        """Test context when user has no subscription"""
        self.user_subscription.delete()
        self.client.force_login(self.user)
        response = self.client.get(IMAGES_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNone(response.context_data["user_subscription_plan"])
        self.assertEqual(response.context_data["allowed_plans"], {})


class ImageDetailTests(CommonTest):
    path_name = "images:image_detail"
    template_name = "images/image-detail.html"
    title = "Image Detail"

    def setUp(self):
        self.client = Client()
        self.user = create_user_with_email()
        self.subscription_plan = create_subscription_plan()
        self.user_subscription = create_user_subscription(user=self.user, plan=self.subscription_plan)
        self.image = create_images()
        # Переопределяем path для detail view, так как нужен pk
        self.path = reverse(self.path_name, kwargs={"pk": self.image.pk})

    def test_common(self):
        """Test common functionality from parent class"""
        self.common_test()

    def test_image_detail_authenticated_user(self):
        """Test image detail view for authenticated user"""
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "images/image-detail.html")
        self.assertEqual(response.context_data["image"], self.image)
        self.assertEqual(response.context_data["title"], "Image Detail")

    def test_image_detail_anonymous_user(self):
        """Test image detail view for anonymous user"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_image_detail_allowed_plans(self):
        """Test allowed plans in image detail context"""
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data["allowed_plans"]["Premium"], ["Basic", "Premium"])

    def test_image_detail_invalid_id(self):
        """Test image detail view with invalid image id"""
        self.client.force_login(self.user)
        url = reverse(IMAGE_DETAIL_URL, kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
