import requests
import json

#nobitex api key
nobitex_api_key = "your_api_key"
nobitex_api_secret = "your_api_secret"

def get_nobitex_price(symbol):
    url = f"https://api.nobitex.ir/v3/orderbook/{symbol}"
    response = requests.get(url)
    data = response.json()
    return data

currency_list = list(get_nobitex_price('all').keys())
currency_list.remove('status')


for currency in currency_list:
    print(f"{currency} : asks is {get_nobitex_price(currency)['asks'][0]} and bids is {get_nobitex_price(currency)['bids'][0]}")

