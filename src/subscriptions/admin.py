from django.contrib import admin

from subscriptions.models import Basic, Enterprise, Premium, Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fields = (
        "subscriber_name",
        "subscription_plan",
        "description",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
        "create_datetime",
        "last_update",
    )
    list_display = (
        "subscriber_name",
        "subscription_plan",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
    )
    list_display_links = ("subscriber_name", "subscription_plan", "subscription_cost")
    list_filter = ("subscription_plan", "is_active")
    date_hierarchy = "create_datetime"
    search_fields = ("subscriber_name", "subscription_plan", "paypal_subscription_id")
    ordering = ("create_datetime", "last_update")
    readonly_fields = ("create_datetime", "last_update")


@admin.register(Basic)
class BasicAdmin(admin.ModelAdmin):
    fields = (
        "subscriber_name",
        "subscription_plan",
        "description",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
        "create_datetime",
        "last_update",
        "thumbnail_photo_200px",
    )
    list_display = (
        "subscriber_name",
        "subscription_plan",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
        "thumbnail_photo_200px",
    )
    list_display_links = ("subscriber_name", "subscription_plan", "subscription_cost")
    list_filter = ("subscription_plan", "is_active")
    date_hierarchy = "create_datetime"
    search_fields = ("subscriber_name", "subscription_plan", "paypal_subscription_id")
    ordering = ("create_datetime", "last_update")
    readonly_fields = ("create_datetime", "last_update")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(subscription_plan="Basic Plan")


@admin.register(Premium)
class PremiumAdmin(admin.ModelAdmin):
    fields = (
        "subscriber_name",
        "subscription_plan",
        "description",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
        "create_datetime",
        "last_update",
        "thumbnail_photo_200px",
        "thumbnail_photo_400px",
        "original_photo",
    )
    list_display = (
        "subscriber_name",
        "subscription_plan",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
        "thumbnail_photo_200px",
        "thumbnail_photo_400px",
        "original_photo",
    )
    list_display_links = ("subscriber_name", "subscription_plan", "subscription_cost")
    list_filter = ("subscription_plan", "is_active")
    date_hierarchy = "create_datetime"
    search_fields = ("subscriber_name", "subscription_plan", "paypal_subscription_id")
    ordering = ("create_datetime", "last_update")
    readonly_fields = ("create_datetime", "last_update")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(subscription_plan="Premium Plan")


@admin.register(Enterprise)
class EnterpriseAdmin(admin.ModelAdmin):
    fields = (
        "subscriber_name",
        "subscription_plan",
        "description",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
        "create_datetime",
        "last_update",
        "thumbnail_photo_200px",
        "thumbnail_photo_400px",
        "original_photo",
        "binary_link",
    )
    list_display = (
        "subscriber_name",
        "subscription_plan",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
        "thumbnail_photo_200px",
        "thumbnail_photo_400px",
        "original_photo",
        "binary_link",
    )
    list_display_links = ("subscriber_name", "subscription_plan", "subscription_cost")
    list_filter = (
        "subscription_plan",
        "is_active",
    )
    date_hierarchy = "create_datetime"
    search_fields = ("subscriber_name", "subscription_plan", "paypal_subscription_id")
    ordering = ("create_datetime", "last_update")
    readonly_fields = ("create_datetime", "last_update")

    def get_queryset(self, request):
        return super().get_queryset(request).filter(subscription_plan="Enterprise Plan")
