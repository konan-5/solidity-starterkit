# Generated by Django 4.2.9 on 2024-01-19 13:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scrape", "0012_remove_clientinfo_resource_id_clientinfo_tendr_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cftfile",
            name="file",
            field=models.CharField(blank=True, max_length=2048, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="tender",
            name="notice_pdf",
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
