# Generated by Django 4.2.9 on 2024-01-15 16:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("waitlist", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="waiter",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]