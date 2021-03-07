from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class TickerModel(models.Model):
    ticker_symbol = models.CharField(max_length=25)
    ticker_company = models.CharField(max_length=50)
    ticker_exchange = models.CharField(max_length=50)
    ticker_owner = models.ForeignKey(
        User, related_name="ticker_owner", on_delete=models.CASCADE
    )
    buy_price = models.FloatField(max_length=25)
    buy_quantity = models.IntegerField()
    bought_when = models.CharField(max_length=50)


class PortfolioHistoryModel(models.Model):
    thistory_symbol = models.CharField(max_length=25)
    thistory_company = models.CharField(max_length=50)
    thistory_exchange = models.CharField(max_length=50)
    thistory_owner = models.ForeignKey(
        User, related_name="thistory_owner", on_delete=models.CASCADE
    )
    thistory_bprice = models.FloatField(max_length=25)
    thistory_squantity = models.IntegerField()
    thistory_bwhen = models.CharField(max_length=50)
    thistory_swhen = models.CharField(max_length=50)
    thistory_sprice = models.FloatField(max_length=25)
    thistory_overallpl = models.FloatField()
    thistory_plper = models.FloatField()
    thistory_pcolor = models.CharField(max_length=25)


class TransactionsModel(models.Model):
    trans_symbol = models.CharField(max_length=25)
    trans_company = models.CharField(max_length=50)
    trans_exchange = models.CharField(max_length=50)
    trans_owner = models.ForeignKey(
        User, related_name="trans_owner", on_delete=models.CASCADE
    )
    trans_type = models.CharField(max_length=25)
    trans_price = models.FloatField(max_length=25)
    trans_quantity = models.IntegerField()
    trans_date = models.CharField(max_length=50)
    trans_pl = models.CharField(max_length=25)
    trans_plper = models.CharField(max_length=25)
    trans_pcolor = models.CharField(max_length=25)
