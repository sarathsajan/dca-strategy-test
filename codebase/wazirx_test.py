import ccxt
import time
import requests
from env_vars import env_vars

ENVIRONMENT_VARIABLES = env_vars.ENV_VARS()

# connect wazirx
wazirx = ccxt.wazirx()
wazirx.apiKey = ENVIRONMENT_VARIABLES['WAZIRX_API_KEY']
wazirx.secret = ENVIRONMENT_VARIABLES['WAZIRX_SECRET_KEY']

quantity = 3
# sys.exit("dfgdsfgsfdg")
price = 20

# buy_status = wazirx.create_order('WRX/INR', 'market', 'buy', quantity)
# print(buy_status)
symbol = 'btcinr'


while True:
    try:
        print(wazirx.fetchBalance()[symbol[:-3].upper()]['free'])
        print(type(wazirx.fetchBalance()[symbol[:-3].upper()]['free']))
        time.sleep(5)
        if wazirx.fetchBalance()[symbol[:-3].upper()]['free'] < 70:
            print('Insufficient fund.')
            # sys.exit()
        break
    except SystemExit:
        print('inside SystemExit except block')
        break
        # sys.exit()
    except:
        print('fetchBalance API endpoint failed, retrying again')

openOrders = wazirx.fetch_open_orders()
print(openOrders)


buy_status_flag = requests.get('https://raw.githubusercontent.com/sarathsajan/dca-strategy-test/main/codebase/buy_status_flag.txt')
print (buy_status_flag.text)
print (type(buy_status_flag.text))