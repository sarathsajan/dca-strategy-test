# run_order : 5

def current_statistics():
    import csv
    import pathlib
    import datetime

    # Get list of coin pairs to check
    # symbol_list = ['ethinr', 'adainr', 'linkinr', 'uniinr', 'algoinr', 'nearinr', 'lunainr', 'manainr', 'xlminr', 'dotinr', 'btcinr']
    # symbol_list = ['btcinr']
    with open("symbol_list.csv", 'r', newline='', encoding='utf-8') as symbol_list_file:
        symbol_list = (list(csv.reader(symbol_list_file)))[0]

    # Clear the old data, if any
    with open(f'statistics/completed_statistics.csv', 'w', newline='', encoding='utf-8') as statistics_file:
        writer = csv.writer(statistics_file)
        writer.writerow(['Symbol', 'Timestamp', 'total_amount_BUY', 'total_amount_SELL', 'profit_in_percent'])
    with open(f'statistics/current_statistics.csv', 'w', newline='', encoding='utf-8') as statistics_file:
        writer = csv.writer(statistics_file)
        writer.writerow(['Symbol', 'Timestamp', 'total_amount_BUY', 'total_SOH', 'total_PROFIT', 'total_amount_SELL', 'selling_PRICE_POINT'])

    # get the list of completed episode files of each coin pair
    # to consolidate the data
    for symbol in symbol_list:
        episode_file_path_list = list(pathlib.Path(f'episodes/{symbol}').glob('*.*'))
        # traverse through each completed episode and extract the necessary data
        # only if there is atleast 1 completed episode for that symbol
        # So if there is atleast 1 completed episode the length of the list will be greater than 1
        # that is the current episode file plus the completed episode file
        if len(episode_file_path_list) > 1:
            episode_data_list = []
            for episode_file_path in episode_file_path_list:
                if episode_file_path.name == f'{symbol}_episode_current.csv':
                    # skip the current episode file, as that episode is not yet completed
                    continue
                with open(episode_file_path, 'r', newline='', encoding='utf-8') as completed_episode_file:
                    episode_data_list.extend(list(csv.reader(completed_episode_file)))

            # using the data from all the completed episodes, consolidate the data for BUY and SELL
            # for BUY
            total_amount_BUY = sum([float(data[2]) for data in episode_data_list if data[0] == 'BUY'])
            # for SELL
            total_amount_SELL = sum([float(data[2]) for data in episode_data_list if data[0] == 'SELL'])

            # Write the consolidated data to a new csv file
            with open(f'statistics/completed_statistics.csv', 'a', newline='', encoding='utf-8') as statistics_file:
                writer = csv.writer(statistics_file)
                writer.writerow([symbol, datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M:%S"), total_amount_BUY, total_amount_SELL, ((total_amount_SELL/total_amount_BUY)-1)*100])

    for symbol in symbol_list:
        episode_file_path = (list(pathlib.Path(f'episodes/{symbol}').glob(f'{symbol}_episode_current.csv')))[0]
        episode_data_list = []
        with open(episode_file_path, 'r', newline='', encoding='utf-8') as current_episode_file:
            episode_data_list = (list(csv.reader(current_episode_file)))

        # check if current episode has data, if data present proceed else skip
        # using the data from the current episode to display total capital spent for BUY,
        # and total capital to be earned from selling along with profit, and the price point at which to SELL    
        if len(episode_data_list) > 0:
            # BUY
            total_amount_BUY = sum([float(data[2]) for data in episode_data_list if data[0] == 'BUY'])
            
            # STOCK ON HAND
            total_SOH = sum([float(data[4]) for data in episode_data_list if data[0] == 'BUY'])
            
            # PROFIT PERCENT
            # Tax rate and WazirX fee structure
            tds_rate = 1
            maker_fee = 0.2
            # taker_fee = 0.2
            # base_p = 1.017 --> this is 1.7%
            # base_p = 1.0122 -> this is 1.22%
            
            base_p = 100 / (100 - tds_rate - maker_fee)
            total_PROFIT = base_p + (0.000125 * len(episode_data_list)) #should match the base_p value in check_sell.py file
            
            # SELL
            total_amount_SELL = total_amount_BUY * total_PROFIT
            
            # PRICE POINT to sell
            selling_PRICE_POINT = total_amount_SELL / total_SOH


            # Write the consolidated data to a new csv file
            with open(f'statistics/current_statistics.csv', 'a', newline='', encoding='utf-8') as statistics_file:
                writer = csv.writer(statistics_file)
                writer.writerow([symbol, datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M:%S"), total_amount_BUY, total_SOH, total_PROFIT, total_amount_SELL, selling_PRICE_POINT])
        
