from django.urls import path

from . import views

urlpatterns = [
    path('events/', views.GoogleCalendarEntryList.as_view(), name='google-calendar-events'),
]
