from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import localdate, now
from django.utils.translation import gettext_lazy as _

NOTIFICATION_DAYS_THRESHOLD: int = 7


class SubscriptionPlan(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        unique=True,
        help_text=_("Name of the subscription plan"),
    )
    description = models.TextField(
        verbose_name=_("description"),
        max_length=1024,
        null=True,
        blank=True,
        help_text=_("Description of the subscription plan"),
    )
    cost = models.DecimalField(
        verbose_name=_("cost"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        help_text=_("Cost of the subscription plan in USD"),
    )
    paypal_plan_id = models.CharField(
        verbose_name=_("paypal plan id"),
        max_length=300,
        unique=True,
        null=True,
        blank=True,
        help_text=_("Unique identifier for the PayPal subscription plan"),
    )
    has_thumbnail_200px = models.BooleanField(
        verbose_name=_("has thumbnail 200px"),
        default=True,
        help_text=_("Indicates if the plan includes a 200px thumbnail"),
    )
    has_thumbnail_400px = models.BooleanField(
        verbose_name=_("has thumbnail 400px"),
        default=False,
        help_text=_("Indicates if the plan includes a 400px thumbnail"),
    )
    has_original_photo = models.BooleanField(
        verbose_name=_("has original photo"),
        default=False,
        help_text=_("Indicates if the plan includes an original photo"),
    )
    has_binary_link = models.BooleanField(
        verbose_name=_("has binary link"),
        default=False,
        help_text=_("Indicates if the plan includes a binary link to the photo"),
    )

    class Meta:
        indexes = [
            models.Index(fields=["cost"]),
            models.Index(fields=["name"]),
        ]
        verbose_name: str = _("Subscription Plan")
        verbose_name_plural: str = _("Subscription Plans")
        ordering = ["cost", "name"]

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        help_text=_("User associated with the subscription"),
    )
    plan = models.ForeignKey(
        "SubscriptionPlan",
        on_delete=models.PROTECT,
        verbose_name=_("subscription plan"),
        help_text=_("Subscription plan selected by the user"),
    )
    paypal_subscription_id = models.CharField(
        verbose_name=_("paypal subscription id"),
        max_length=300,
        null=True,
        blank=True,
        help_text=_("Unique identifier for the PayPal subscription"),
    )
    is_active = models.BooleanField(
        verbose_name=_("is active"),
        default=False,
        help_text=_("Indicates if the subscription is currently active"),
    )
    create_datetime = models.DateTimeField(
        verbose_name=_("create datetime"),
        auto_now_add=True,
        help_text=_("Timestamp when the subscription was created"),
    )
    last_update = models.DateTimeField(
        verbose_name=_("last update"),
        auto_now=True,
        help_text=_("Timestamp when the subscription was last updated"),
    )
    expiration_date = models.DateTimeField(
        verbose_name=_("expiration date"),
        null=True,
        blank=True,
        help_text=_("Date when the subscription expires, if applicable"),
    )
    expiration_notification_sent = models.BooleanField(
        verbose_name=_("expiration notification sent"),
        default=False,
        help_text=_("Indicates if an expiration notification has been sent"),
    )

    class Meta:
        verbose_name: str = _("User Subscription")
        verbose_name_plural: str = _("User Subscriptions")
        indexes = [
            models.Index(fields=["paypal_subscription_id"]),
            models.Index(fields=["user"]),
            models.Index(fields=["plan"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.plan.name} subscription"

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            self.expiration_date = now() + timedelta(days=30)
        super().save(*args, **kwargs)

    @property
    def subscriber_name(self) -> str:
        return self.user.get_full_name()

    @property
    def subscription_plan(self) -> str:
        return self.plan.name

    @property
    def subscription_cost(self) -> Decimal:
        return self.plan.cost

    @property
    def days_until_expiry(self) -> int | None:
        if not self.expiration_date:
            return None
        return (self.expiration_date - now()).days

    @property
    def send_expiration_notification(self):
        if not self.expiration_date or self.expiration_notification_sent:
            return False

        days_left = (self.expiration_date.date() - localdate()).days
        return days_left <= NOTIFICATION_DAYS_THRESHOLD

    @property
    def is_expired(self) -> bool:
        if not self.expiration_date:
            return False
        return now() > self.expiration_date
