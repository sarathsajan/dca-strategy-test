import csv
import ccxt
import time
import requests
from env_vars import env_vars

ENVIRONMENT_VARIABLES = env_vars.ENV_VARS()

# connect wazirx
wazirx = ccxt.wazirx()
wazirx.apiKey = ENVIRONMENT_VARIABLES['WAZIRX_API_KEY']
wazirx.secret = ENVIRONMENT_VARIABLES['WAZIRX_SECRET_KEY']

symbol = 'btcinr'

while True:
    try:
        symbol = symbol[-3:].upper()
        print(wazirx.fetchBalance()[symbol]['free'])
        print(type(wazirx.fetchBalance()[symbol]['free']))
        time.sleep(5)
        if wazirx.fetchBalance()[symbol]['free'] < 70:
            print('Insufficient fund.')
            # sys.exit()
        break
    except SystemExit:
        print('inside SystemExit except block')
        break
        # sys.exit()
    except:
        print('fetchBalance API endpoint failed, retrying again')

# ----------------------------------------------------------------------------------------------------------------------

openOrders = wazirx.fetch_open_orders()
print('open orders - ', openOrders)

# ----------------------------------------------------------------------------------------------------------------------

buy_status_flag = requests.get('https://raw.githubusercontent.com/sarathsajan/dca-strategy-test/main/codebase/flag_data.txt')
print ('buy_status_flag - ', buy_status_flag.text)
print (type(buy_status_flag.text))

# ----------------------------------------------------------------------------------------------------------------------

symbol_list = ['btcinr', 'ethinr']

for symbol in symbol_list:
    print('\n', symbol)
    # Opening the CSV file in read mode and reading
    # all the hourly data and storing it as list
    with open(f"price_data/{symbol}.csv", 'r', newline='', encoding='utf-8') as price_file:
        price_data_list = list(csv.reader(price_file))

    with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'r', newline='', encoding='utf-8') as current_episode_file:
        current_episode_list = list(csv.reader(current_episode_file))

    # get the lowest value of the last 3 day rolling window(72 hours or 72 items) in the price_data_list
    # and compare it with the current price. If the current price is less than or equal to the lowest value
    # then buy the coin else, do nothing.
    if len(current_episode_list) != 0:
        current_price = float(price_data_list[-1][1])
        sma_3_rolling_window_range = 24*3
        sma_12_rolling_window_range = 24*12

        list_of_price_in_sma_3_rolling_window_range = []
        list_of_price_in_sma_12_rolling_window_range = []
        for price_data in price_data_list[-sma_3_rolling_window_range:]:
            list_of_price_in_sma_3_rolling_window_range.append(float(price_data[1]))
        for price_data in price_data_list[-sma_12_rolling_window_range:]:
            list_of_price_in_sma_12_rolling_window_range.append(float(price_data[1]))
        print('list_of_price_in_sma_3_rolling_window_range - ', list_of_price_in_sma_3_rolling_window_range)
        print('list_of_price_in_sma_12_rolling_window_range - ', list_of_price_in_sma_12_rolling_window_range)
        sma_3_day = sum(list_of_price_in_sma_3_rolling_window_range)/(3*24)
        sma_12_day = sum(list_of_price_in_sma_12_rolling_window_range)/(12*24)
        print('SMA3  - ', sma_3_day)
        print('SMA12 - ', sma_12_day)
        print('Live - ', current_price)

        if sma_3_day < sma_12_day:
            print("Time to Buy")
        else:
            print("Time to Wait")