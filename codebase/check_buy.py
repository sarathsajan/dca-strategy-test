# run_order : 3

def buy():
    import csv
    import datetime
    import time
    import sys
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

    # Read the price data from the CSV file present
    # in the price_data directory.
    for symbol in symbol_list:
        print('\n', symbol)
        # Opening the CSV file in read mode and reading
        # all the hourly data and storing it as list
        with open(f"price_data/{symbol}.csv", 'r', newline='', encoding='utf-8') as price_file:
            price_data_list = list(csv.reader(price_file))
            # print(price_data_list, '\n')

        # open the current episode file of the symbol and make the initial buy
        # if there is no other BUY(file is empty) and the current price is at 7-day low.
        # else if there is an initial BUY already, then new BUYs should have price less than
        # the initial BUY present in the current episode file.
        with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'r', newline='', encoding='utf-8') as current_episode_file:
            current_episode_list = list(csv.reader(current_episode_file))
        
        # get the lowest value of the last 7 day rolling window(168 hours or 168 items) in the price_data_list
        # and compare it with the current price. If the current price is less than or equal to the lowest value
        # then buy the coin else, do nothing.
        if len(current_episode_list) == 0:
            current_price = float(price_data_list[-1][1])
            rolling_window_range = 167
            # list_of_price_data_in_rolling_window_range = price_data_list[-rolling_window_range:]
            list_of_price_in_rolling_window_range = []
            for price_data in price_data_list[-rolling_window_range:]:
                list_of_price_in_rolling_window_range.append(float(price_data[1]))
            lowest_price_in_rolling_window_range = min(list_of_price_in_rolling_window_range)
            highest_price_in_rolling_window_range = max(list_of_price_in_rolling_window_range)
            print('min - ', lowest_price_in_rolling_window_range)
            print('max - ', highest_price_in_rolling_window_range)
            print('now - ', current_price)

            if current_price <= lowest_price_in_rolling_window_range:
                amount_per_transaction = 60
                buy_details = []

                # WazirX API call for sufficient fund check
                # print(wazirx.fetchBalance()['INR']['free'])
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

                # WazirX API call for BUY
                wazirx.create_order(f'{symbol[:-3].upper()}/INR', 'limit', 'buy', amount_per_transaction/current_price, current_price)
                
                with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'a', newline='', encoding='utf-8') as episode_file:
                    buy_details.append(['BUY', datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y%m%d%H%M%S"), amount_per_transaction, current_price, amount_per_transaction/current_price])
                    # buy_details --> ['BUY', timestamp, amount spent, price bought at, no. of item bought]
                    csv.writer(episode_file).writerows(buy_details)
                print('Initial BUY')
        
        elif len(current_episode_list) > 0:
            current_price = float(price_data_list[-1][1])
            price_at_initial_buy = float(current_episode_list[0][3])

            if current_price <= price_at_initial_buy:
                amount_per_transaction = 60
                buy_details = []

                # WazirX API call for sufficient fund check
                # print(wazirx.fetchBalance()['INR']['free'])
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

                # WazirX API call for BUY
                wazirx.create_order(f'{symbol[:-3].upper()}/INR', 'limit', 'buy', amount_per_transaction/current_price, current_price)

                with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'a', newline='', encoding='utf-8') as episode_file:
                    # buy_details = [BUY, timestamp, amount spent, price bought at, no. of item bought]
                    buy_details.append(['BUY', datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y%m%d%H%M%S"), amount_per_transaction, current_price, amount_per_transaction/current_price])
                    csv.writer(episode_file).writerows(buy_details)
                print('Subsequent BUY')