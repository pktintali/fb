from .models import *
import django_filters

class RoomChatFilter(django_filters.FilterSet):
    class Meta:
        model = RoomMessage
        fields = {
            'room': ['exact']
        }
        filterset_fields = ['room']