from typing import List, Tuple
from django.urls import reverse


from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from faker import Faker

SUBSCRIPTION_PLANS: List[Tuple[str, str]] = [
    ("Basic", "Basic Plan"),
    ("Premium", "Premium Plan"),
    ("Enterprise", "Enterprise Plan"),
]


class Images(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])],)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=200)
    description = models.TextField(max_length=1024)
    subscription_plans = models.CharField(max_length=200, choices=SUBSCRIPTION_PLANS, default="Basic")
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    total_quantity = models.GeneratedField(
        expression=models.F("quantity") * models.F("price"),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
    )

    class Meta:
        verbose_name: str = "Image"
        verbose_name_plural: str = "Images"
        ordering = ["-created_at", "updated_at"]
        indexes = [
            models.Index(fields=["title", "author"])
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("images:image-list", args=[self.id])

    @classmethod
    def generate_instances(cls, count):
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
