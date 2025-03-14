
import requests
# Wallex API key
wallex_api_key = "your_api_key"
wallex_api_secret = "your_api_secret"

def get_wallex_currency_list():
    url = f"https://api.wallex.ir/v1/markets"
    response = requests.get(url)
    data = response.json()
    return data


currency_list = list(get_wallex_currency_list()["result"]["symbols"].keys())

#print(currency_list)

def get_wallex_price(symbol):
    url = f"https://api.wallex.ir/v1/depth?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return data


for currency in currency_list:
    currency_value = get_wallex_price(currency)["result"]
    print(f"currency is {currency} and ask is {currency_value["ask"][0]} and bid is {currency_value["ask"][0]}")

        
