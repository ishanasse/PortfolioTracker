from portfoliowebsite.models import PortfolioHistoryModel

# ({symbol:sell_instance.ticker_symbol,company:sell_instance.ticker_company, owner:sell_instance.ticker_owner,
#             buyprice:sell_instance.buy_price, buydate:sell_instance.bought_when, sellprice:get_market_price([sell_instance])[sell_instance],
#             selldate:str(date.today())})
#             sell_instance.delete()

# thistory_symbol = models.CharField(max_length=25)
# thistory_company = models.CharField(max_length=50)
# thistory_owner = models.ForeignKey(
#     User, related_name="thistory_owner", on_delete=models.CASCADE
# )
# thistory_bprice = models.FloatField(max_length=25)
# thistory_bquantity = models.IntegerField()
# thistory_bwhen = models.CharField(max_length=50)
# thistory_swhen = models.CharField(max_length=50)
# close_pl = models.FloatField()
def move_to_pt_history(data: dict):
    thistory_symbol = data["symbol"]
    thistory_company = data[""]
    thistory_owner = data["owner"]
    thistory_bprice = data["buyprice"]
    thistory_bquantity = data["buyquantity"]
    thistory_ = data[""]
    thistory_ = data[""]
    thistory_ = data[""]
