from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField

from account.models import Profile


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    captcha = ReCaptchaField()

    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name", "phone_number", "password1", "password2", "captcha")

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
    phone_number = forms.CharField(max_length=15, required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "remember_me"})
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "phone_number", "password", "remember_me")


class ProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField()
    avatar = forms.ImageField()
    is_active = forms.BooleanField()
    date_joined = forms.DateTimeField()
    birth_date = forms.DateField()

    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "phone_number", "email", "avatar", "is_active",
                  "date_joined", "birth_date")


