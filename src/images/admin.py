from django.contrib import admin
from django.utils.html import format_html

from images.models import Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html('<img src="{}" width="40";" />'.format(object.image.url))

    thumbnail.short_description = "Image"
    list_display = ("title", "thumbnail", "description", "author", "subscription_plans", "created_at", "updated_at")
    list_display_links = ("title", "thumbnail", "description")
    search_fields = ("title", "description")
    ordering = ("title", "description")
    readonly_fields = ("created_at", "updated_at")
    list_filter = ("title", "description")
    list_per_page = 10
