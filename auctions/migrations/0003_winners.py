# Generated by Django 5.1.2 on 2024-11-12 04:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_alter_listings_owner"),
    ]

    operations = [
        migrations.CreateModel(
            name="Winners",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "listing_won",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auctions.listings",
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
