import json
import requests
from confing import exchanges, TOKEN



class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')


        r = requests.get(f"http://api.exchangeratesapi.io/latest?access_key=e738e59424c5f8b9df7e7f39d93b7d97&base={base_key}&symbols={quote_key}")
        resp = json.loads(r.content)
        print(r.content)
        print(resp)
        new_price = resp['rates'][quote_key] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {quote_key} : {new_price}"
        return message
