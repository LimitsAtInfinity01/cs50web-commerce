# Generated by Django 5.1.2 on 2024-11-05 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="listings",
            name="closing_time",
        ),
        migrations.AlterField(
            model_name="listings",
            name="image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
