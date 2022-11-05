import ccxt
import sys
from env_vars import env_vars

ENVIRONMENT_VARIABLES = env_vars.ENV_VARS()

# connect wazirx
wazirx = ccxt.wazirx()
wazirx.apiKey = ENVIRONMENT_VARIABLES['WAZIRX_API_KEY']
wazirx.secret = ENVIRONMENT_VARIABLES['WAZIRX_SECRET_KEY']

quantity = 3
print(quantity)
# sys.exit("dfgdsfgsfdg")
price = 20

buy_status = wazirx.create_order('WRX/INR', 'market', 'buy', quantity)
print(buy_status)

# print(type(wazirx.fetchBalance()['INR']['free']))