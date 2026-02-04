from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class SubscriptionPlan(models.Model):
    """Model SubscriptionPlan to define various subscription plans available to users."""

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
        verbose_name = _("Subscription Plan")
        verbose_name_plural = _("Subscription Plans")
        ordering = ["cost", "name"]

    def __str__(self) -> str:
        return self.name
