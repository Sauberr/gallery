# Generated by Django 5.0 on 2024-12-12 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0018_remove_profile_phone_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="avatar",
        ),
        migrations.RemoveField(
            model_name="user",
            name="birth_date",
        ),
        migrations.RemoveField(
            model_name="user",
            name="date_joined",
        ),
    ]
