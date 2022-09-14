from rest_framework import routers
from .views import MessageViewSet

router = routers.DefaultRouter()
router.register('chat', MessageViewSet)

urlpatterns = []+router.urls
