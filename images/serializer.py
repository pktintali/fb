from rest_framework import serializers

from images.models import Image,BGImage

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class BGImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BGImage
        fields = "__all__"