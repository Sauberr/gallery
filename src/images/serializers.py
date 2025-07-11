from rest_framework import serializers

from images.models import Images


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at", "author"]
