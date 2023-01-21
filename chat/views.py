from rest_framework import viewsets,authentication

from .models import Message, PublicMessage, Activity
from . paginations import ChatPagination
from .serializers import MessageSerializer, PublicMessageSerializer, PublicMessageAddSerializer, ActivitySerializer
# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    serializer_class = MessageSerializer
    pagination_class = ChatPagination


class PublicMessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.BasicAuthentication]
    queryset = PublicMessage.objects.all()
    serializer_class = PublicMessageSerializer
    pagination_class = ChatPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PublicMessageSerializer
        return PublicMessageAddSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.BasicAuthentication]
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = ChatPagination
