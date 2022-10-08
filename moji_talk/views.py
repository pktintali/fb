from rest_framework import viewsets
from .models import GameRoom
from .serializers import GameRoomSerializer
# Create your views here.


class GameRoomViewSet(viewsets.ModelViewSet):
    queryset = GameRoom.objects.order_by('-id').all()
    serializer_class = GameRoomSerializer