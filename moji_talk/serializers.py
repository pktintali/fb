from django.contrib.humanize.templatetags import humanize
from rest_framework import serializers
from .models import GameRoom,RoomMessage

class GameRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRoom
        fields = "__all__"

class RoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomMessage
        fields = "__all__"

    timestamp = serializers.SerializerMethodField(
        method_name='human_date')

    def human_date(self, msg: RoomMessage):
        return humanize.naturaltime(msg.timestamp)