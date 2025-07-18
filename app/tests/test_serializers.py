from django.test import TestCase
from app.models import GoogleCalendarEntry
from app.serializer import EventSummarySerializer, EventDetailSerializer

class EventSerializerTests(TestCase):
    def setUp(self):
        self.event = GoogleCalendarEntry.objects.create(
            googleEventId='1',
            summary='An event',
            description='Description for the event',
            startTime='2023-09-23T08:00:00Z',
            endTime='2023-09-23T11:00:00Z',
            lastUpdated='2023-09-20T07:00:00Z',
            location='A location')

    def test_summary_serializer_fields(self):
        serializer = EventSummarySerializer(self.event)
        self.assertEqual(set(serializer.data.keys()), {'id', 'summary', 'startTime', 'endTime', 'location'})

    def test_detail_serializer_fields(self):
        serializer = EventDetailSerializer(self.event)
        self.assertIn('description', serializer.data)

    def test_missing_required_fields(self):
        data = {
            'summary': '',
            'startTime': '',
        }
        serializer = EventSummarySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('summary', serializer.errors)
        self.assertIn('startTime', serializer.errors)

    def test_optional_fields_accept_blank_or_null(self):
        data = {
            'googleEventId': '1',
            'summary': 'Test Event',
            'startTime': '2025-07-08T10:00:00Z',
            'lastUpdated': '2025-07-08T09:00:00Z',
            'endTime': None,
            'description': '',
            'location': '',
        }
        serializer = EventDetailSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_datetime_format(self):
        data = {
            'summary': 'Bad Time',
            'startTime': 'not-a-date',
            'endTime': '2025-08-10T15:00:00Z',
            'location': 'Somewhere',
        }

        serializer = EventDetailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('startTime', serializer.errors)

