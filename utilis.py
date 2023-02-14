import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class Convert:
    @staticmethod
    def get_price(quote: str, base: str, amount: float):

        if quote == base:
            raise ConvertionException(f'Невозможно перевеси {base} в {quote}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту!')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException('Не удалось обработать валюту!')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException('Введите число')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/3540f6c9e4e2a7f46eb4beb9/pair/{quote_ticker}/{base_ticker}')
        data = json.loads(r.content)
        total_base = data['conversion_rate'] * float(amount)
        finish_base = round(total_base, 2)
        return finish_base