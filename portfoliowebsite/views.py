from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from portfoliowebsite.models import TickerModel
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User, auth
from django.contrib import messages
from backend.retrieve_tickers_data import retrieve_data


# Create your views here.
class Portfolio(View):
    def get(self, request):
        stocks = TickerModel.objects.all()
        print(stocks)
        return render(request, "portfolio.html", {"stocks": stocks})

    def post(self, request):
        title = request.POST["title"]
        category = request.POST["category"]
        # author = request.POST["author"]
        author = request.user
        content = request.POST["content"]

        TickerModel.objects.create(
            title=title,
            category=category.upper(),
            author=author,
            content=content,
            created_at=datetime.now(),
        )
        return redirect("/articles/")


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
            try:
                buy_quantity = int(request.POST.get("buy_quantity"))
                if buy_quantity > 0 and buy_quantity < 1001:
                    # ticker_owner = request.user
                    ticker_symbol = SearchToAdd.ticker_data["symbol"]
                    ticker_company = SearchToAdd.ticker_data["shortName"]
                    ticker_exchange = SearchToAdd.ticker_data["fullExchangeName"]
                    buy_price = SearchToAdd.ticker_data["regularMarketPrice"]
                    bought_when = datetime.now()
                    # profit_loss = SearchToAdd.ticker_data[""]
                    # pl_percent = SearchToAdd.ticker_data[""]
                    # is_sold = SearchToAdd.ticker_data[""]
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
