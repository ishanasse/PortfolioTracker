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
        if not request.user.is_authenticated:
            messages.warning(request, "Please log-in to access your Portfolio.")
            return redirect("/")
        # stocks = TickerModel.objects.all()
        stocks = TickerModel.objects.filter(ticker_owner=request.user)
        stocks_buy_stats = {}
        portfolio_symbols = [stock.ticker_symbol for stock in stocks]
        market_price_data = get_market_price(portfolio_symbols)
        # print(market_price_data)
        for stock in stocks:
            stock.market_price = market_price_data[stock.ticker_symbol]
            stock.pl_amount = round(
                ((stock.market_price - stock.buy_price) * stock.buy_quantity), 2
            )
            stock.pl_percent = round(
                ((stock.pl_amount * 100) / (stock.buy_quantity * stock.buy_price)), 2
            )
            stock.color = "#22bd00" if stock.pl_amount > 0 else "#bd0000"
        return render(request, "portfolio.html", {"stocks": stocks})

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
        if not request.user.is_authenticated:
            messages.warning(request, "Please log-in to update your Portfolio.")
            return redirect("/")
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
                    for stock in TickerModel.objects.all():
                        print(stock.ticker_symbol, SearchToAdd.ticker)
                        if (SearchToAdd.ticker == stock.ticker_symbol) or (
                            SearchToAdd.ticker.upper() == stock.ticker_symbol
                        ):
                            stock.buy_quantity = stock.buy_quantity + buy_quantity
                            stock.save()
                            return redirect("/portfolio/")
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
                        ticker_owner=request.user,
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
