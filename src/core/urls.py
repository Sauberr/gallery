from django.urls import path

from core.views import BookList, IndexView, SubscriptionPlansView, ContactView, ajax_contact_form

app_name: str = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),

    path("books/", BookList.as_view(), name="books_list"),

    path("pricing/", SubscriptionPlansView.as_view(), name="pricing"),

    path("contact/", ContactView.as_view(), name="contact"),
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),
]
