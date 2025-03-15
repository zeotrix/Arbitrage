from django.shortcuts import render
from django.db import connection

def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT nobitex_currencies, wallex_currencies, common_currencies FROM prices")
        data = cursor.fetchall()
    base_url = "https://www.binance.com/en/trade/"
    nobitex_url = "https://nobitex.ir/panel/exchange/"
    wallex_url = "https://wallex.ir/app/trade/"
    return render(request, 'home.html', {'data': data, 'base_url': base_url, 'nobitex_url': nobitex_url, 'wallex_url': wallex_url})