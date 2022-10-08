from rest_framework import routers
from .views import GameRoomViewSet

router = routers.DefaultRouter()
router.register('room', GameRoomViewSet)

urlpatterns = []+router.urls
