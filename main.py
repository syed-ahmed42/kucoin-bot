import base64
import hashlib
import hmac
import json
import random

import requests
import decimal
import time



URL = 'https://api.kucoin.com'
KUCOIN_ORDERS = '/api/v1/orders'

API_KEY = "63066e7e650b2d00012fa331"
API_SECRET = "d2e0887c-456d-417f-ba5d-d1157ae140cd"
API_PASSPHRASE = "1234567"


def get_currency_moving_average(currency_code, number_of_months):
    av_monthly_data_url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol={currency_code}&market=USD&apikey=8AF6LT7I8TKBJ173'
    my_sum = 0
    counter = 0
    ticker = requests.get(av_monthly_data_url).json()
    for data in ticker:
        for month in ticker[data]:
            for data_stored_in_month in ticker[data][month]:
                if counter < number_of_months and data_stored_in_month == '4a. close (USD)':
                    my_sum += float(ticker[data][month][data_stored_in_month])
                    counter += 1
                if counter >= number_of_months:
                    return my_sum/number_of_months

    return 0

def make_limit_order(base_currency_symbol, quote_currency_symbol, quote_amount):
    order_id = random.getrandbits(128)
    payload = {'clientOid': order_id, 'side': 'buy',
               'symbol': f'{base_currency_symbol}-{quote_currency_symbol}'
               , 'type': 'market', 'funds': f'{quote_amount}'}
    payload_json = json.dumps(payload)
    headers = create_header('POST', API_KEY, API_SECRET, API_PASSPHRASE, payload_json)
    result = requests.request('POST', URL + KUCOIN_ORDERS, data=payload_json, headers=headers)
    print(result.json())
def get_currency_history(currency_code):
    ticker = requests.get(URL + '/api/v1/market/histories?symbol=' + currency_code + '-USDT').json()
    return ticker

def get_current_currency_price(currency_code):
    payload = {'base': 'USD', 'currencies': currency_code}
    ticker = requests.get(URL + '/api/v1/prices', params=payload).json()
    current_price = ticker['data'][currency_code]
    return decimal.Decimal(current_price)
def create_header(method, api_key, api_secret, api_passphrase, data):
    time_now = int(time.time() * 1000)
    api_key = api_key
    api_secret = api_secret
    api_passphrase = api_passphrase
    str_to_sign = str(time_now) + method + KUCOIN_ORDERS + data
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(time_now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": '2',
        "Content-Type": "application/json"  # specifying content type or using json=data in request
    }
    return headers

if __name__ == "__main__":
    #print(get_currency_moving_average('BTC', 4))
    #print(get_currency_moving_average('BTC', 2))

    make_limit_order('BTC', 'USDT', 2)
    #test_func()
