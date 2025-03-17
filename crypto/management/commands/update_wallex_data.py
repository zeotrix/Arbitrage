import asyncio
import aiohttp
from django.core.management.base import BaseCommand
from crypto.models import Prices
from asgiref.sync import sync_to_async

class Command(BaseCommand):
    help = 'Fetches and updates Wallex currency data'

    @sync_to_async
    def get_currencies_from_db(self):
        # Get all unique currencies from the database
        return list(Prices.objects.values_list('currencies', flat=True).distinct())

    async def get_wallex_price(self, session, symbol):
        url = f"https://api.wallex.ir/v1/trades?symbol={symbol}"
        timeout = aiohttp.ClientTimeout(total=1)  # Set a 10-second timeout
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status == 429:
                    await asyncio.sleep(1)  # Handle rate limiting
                    return await self.get_wallex_price(session, symbol)
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type:
                    self.stdout.write(self.style.WARNING(f"Unexpected content type for {symbol}: {content_type}"))
                    return {"success": False}
                data = await response.json()
                return data
        except asyncio.TimeoutError:
            self.stdout.write(self.style.ERROR(f"Request timed out for {symbol}"))
            return {"success": False}
        except aiohttp.ClientError as e:
            self.stdout.write(self.style.ERROR(f"Connection error for {symbol}: {e}"))
            return {"success": False}

    @sync_to_async
    def update_currency_price(self, currency, trade_price):
        Prices.objects.filter(currencies=currency).order_by('currency_id').update(
            wallex_last_trade_price=trade_price
        )

    async def fetch_all_prices(self):
        async with aiohttp.ClientSession() as session:
            # Get currencies from database
            currency_list = await self.get_currencies_from_db()

            # Fetch prices for each currency concurrently
            tasks = {}
            
            for currency in currency_list:                
                
                task = asyncio.create_task(self.get_wallex_price(session, currency))
                tasks[currency] = task
            
            # Wait for all tasks to complete
            results = {}
            for currency, task in tasks.items():
                results[currency] = await task
           
            
            # Update the database using sync_to_async
            for currency in currency_list:
               
                if len(results) > 0 and results[currency]["success"] == True:
                    trade_price = results[currency]["result"]["latestTrades"][0]["price"]  # Last trade price
                    await self.update_currency_price(currency, trade_price)
                    self.stdout.write(self.style.SUCCESS(f"Updated {currency}: Trade Price={trade_price}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No data available for {currency}"))

    def handle(self, *args, **kwargs):
        asyncio.run(self.fetch_all_prices())