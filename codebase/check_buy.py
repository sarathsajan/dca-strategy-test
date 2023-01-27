# run_order : 4

def buy_status():
    import requests
    flag_data = requests.get('https://raw.githubusercontent.com/sarathsajan/dca-strategy-test/main/codebase/flag_data.txt')
    buy_status_flag = flag_data.text
    if buy_status_flag == 'Y':
        print('Y')
        buy()
    else:
        print(buy_status_flag)

def buy():
    import statistics
    import csv
    import datetime
    import time
    import ccxt

    from env_vars import env_vars
    ENVIRONMENT_VARIABLES = env_vars.ENV_VARS()

    # connect wazirx
    wazirx = ccxt.wazirx()
    wazirx.apiKey = ENVIRONMENT_VARIABLES['WAZIRX_API_KEY']
    wazirx.secret = ENVIRONMENT_VARIABLES['WAZIRX_SECRET_KEY']
    
    # INR amount going to be used for each BUY order
    amount_per_transaction = 60

    # Get list of coin pairs to check
    # symbol_list = ['ethinr', 'adainr', 'linkinr', 'uniinr', 'algoinr', 'nearinr', 'manainr', 'xlminr', 'dotinr', 'btcinr']
    # symbol_list = ['btcinr', 'ethinr']
    with open("symbol_list.csv", 'r', newline='', encoding='utf-8') as symbol_list_file:
        symbol_list = (list(csv.reader(symbol_list_file)))[0]

    # WazirX API call for sufficient fund check
    # print(wazirx.fetchBalance()['INR']['free'])
    while True:
        try:
            print(wazirx.fetchBalance()['INR']['free'])
            time.sleep(5)
            if wazirx.fetchBalance()['INR']['free'] < amount_per_transaction + 10:
                print('Insufficient fund.')
                return
            print('Sufficient fund for transaction.')
            break
        except:
            print('fetchBalance API endpoint failed, retrying again')

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
        # if there is no other BUY(file is empty) and the 3-Day SMA is below 12-Day SMA.
        # else if there is an initial BUY already, then new BUYs should have price less than
        # the previous BUY present in the current episode file.
        with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'r', newline='', encoding='utf-8') as current_episode_file:
            current_episode_list = list(csv.reader(current_episode_file))
        
        # get the lowest value of the last 3 day rolling window(72 hours or 72 items) in the price_data_list
        # and compare it with the current price. If the current price is less than or equal to the lowest value
        # then buy the coin else, do nothing.
        if len(current_episode_list) == 0:
            current_price = float(price_data_list[-1][1])
            rolling_window_range = 300
            # list_of_price_data_in_rolling_window_range = price_data_list[-rolling_window_range:]
            list_of_price_in_rolling_window_range = []
            for price_data in price_data_list[-rolling_window_range:]:
                list_of_price_in_rolling_window_range.append(float(price_data[1]))
            sma_3_day = sum(list_of_price_in_rolling_window_range[3*24])/(3*24)
            sma_12_day = sum(list_of_price_in_rolling_window_range[12*24])/(12*24)
            print('SMA3  - ', sma_3_day)
            print('SMA12 - ', sma_12_day)
            print('Live - ', current_price)

            if sma_3_day < sma_12_day:
                buy_details = []

                # WazirX API call for BUY
                try:
                    wazirx.create_order(f'{symbol[:-3].upper()}/INR', 'limit', 'buy', amount_per_transaction/current_price, current_price)
                
                    with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'a', newline='', encoding='utf-8') as episode_file:
                        buy_details.append(['BUY', datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y%m%d%H%M%S"), amount_per_transaction, current_price, amount_per_transaction/current_price])
                        # buy_details --> ['BUY', timestamp, amount spent, price bought at, no. of item bought]
                        csv.writer(episode_file).writerows(buy_details)
                    print('Initial BUY')
                except Exception as error:
                    print(error)
                    print('skipping symbol - ', symbol)
                    continue
        
        elif len(current_episode_list) > 0:
            current_price = float(price_data_list[-1][1])
            price_at_latest_buy = float(current_episode_list[len(current_episode_list)-1][3])

            if current_price <= price_at_latest_buy:
                buy_details = []

                # WazirX API call for BUY
                try:
                    wazirx.create_order(f'{symbol[:-3].upper()}/INR', 'limit', 'buy', amount_per_transaction/current_price, current_price)

                    with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'a', newline='', encoding='utf-8') as episode_file:
                        # buy_details = [BUY, timestamp, amount spent, price bought at, no. of item bought]
                        buy_details.append(['BUY', datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y%m%d%H%M%S"), amount_per_transaction, current_price, amount_per_transaction/current_price])
                        csv.writer(episode_file).writerows(buy_details)
                    print('Subsequent BUY')
                except Exception as error:
                    print(error)
                    print('skipping symbol - ', symbol)
                    continue