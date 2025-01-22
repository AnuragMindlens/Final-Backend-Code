# serializers.py in the images app
from rest_framework import serializers

from .models import Images


class ImageSerializer(serializers.ModelSerializer):
    """Defines the way in which images are serialized and sent
    Mostly won't be edited

    Args:
        serializers (ModelSerializer): none
    """
    class Meta:
        model = Images
        fields = ['id', 'title', 'image_file', 'uploaded_at']
