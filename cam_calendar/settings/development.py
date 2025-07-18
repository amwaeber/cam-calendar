from cam_calendar.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.0.81']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8081",  # typical Expo dev server port
    "http://localhost:19006",  # Expo Web preview port
    "http://127.0.0.1:8081",
    "http://127.0.0.1:19006",
    "http://192.168.0.81:19000",  # Expo Go DevTools
    "http://192.168.0.81:19006",  # Web bundler
    "http://192.168.0.81:8000",  # Own API access from device
]