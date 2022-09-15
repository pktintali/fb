from email import message
from django.contrib.humanize.templatetags import humanize
from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'timestamp', 'uid', 'msg', 'img']

    timestamp = serializers.SerializerMethodField(
        method_name='human_date')

    def human_date(self, msg: Message):
        return humanize.naturaltime(msg.timestamp)
