from django.urls import path
from images.views import ImagesList

app_name: str = "images"

urlpatterns = [
    path("images/", ImagesList.as_view(),  name="images_list"),
]