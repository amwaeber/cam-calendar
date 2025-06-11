from django.utils.timezone import now

from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from .models import GoogleCalendarEntry
from .serializer import EventSummarySerializer, EventDetailSerializer



class EventPagination(PageNumberPagination):
    page_size = 8

class EventViewSet(viewsets.ReadOnlyModelViewSet):

    pagination_class = EventPagination

    def get_queryset(self):
        today = now().date()
        return GoogleCalendarEntry.objects.filter(startTime__date__gte=today).order_by('startTime')

    def get_serializer_class(self):
        # If 'pk' is present → this is a detail view → return full event serializer
        if self.action == 'retrieve':
            return EventDetailSerializer
        # Else → list view → return summary serializer
        return EventSummarySerializer
