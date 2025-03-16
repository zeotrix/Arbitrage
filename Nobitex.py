import aiohttp
import asyncio


# Nobitex API key
nobitex_api_key = "your_api_key"
nobitex_api_secret = "your_api_secret"

async def get_nobitex_price(session, symbol):
    url = f"https://api.nobitex.ir/v3/orderbook/{symbol}"
    async with session.get(url) as response:
        data = await response.json()
        return data

async def fetch_all_prices():
    async with aiohttp.ClientSession() as session:
        # Fetch the list of currencies
        initial_data = await get_nobitex_price(session, 'all')
        currency_list = list(initial_data.keys())
        currency_list.remove('status')

        # Fetch prices for each currency concurrently
        tasks = []
        for currency in currency_list:
            task = asyncio.create_task(get_nobitex_price(session, currency))
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)

        # Print the results
        for currency, result in zip(currency_list, results):
            if 'asks' in result and 'bids' in result and len(result['asks']) > 0 and len(result['bids']) > 0:
                print(f"{currency} : asks is {result['asks'][0]} and bids is {result['bids'][0]}")
            else:
                print(f"{currency} : No data available")


async def new():
    async with aiohttp.ClientSession() as session:
        # Fetch the list of currencies
        initial_data = await get_nobitex_price(session, 'BTCIRT')
        print(initial_data["lastTradePrice"])
        currency_list = list(initial_data.keys())
        currency_list.remove('status')

# Run the async function
asyncio.run(new())