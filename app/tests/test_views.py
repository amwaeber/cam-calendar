from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta

from app.models import GoogleCalendarEntry

class EventViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.today = timezone.now()
        self.later = self.today + timedelta(days=1)
        self.yesterday = self.today - timedelta(days=1)

        self.event = GoogleCalendarEntry.objects.create(
            googleEventId='1',
            summary='An event',
            description='Description for the event',
            startTime=self.later,
            endTime=self.later + timedelta(hours=2),
            lastUpdated='2023-09-20T07:00:00Z',
            location='A location')

        self.past_event = GoogleCalendarEntry.objects.create(
            googleEventId='2',
            summary='A past event',
            description='Description for the past event',
            startTime=self.yesterday - timedelta(hours=2),
            endTime=self.yesterday,
            lastUpdated='2023-09-20T07:00:00Z',
            location='A location')

    def test_event_list_returns_upcoming_events(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

        summaries = [event['summary'] for event in response.data['results']]

        # Only the future event was fetched
        self.assertIn("An event", summaries)
        self.assertNotIn("A past event", summaries)

        # The description entry is not part of the response
        event_data = response.data['results'][0]
        self.assertNotIn('description', event_data)  # summary serializer

    def test_event_detail_returns_full_event(self):
        url = reverse('event-detail', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['summary'], "An event")
        self.assertEqual(response.data['description'], "Description for the event")

class EventViewPaginationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.today = timezone.now()
        self.later = self.today + timedelta(days=1)
        for i in range(20):
            GoogleCalendarEntry.objects.create(
                googleEventId=f"id-{i}",
                summary=f"Event {i}",
                startTime=self.later + timedelta(days=i),
                endTime=self.later + timedelta(days=i, hours=2),
                lastUpdated=self.today,
                location="Paginated Location"
            )

    def test_first_page(self):
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 8)  # page size from pagination class
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_second_page(self):
        url = reverse('event-list')
        response = self.client.get(url + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 8)  # page size from pagination class
        self.assertIn('next', response.data)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])

    def test_second_page(self):
        url = reverse('event-list')
        response = self.client.get(url + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 4)  # page size from pagination class
        self.assertIn('next', response.data)
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
