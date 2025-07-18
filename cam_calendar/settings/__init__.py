import os

env = os.getenv("DJANGO_ENV", "development").lower()
print(env)
if env == "production":
    from cam_calendar.settings.production import *
else:
    from cam_calendar.settings.development import *