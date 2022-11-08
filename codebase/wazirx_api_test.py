# run_order : 2.5

def test_api():
    import sys
    import ccxt
    import time
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

    while True:
        try:
            print(wazirx.fetchBalance()['INR']['free'])
            time.sleep(5)
            if wazirx.fetchBalance()['INR']['free'] < 70:
                print('Insufficient fund.')
                sys.exit()
            break
        except SystemExit:
            print('inside SystemExit except block')
            sys.exit()
        except:
            print('fetchBalance API endpoint failed, retrying again')