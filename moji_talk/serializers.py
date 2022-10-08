from rest_framework import serializers
from .models import GameRoom


class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom
        fields = "__all__"