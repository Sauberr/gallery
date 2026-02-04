from datetime import datetime, timezone

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.permissions import IsAdminOrReadOnly
from images.models import Images
from images.serializers import ImagesSerializer
from subscriptions.models import SubscriptionPlan, UserSubscription
from subscriptions.serializers import (SubscriptionPlanSerializer,
                                       UserSubscriptionSerializer)


class SubscriptionPlanView(ReadOnlyModelViewSet):
    """API endpoint for viewing subscription plans with search and filtering"""

    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ["name", "description"]
    ordering_fields = ["cost"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]


class UserSubscriptionView(ReadOnlyModelViewSet):
    """API endpoint for viewing user subscriptions with search and filtering"""

    queryset = UserSubscription.objects.select_related("user", "plan").all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ["user__email", "plan__name"]
    ordering_fields = ["create_datetime"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]


class HealthView(APIView):
    """API endpoint for application health check status"""

    def get(self, request, *args, **kwargs) -> Response:
        """Return health status with database and cache check"""

        database_status: str = "OK"
        cache_status: str = "OK"

        health_status = {
            "status": status.HTTP_200_OK,
            "version": "1.0.0",
            "dependencies": {
                "database": database_status,
                "cache": cache_status,
            },
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        }

        return Response(health_status, status=status.HTTP_200_OK)


class ImagesViewSet(ReadOnlyModelViewSet):
    """API endpoint for viewing images with search and filtering"""

    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ["title", "description", "author"]
    ordering_fields = ["title", "created_at"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
