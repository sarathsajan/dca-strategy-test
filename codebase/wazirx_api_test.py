import ccxt

# provide an api_key and secret_key as keyword arguments
secret_key = 'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
API_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxx'

# connect wazirx
wazirx = ccxt.wazirx()
wazirx.apiKey = API_key
wazirx.secret = secret_key

amount = 3
price = 17.44

wazirx.create_order('WRX/INR', 'limit', 'sell', amount, price)