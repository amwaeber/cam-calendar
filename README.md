Syncing Google Calendar using a cron job:
*/10 * * * * ~/repos/cam-calendar/.condaenv/bin/python ~/repos/cam-calendar/manage.py sync_calendar

Migrate database
python manage.py makemigrations
python manage.py migrate

Run backend
python manage.py runserver

