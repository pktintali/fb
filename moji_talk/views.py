from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import GameRoom,RoomMessage
from .serializers import GameRoomSerializer,RoomMessageSerializer
from .filters import RoomChatFilter
from .paginations import GamePagination

class GameRoomViewSet(viewsets.ModelViewSet):
    queryset = GameRoom.objects.order_by('-id').all()
    serializer_class = GameRoomSerializer
    pagination_class = GamePagination
    
class RoomMessageViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomChatFilter
    queryset = RoomMessage.objects.all()
    serializer_class = RoomMessageSerializer
    pagination_class = GamePagination