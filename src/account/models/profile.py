from typing import Sequence

import pycountry
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES: Sequence[tuple[str, str]] = (
    ("Unmarried", "Unmarried"),
    ("Married", "Married"),
)

SEX_CHOICES: Sequence[tuple[str, str]] = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Undefined", "I don't want to tell"),
)

COUNTRY_CHOICES = [(f"{country.name}", f"{country.name}") for country in pycountry.countries]


class Profile(models.Model):
    """Model to store additional user profile information"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    location = models.CharField(max_length=44, choices=COUNTRY_CHOICES, default="Undefined")
    avatar = models.ImageField(_("avatar"), upload_to="avatars/", blank=True, null=True)
    sex = models.CharField(max_length=9, choices=SEX_CHOICES, default="Undefined")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="Unmarried")
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birth_date = models.DateField(_("birth date"), blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user} {self.status}"

    def clean(self) -> None:
        """Validate birth date is not in the future."""
        super().clean()
        if self.birth_date and self.birth_date > timezone.now().date():
            raise ValueError("Birth date cannot be in the future")

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
