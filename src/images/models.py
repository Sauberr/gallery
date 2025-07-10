from typing import List, Tuple
from django.urls import reverse


from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from faker import Faker
from django.utils.translation import gettext_lazy as _

SUBSCRIPTION_PLANS: List[Tuple[str, str]] = [
    ("Basic", "Basic Plan"),
    ("Premium", "Premium Plan"),
    ("Enterprise", "Enterprise Plan"),
]


class Images(models.Model):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=200,
        unique=True,
        help_text=_("Title of the image")
    )
    image = models.ImageField(
        verbose_name=_("image"),
        upload_to="images/",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg", "gif"])],
        help_text=_("Image file to be uploaded"),
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        help_text=_("Timestamp when the image was created")
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updated at"),
        auto_now=True,
        help_text=_("Timestamp when the image was last updated")
    )
    author = models.CharField(
        verbose_name=_("author"),
        max_length=200,
        help_text=_("Author of the image")
    )
    description = models.TextField(
        verbose_name=_("description"),
        max_length=1024,
        null=True,
        blank=True,
        help_text=_("Description of the image")
    )
    subscription_plans = models.CharField(
        verbose_name=_("subscription plans"),
        max_length=200,
        choices=SUBSCRIPTION_PLANS,
        default="Basic",
        help_text=_("Subscription plan required to access this image"),
    )
    price = models.DecimalField(
        verbose_name=_("price"),
        default=0.00,
        max_digits=10,
        decimal_places=2,
        help_text=_("Price of the image in USD")
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("quantity"),
        default=0,
        validators=[MinValueValidator(0)],
        help_text=_("Quantity of the image available")
    )
    total_quantity = models.GeneratedField(
        expression=models.F("quantity") * models.F("price"),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
        help_text=_("Total value of the image based on quantity and price"),
        verbose_name=_("total quantity"),
    )

    class Meta:
        verbose_name: str = _("Image")
        verbose_name_plural: str = _("Images")
        ordering = ["-created_at", "updated_at"]
        indexes = [models.Index(fields=["title", "author"])]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("images:image-list", args=[self.id])

    @classmethod
    def generate_instances(cls, count) -> None:
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                title=faker.sentence(),
                image=faker.image_url(),
                author=faker.name(),
                description=faker.text(),
                price=faker.random_number(digits=2),
                quantity=faker.random_number(digits=2),
            )
