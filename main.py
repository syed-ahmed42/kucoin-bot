import base64
import hashlib
import hmac
import json
import random

import requests
import decimal
import time

# TODO
# Keep datapoints and kline request data in memory if requesting same curr data as previoues

URL = 'https://api.kucoin.com'
KUCOIN_ORDERS = '/api/v1/orders'
KUCOIN_CANDLES = '/api/v1/market/candles'

API_KEY = "63066e7e650b2d00012fa331"
API_SECRET = "d2e0887c-456d-417f-ba5d-d1157ae140cd"
API_PASSPHRASE = "1234567"

WEEK_TIME_UNIX = 604800

def get_average_currency_price(currency_pair, time_period, start_time=0, end_time=0):
    #default interval goes back two years
    payload = {'symbol': currency_pair, 'startAt': start_time, 'endAt': end_time, 'type': time_period}
    ticker = requests.get(URL + KUCOIN_CANDLES, params=payload).json()
    closing_price_index = 2
    counter = 0
    avg_closing_price_sum = 0
    for array in ticker['data']:
        avg_closing_price_sum += float(array[closing_price_index])
        counter += 1
    return avg_closing_price_sum / counter

def make_limit_order(base_currency_symbol, quote_currency_symbol, quote_amount, side):
    order_id = random.getrandbits(128)
    payload = {'clientOid': order_id, 'side': side,
               'symbol': f'{base_currency_symbol}-{quote_currency_symbol}'
               , 'type': 'market', 'funds': f'{quote_amount}'}
    payload_json = json.dumps(payload)
    headers = create_header('POST', API_KEY, API_SECRET, API_PASSPHRASE, payload_json)
    result = requests.request('POST', URL + KUCOIN_ORDERS, data=payload_json, headers=headers)
    print(result.json())
def get_current_currency_price(currency_code):
    payload = {'base': 'USD', 'currencies': currency_code}
    ticker = requests.get(URL + '/api/v1/prices', params=payload).json()
    current_price = ticker['data'][currency_code]
    return float(current_price)
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

def make_historical_data_points(currency_pair, time_period, start_time=0, end_time=0):
    payload = {'symbol': currency_pair, 'startAt': start_time, 'endAt': end_time, 'type': time_period}
    ticker = requests.get(URL + KUCOIN_CANDLES, params=payload).json()
    balance = {'time': [], 'closing_price': []}
    for array in reversed(ticker['data']):
        balance['time'].append(array[0])
        balance['closing_price'].append(array[2])
    return balance

def backtest_curr_past_3_months(currency_pair, starting_balance, buy_margin, sell_margin):
    past_3_month_daily_closing_prices = make_historical_data_points(currency_pair, '1day')
    balance = starting_balance
    starting_time = int(past_3_month_daily_closing_prices['time'][0])
    end_time = int(starting_time) + (WEEK_TIME_UNIX * 12)
    backtest_moving_average = get_average_currency_price(currency_pair, '1week', starting_time, end_time)
    stock_of_currency = 0
    for price in past_3_month_daily_closing_prices['closing_price']:
        #Buy when price falls from base index of 1 by buy margin %
        if float(price) / backtest_moving_average <= 1 - buy_margin:
            if balance > 0:
                stock_of_currency = float(balance) / float(price)
                balance -= float(price) * stock_of_currency
        #Sell when price rises from base index of 1 by sell margin %
        elif float(price) / backtest_moving_average >= 1 + sell_margin:
            if stock_of_currency > 0:
                balance += float(price) * stock_of_currency
                stock_of_currency = 0
    if balance != 0:
        print(f'Final Balance after 3 months: {balance} (In ' + str(currency_pair[currency_pair.find('-') + 1:]) + ')')
    else:
        print('Valuation of stock in account waiting to sell: '
              + str(stock_of_currency * float(price)) + ' (In ' +
              str(currency_pair[currency_pair.find('-') + 1:]) + ')')
        print(f'Final balance after 3 months: {balance} (In ' + str(currency_pair[currency_pair.find('-') + 1:]) + ')')

if __name__ == "__main__":
    backtest_curr_past_3_months('ETH-BTC', 1, 0.02, 0.02)
    #while True:
     #   current_price = get_current_currency_price('BTC')
        #if current_price / moving_average_50 <= 0.85:
        #    print('BUY STOCK')
        #elif current_price / moving_average_50 >= 1.15:
        #    print('SELL STOCK')
