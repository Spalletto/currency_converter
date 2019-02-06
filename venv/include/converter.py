# TODO: 1. Implement get requests to the API server.
# TODO: 2. Create database.
# TODO: 3. Create table in database: CURRENCY, COST
# TODO: 4. Insert data into database
# TODO: 5. Make an CLI implementation: list all currencies, preferred currency, convert UAN to SMTH, convert SMTH to UAN
# TODO: 6. Implement difflib to parse errors
# TODO: 7. PyQT
# TODO: 8. TKinter
# TODO: 9. Kivy
# TODO: 10. Telegram Bot

import json
from requests import get
from pprint import pprint
import sqlite3


def get_currencies():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    response = get(url)
    data = json.loads(response.content)

    return data


def create_database(name, all_currencies):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS Currencies(code text, name text, price real)""")

    for currency in all_currencies:
        cursor.execute("""INSERT INTO Currencies values(?,?,?)""",
                       (currency['cc'], currency['txt'], currency['rate']))
        conn.commit()


def main():
    all_currencies = get_currencies()
    create_database('currencies.db', all_currencies)


if __name__ == "__main__":
    main()
