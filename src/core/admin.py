from django.contrib import admin

from .models import ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    fields = ("name", "email", "message", "created_at")
    list_display = ("name", "email", "message", "created_at")
    list_display_links = ("name", "email", "message")
    search_fields = ("name", "email", "message")
    ordering = ("name", "email", "message")
    readonly_fields = ("created_at",)
    list_filter = ("name", "email", "message")
    list_per_page = 10
