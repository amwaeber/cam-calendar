from django.db import models

# Create your models here.

class GoogleCalendarEntry(models.Model):
    google_event_id = models.CharField(max_length=255, unique=True)
    recurring_event_id = models.CharField(max_length=255, null=True, blank=True)
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    last_updated = models.DateTimeField()
    location = models.CharField(max_length=255)

    # name = models.CharField(max_length=200)
    # begin = models.DateTimeField()
    # end = models.DateTimeField()
    # description = models.TextField()
    # location = models.CharField(max_length=200)

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField()
    bookingDetails = models.TextField()
    eventPage = models.TextField()
    location = models.CharField(max_length=200)
    rejected = models.BooleanField(default=False)
    googleCalendarEntry = models.ForeignKey(GoogleCalendarEntry, on_delete=models.DO_NOTHING)
