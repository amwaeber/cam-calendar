from django.test import TestCase
from unittest.mock import patch, MagicMock
from app.models import GoogleCalendarEntry
from app.google_calendar import sync_google_calendar
import datetime

class GoogleCalendarSyncTests(TestCase):
    @patch('app.google_calendar.build')  # Patch googleapiclient.discovery.build
    @patch('app.google_calendar.service_account.Credentials.from_service_account_file')
    def test_sync_google_calendar_creates_event(self, mock_creds, mock_build):
        # Mock the credentials and service
        mock_service = MagicMock()
        mock_events = {
            'items': [
                {
                    'id': 'event123',
                    'recurringEventId': '',
                    'summary': 'Mocked Event',
                    'description': 'Visit https://example.com',
                    'start': {'dateTime': '2025-07-10T10:00:00Z'},
                    'end': {'dateTime': '2025-07-10T11:00:00Z'},
                    'updated': '2025-07-07T10:00:00Z',
                    'location': 'Mocked Location'
                }
            ]
        }

        mock_service.events.return_value.list.return_value.execute.return_value = mock_events
        mock_build.return_value = mock_service

        sync_google_calendar()

        self.assertEqual(GoogleCalendarEntry.objects.count(), 1)
        event = GoogleCalendarEntry.objects.get(googleEventId='event123')
        self.assertEqual(event.summary, 'Mocked Event')
        self.assertIn('<a href="https://example.com">https://example.com</a>', event.description)

    @patch('app.google_calendar.build')  # Patch googleapiclient.discovery.build
    @patch('app.google_calendar.service_account.Credentials.from_service_account_file')
    def test_sync_skips_all_day_events(self, mock_creds, mock_build):
        mock_service = MagicMock()
        mock_events = {
            'items': [
                {
                    'id': 'allDayEvent123',
                    'summary': 'All-Day Event',
                    'start': {'date': '2025-07-10'},
                    'end': {'date': '2025-07-11'},
                    'updated': '2025-07-07T10:00:00Z',
                }
            ]
        }

        mock_service.events.return_value.list.return_value.execute.return_value = mock_events
        mock_build.return_value = mock_service

        sync_google_calendar()

        self.assertEqual(GoogleCalendarEntry.objects.count(), 0)


    @patch('app.google_calendar.build')  # Patch googleapiclient.discovery.build
    @patch('app.google_calendar.service_account.Credentials.from_service_account_file')
    def test_sync_handles_missing_fields(self, mock_creds, mock_build):
        mock_service = MagicMock()
        mock_events = {
            'items': [
                {
                    'id': 'partialEvent',
                    'summary': 'Partial Event',
                    'start': {'dateTime': '2025-07-10T10:00:00Z'},
                    'end': {'dateTime': '2025-07-10T11:00:00Z'},
                    'updated': '2025-07-07T10:00:00Z'
                    # Missing location, description, recurringEventId
                }
            ]
        }

        mock_service.events.return_value.list.return_value.execute.return_value = mock_events
        mock_build.return_value = mock_service

        sync_google_calendar()

        event = GoogleCalendarEntry.objects.get(googleEventId='partialEvent')
        self.assertEqual(event.recurringEventId, '')
        self.assertEqual(event.location, '')
        self.assertEqual(event.description, '')

    @patch('app.google_calendar.build')  # Patch googleapiclient.discovery.build
    @patch('app.google_calendar.service_account.Credentials.from_service_account_file')
    def test_sync_updates_existing_event(self, mock_creds, mock_build):
        # Create existing event
        existing = GoogleCalendarEntry.objects.create(
            googleEventId='event123',
            summary='Old Summary',
            description='Old Description',
            startTime='2025-07-10T10:00:00Z',
            endTime='2025-07-10T11:00:00Z',
            lastUpdated='2025-07-01T10:00:00Z',
            location='Old Location'
        )

        mock_service = MagicMock()
        mock_events = {
            'items': [
                {
                    'id': 'event123',
                    'summary': 'Updated Summary',
                    'description': 'New https://example.com',
                    'start': {'dateTime': '2025-07-10T10:00:00Z'},
                    'end': {'dateTime': '2025-07-10T11:00:00Z'},
                    'updated': '2025-07-07T10:00:00Z',
                    'location': 'New Location'
                }
            ]
        }

        mock_service.events.return_value.list.return_value.execute.return_value = mock_events
        mock_build.return_value = mock_service

        sync_google_calendar()

        updated = GoogleCalendarEntry.objects.get(googleEventId='event123')
        self.assertEqual(updated.summary, 'Updated Summary')
        self.assertEqual(updated.location, 'New Location')
        self.assertIn('<a href="https://example.com">https://example.com</a>', updated.description)
