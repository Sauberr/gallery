# Generated by Django 5.0 on 2024-08-17 11:54

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "subscriber_name",
                    models.CharField(
                        max_length=255,
                        validators=[django.core.validators.MinLengthValidator(2)],
                    ),
                ),
                (
                    "subscriber_plan",
                    models.CharField(
                        max_length=255,
                        validators=[django.core.validators.MinLengthValidator(2)],
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=1024, null=True),
                ),
                (
                    "subscriber_cost",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0.0)],
                    ),
                ),
                (
                    "paypal_subscription_id",
                    models.CharField(blank=True, max_length=300, null=True),
                ),
                ("is_active", models.BooleanField(default=False)),
                ("create_datetime", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_update", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Subscription",
                "verbose_name_plural": "Subscriptions",
            },
        ),
    ]