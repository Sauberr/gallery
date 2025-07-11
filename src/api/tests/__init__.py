from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from api.views import (CategoryModelViewSet, OrderModelViewSet,
                       ProductModelViewSet)

app_name = "api"


router = routers.DefaultRouter()
router.register(r"categories", CategoryModelViewSet)
router.register(r"products", ProductModelViewSet)
router.register(r"orders", OrderModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
