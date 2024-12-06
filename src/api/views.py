from datetime import datetime, timezone

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from subscriptions.models import Basic, Enterprise, Premium, Subscription
from subscriptions.serializers import BasicSubscriptionSerializer, EnterpriseSubscriptionSerializer,  \
    PremiumSubscriptionSerializer, SubscriptionSerializer
from images.models import Images
from images.serializers import ImagesSerializer
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status


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


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class BasicSubscriptionViewSet(ModelViewSet):
    serializer_class = BasicSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return Basic.objects.filter(id=1)


class PremiumSubscriptionViewSet(ModelViewSet):
    serializer_class = PremiumSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return Premium.objects.filter(id=1)


class EnterpriseSubscriptionViewSet(ModelViewSet):
    serializer_class = EnterpriseSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return Enterprise.objects.filter(id=1)


class ImagesViewSet(ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    search_fields = ["title", "description", "author"]
    ordering_fields = ["title", "created_at"]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]