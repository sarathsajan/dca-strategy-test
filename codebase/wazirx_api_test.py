import ccxt
from env_vars import ENV_VARS

ENVIRONMENT_VARIABLES = ENV_VARS()

# connect wazirx
wazirx = ccxt.wazirx()
wazirx.apiKey = ENVIRONMENT_VARIABLES.WAZIRX_API_KEY
wazirx.secret = ENVIRONMENT_VARIABLES.WAZIRX_SECRET_KEY

amount = 3
price = 30

wazirx.create_order('BTC/INR', 'limit', 'buy', amount, price)