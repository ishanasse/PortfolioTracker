# Generated by Django 3.1.6 on 2021-03-07 05:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("portfoliowebsite", "0002_auto_20210301_0021"),
    ]

    operations = [
        migrations.CreateModel(
            name="TransactionsModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("trans_symbol", models.CharField(max_length=25)),
                ("trans_company", models.CharField(max_length=50)),
                ("trans_exchange", models.CharField(max_length=50)),
                ("trans_type", models.CharField(max_length=25)),
                ("trans_price", models.FloatField(max_length=25)),
                ("trans_quantity", models.IntegerField()),
                ("trans_date", models.CharField(max_length=50)),
                ("trans_pl", models.CharField(max_length=25)),
                ("trans_plper", models.CharField(max_length=25)),
                ("trans_pcolor", models.CharField(max_length=25)),
                (
                    "trans_owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="trans_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        )
    ]
