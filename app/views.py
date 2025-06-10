from django.utils.timezone import now

from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from .models import GoogleCalendarEntry
from .serializer import GoogleCalendarEntrySerializer


class EventPagination(PageNumberPagination):
    page_size = 8

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GoogleCalendarEntrySerializer
    pagination_class = EventPagination
    def get_queryset(self):
        today = now().date()
        return GoogleCalendarEntry.objects.filter(startTime__date__gte=today).order_by('startTime')

class GoogleCalendarEntryList(generics.ListAPIView):
    queryset = GoogleCalendarEntry.objects.all()
    serializer_class = GoogleCalendarEntrySerializer
