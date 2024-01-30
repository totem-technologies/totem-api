# Generated by Django 5.0.1 on 2024-01-30 22:13

import django.core.validators
import totem.utils.md
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0025_remove_actiontoken_used_alter_actiontoken_expires_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="keeperprofile",
            name="bio",
            field=totem.utils.md.MarkdownField(
                blank=True,
                max_length=500,
                validators=[
                    totem.utils.md.MarkdownMixin.validate_markdown,
                    django.core.validators.MaxLengthValidator(500),
                ],
            ),
        ),
    ]
