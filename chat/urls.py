from rest_framework import routers
from .views import MessageViewSet,ActivityViewSet

router = routers.DefaultRouter()
router.register('chat', MessageViewSet)
router.register('activity', ActivityViewSet)

urlpatterns = []+router.urls
