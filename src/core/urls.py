from django.urls import path

from core.views import ImageList, IndexView, SubscriptionPlansView, ContactView, ajax_contact_form

app_name: str = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    path("images/", ImageList.as_view(), name="image_list"),

    path("pricing/", SubscriptionPlansView.as_view(), name="pricing"),

    path("contact/", ContactView.as_view(), name="contact"),
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),
]
