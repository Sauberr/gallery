from django.urls import path

from core.views import IndexView, BookList, subscription_plans

app_name: str = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("books/", BookList.as_view(),  name="books_list"),
    path("pricing/", subscription_plans, name="pricing"),
]
