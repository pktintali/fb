from rest_framework import viewsets
from .models import Message, Activity
from . paginations import ChatPagination
from .serializers import MessageSerializer, ActivitySerializer
# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = ChatPagination


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = ChatPagination
