import requests
import decimal


URL = 'https://api.kucoin.com'

def get_currency_data(currency_code):
    ticker = requests.get(URL + '/api/v1/market/orderbook/level1?symbol='+ currency_code + '-USDT').json()
    return ticker


def get_current_currency_price(currency_code):
    payload = {'base': 'USD', 'currencies': currency_code}
    ticker = requests.get(URL + '/api/v1/prices', params=payload).json()
    current_price = ticker['data'][currency_code]
    return decimal.Decimal(current_price)


if __name__ == "__main__":
    print(get_current_currency_price('LOKI'))

