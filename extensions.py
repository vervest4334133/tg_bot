import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise APIException(f'Введите разные валюты! Невозможно перевести одинаковые валюты {quote}!')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество валюты {amount}!')

        if amount <= 0:
            raise APIException(f'Не удалось обработать количество валюты {amount}!')

        r = requests.get(
            f'https://v6.exchangerate-api.com/v6/код_api/pair/{quote_ticker}/{base_ticker}/{amount}')
        data = json.loads(r.content)['conversion_result']

        return data
