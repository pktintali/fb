from django.db import models

from api.models import User
# Create your models here.


class Message(models.Model):
    msg = models.CharField(max_length=500, null=True, blank=True)
    img = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    uid = models.PositiveSmallIntegerField()
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

class PublicMessage(models.Model):
    msg = models.CharField(max_length=500, null=True, blank=True)
    img = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']


class Activity(models.Model):
    last_seen = models.DateTimeField(auto_now=True)
    last_open = models.DateTimeField(auto_now=True)
    device_info = models.TextField()
    uid = models.PositiveSmallIntegerField()
