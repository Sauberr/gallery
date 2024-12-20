# Generated by Django 5.0 on 2024-10-05 14:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("subscriptions", "0007_alter_basic_thumbnail_photo_200px_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Images",
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
                ("title", models.CharField(max_length=200)),
                ("image", models.ImageField(upload_to="images/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("author", models.CharField(max_length=200)),
                ("description", models.TextField()),
                (
                    "subscription",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="subscriptions.subscription",
                    ),
                ),
            ],
            options={
                "verbose_name": "Image",
                "verbose_name_plural": "Images",
            },
        ),
    ]
