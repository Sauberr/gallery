from django.urls import include, path
from rest_framework import routers, permissions
from api.views import ImagesViewSet, SubscriptionViewSet, BasicSubscriptionViewSet, PremiumSubscriptionViewSet, \
    EnterpriseSubscriptionViewSet, HealthView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "api"


schema_view = get_schema_view(
    openapi.Info(
        title="Images API",
        default_version="v1",
        description="API for Images",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sauberr10@gmail.com"),
       license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[
        permissions.AllowAny,
    ],
)


router = routers.DefaultRouter()

router.register(r"images", ImagesViewSet, basename="images")
router.register(r"subscription", SubscriptionViewSet, basename="subscription")
router.register(r"basic-subscription", BasicSubscriptionViewSet, basename="basic-subscription")
router.register(r"premium-subscription", PremiumSubscriptionViewSet, basename="premium-subscription")
router.register(r"enterprise-subscription", EnterpriseSubscriptionViewSet, basename="enterprise-subscription")

urlpatterns = [
    path("", include(router.urls)),
    path("health/", HealthView.as_view(), name="health"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger_docs"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]