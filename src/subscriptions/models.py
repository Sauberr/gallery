from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, null=True, blank=True)
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)]
    )
    paypal_plan_id = models.CharField(max_length=300, unique=True)

    has_thumbnail_200px = models.BooleanField(default=True)
    has_thumbnail_400px = models.BooleanField(default=False)
    has_original_photo = models.BooleanField(default=False)
    has_binary_link = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['cost']),
            models.Index(fields=['name']),
        ]
        verbose_name: str = _("Subscription Plan")
        verbose_name_plural: str = _("Subscription Plans")
        ordering = ['cost']

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    paypal_subscription_id = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name: str = _("User Subscription")
        verbose_name_plural: str = _("User Subscriptions")
        indexes = [
            models.Index(fields=['paypal_subscription_id']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.plan.name} subscription"

    @property
    def subscriber_name(self):
        return self.user.get_full_name()

    @property
    def subscription_plan(self):
        return self.plan.name

    @property
    def subscription_cost(self):
        return self.plan.cost