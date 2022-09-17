from rest_framework import viewsets
from .models import Message, Activity
from .serializers import MessageSerializer, ActivitySerializer
# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
