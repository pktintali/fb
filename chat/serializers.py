from dataclasses import fields
from email import message
from django.contrib.humanize.templatetags import humanize
from rest_framework import serializers

from api.models import User
from .models import Message, PublicMessage, Activity


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    timestamp = serializers.SerializerMethodField(
        method_name='human_date')

    def human_date(self, msg: Message):
        return humanize.naturaltime(msg.timestamp)


class PublicMessageSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()

    class Meta:
        model = PublicMessage
        fields = "__all__"

    timestamp = serializers.SerializerMethodField(
        method_name='human_date')

    def human_date(self, msg: Message):
        return humanize.naturaltime(msg.timestamp)


class PublicMessageAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicMessage
        fields = "__all__"

    timestamp = serializers.SerializerMethodField(
        method_name='human_date')

    def human_date(self, msg: Message):
        return humanize.naturaltime(msg.timestamp)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"

    last_seen = serializers.SerializerMethodField(
        method_name='human_date')

    def human_date(self, msg: Activity):
        return humanize.naturaltime(msg.last_seen)
