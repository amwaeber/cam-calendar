from rest_framework import serializers
from .models import GoogleCalendarEntry

class GoogleCalendarEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleCalendarEntry
        fields = '__all__'