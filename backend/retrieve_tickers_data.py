from backend.call_yf import fetch_data
from pprint import pprint

important_details_list = [
    "quoteType",
    "shortName",
    "fullExchangeName",
    "regularMarketPrice",
    "marketState",
    "regularMarketChange",
    "regularMarketChangePercent",
    "regularMarketDayRange",
    "fiftyTwoWeekRange",
    "fiftyDayAverage",
    "currency",
    "regularMarketVolume",
    "symbol",
    "regularMarketOpen",
    "regularMarketPreviousClose",
]


def retrieve_data(tickers: list) -> dict:
    tickers_data = fetch_data(tickers)
    verified_tickers_data = {}

    for ticker in tickers:
        if len(tickers_data[ticker]["quoteResponse"]["result"]) == 0:
            verified_tickers_data[ticker] = "invalid"
        else:
            verified_tickers_data[ticker] = {}
            for detail in important_details_list:
                try:
                    detail_data = tickers_data[ticker]["quoteResponse"]["result"][0][
                        detail
                    ]
                    if detail == "shortName" and len(detail_data) > 18:
                        detail_data = detail_data[:18]
                except:
                    detail_data = "--"
                verified_tickers_data[ticker][detail] = detail_data
    return verified_tickers_data
    # pprint(verified_tickers_data)


# retrieve_data(["AAPL","TSLA","NAKD", "YYYY"])
