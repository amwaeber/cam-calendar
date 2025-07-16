from app.google_calendar import safe_linkify
from django.core.exceptions import ValidationError
from django.test import TestCase
from app.models import GoogleCalendarEntry, Event

class GoogleCalendarEntryTestCase(TestCase):
    def test_str_representation(self):
        event = GoogleCalendarEntry.objects.create(
            googleEventId='1',
            summary='An event',
            description='Description for the event',
            startTime='2023-09-23T08:00:00Z',
            endTime='2023-09-23T11:00:00Z',
            lastUpdated='2023-09-20T07:00:00Z',
            location='A location')
        recurring_event = GoogleCalendarEntry.objects.create(
            googleEventId='2',
            recurringEventId='666',
            summary='A recurring event',
            description='Description for the recurring event',
            startTime='2023-09-24T08:00:00Z',
            endTime='2023-09-24T11:00:00Z',
            lastUpdated='2023-09-20T07:00:00Z')

        self.assertEqual(str(event), 'An event')
        self.assertEqual(str(recurring_event), 'A recurring event')

    def test_safe_linkify_description(self):
        raw_description = 'Visit https://example.com or contact me@example.com'
        processed = safe_linkify(raw_description)

        event = GoogleCalendarEntry.objects.create(
            googleEventId='3',
            summary='An event with links',
            description=processed,
            startTime='2023-09-23T08:00:00Z',
            endTime='2023-09-23T11:00:00Z',
            lastUpdated='2023-09-20T07:00:00Z',
            location='A location nearby')
        self.assertIn('<a href="https://example.com">https://example.com</a>', event.description)
        self.assertIn('<a href="mailto:me@example.com">me@example.com</a>', event.description)

    def test_end_time_before_start_time_raises_error(self):

        entry = GoogleCalendarEntry(
            googleEventId='4',
            summary='Backwards Event',
            startTime='2023-09-23T11:00:00Z',
            endTime='2023-09-23T08:00:00Z',
            lastUpdated='2023-09-20T07:00:00Z',
            location='Wrong time, wrong palce')

        with self.assertRaises(ValidationError) as cm:
            entry.full_clean()

        self.assertIn('endTime must be after startTime.', str(cm.exception))


class EventTestCase(TestCase):
    def test_str_representation(self):
        google_event = GoogleCalendarEntry.objects.create(
            googleEventId='3',
            summary='A new event',
            description='This is an event',
            startTime='2023-09-23T08:00:00Z',
            endTime='2023-09-23T12:00:00Z',
            lastUpdated='2023-09-20T07:00:00Z',
            location='Some location')
        event = Event.objects.create(
            title='A new event',
            startDate = '2023-09-23',
            endDate = '2023-09-23',
            startTime = '08:00:00Z',
            endTime = '12:00:00Z',
            location = 'Some location',
            cost = 1,
            minAge = 2,
            maxAge = 4,
            bookingLink = 'https://www.booking-page.co.uk',
            eventLink = 'https://www.event-page.co.uk',
            description = 'This is an event',
            approved = False,
            googleCalendarEntry = google_event)

        self.assertEqual(str(google_event), 'A new event')
        self.assertEqual(str(event), 'A new event')

        google_event.delete()

        self.assertEqual(str(event), 'A new event')
