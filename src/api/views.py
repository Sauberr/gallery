from rest_framework.viewsets import ModelViewSet
from subscriptions.models import Basic, Enterprise, Premium, Subscription
from subscriptions.serializers import BasicSubscriptionSerializer, EnterpriseSubscriptionSerializer,  \
    PremiumSubscriptionSerializer, SubscriptionSerializer
from images.models import Images
from images.serializers import ImagesSerializer
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrReadOnly
from rest_framework import filters


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