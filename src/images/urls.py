from django.urls import path

from images.views import ImagesList, ImageDetail

app_name: str = "images"

urlpatterns = [
    path("images/", ImagesList.as_view(), name="images"),
    path("images/<int:pk>/", ImageDetail.as_view(), name="image_detail"),
]
