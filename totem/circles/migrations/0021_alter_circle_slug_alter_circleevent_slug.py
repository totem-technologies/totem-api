# Generated by Django 4.2.5 on 2023-09-18 01:07

from django.db import migrations, models
import totem.utils.models


class Migration(migrations.Migration):
    dependencies = [
        ("circles", "0020_circleevent_advertised_circleevent_notified"),
    ]

    operations = [
        migrations.AlterField(
            model_name="circle",
            name="slug",
            field=models.SlugField(blank=True, default=totem.utils.models.make_slug, unique=True),
        ),
        migrations.AlterField(
            model_name="circleevent",
            name="slug",
            field=models.SlugField(blank=True, default=totem.utils.models.make_slug, unique=True),
        ),
    ]
