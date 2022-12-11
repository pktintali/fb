from rest_framework import routers
from .views import MessageViewSet, PublicMessageViewSet, ActivityViewSet

router = routers.DefaultRouter()
router.register('chat', MessageViewSet)
router.register('chat-server1', PublicMessageViewSet)
router.register('activity', ActivityViewSet)

urlpatterns = []+router.urls
