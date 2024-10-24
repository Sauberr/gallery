# Generated by Django 5.0 on 2024-09-18 17:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0006_alter_basic_thumbnail_photo_200px"),
    ]

    operations = [
        migrations.AlterField(
            model_name="basic",
            name="thumbnail_photo_200px",
            field=models.CharField(
                max_length=255,
                validators=[django.core.validators.MinLengthValidator(2)],
            ),
        ),
        migrations.AlterField(
            model_name="enterprise",
            name="binary_link",
            field=models.CharField(
                max_length=255,
                validators=[django.core.validators.MinLengthValidator(2)],
            ),
        ),
    ]