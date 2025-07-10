from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from faker import Faker


class ContactUs(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        max_length=255,
        db_index=True,
        validators=[
            MinLengthValidator(2),
            RegexValidator(
                regex='^[a-zA-Z ]*$',
                message=_('Name must contain only alphabetic characters and spaces')
            )
        ],
        help_text=_("Full name of the person contacting us")
    )
    email = models.EmailField(
        verbose_name=_("email"),
        max_length=255,
        db_index=True,
        validators=[EmailValidator(message=_("Invalid email address"))],
        help_text=_("Email address for contact")
    )
    message = models.TextField(
        verbose_name=_("message"),
        max_length=1024,
        help_text=_("Message content")
    )
    created_at = models.DateTimeField(
        verbose_name=_("created at"),
        auto_now_add=True,
        help_text=_("Timestamp when the message was created")
    )

    class Meta:
        verbose_name: str = _("Contact Us")
        verbose_name_plural: str = _("Contact Us")

    def __str__(self):
        return self.name

    @classmethod
    def generate_instances(cls, count) -> None:
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                name=faker.name(),
                email=faker.email(),
                message=faker.text(),
            )
