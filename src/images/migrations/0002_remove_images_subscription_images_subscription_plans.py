# Generated by Django 5.0 on 2024-10-11 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="images",
            name="subscription",
        ),
        migrations.AddField(
            model_name="images",
            name="subscription_plans",
            field=models.CharField(
                choices=[
                    ("Basic", "Basic Plan"),
                    ("Premium", "Premium Plan"),
                    ("Enterprise", "Enterprise Plan"),
                ],
                default="Basic",
                max_length=200,
            ),
        ),
    ]
