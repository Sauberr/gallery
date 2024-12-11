from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.db import models
from faker import Faker


class ContactUs(models.Model):
    name = models.CharField(max_length=255, db_index=True, validators=[MinLengthValidator(2),
        RegexValidator(regex='^[a-zA-Z ]*$', message='Name must contain only alphabetic characters and spaces')])
    email = models.EmailField(max_length=255, db_index=True, validators=[EmailValidator(
        message="Invalid email address")])
    message = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name: str = "Contact Us"
        verbose_name_plural: str = "Contact Us"

    def __str__(self):
        return self.name

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                name=faker.name(),
                email=faker.email(),
                message=faker.text(),
            )
