# Generated by Django 4.2.7 on 2024-01-15 18:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("database", "0024_alter_entry_embeddings"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchmodelconfig",
            name="embeddings_inference_endpoint",
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="searchmodelconfig",
            name="embeddings_inference_endpoint_api_key",
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
