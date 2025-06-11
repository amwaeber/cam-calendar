from rest_framework import serializers
from .models import GoogleCalendarEntry

class EventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleCalendarEntry
        fields = ['id', 'summary', 'startTime', 'endTime', 'location']  # no description

class EventDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleCalendarEntry
        fields = ['id', 'summary', 'startTime', 'endTime', 'location', 'description']