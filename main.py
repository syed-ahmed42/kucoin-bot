import requests
import decimal
import time



URL = 'https://api.kucoin.com'

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

def get_currency_history(currency_code):
    ticker = requests.get(URL + '/api/v1/market/histories?symbol=' + currency_code + '-USDT').json()
    return ticker

def get_current_currency_price(currency_code):
    payload = {'base': 'USD', 'currencies': currency_code}
    ticker = requests.get(URL + '/api/v1/prices', params=payload).json()
    current_price = ticker['data'][currency_code]
    return decimal.Decimal(current_price)


if __name__ == "__main__":
    print(get_currency_moving_average('BTC', 4))
    # while True:
    #     last_recorded_stock_price = get_current_currency_price('LOKI')
    #     time.sleep(60)
    #     if get_current_currency_price('LOKI') > last_recorded_stock_price * decimal.Decimal(1):
    #         print('Selling the stock right now')
    #     elif get_current_currency_price('LOKI') < last_recorded_stock_price * decimal.Decimal(1):
    #         print('Buying the stock right now')
    #     else:
    #         print('Doing nothing')
