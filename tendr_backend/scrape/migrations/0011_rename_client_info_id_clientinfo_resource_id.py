# Generated by Django 4.2.9 on 2024-01-18 16:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("scrape", "0010_remove_tender_client_info_clientinfo_client_info_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="clientinfo",
            old_name="client_info_id",
            new_name="resource_id",
        ),
    ]
