from collections import namedtuple

# from django.contrib.auth.models import User
from portfoliowebsite.models import PortfolioHistoryModel, TransactionsModel
from datetime import date


def move_to_pt_history(data: dict):
    # PortfolioHistoryModel.objects.all().delete()
    overall_pl = round((data["sellprice"] - data["buyprice"]) * data["sellquantity"], 2)
    history_objects = (
        PortfolioHistoryModel.objects.filter(thistory_owner=data["owner"])
    ).filter(thistory_symbol=data["symbol"])

    if len(history_objects) > 0:
        for item in history_objects:
            print(f"{item.thistory_symbol} is already in history")
            item.thistory_bprice = round(
                (
                    (
                        (item.thistory_bprice * item.thistory_squantity)
                        + (data["buyprice"] * data["sellquantity"])
                    )
                    / (item.thistory_squantity + data["sellquantity"])
                ),
                2,
            )
            item.thistory_sprice = round(
                (
                    (item.thistory_sprice * item.thistory_squantity)
                    + (data["sellprice"] * data["sellquantity"])
                    / (item.thistory_squantity + data["sellquantity"])
                ),
                2,
            )
            item.thistory_squantity = item.thistory_squantity + data["sellquantity"]
            item.thistory_swhen = data["selldate"]
            item.thistory_overallpl = round((item.thistory_overallpl + overall_pl), 2)
            item.thistory_plper = round(
                item.thistory_overallpl
                / (item.thistory_squantity * item.thistory_bprice),
                2,
            )
            item.save()
    else:
        pl_per = round(
            ((overall_pl * 100) / (data["sellquantity"] * data["buyprice"])), 2
        )
        PortfolioHistoryModel.objects.create(
            thistory_symbol=data["symbol"],
            thistory_company=data["company"],
            thistory_exchange=data["exchange"],
            thistory_owner=data["owner"],
            thistory_bprice=data["buyprice"],  # avg_buy_price
            thistory_squantity=data["sellquantity"],
            thistory_bwhen=data["buydate"],
            thistory_swhen=data["selldate"],
            thistory_sprice=data["sellprice"],
            thistory_overallpl=overall_pl,
            thistory_plper=pl_per,
            thistory_pcolor="#1da400" if overall_pl > 0 else "#bd0000",
        )


def add_to_trans(data: list):
    pl = "-"
    plper = ""
    pcolor = "#000000"
    ttype = data[4]
    price = data[5]
    quantity = data[6]
    avg_buy = data[8]
    if ttype == "SELL":
        cost = float(avg_buy) * quantity
        value = price * quantity
        pl = round((value - cost), 2)
        plper = round(((pl / cost) * 100), 2)
        pcolor = "#1da400" if (float(pl)) > 0 else "#bd0000"
    TransactionsModel.objects.create(
        owner=data[0],
        symbol=data[1],
        company=data[2],
        exchange=data[3],
        ttype=ttype,
        price=price,
        quantity=quantity,
        date=data[7],
        avg_buy=avg_buy,
        pl=pl,
        plper=plper,
        pcolor=pcolor,
    )


# def get_portfolio_stats(user):
#     #Pstats = namedtuple('Pstats',['no_of_trans','total_invested','market_value','pl','return'])
#     transactions = TransactionsModel.objects.filter(owner=user)
#     sincebought = {"no_of_trans":len(transactions),"total_invested":0,"market_value":0,"pl":0,"return":0}
#     today = {"no_of_trans":len(transactions.filter(date=str(date.today()))),"total_invested":0,"market_value":0,"pl":0,"return":0}
#     return (sincebought, today)
