import requests
import datetime
import csv

# List of Coin pairs to check
symbol_list = ['ethinr', 'adainr', 'linkinr', 'uniinr', 'algoinr', 'nearinr', 'lunainr', 'manainr', 'xlminr', 'dotinr', 'btcinr']
# symbol_list = ['btcinr']

# REST API URL for WazirX Exchange
rest_api_url = 'https://api.wazirx.com/sapi/v1/tickers/24hr'

# Get the current price data from WazirX Exchange, and convert to JSON
current_market_status_raw = requests.get(rest_api_url)
current_market_status_json = current_market_status_raw.json()

# Get current UTC time in ISO 8601 format, add offset to match Indian Standard Time, and format the string to 'YmdHMS'
print(datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y%m%d%H%M%S"))

# Loop through each coin pair in the list and
# get the current price of coin pair if present then
# print the price along with symbol and timestamp
for pair in current_market_status_json:
  if pair['symbol'] in symbol_list:
    print(pair['symbol'], ' \t-', pair['lastPrice'])

# Updating the price data in the CSV file
for pair in current_market_status_json:
  if pair['symbol'] in symbol_list:
    # Opening the CSV file in read mode and reading
    # all the hourly data and storing it as list
    with open(f"{pair['symbol']}.csv", 'r', newline='', encoding='utf-8') as price_file:
      price_data_list = list(csv.reader(price_file))
    
    # Opening the CSV file in truncate mode and writing new data
    # Check if current price_data_list is longer than 720 items or not
    # If yes, then delete the first item from the list and append new data at end
    # If no, then append new data at the end
    # and write this new list in csv format to the file
    with open(f"{pair['symbol']}.csv", 'w', newline='', encoding='utf-8') as price_file:
      if len(price_data_list) > 719:
        price_data_list.pop(0)
        price_data_list.append([datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y%m%d%H%M%S"), pair['lastPrice']])
      else:
        price_data_list.append([datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y%m%d%H%M%S"), pair['lastPrice']])
      csv.writer(price_file).writerows(price_data_list)