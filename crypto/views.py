from django.shortcuts import render, redirect
from django.db import connection
from django.core.management import call_command
from django.contrib import messages


def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT currency_id , currencies, binance_last_trade_price , nobitex_last_trade_price , wallex_last_trade_price FROM prices")
        data = cursor.fetchall()
    binance_url = "https://www.binance.com/en/trade/"
    nobitex_url = "https://nobitex.ir/panel/exchange/"
    wallex_url = "https://wallex.ir/app/trade/"
    return render(request, 'home.html', {'data': data, 'binance_url': binance_url, 'nobitex_url': nobitex_url, 'wallex_url': wallex_url})

def update_nobitex_data(request):
    if request.method == 'POST':
        try:
            call_command('update_nobitex_data')
            messages.success(request, 'Nobitex data updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating Nobitex data: {str(e)}')
        return redirect('home')
    else:
        return redirect('home')