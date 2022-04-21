import requests
import datetime


# List of Coin pairs to check
symbol_list = ['ethinr', 'adainr', 'linkinr', 'uniinr', 'algoinr', 'nearinr', 'lunainr', 'manainr', 'xlminr', 'dotinr', 'btcinr']

# REST API URL for WazirX Exchange
rest_api_url = 'https://api.wazirx.com/sapi/v1/tickers/24hr'

# Get the current price data from WazirX Exchange, and convert to JSON
current_market_status_raw = requests.get(rest_api_url)
current_market_status_json = current_market_status_raw.json()

# Get current UTC time in ISO 8601 format, add offset to match Indian Standard Time, and format the string to 'Y_m_d_H_M_S'
print(datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y_%m_%d_%H_%M_%S"))

# Loop through each coin pair in the list and
# get the current price of coin pair if present then
# save the price along with symbol and timestamp to a CSV file
for pair in current_market_status_json:
  if pair['symbol'] in symbol_list:
    print(pair['symbol'], ' \t-', pair['lastPrice'])