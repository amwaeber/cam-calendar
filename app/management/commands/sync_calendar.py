from django.core.management.base import BaseCommand
from app.google_calendar import sync_google_calendar

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        sync_google_calendar()
