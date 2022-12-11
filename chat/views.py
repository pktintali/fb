from rest_framework import viewsets
from .models import Message, PublicMessage, Activity
from . paginations import ChatPagination
from .serializers import MessageSerializer, PublicMessageSerializer, PublicMessageAddSerializer, ActivitySerializer
# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = ChatPagination


class PublicMessageViewSet(viewsets.ModelViewSet):
    queryset = PublicMessage.objects.all()
    serializer_class = PublicMessageSerializer
    pagination_class = ChatPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PublicMessageSerializer
        return PublicMessageAddSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = ChatPagination
