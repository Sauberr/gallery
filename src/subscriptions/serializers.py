from subscriptions.models import Basic, Enterprise, Premium, Subscription
from rest_framework import serializers


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
        read_only_fields = ["create_datetime", "last_update"]
        extra_kwargs = {
            "user": {"required": False},
        }

class BasicSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basic
        fields = "__all__"


class PremiumSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premium
        fields = "__all__"


class EnterpriseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = "__all__"
