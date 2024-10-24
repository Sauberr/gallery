from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from account.models import User


class Subscription(models.Model):
    subscriber_name = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    subscription_plan = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    description = models.TextField(max_length=1024, null=True, blank=True)
    subscription_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)]
    )
    paypal_subscription_id = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True, null=True)
    last_update = models.DateTimeField(auto_now=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.subscriber_name} - {self.subscription_plan} subscription"

    class Meta:
        verbose_name: str = "Subscription"
        verbose_name_plural: str = "Subscriptions"


class Basic(Subscription):
    thumbnail_photo_200px = models.CharField(max_length=255, validators=[MinLengthValidator(2)])

    def __str__(self):
        return f"{self.subscriber_name} - {self.subscription_plan} subscription"

    class Meta:
        verbose_name: str = "Basic Subscription"
        verbose_name_plural: str = "Basic Subscriptions"


class Premium(Basic):
    thumbnail_photo_400px = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    original_photo = models.CharField(max_length=255, validators=[MinLengthValidator(2)])

    def __str__(self):
        return f"{self.subscriber_name} - {self.subscription_plan} subscription"

    class Meta:
        verbose_name: str = "Premium Subscription"
        verbose_name_plural: str = "Premium Subscriptions"


class Enterprise(Premium):
    binary_link = models.CharField(max_length=255, validators=[MinLengthValidator(2)])

    def __str__(self):
        return f"{self.subscriber_name} - {self.subscription_plan} subscription"

    class Meta:
        verbose_name: str = "Enterprise Subscription"
        verbose_name_plural: str = "Enterprise Subscriptions"