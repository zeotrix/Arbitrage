import requests
import psycopg2
from psycopg2 import sql

# Database connection parameters
db_params = {
    "dbname": "crypto_prices",
    "user": "postgres",  # Replace with your PostgreSQL username
    "password": "145294",  # Replace with your PostgreSQL password
    "host": "localhost",
    "port": 5432
}

def get_nobitex_currency_list():
    url = "https://api.nobitex.ir/v3/orderbook/all"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()
        currency_list = list(data.keys())
        currency_list.remove('status')
        return currency_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Nobitex currency list: {e}")
        return []

def get_wallex_currency_list():
    url = "https://api.wallex.ir/v1/markets"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()
        currency_list = list(data["result"]["symbols"].keys())
        return currency_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Wallex currency list: {e}")
        return []

def fetch_and_compare_currencies():
    # Fetch currency lists from both exchanges
    nobitex_currencies = get_nobitex_currency_list()
    wallex_currencies = get_wallex_currency_list()

    # Convert to sets for easy comparison
    nobitex_set = set(nobitex_currencies)
    wallex_set = set(wallex_currencies)

    # Find common currencies
    common_currencies = nobitex_set.intersection(wallex_set)
    print("Common Currencies:", common_currencies)

    # Find currencies only in Nobitex
    only_nobitex = nobitex_set - wallex_set
    print("Currencies only in Nobitex:", only_nobitex)

    # Find currencies only in Wallex
    only_wallex = wallex_set - nobitex_set
    print("Currencies only in Wallex:", only_wallex)

    # Insert data into the database
    with psycopg2.connect(**db_params) as conn:
        with conn.cursor() as cursor:
            # Insert common currencies
            for currency in common_currencies:
                insert_into_database(cursor, currency, currency, currency)

            # Insert currencies only in Nobitex
            for currency in only_nobitex:
                insert_into_database(cursor, currency, None, None)

            # Insert currencies only in Wallex
            for currency in only_wallex:
                insert_into_database(cursor, None, currency, None)

def insert_into_database(cursor, nobitex_currency, wallex_currency, common_currency):
    try:
        # Insert data into the table
        insert_query = sql.SQL("""
            INSERT INTO prices (nobitex_currencies, wallex_currencies, common_currencies)
            VALUES (%s, %s, %s)
        """)
        cursor.execute(insert_query, (nobitex_currency, wallex_currency, common_currency))
        print(f"Inserted {nobitex_currency}, {wallex_currency}, {common_currency} into the database.")
    except Exception as e:
        print(f"Error inserting {nobitex_currency}, {wallex_currency}, {common_currency}: {e}")

if __name__ == "__main__":
    fetch_and_compare_currencies()