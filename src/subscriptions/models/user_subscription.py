from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import localdate, now
from django.utils.translation import gettext_lazy as _

NOTIFICATION_DAYS_THRESHOLD: int = 7


class UserSubscription(models.Model):
    """Model UserSubscription to track user subscriptions to various plans"""

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
        verbose_name = _("User Subscription")
        verbose_name_plural = _("User Subscriptions")
        indexes = [
            models.Index(fields=["paypal_subscription_id"]),
            models.Index(fields=["user"]),
            models.Index(fields=["plan"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} - {self.plan.name} subscription"

    def save(self, *args, **kwargs):
        """Save user subscription and set default expiration date."""
        if not self.expiration_date:
            self.expiration_date = now() + timedelta(days=30)
        super().save(*args, **kwargs)

    @property
    def subscriber_name(self) -> str:
        """Return full name of the subscriber."""
        return self.user.get_full_name()

    @property
    def subscription_plan(self) -> str:
        """Return name of the subscription plan."""
        return self.plan.name

    @property
    def subscription_cost(self) -> Decimal:
        """Return cost of the subscription plan."""
        return self.plan.cost

    @property
    def days_until_expiry(self) -> int | None:
        """Calculate days until subscription expires."""
        if not self.expiration_date:
            return None
        return (self.expiration_date - now()).days

    @property
    def send_expiration_notification(self) -> bool:
        """Check if expiration notification should be sent."""
        if not self.expiration_date or self.expiration_notification_sent:
            return False

        days_left = (self.expiration_date.date() - localdate()).days
        return days_left <= NOTIFICATION_DAYS_THRESHOLD

    @property
    def is_expired(self) -> bool:
        """Check if subscription has expired."""
        if not self.expiration_date:
            return False
        return now() > self.expiration_date
