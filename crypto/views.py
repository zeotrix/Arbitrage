from django.shortcuts import render
from django.db import connection

def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT nobitex_currencies, wallex_currencies, common_currencies FROM prices")
        data = cursor.fetchall()
    return render(request, 'home.html', {'data': data})