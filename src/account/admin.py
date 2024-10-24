from django.contrib import admin
from django.contrib.auth import get_user_model

from account.models import ProxyUser, Profile

admin.site.register([ProxyUser, Profile])


class ProfileAdmin(admin.StackedInline):
    model = Profile


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileAdmin]
    fields = ("first_name", "last_name", "password", "email", "phone_number", "is_active", "mfa_enabled", "mfa_secret")
    list_display = ("first_name", "last_name", "email", "is_active")
    list_display_links = ("first_name", "last_name", "email")
    fieldsets = None
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email", "first_name", "last_name")
    readonly_fields = ("email", "phone_number")
