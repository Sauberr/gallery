from typing import List, Tuple

from django.db import models
from faker import Faker

SUBSCRIPTION_PLANS: List[Tuple[str, str]] = [
    ("Basic", "Basic Plan"),
    ("Premium", "Premium Plan"),
    ("Enterprise", "Enterprise Plan"),
]


class Images(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=200)
    description = models.TextField()
    subscription_plans = models.CharField(max_length=200, choices=SUBSCRIPTION_PLANS, default="Basic")

    class Meta:
        verbose_name: str = "Image"
        verbose_name_plural: str = "Images"
        ordering = ["-created_at", "updated_at"]
        indexes = [
            models.Index(fields=["title", "author"])
        ]

    def __str__(self):
        return self.title

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                title=faker.sentence(),
                image=faker.image_url(),
            )
