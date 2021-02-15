import asyncio
import aiohttp
import httpx
import datetime

yf_url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols="

async def fetch_ticker_dict(ticker: str) -> dict:
    print(f"{datetime.datetime.now()} Fetching data for {ticker}")
    async with httpx.AsyncClient() as client:
        ticker_url = yf_url + ticker
        resp = await client.get(ticker_url)
        resp_dict = resp.json()
        print(f"{datetime.datetime.now()} {ticker}")
        print(resp_dict)

async def main():
    ticker_list = ["AAPL","TSLA","NAKD", "YYYY"]

    task_list = []
    for ticker in ticker_list:
        task_list.append(fetch_ticker_dict(ticker))
    await asyncio.gather(*task_list)

if __name__ == "__main__":
    asyncio.run(main())
