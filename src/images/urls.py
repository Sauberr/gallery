from django.urls import path

from images.views import ImageCreateView, ImageDetail, ImagesList

app_name: str = "images"

urlpatterns = [
    path("images/", ImagesList.as_view(), name="images"),
    path("images/<int:pk>/", ImageDetail.as_view(), name="image_detail"),
    path("feature/", ImageCreateView.as_view(), name="image_feature"),
]
