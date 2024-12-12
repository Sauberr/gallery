from subscriptions.models import SubscriptionPlan, UserSubscription
from rest_framework import serializers


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "description",
            "cost",
            "paypal_plan_id",
            "has_thumbnail_200px",
            "has_thumbnail_400px",
            "has_original_photo",
            "has_binary_link",
        ]



class UserSubscriptionSerializer(serializers.ModelSerializer):
    plan_details = SubscriptionPlanSerializer(source='plan', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserSubscription
        fields = [
            'id',
            'user',
            'user_email',
            'plan',
            'plan_details',
            'paypal_subscription_id',
            'is_active',
            'create_datetime',
            'last_update',
            'subscriber_name',
            'subscription_plan',
            'subscription_cost',
        ]
