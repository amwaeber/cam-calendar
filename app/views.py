from rest_framework import generics
from .models import GoogleCalendarEntry
from .serializer import GoogleCalendarEntrySerializer

class GoogleCalendarEntryList(generics.ListAPIView):
    queryset = GoogleCalendarEntry.objects.all()
    serializer_class = GoogleCalendarEntrySerializer
