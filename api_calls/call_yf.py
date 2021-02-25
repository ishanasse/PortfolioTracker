import asyncio
import aiohttp
import httpx
import datetime

yf_url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols="
tickers_data = {}


async def fetch_ticker_dict(ticker: str) -> dict:
    print(f"[{str(datetime.datetime.now())[:19]}] Fetching data for {ticker}")
    async with httpx.AsyncClient() as client:
        ticker_url = yf_url + ticker
        resp = await client.get(ticker_url)
        resp_dict = resp.json()

        global tickers_data
        tickers_data[ticker] = resp_dict
        # print(f"{datetime.datetime.now()} {ticker}")
        # print(resp_dict)
        return tickers_data


async def main(tickers: list) -> dict:
    # tickers = ["AAPL","TSLA","NAKD", "YYYY"]

    task_list = []
    for ticker in tickers:
        task_list.append(fetch_ticker_dict(ticker))
    await asyncio.gather(*task_list)
    # print(tickers_data)


def fetch_data(tickers: list) -> dict:
    asyncio.run(main(tickers))
    global tickers_data
    return tickers_data


# if __name__ == "__main__":
#     asyncio.run(main())
# print(getdata(["AAPL","TSLA","NAKD", "YYYY"]))
# print(f"{str(datetime.datetime.now())} Operation Completed")
