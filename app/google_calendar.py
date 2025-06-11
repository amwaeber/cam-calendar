from google.oauth2 import service_account
from googleapiclient.discovery import build
from .models import GoogleCalendarEntry
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'service_keys/calendar-service-account.json'
CALENDAR_ID = 'cambridgecommunityevents@gmail.com'

def sync_google_calendar():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    print(creds.service_account_email)
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.datetime.now(datetime.UTC)
    two_weeks_later = now + datetime.timedelta(weeks=2)

    time_min = now.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    time_max = two_weeks_later.replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=time_min,
        timeMax=time_max,
        maxResults=250,
        singleEvents=True,
        orderBy='startTime',
    ).execute()
    events = events_result.get('items', [])

    for event in events:
        start = event.get('start', {}).get('dateTime')
        end = event.get('end', {}).get('dateTime')

        if not start or not end:
            continue  # Skip all-day events for now

        # https://developers.google.com/workspace/calendar/api/v3/reference/events#resource
        GoogleCalendarEntry.objects.update_or_create(
            googleEventId=event['id'],
            defaults={
                'recurringEventId': event.get('recurringEventId'),
                'summary': event.get('summary', ''),
                'description': event.get('description', ''),
                'startTime': start,
                'endTime': end,
                'lastUpdated': event['updated'],
                'location': event.get('location', ''),
            }
        )

