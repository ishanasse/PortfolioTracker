from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class PortfolioModel(models.Model):
    ticker_symbol = models.CharField(max_length=25)
    ticker_company = models.CharField(max_length=50)
    ticker_exchange = models.CharField(max_length=50)
    ticker_owner = models.ForeignKey(
        User, related_name="ticker_owner", on_delete=models.CASCADE
    )
    buy_price = models.FloatField(max_length=25)
    buy_quantity = models.IntegerField()
    bought_when = models.CharField(max_length=50)
    # total_invested = models.FloatField(max_length=25)
    # market_value = models.FloatField(max_length=25)
    # total_pl = models.FloatField(max_length=25)


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
    symbol = models.CharField(max_length=25)
    company = models.CharField(max_length=50)
    exchange = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    ttype = models.CharField(max_length=25)
    price = models.FloatField(max_length=25)
    quantity = models.IntegerField()
    date = models.CharField(max_length=50)
    avg_buy = models.CharField(max_length=25)
    pl = models.CharField(max_length=25)
    plper = models.CharField(max_length=25)
    pcolor = models.CharField(max_length=25)
