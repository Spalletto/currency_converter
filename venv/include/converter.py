# TODO: 1. Implement get requests to the API server.
# TODO: 2. Create database.
# TODO: 3. Create table in database: CURRENCY, COST
# TODO: 4. Insert data into database
# TODO: 5. Make an CLI implementation: list all currencies, preferred currency, convert UAN to SMTH, convert SMTH to UAN
# TODO: 6. PyQT
# TODO: 7. TKinter
# TODO: 8. Kivy
# TODO: 9. Telegram Bot

import json
from requests import get
from pprint import pprint


def get_data():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    response = get(url)
    data = json.loads(response.content)

    return data


def main():
    get_data()


if __name__ == "__main__":
    main()
