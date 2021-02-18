from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class TickerModel(models.Model):
    # ticker_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker_symbol = models.CharField(max_length=25)
    ticker_company = models.CharField(max_length=50)
    ticker_exchange = models.CharField(max_length=50)
    # mrkt_price = models.FloatField(max_length=25)
    buy_price = models.FloatField(max_length=25)
    buy_quantity = models.IntegerField()
    bought_when = models.CharField(max_length=50)
    # profit_loss = models.FloatField(max_length=25)
    # pl_percent = models.CharField(max_length=25)
    # is_sold = models.BooleanField()
    # sell_price = models.FloatField(max_length=25)

    # def __str__(self):
    #     return str(self.ticker_symbol)+str(user)

    # ticker = "AAPL"
    # ticker_company = "Apple Inc."
    # ticker_type = "Equity"
    # ticker_exchange = "NYSE"

    # buy_price = 200
    # quantity = 50
    # bought_when = str(datetime.datetime.now())[:19]

    # volume = 100000

    # is_sold = False
    # sell_price = None

    # title = models.CharField(max_length=100)
    # category = models.CharField(max_length=30)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    # content = models.TextField()
    # created_at = models.DateTimeField(default=timezone.now)
