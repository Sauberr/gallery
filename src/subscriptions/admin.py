from django.contrib import admin

from subscriptions.models import SubscriptionPlan, UserSubscription


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "cost", "has_thumbnail_200px", "has_thumbnail_400px", "has_original_photo", "has_binary_link")
    list_display_links = ("name", "cost")
    search_fields = ("name", "cost")
    ordering = ("cost",)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "paypal_subscription_id", "is_active", "create_datetime", "last_update")
    list_display_links = ("user", "plan")
    search_fields = ("user", "plan")
    ordering = ("plan",)
    readonly_fields = ("paypal_subscription_id", "create_datetime", "last_update")
