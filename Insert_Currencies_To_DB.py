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
    response = requests.get(url)
    data = response.json()
    currency_list = list(data.keys())
    currency_list.remove('status')
    return currency_list

def get_wallex_currency_list():
    url = "https://api.wallex.ir/v1/markets"
    response = requests.get(url)
    data = response.json()
    currency_list = list(data["result"]["symbols"].keys())
    return currency_list

def fetch_and_compare_currencies():
    # Fetch currency lists from both exchanges
    nobitex_currencies = get_nobitex_currency_list()
    wallex_currencies = get_wallex_currency_list()
    
    #for x in wallex_currencies:
    #    if "TMN" in x : 
    #        wallex_currencies.remove(x)  
    #        x = x.replace("TMN", "IRT")
    #        wallex_currencies.append(x)

    # Convert to sets for easy comparison
    nobitex_set = set(nobitex_currencies)
    wallex_set = set(wallex_currencies)

    # Find common currencies
    common_currencies = nobitex_set.intersection(wallex_set)
    #print("Common Currencies:", common_currencies)
    print("common currencies are set")

    # Find currencies only in Nobitex
    only_nobitex = nobitex_set - wallex_set
    only_nobitex = only_nobitex - common_currencies
    #print("Currencies only in Nobitex:", only_nobitex)

    # Find currencies only in Wallex
    only_wallex = wallex_set - nobitex_set
    only_wallex = only_wallex - common_currencies
    #print("Currencies only in Wallex:", only_wallex)


    for currency in common_currencies:
        insert_into_database( currency,currency,currency)
    for currency in only_nobitex:
        insert_into_database(currency,"nothing","nothing")
    for currency in only_wallex:
        insert_into_database("nothing",currency,"nothing")


def insert_into_database(nobitex_currencies, wallex_currencies , common_currencies):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Insert data into the table
        insert_query = sql.SQL("""
            INSERT INTO prices (nobitex_currencies, wallex_currencies , common_currencies)
            VALUES (%s, %s, %s)
        """)
        cursor.execute(insert_query, (nobitex_currencies, wallex_currencies , common_currencies))  # Note the comma after currency_pair
        conn.commit()
        print(f"Inserted {nobitex_currencies} , {wallex_currencies} , {common_currencies} into the database.")

    except Exception as e:
        print(f"Error inserting {nobitex_currencies} , {wallex_currencies} , {common_currencies}: {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    fetch_and_compare_currencies()