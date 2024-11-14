# Generated by Django 5.0 on 2024-11-14 17:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0007_alter_basic_thumbnail_photo_200px_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subscription",
            options={
                "ordering": ["-create_datetime", "is_active", "last_update"],
                "verbose_name": "Subscription",
                "verbose_name_plural": "Subscriptions",
            },
        ),
        migrations.AddIndex(
            model_name="subscription",
            index=models.Index(
                fields=["subscriber_name", "subscription_plan", "subscription_cost"],
                name="subscriptio_subscri_07270d_idx",
            ),
        ),
    ]