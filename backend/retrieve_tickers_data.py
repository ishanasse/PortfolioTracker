from call_yf import fetch_data
from pprint import pprint

important_details_list=['quoteType', 'shortName', 'fullExchangeName', 'regularMarketPrice', 'marketState',
                         'regularMarketChange', 'regularMarketChangePercent', 'regularMarketDayRange',
                         'fiftyTwoWeekRange','fiftyDayAverage','financialCurrency','regularMarketVolume']

def retrieve_data(tickers: list) -> dict:
    tickers_data = fetch_data(tickers)
    verified_tickers_data = {}
    
    for ticker in tickers:        
        if len(tickers_data[ticker]['quoteResponse']['result']) == 0:
            verified_tickers_data[ticker] = "invalid"
        else:
            verified_tickers_data[ticker] = {}
            for detail in important_details_list:
                verified_tickers_data[ticker][detail] = tickers_data[ticker]['quoteResponse']['result'][0][detail]
    pprint(verified_tickers_data)


retrieve_data(["AAPL","TSLA","NAKD", "YYYY"])