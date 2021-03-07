from portfoliowebsite.models import PortfolioHistoryModel, TransactionsModel


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
    TransactionsModel.objects.create(
        trans_owner=data[0],
        trans_symbol=data[1],
        trans_company=data[2],
        trans_exchange=data[3],
        trans_type=data[4],
        trans_price=data[5],
        trans_quantity=data[6],
        trans_date=data[7],
        trans_pl=data[8],
        trans_plper=data[9],
        trans_pcolor=data[10],
    )
