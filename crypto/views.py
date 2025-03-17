from django.shortcuts import render, redirect
from django.db import connection
from django.core.management import call_command
from django.contrib import messages
from .models import Prices

def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT currency_id , currencies, binance_last_trade_price , nobitex_last_trade_price , wallex_last_trade_price FROM prices ORDER BY currency_id")
        data = cursor.fetchall()
    binance_url = "https://www.binance.com/en/trade/"
    
    wallex_url = "https://wallex.ir/app/trade/"
    

    #Calculate difference between brokers
    processed_data = []
    
    for row in data:
        row = list(row)
        nobitex_price = row[3] if row[3] is not None else 0
        wallex_price = row[4] if row[4] is not None else 0

        # Add thresholds to the row
        if nobitex_price > wallex_price:
            difference = round(nobitex_price - wallex_price, 5)
        else:
            difference = round(wallex_price - nobitex_price, 5)
        row.append(difference) 

         # Check if Nobitex price is more than 1.03 times Wallex price or vice versa
        if (nobitex_price > wallex_price * 1.03) or (wallex_price > nobitex_price * 1.03):
            row.append(True)  # Append True if the condition is met
        else:
            row.append(False)  # Append False otherwise

        if "USDT" in row[1]:
                nobitex_url = f"https://nobitex.ir/panel/exchange/{row[1].replace('USDT', '-USDT')}"
        else:
                nobitex_url = "https://nobitex.ir/panel/exchange/"     
        row.append(nobitex_url)
        
        processed_data.append(row)

    return render(request, 'home.html', {'data': processed_data, 'binance_url': binance_url,  'wallex_url': wallex_url})

def update_brokers_data(request):
    if request.method == 'POST':
        try:
            call_command('update_binance_data')
            messages.success(request, 'binance data updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating binance data: {str(e)}')
        try:
            call_command('update_nobitex_data')
            messages.success(request, 'nobitex data updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating nobitex data: {str(e)}')
        try:
            call_command('update_wallex_data')
            messages.success(request, 'wallex data updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating wallex data: {str(e)}')
        return redirect('home')
    else:
        return redirect('home')

