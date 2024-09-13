# Generated by Django 4.2.10 on 2024-04-17 13:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0035_processlock"),
    ]

    operations = [
        migrations.CreateModel(
            name="PublicConversation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("conversation_log", models.JSONField(default=dict)),
                ("slug", models.CharField(blank=True, default=None, max_length=200, null=True)),
                ("title", models.CharField(blank=True, default=None, max_length=200, null=True)),
                (
                    "agent",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="database.agent",
                    ),
                ),
                (
                    "source_owner",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
