import ccxt
from env_vars import env_vars

ENVIRONMENT_VARIABLES = env_vars.ENV_VARS()

# connect wazirx
wazirx = ccxt.wazirx()
wazirx.apiKey = ENVIRONMENT_VARIABLES['WAZIRX_API_KEY']
wazirx.secret = ENVIRONMENT_VARIABLES['WAZIRX_SECRET_KEY']

quantity = 0.9
price = 60

# wazirx.create_order('WRX/INR', 'limit', 'sell', quantity, price)
print(wazirx.fetchBalance()['INR'])