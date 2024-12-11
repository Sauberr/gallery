import pycountry
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from faker import Faker
from phonenumber_field.modelfields import PhoneNumberField
from phonenumbers import format_number, PhoneNumberFormat, parse

from account.managers import CustomerManager, PeopleManager

STATUS_CHOICES = (
    ("Unmarried", "Unmarried"),
    ("Married", "Married"),
)

SEX_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Undefined", "I don't want to tell"),
)

COUNTRY_CHOICES = [(f"{country.name}", f"{country.name}") for country in pycountry.countries]


class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    first_name = models.CharField(_("name"), max_length=150, blank=True)
    last_name = models.CharField(_("surname"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True, null=True, unique=True)
    phone_number = PhoneNumberField(_("phone number"), blank=True, null=True, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birth_date = models.DateField(_("birth date"), blank=True, null=True)
    avatar = models.ImageField(_("avatar"), upload_to="avatars/", blank=True, null=True)
    mfa_secret = models.CharField(max_length=32, blank=True, null=True)
    mfa_enabled = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name: str = _("User")
        verbose_name_plural: str = _("Users")
        ordering = ("first_name",)
        indexes = [
            models.Index(fields=["first_name", "last_name", "email"]),
        ]

    def __str__(self):
        return f"{self.first_name}_{self.last_name}"

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            user = cls.objects.create(  # noqa
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                phone_number=faker.phone_number(),
                birth_date=faker.date_time_between(start_date="-30y", end_date="-18y"),
                avatar=faker.image_url(),
                date_joined=faker.date_time_this_year(),
            )

    def format_phone_number(self):
        if self.phone_number:
            parsed_number = parse(str(self.phone_number), None)
            return format_number(parsed_number, PhoneNumberFormat.INTERNATIONAL)
        return None

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_working_time(self):
        return f"Time on site: {timezone.now() - self.date_joined}"


class ProxyUser(get_user_model()):
    people = PeopleManager()

    class Meta:
        proxy = True
        ordering = ("-pk",)
        verbose_name: str = "Proxy User"
        verbose_name_plural: str = "Proxy Users"


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    location = models.CharField(max_length=44, choices=COUNTRY_CHOICES, default="Undefined")
    avatar = models.ImageField(_("avatar"), upload_to="avatars/", blank=True, null=True)
    sex = models.CharField(max_length=9, choices=SEX_CHOICES, default="Undefined")
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="Unmarried")
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birth_date = models.DateField(_("birth date"), blank=True, null=True)

    def __str__(self):
        return f"{self.user} {self.status}"

    class Meta:
        verbose_name: str = "User Profile"
        verbose_name_plural: str = "User Profiles"
