from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from portfoliowebsite.models import TickerModel
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User, auth
from django.contrib import messages
from backend.retrieve_tickers_data import retrieve_data
from backend.retrieve_tickers_data import get_market_price


# Create your views here.
class Portfolio(View):
    def get(self, request):
        stocks = TickerModel.objects.all()
        portfolio_symbols = []
        stocks_buy_stats = {}
        for stock in stocks:
            portfolio_symbols.append(stock.ticker_symbol)
            stocks_buy_stats[stock.ticker_symbol] = {"buy_price": stock.buy_price}
            stocks_buy_stats[stock.ticker_symbol]["buy_quantity"] = stock.buy_quantity
        # print(stocks_buy_stats)
        additional_data = get_market_price(portfolio_symbols)
        for stock in portfolio_symbols:
            additional_data[stock]["pl_amount"] = round(
                (
                    additional_data[stock]["market_price"]
                    - stocks_buy_stats[stock]["buy_price"]
                )
                * stocks_buy_stats[stock]["buy_quantity"],
                2,
            )
            additional_data[stock]["pl_percent"] = round(
                (additional_data[stock]["pl_amount"] * 100)
                / (
                    stocks_buy_stats[stock]["buy_price"]
                    * stocks_buy_stats[stock]["buy_quantity"]
                ),
                2,
            )
        print(additional_data)
        return render(
            request,
            "portfolio.html",
            {"stocks": stocks, "additional_data": additional_data},
        )

    def post(self, request):
        if "sell" in request.POST:
            sell_ticker = request.POST.get("sell")
            print(f"Selling {sell_ticker}")
            TickerModel.objects.filter(ticker_symbol=sell_ticker).delete()
            stocks = TickerModel.objects.all()
            return render(request, "portfolio.html", {"stocks": stocks})


class SearchToAdd(View):

    ticker = ""
    ticker_data = {}

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
            if len(TickerModel.objects.all()) > 10:
                messages.warning(
                    request, "FAILURE: Unable to track more than 10 stocks."
                )
                return redirect("/portfolio/")
            try:
                buy_quantity = int(request.POST.get("buy_quantity"))
                if buy_quantity > 0 and buy_quantity < 1001:
                    # ticker_owner = request.user
                    ticker_symbol = SearchToAdd.ticker_data["symbol"]
                    ticker_company = SearchToAdd.ticker_data["shortName"]
                    ticker_exchange = SearchToAdd.ticker_data["fullExchangeName"]
                    buy_price = SearchToAdd.ticker_data["regularMarketPrice"]
                    bought_when = str(date.today())
                    # is_sold = SearchToAdd.ticker_data[""]
                    # profit_loss = SearchToAdd.ticker_data[""]
                    # pl_percent = SearchToAdd.ticker_data[""]
                    # sell_price = SearchToAdd.ticker_data[""]
                    TickerModel.objects.create(
                        ticker_symbol=ticker_symbol.upper(),
                        ticker_company=ticker_company,
                        ticker_exchange=ticker_exchange.upper(),
                        buy_price=buy_price,
                        buy_quantity=buy_quantity,
                        bought_when=bought_when,
                    )
                    print(
                        f"Ticker:{SearchToAdd.ticker}  Quantity: {buy_quantity}. Created an object for this transaction."
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
