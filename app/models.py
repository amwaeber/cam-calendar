from django.core.exceptions import ValidationError
from django.db import models

# Events imported from the Cambridge Community Events Google calendar
class GoogleCalendarEntry(models.Model):
    googleEventId = models.CharField(max_length=255, unique=True)
    recurringEventId = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField(null=True, blank=True)
    lastUpdated = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.summary}"

    def clean(self):
        if self.endTime and self.startTime and self.endTime <= self.startTime:
            raise ValidationError("endTime must be after startTime.")

# Standardised event model - intention is to switch to this model at a later point
class Event(models.Model):
    title = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField(null=True, blank=True)
    startTime = models.TimeField()
    endTime = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    minAge = models.IntegerField(blank=True, null=True)
    maxAge = models.IntegerField(blank=True, null=True)
    bookingLink = models.TextField(blank=True)
    eventLink = models.TextField(blank=True)
    description = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    googleCalendarEntry = models.ForeignKey(GoogleCalendarEntry, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.title}"
