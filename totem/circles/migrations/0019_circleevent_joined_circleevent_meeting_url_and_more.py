# Generated by Django 4.2.4 on 2023-09-01 08:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("circles", "0018_remove_circle_duration"),
    ]

    operations = [
        migrations.AddField(
            model_name="circleevent",
            name="joined",
            field=models.ManyToManyField(blank=True, related_name="events_joined", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="circleevent",
            name="meeting_url",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="circleevent",
            name="attendees",
            field=models.ManyToManyField(blank=True, related_name="events_attending", to=settings.AUTH_USER_MODEL),
        ),
    ]
