from rest_framework import serializers
from api.models import Event
from api.models import RoomType

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['event_name', 'event_code', 'event_type_name', 'event_type_code','event_demography', 'event_demography_code', 'show_time_code']
