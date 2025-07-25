# Generated by Django 5.2.1 on 2025-07-02 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCalendarEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('googleEventId', models.CharField(max_length=255, unique=True)),
                ('recurringEventId', models.CharField(blank=True, max_length=255, null=True)),
                ('summary', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('lastUpdated', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('description', models.TextField()),
                ('bookingDetails', models.TextField()),
                ('eventPage', models.TextField()),
                ('location', models.CharField(max_length=200)),
                ('rejected', models.BooleanField(default=False)),
                ('googleCalendarEntry', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.googlecalendarentry')),
            ],
        ),
    ]
