from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from phonenumber_field.formfields import PhoneNumberField
from account.tasks import send_registration_email

from account.models import Profile

from account.models import STATUS_CHOICES, SEX_CHOICES, COUNTRY_CHOICES


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = PhoneNumberField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    captcha = ReCaptchaField()

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "phone_number", "password1", "password2", "captcha")


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_registration_email.delay(user.id)
        return user

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        special_characters = "!@#$%^&*()_-+={}[]|\:;'<>?,./"  # noqa
        capitalize_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"  # noqa

        has_special = any(char in special_characters for char in password1)
        has_capital = any(char in capitalize_letters for char in password1)

        if not has_special and not has_capital:
            raise ValidationError("Password must contain at least one special character and one uppercase letter")
        elif not has_special:
            raise ValidationError("Password must contain at least one special character")
        elif not has_capital:
            raise ValidationError("Password must contain at least one uppercase letter")

        return password1


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(required=False)
    phone_number = PhoneNumberField(max_length=15, required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "remember_me"})
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "phone_number", "password", "remember_me")



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter first name"}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter last name"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter email",
                "readonly": True,
            }
        )
    )
    phone_number = PhoneNumberField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Enter phone number"}
        ),
        required=False
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "type": "date"}
        ),
        required=False
    )
    sex = forms.ChoiceField(
        choices=SEX_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )
    location = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={"class": "custom-file-input"})
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'phone_number')