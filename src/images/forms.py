from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Images


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ["title", "description", "author", "subscription_plans", "price", "quantity", "image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter image title...", "required": True}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-textarea", "placeholder": "Enter image description...", "rows": 4}
            ),
            "author": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter author name...", "required": True}
            ),
            "subscription_plans": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(
                attrs={"class": "form-input", "placeholder": "0.00", "step": "0.01", "min": "0"}
            ),
            "quantity": forms.NumberInput(attrs={"class": "form-input", "placeholder": "0", "min": "0"}),
            "image": forms.FileInput(
                attrs={"class": "form-file-input", "accept": "image/*", "style": "display: none;"}
            ),
        }
