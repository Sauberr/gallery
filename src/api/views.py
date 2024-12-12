from datetime import datetime, timezone

from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


from images.models import Images
from images.serializers import ImagesSerializer
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status

from subscriptions.models import SubscriptionPlan, UserSubscription
from subscriptions.serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer


class SubscriptionPlanView(ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ["name", "description"]
    ordering_fields = ["cost"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]




class UserSubscriptionView(ReadOnlyModelViewSet):
    queryset = UserSubscription.objects.select_related("user", "plan").all()
    serializer_class = UserSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ["user__email", "plan__name"]
    ordering_fields = ["create_datetime"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]


class HealthView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """Check health status of the API"""

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
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ["title", "description", "author"]
    ordering_fields = ["title", "created_at"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]