import asyncio
import aiohttp
from django.core.management.base import BaseCommand
from crypto.models import Prices
from asgiref.sync import sync_to_async

class Command(BaseCommand):
    help = 'Fetches and updates Nobitex currency data'

    @sync_to_async
    def get_currencies_from_db(self):
        # Get all unique currencies from the database
        return list(Prices.objects.values_list('currencies', flat=True).distinct())

    async def get_nobitex_price(self, session, symbol):
        url = f"https://api.nobitex.ir/v3/orderbook/{symbol}"
        async with session.get(url) as response:
            data = await response.json()
            return data

    @sync_to_async
    def update_currency_price(self, currency, trade_price):
        Prices.objects.filter(currencies=currency).update(
            nobitex_last_trade_price=trade_price
        )

    async def fetch_all_prices(self):
        async with aiohttp.ClientSession() as session:
            # Get currencies from database
            currency_list = await self.get_currencies_from_db()

            # Fetch prices for each currency concurrently
            tasks = {}
            
            for currency in currency_list:                
                
                task = asyncio.create_task(self.get_nobitex_price(session, currency))
                tasks[currency] = task
            
            # Wait for all tasks to complete
            results = {}
            for currency, task in tasks.items():
                results[currency] = await task
           
        
            # Update the database using sync_to_async
            for currency in currency_list:
                if len(results) > 0:
                    trade_price = results[currency]['lastTradePrice']  # Last trade price
                    await self.update_currency_price(currency, trade_price)
                    self.stdout.write(self.style.SUCCESS(f"Updated {currency}: Trade Price={trade_price}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No data available for {currency}"))

    def handle(self, *args, **kwargs):
        asyncio.run(self.fetch_all_prices())