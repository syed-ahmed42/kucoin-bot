import base64
import hashlib
import hmac
import json

import requests
import decimal
import time



URL = 'https://api.kucoin.com'
KUCOIN_ORDERS = '/api/v1/orders'




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

def make_limit_order(currency_code):
    print('made order')

    payload = {'clientOid': '343AS2ew_', 'side': 'buy', 'symbol': 'BTC-USDT', 'type': 'market', 'funds': '5'}
    payload_json = json.dumps(payload)
    headers = create_header(payload_json)
    result = requests.request('post', URL + KUCOIN_ORDERS, data=payload_json, headers=headers)
    print(result.json())
def get_currency_history(currency_code):
    ticker = requests.get(URL + '/api/v1/market/histories?symbol=' + currency_code + '-USDT').json()
    return ticker

def get_current_currency_price(currency_code):
    payload = {'base': 'USD', 'currencies': currency_code}
    ticker = requests.get(URL + '/api/v1/prices', params=payload).json()
    current_price = ticker['data'][currency_code]
    return decimal.Decimal(current_price)
def create_header(data):
    time_now = int(time.time() * 1000)
    api_key = "63066e7e650b2d00012fa331"
    api_secret = "d2e0887c-456d-417f-ba5d-d1157ae140cd"
    api_passphrase = "1234567"
    str_to_sign = str(time_now) + 'POST' + KUCOIN_ORDERS + data
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
def test_func():
    api_key = "63066e7e650b2d00012fa331"
    api_secret = "d2e0887c-456d-417f-ba5d-d1157ae140cd"
    api_passphrase = "1234567"
    url = URL + '/api/v1/accounts'
    now = int(time.time() * 1000)
    str_to_sign = str(now) + 'GET' + '/api/v1/accounts'
    signature = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest())
    passphrase = base64.b64encode(
        hmac.new(api_secret.encode('utf-8'), api_passphrase.encode('utf-8'), hashlib.sha256).digest())
    headers = {
        "KC-API-SIGN": signature,
        "KC-API-TIMESTAMP": str(now),
        "KC-API-KEY": api_key,
        "KC-API-PASSPHRASE": passphrase,
        "KC-API-KEY-VERSION": "2"
    }
    response = requests.request('get', url, headers=headers)
    print(response.status_code)
    print(response.json())
if __name__ == "__main__":
    #print(get_currency_moving_average('BTC', 4))
    #print(get_currency_moving_average('BTC', 2))

    make_limit_order('BTC')
    #test_func()
