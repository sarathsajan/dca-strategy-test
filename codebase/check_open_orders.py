# run_order : 3

def open_orders():
    import csv
    import time
    import ccxt

    from env_vars import env_vars
    ENVIRONMENT_VARIABLES = env_vars.ENV_VARS()

    # connect wazirx
    wazirx = ccxt.wazirx()
    wazirx.apiKey = ENVIRONMENT_VARIABLES['WAZIRX_API_KEY']
    wazirx.secret = ENVIRONMENT_VARIABLES['WAZIRX_SECRET_KEY']

    # Get list of coin pairs to check
    # symbol_list = ['ethinr', 'adainr', 'linkinr', 'uniinr', 'algoinr', 'nearinr', 'manainr', 'xlminr', 'dotinr', 'btcinr']
    # symbol_list = ['btcinr', 'ethinr']
    with open("symbol_list.csv", 'r', newline='', encoding='utf-8') as symbol_list_file:
        symbol_list = (list(csv.reader(symbol_list_file)))[0]

    # get status of pending open orders in the exchange
    # if pending open entries are found, then cancel them
    # and remove the latest BUY entry from the current episode file
    # WILL NEED TO USE THE try-retry method from check_buy.py, if this fails 
    while True:
        try:
            time.sleep(5)
            pending_open_orders = wazirx.fetchOpenOrders()
            break
        except:
            print('fetchOpenOrders API endpoint failed, retrying again.')

    for symbol in symbol_list:
        for pending_open_order in pending_open_orders:
            if symbol == pending_open_order['info']['symbol'] and 'buy' == pending_open_order['info']['side']:
                print('pending symbol   - ', pending_open_order['info']['symbol'])
                print('pending order id - ', pending_open_order['info']['id'])
                while True:
                        try:
                            time.sleep(5)
                            wazirx.cancelOrder(pending_open_order['info']['id'],pending_open_order['info']['symbol'])
                            print('pending open orders cancelled.')
                            
                            # getting all the BUY orders present in the current episode file of the symbol into a list format.
                            with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'r', newline='', encoding='utf-8') as current_episode_file:
                                buy_orders_list = list(csv.reader(current_episode_file))

                            # deleting the lastest entry of BUY order in the current episode list
                            # since the BUY order was not fulfilled and has now been cancelled.
                            # for that open the current episode file in truncate mode and re-insert
                            # data after popping out (deleting) the latest entry
                            with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'w', newline='', encoding='utf-8') as current_episode_file:
                                buy_orders_list = buy_orders_list.pop()
                                csv.writer(current_episode_file).writerows(buy_orders_list)
                            break
                        except ccxt.OrderNotFound:
                            print('Exception raised - OrderNotFound.')
                            print('order already cancelled or executed before the cancelling.')
                            break
                        except:
                            print('cancelOrder API endpoint failed, retrying again.')
