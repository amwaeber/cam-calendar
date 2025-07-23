from cam_calendar.settings.base import *

DEBUG = False

ALLOWED_HOSTS = ["mydomain.com"]

CORS_ALLOWED_ORIGINS = [
    "https://my-frontend.com"
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True