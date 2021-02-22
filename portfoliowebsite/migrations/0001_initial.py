# Generated by Django 3.1.6 on 2021-02-22 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TickerModel",
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
                ("ticker_symbol", models.CharField(max_length=25)),
                ("ticker_owner", models.CharField(max_length=25)),
                ("ticker_company", models.CharField(max_length=50)),
                ("ticker_exchange", models.CharField(max_length=50)),
                ("buy_price", models.FloatField(max_length=25)),
                ("buy_quantity", models.IntegerField()),
                ("bought_when", models.CharField(max_length=50)),
            ],
        )
    ]
