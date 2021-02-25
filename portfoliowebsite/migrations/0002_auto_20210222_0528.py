# Generated by Django 3.1.6 on 2021-02-22 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("portfoliowebsite", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tickermodel",
            name="ticker_owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ticker_owner",
                to=settings.AUTH_USER_MODEL,
            ),
        )
    ]