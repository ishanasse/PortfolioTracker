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
    # profit_loss = models.FloatField(max_length=25)
    # pl_percent = models.CharField(max_length=25)
    # is_sold = models.BooleanField()
    # sell_price = models.FloatField(max_length=25)
    # is_sold = False
    # sell_price = None

    # def __str__(self):
    #     return str(self.ticker_symbol)+str(self.ticker_owner)


class PortfolioHistoryModel(models.Model):
    thistory_symbol = models.CharField(max_length=25)
    thistory_company = models.CharField(max_length=50)
    thistory_owner = models.ForeignKey(
        User, related_name="thistory_owner", on_delete=models.CASCADE
    )
    thistory_bprice = models.FloatField(max_length=25)
    thistory_bquantity = models.IntegerField()
    thistory_bwhen = models.CharField(max_length=50)
    thistory_swhen = models.CharField(max_length=50)
    close_pl = models.FloatField()
