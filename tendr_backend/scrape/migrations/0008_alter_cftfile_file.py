# Generated by Django 4.2.9 on 2024-01-18 09:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scrape", "0007_tender_client_info"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cftfile",
            name="file",
            field=models.FileField(blank=True, null=True, unique=True, upload_to="cft_file/"),
        ),
    ]