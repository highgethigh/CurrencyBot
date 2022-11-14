import requests
import json
from config import currency, payload, headers

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести 2 одинаковые валюты "{base}".\n\n'
                               f'Попробуйте, ввести две разные валюты из списка доступных валют! /values')

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}".\n\n'
                               f'Укажите валюту из списка доступных валют! /values')

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}".\n\n'
                               f'Укажите валюту из списка доступных валют! /values')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f"https://api.apilayer.com/exchangerates_data/convert?to={quote_ticker}&from={base_ticker}&amount={amount}",headers=headers, data=payload)
        total_base = json.loads(r.content)
        price = total_base['result']
        return price

