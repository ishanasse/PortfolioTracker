from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from portfoliowebsite.models import (
    PortfolioModel,
    PortfolioHistoryModel,
    TransactionsModel,
)
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User, auth
from django.contrib import messages
from api_calls.retrieve_tickers_data import retrieve_data, get_market_price
from .backend_functions import move_to_pt_history, add_to_trans


# Create your views here.


class HomePage(View):
    def get(self, request):
        return render(request, "home.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/portfolio/")
        else:
            messages.warning(request, "invalid credentials")
            return redirect("/")


class Portfolio(View):
    def get(self, request):
        stocks = PortfolioModel.objects.filter(ticker_owner=request.user)
        portfolio_symbols = [stock.ticker_symbol for stock in stocks]
        market_price_data = get_market_price(portfolio_symbols)
        sincebought = {
            "total_invested": 0,
            "market_value": 0,
            "total_pl": 0,
            "returnper": 0,
            "date": str(date.today()),
        }
        total_invested = market_value = 0
        for stock in stocks:
            stock.market_price = round(market_price_data[stock.ticker_symbol], 2)
            stock.pl_amount = round(
                ((stock.market_price - stock.buy_price) * stock.buy_quantity), 2
            )
            stock.pl_percent = round(
                ((stock.pl_amount * 100) / (stock.buy_quantity * stock.buy_price)), 2
            )
            stock.color = "#1da400" if stock.pl_amount > 0 else "#bd0000"
            total_invested = total_invested + stock.buy_price * stock.buy_quantity
            market_value = market_value + stock.market_price * stock.buy_quantity
        total_pl = market_value - total_invested
        color = "#1da400" if total_pl > 0 else "#bd0000"
        if total_invested != 0:
            sincebought = {
                "total_invested": total_invested,
                "market_value": market_value,
                "total_pl": total_pl,
                "returnper": round((total_pl * 100 / total_invested), 2),
                "color": color,
            }
        stocks = reversed(stocks)
        return render(
            request, "portfolio.html", {"stocks": stocks, "sincebought": sincebought}
        )  # ,"today":today})

    def post(self, request):
        try:
            action_quantity = int(request.POST["qty"])
            if action_quantity > 1000 or action_quantity < 1:
                raise ValueError("Unsupported quantity")
        except:
            messages.warning(request, "Invalid quantity")
            return redirect("/portfolio/")

        if "buy" in request.POST:
            action_ticker = request.POST.get("buy")
            action_instance = (
                PortfolioModel.objects.filter(ticker_owner=request.user)
                .filter(ticker_symbol=action_ticker)
                .get()
            )
            market_price = get_market_price([action_instance.ticker_symbol])[
                action_instance.ticker_symbol
            ]
            action_instance.buy_quantity = (
                action_instance.buy_quantity + action_quantity
            )
            if action_instance.buy_quantity > 2000:
                messages.warning(
                    request,
                    "FAILURE: Not allowed to own over 2000 stocks of single Equity.",
                )
                return redirect("/portfolio/")
            action_instance.buy_price = round(
                (
                    (
                        (action_instance.buy_price * action_instance.buy_quantity)
                        + (market_price * action_quantity)
                    )
                    / (action_instance.buy_quantity + action_quantity)
                ),
                2,
            )  # avg_buy_price
            add_to_trans(
                [
                    request.user,
                    action_instance.ticker_symbol.upper(),
                    action_instance.ticker_company,
                    action_instance.ticker_exchange.upper(),
                    "BUY",
                    market_price,
                    action_quantity,
                    str(date.today()),
                    "-",
                ]
            )
            action_instance.save()
            return redirect("/portfolio/")

        else:
            action_ticker = request.POST.get("sell")
            market_price = get_market_price([action_ticker])[action_ticker]
            action_instance = (
                PortfolioModel.objects.filter(ticker_owner=request.user)
                .filter(ticker_symbol=action_ticker)
                .get()
            )
            print(f"Selling {action_ticker} Qty:{action_quantity}")

            if action_quantity > action_instance.buy_quantity:
                messages.warning(
                    request, "Quantity to sell greater-than Quantity owned"
                )
                return redirect("/portfolio/")

            else:
                add_to_trans(
                    [
                        request.user,
                        action_instance.ticker_symbol.upper(),
                        action_instance.ticker_company,
                        action_instance.ticker_exchange.upper(),
                        "SELL",
                        market_price,
                        action_quantity,
                        str(date.today()),
                        str(action_instance.buy_price),
                    ]
                )
                all_sold = False
                if action_quantity < action_instance.buy_quantity:
                    action_instance.buy_quantity = (
                        action_instance.buy_quantity - action_quantity
                    )
                    action_instance.save()

                else:
                    all_sold = True

                move_to_pt_history(
                    {
                        "symbol": action_instance.ticker_symbol,
                        "company": action_instance.ticker_company,
                        "exchange": action_instance.ticker_exchange,
                        "owner": action_instance.ticker_owner,
                        "buyprice": action_instance.buy_price,
                        "buydate": action_instance.bought_when,
                        "sellprice": get_market_price([action_ticker])[action_ticker],
                        "selldate": str(date.today()),
                        "sellquantity": action_quantity,
                    }
                )

                if all_sold == True:
                    action_instance.delete()
            return redirect("/portfolio/")


class SearchToAdd(View):

    # ticker = ""
    # ticker_data = {}

    def get(self, request):
        return render(request, "search_toadd.html")

    def post(self, request):
        if ("search" in request.POST) and (request.POST.get("ticker") != ""):
            SearchToAdd.ticker = request.POST.get("ticker")
            SearchToAdd.ticker_data = retrieve_data([SearchToAdd.ticker])[
                SearchToAdd.ticker
            ]
            if SearchToAdd.ticker_data == "invalid":
                messages.warning(request, "WARNING: invalid ticker")
                return render(request, "search_toadd.html")
            return render(
                request, "search_toadd.html", {"details": SearchToAdd.ticker_data}
            )

        elif ("buy" in request.POST) and (SearchToAdd.ticker != ""):
            print(
                f"LENGTH IS {len(PortfolioModel.objects.all().filter(ticker_owner=request.user))}"
            )
            if len(PortfolioModel.objects.all().filter(ticker_owner=request.user)) > 10:
                messages.warning(
                    request, "FAILURE: Unable to track more than 10 stocks"
                )
                return redirect("/portfolio/")
            try:
                buy_quantity = int(request.POST.get("buy_quantity"))
                if buy_quantity > 0 and buy_quantity < 1001:

                    try:
                        stock = (
                            PortfolioModel.objects.filter(ticker_owner=request.user)
                            .filter(ticker_symbol=SearchToAdd.ticker.upper())
                            .get()  # If no entries, go to except block
                        )
                        market_price = get_market_price([stock.ticker_symbol])[
                            stock.ticker_symbol
                        ]
                        stock.buy_price = round(
                            (
                                (
                                    (stock.buy_price * stock.buy_quantity)
                                    + (market_price * buy_quantity)
                                )
                                / (stock.buy_quantity + buy_quantity)
                            ),
                            2,
                        )  # avg_buy_price
                        stock.buy_quantity = stock.buy_quantity + buy_quantity
                        if stock.buy_quantity > 2000:
                            messages.warning(
                                request,
                                "FAILURE: Not allowed to own over 2000 stocks of single Equity.",
                            )
                            return redirect("/portfolio/")
                        add_to_trans(
                            [
                                request.user,
                                stock.ticker_symbol.upper(),
                                stock.ticker_company,
                                stock.ticker_exchange.upper(),
                                "BUY",
                                market_price,
                                buy_quantity,
                                str(date.today()),
                                "-",
                            ]
                        )
                        stock.save()
                        return redirect("/portfolio/")

                    except:
                        # ticker_symbol = SearchToAdd.ticker_data["symbol"]
                        # ticker_company = SearchToAdd.ticker_data["shortName"]
                        # ticker_exchange = SearchToAdd.ticker_data["fullExchangeName"]
                        # buy_price = SearchToAdd.ticker_data["regularMarketPrice"]
                        # bought_when = str(date.today())
                        PortfolioModel.objects.create(
                            ticker_owner=request.user,
                            ticker_symbol=SearchToAdd.ticker_data["symbol"].upper(),
                            ticker_company=SearchToAdd.ticker_data["shortName"],
                            ticker_exchange=SearchToAdd.ticker_data[
                                "fullExchangeName"
                            ].upper(),
                            buy_price=SearchToAdd.ticker_data["regularMarketPrice"],
                            buy_quantity=buy_quantity,
                            bought_when=str(date.today()),
                        )
                        add_to_trans(
                            [
                                request.user,
                                SearchToAdd.ticker_data["symbol"].upper(),
                                SearchToAdd.ticker_data["shortName"],
                                SearchToAdd.ticker_data["fullExchangeName"].upper(),
                                "BUY",
                                SearchToAdd.ticker_data["regularMarketPrice"],
                                buy_quantity,
                                str(date.today()),
                                "-",
                            ]
                        )

                        print(
                            f"Ticker:{SearchToAdd.ticker}  Quantity: {buy_quantity}. Created an object for this transaction"
                        )
                        return redirect("/portfolio/")
                else:
                    messages.warning(request, "WARNING: unsupported quantity")
                    return render(
                        request,
                        "search_toadd.html",
                        {"details": SearchToAdd.ticker_data},
                    )
            except:
                messages.warning(request, "WARNING: invalid quantity")
                return render(
                    request, "search_toadd.html", {"details": SearchToAdd.ticker_data}
                )

        else:
            messages.warning(request, "WARNING: invalid ticker")
            return render(request, "search_toadd.html")


class PortfolioHistory(View):
    def get(self, request):
        history = PortfolioHistoryModel.objects.filter(thistory_owner=request.user)
        history_symbols = [item.thistory_symbol for item in history]
        market_price_data = get_market_price(history_symbols)
        for item in history:
            item.thistory_mprice = round(market_price_data[item.thistory_symbol], 2)
        history = reversed(history)
        return render(request, "portfoliohistory.html", {"history": history})

    def post(self, request):
        try:
            action_quantity = int(request.POST["qty"])
            if action_quantity > 1000 or action_quantity < 1:
                raise ValueError("Unsupported quantity")
        except:
            messages.warning(request, "Invalid quantity")
            return redirect("/portfolio/history/")

        if "buy" in request.POST:
            action_ticker = request.POST.get("buy")
            action_instance = (
                PortfolioModel.objects.filter(ticker_owner=request.user)
                .filter(ticker_symbol=action_ticker)
                .get()
            )
            market_price = get_market_price([action_instance.ticker_symbol])[
                action_instance.ticker_symbol
            ]
            action_instance.buy_price = round(
                (
                    (
                        (action_instance.buy_price * action_instance.buy_quantity)
                        + (market_price * action_quantity)
                    )
                    / (action_instance.buy_quantity + action_quantity)
                ),
                2,
            )  # avg_buy_price
            action_instance.buy_quantity = (
                action_instance.buy_quantity + action_quantity
            )
            if action_instance.buy_quantity > 2000:
                messages.warning(
                    request,
                    "FAILURE: Not allowed to own over 2000 stocks of single Equity.",
                )
                return redirect("/portfolio/history/")
            action_instance.save()
            return redirect("/portfolio/history/")

        else:
            action_ticker = request.POST.get("sell")
            action_instance = (
                PortfolioModel.objects.filter(ticker_owner=request.user)
                .filter(ticker_symbol=action_ticker)
                .get()
            )
            print(f"Selling {action_ticker} Qty:{action_quantity}")

            if action_quantity > action_instance.buy_quantity:
                messages.warning(
                    request, "Quantity to sell greater-than Quantity owned"
                )
                return redirect("/portfolio/")

            else:
                all_sold = False
                if action_quantity < action_instance.buy_quantity:
                    action_instance.buy_quantity = (
                        action_instance.buy_quantity - action_quantity
                    )
                    action_instance.save()

                else:
                    all_sold = True

                print(
                    action_instance.ticker_owner,
                    action_instance.ticker_symbol,
                    action_quantity,
                )
                move_to_pt_history(
                    {
                        "symbol": action_instance.ticker_symbol,
                        "company": action_instance.ticker_company,
                        "owner": action_instance.ticker_owner,
                        "buyprice": action_instance.buy_price,
                        "buydate": action_instance.bought_when,
                        "sellprice": get_market_price([sell_ticker])[sell_ticker],
                        "selldate": str(date.today()),
                        "sellquantity": action_quantity,
                    }
                )

                if all_sold == True:
                    action_instance.delete()
            return redirect("/portfolio/")


class AllTransactions(View):
    def get(self, request):
        transactions = reversed(TransactionsModel.objects.filter(owner=request.user))
        return render(request, "transactions.html", {"transactions": transactions})
