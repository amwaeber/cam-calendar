from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from .models import GoogleCalendarEntry
from .serializer import GoogleCalendarEntrySerializer


class EventPagination(PageNumberPagination):
    page_size = 8

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GoogleCalendarEntry.objects.all().order_by('start_time')
    serializer_class = GoogleCalendarEntrySerializer
    pagination_class = EventPagination

class GoogleCalendarEntryList(generics.ListAPIView):
    queryset = GoogleCalendarEntry.objects.all()
    serializer_class = GoogleCalendarEntrySerializer
