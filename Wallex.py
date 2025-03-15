import aiohttp
import asyncio

# Wallex API key
wallex_api_key = "your_api_key"
wallex_api_secret = "your_api_secret"

async def get_wallex_currency_list(session):
    url = "https://api.wallex.ir/v1/markets"
    async with session.get(url) as response:
        data = await response.json()
        return data

async def get_wallex_price(session, symbol):
    url = f"https://api.wallex.ir/v1/depth?symbol={symbol}"
    async with session.get(url) as response:
        data = await response.json()
        return data

async def fetch_all_prices():
    async with aiohttp.ClientSession() as session:
        # Fetch the list of currencies
        currency_data = await get_wallex_currency_list(session)
        currency_list = list(currency_data["result"]["symbols"].keys())

        # Fetch prices for each currency concurrently
        tasks = []
        for currency in currency_list:
            task = asyncio.create_task(get_wallex_price(session, currency))
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)

        # Print the results
        for currency, result in zip(currency_list, results):
            if "result" in result and "ask" in result["result"] and "bid" in result["result"]:
                ask_price = result["result"]["ask"][0] if len(result["result"]["ask"]) > 0 else "N/A"
                bid_price = result["result"]["bid"][0] if len(result["result"]["bid"]) > 0 else "N/A"
                print(f"Currency is {currency}, ask is {ask_price}, and bid is {bid_price}")
            else:
                print(f"{currency} : No data available")

# Run the async function
asyncio.run(fetch_all_prices())