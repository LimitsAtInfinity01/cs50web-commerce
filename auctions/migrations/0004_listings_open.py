# Generated by Django 5.1.2 on 2024-11-12 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0003_winners"),
    ]

    operations = [
        migrations.AddField(
            model_name="listings",
            name="open",
            field=models.BooleanField(default=True),
        ),
    ]
