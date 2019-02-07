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
import click
from requests import get
from pprint import pprint
import sqlite3
from datetime import datetime


def get_currencies():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    response = get(url)
    data = json.loads(response.content)

    return data


def create_database(name, all_currencies):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    cursor.execute("""DROP TABLE IF EXISTS Currencies;""")
    cursor.execute("""CREATE TABLE Currencies(code text, name text, price real)""")
    cursor.execute("""INSERT INTO Currencies values(?,?,?)""", ('UAN', 'Українська гривня', 1))

    for currency in all_currencies:
        cursor.execute("""INSERT INTO Currencies values(?,?,?)""",
                       (currency['cc'], currency['txt'], currency['rate']))
        conn.commit()

    conn.close()


def print_all(data):
    now = datetime.now()
    click.secho("Курс валют станом на {time}:\n".format(time=now.strftime('%d.%m.%Y %H:%M')), fg='blue', bold=True)
    for row in data:
        click.secho('{}\t{:40}\t{}'.format(*row), fg='cyan', bold=True)


@click.group()
@click.pass_context
def main(ctx):
    all_currencies = get_currencies()
    create_database('currencies.db', all_currencies)

    ctx.obj = {
        'database_name': 'currencies.db'
    }


@main.command()
@click.pass_context
def show_all(ctx):
    conn = sqlite3.connect(ctx.obj.get('database_name'))
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Currencies""")
    print_all(cursor.fetchall())
    conn.close()


@main.command()
@click.option('--name', prompt='Код валюти')
@click.pass_context
def show_preffered(ctx, name):
    conn = sqlite3.connect(ctx.obj.get('database_name'))
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM Currencies WHERE code=?""", (name,))
    print_all(cursor.fetchall())
    conn.close()

@main.command()
@click.option('--first', prompt='Код валюти, яку ви маєте', default='UAN')
@click.option('--amount', prompt='Кількість цієї валюти')
@click.option('--second', prompt='Код валюти, яку бажаєте отримати')
@click.pass_context
def converter(ctx, first, amount, second):
    conn = sqlite3.connect(ctx.obj.get('database_name'))
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM Currencies WHERE code=?""", (first,))
    first_currency = cursor.fetchone()

    cursor.execute("""SELECT * FROM Currencies WHERE code=?""", (second,))
    second_currency = cursor.fetchone()

    result = first_currency[2] * int(amount) / second_currency[2]
    click.secho(f"{amount} {first_currency[0]} = {str(result)} {second_currency[0]}", fg='cyan')


if __name__ == "__main__":
    main()
