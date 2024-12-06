from django.core.validators import MinValueValidator, RegexValidator, MinLengthValidator, EmailValidator
from django.db import models
from faker import Faker


class Books(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, db_index=True)
    description = models.TextField(max_length=1024)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    total_quantity = models.GeneratedField(
        expression=models.F("quantity") * models.F("price"),
        output_field=models.DecimalField(max_digits=10, decimal_places=2),
        db_persist=True,
    )

    class Meta:
        verbose_name: str = "Book"
        verbose_name_plural: str = "Books"

    def __str__(self):
        return self.title

    @classmethod
    def generate_instances(cls, count):
        faker = Faker()
        for _ in range(count):
            cls.objects.create(
                title=faker.sentence(),
                author=faker.name(),
                description=faker.text(),
                price=faker.random_int(1, 100),
                quantity=faker.random_int(1, 10),
            )


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
