# Generated by Django 5.0 on 2024-09-29 15:06

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_alter_user_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
    ]
