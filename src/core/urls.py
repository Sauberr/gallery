from django.urls import path

from core.views import BookList, IndexView, SubscriptionPlansView, contact

app_name: str = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("books/", BookList.as_view(), name="books_list"),
    path("pricing/", SubscriptionPlansView.as_view(), name="pricing"),
    path("contact/", contact, name="contact"),
]
