import requests
import json
from config import keys


class APIException(Exception):
    """Класс собственных исключений для обработки ошибок пользователя"""
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f"Невозможно перевести одинаковые валюты: {base}")

        try:
            base_ticker = keys[base.lower()]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту: {base}")

        try:
            quote_ticker = keys[quote.lower()]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту: {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество: {amount}")

        # используем бесплатное API exchangerate.host
        url = f"https://api.exchangerate.host/convert?from={base_ticker}&to={quote_ticker}&amount={amount}"
        r = requests.get(url)
        data = json.loads(r.content)

        if "result" not in data or data["result"] is None:
            raise APIException("Ошибка при получении данных от API")

        return data["result"]
