from google.oauth2 import service_account
from googleapiclient.discovery import build
from .models import GoogleCalendarEntry
import datetime
import re

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'service_keys/calendar-service-account.json'
CALENDAR_ID = 'cambridgecommunityevents@gmail.com'


def safe_linkify(text: str) -> str:

    # 1. Extract and protect <a>...</a> blocks
    a_tag_pattern = re.compile(r'<a\s+[^>]*?>.*?</a>', re.DOTALL | re.IGNORECASE)
    protected = []

    def protect(match):
        protected.append(match.group(0))
        return f"[[PROTECTED_LINK_{len(protected) - 1}]]"

    text = a_tag_pattern.sub(protect, text)

    # 2. Replace https:// and www. (but not http://)
    def url_repl(match):
        url = match.group(0)
        href = url if url.startswith("https://") else f"https://{url}"
        return f'<a href="{href}">{url}</a>'

    url_pattern = re.compile(r'\b(?:https://[^\s<>"\']+|www\.[^\s<>"\']+)', re.IGNORECASE)
    text = url_pattern.sub(url_repl, text)

    # 3. Replace email addresses not already inside links
    def email_repl(match):
        email = match.group(0)
        return f'<a href="mailto:{email}">{email}</a>'

    email_pattern = re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w+\b')
    text = email_pattern.sub(email_repl, text)

    # 4. Restore protected <a> tags
    for i, original in enumerate(protected):
        text = text.replace(f"[[PROTECTED_LINK_{i}]]", original)

    return text

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
                'description': safe_linkify(event.get('description', '')),
                'startTime': start,
                'endTime': end,
                'lastUpdated': event['updated'],
                'location': event.get('location', ''),
            }
        )

