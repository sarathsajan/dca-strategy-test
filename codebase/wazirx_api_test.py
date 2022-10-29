import ccxt

# provide an api_key and secret_key as keyword arguments
secret_key = '3tRO01dVziBT39NTxFK7p7Qt6Nsr7FdwzmAa9QwH'
API_key = 'aC5HuLlLeWOVi1fV3hjmmIVnXH0Py3UfXAmjb21TtcJMSdifmGbzSrP7jN4U7eli'

# connect wazirx
wazirx = ccxt.wazirx()
wazirx.apiKey = API_key
wazirx.secret = secret_key

amount = 3
price = 17.44

wazirx.create_order('WRX/INR', 'limit', 'sell', amount, price)