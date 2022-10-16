from rest_framework import routers
from .views import GameRoomViewSet, RoomMessageViewSet

router = routers.DefaultRouter()
router.register('room', GameRoomViewSet)
router.register('room_chat', RoomMessageViewSet)

urlpatterns = []+router.urls
