# Generated by Django 5.0 on 2024-09-08 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("subscriptions", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="subscription",
            old_name="subscriber_cost",
            new_name="subscription_cost",
        ),
        migrations.RenameField(
            model_name="subscription",
            old_name="subscriber_plan",
            new_name="subscription_plan",
        ),
    ]