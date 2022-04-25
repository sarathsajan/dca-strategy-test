import csv
import shutil
import datetime

# Get list of coin pairs to check
# symbol_list = ['ethinr', 'adainr', 'linkinr', 'uniinr', 'algoinr', 'nearinr', 'lunainr', 'manainr', 'xlminr', 'dotinr', 'btcinr']
# symbol_list = ['btcinr', 'ethinr']
with open("symbol_list.csv", 'r', newline='', encoding='utf-8') as symbol_list_file:
    symbol_list = (list(csv.reader(symbol_list_file)))[0]

# Read the current episode data from the episodes directory for
# each coin pair in the symbol list
for symbol in symbol_list:
    print('\n', symbol)
    # Opening the CSV file in read mode and reading
    # all the BUY details and storing it as list
    with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'r', newline='', encoding='utf-8') as episode_file:
        episode_buy_details_list = list(csv.reader(episode_file))
        # print(episode_buy_details_list)
    
    # Check SELL condition only if there is a BUY transaction in the current episode
    if len(episode_buy_details_list) > 0:
        # get the total amount of capital A, spend in the current episode
        A = sum([float(buy_details[2]) for buy_details in episode_buy_details_list])
        print(A)

        # get the total number of items bought N, in the current episode
        N = sum([float(buy_details[4]) for buy_details in episode_buy_details_list])
        print(N)

        # profit percentage indicated as fraction 3% meaning 103% meaning 1.03
        P = 1.03

        # after getting P percent profit, the episode portfolio will
        # reach Z amount of capital
        Z = A * P
        print(Z)

        # price to SELL S, to make P percent profit
        S = Z / N
        print(S)

        # opening the CSV file in read mode and reading all the hourly data and
        # storing it as list. All this to just get the current price
        with open(f"price_data/{symbol}.csv", 'r', newline='', encoding='utf-8') as price_file:
            price_data_list = list(csv.reader(price_file))
        current_price = float(price_data_list[-1][1])
        if current_price >= S:
            print('SELL')
            sell_details = []
            with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'a', newline='', encoding='utf-8') as episode_file:
                # sell_details = [SELL, timestamp, capital gained by selling, current price, no. of items sold]
                sell_details.append(['SELL', datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y%m%d%H%M%S"), Z, current_price, Z/current_price])
                csv.writer(episode_file).writerows(sell_details)
            
            # since the current episode is now finished, copy the current episode csv file to another csv file with timestamp
            shutil.copyfile(f"episodes/{symbol}/{symbol}_episode_current.csv", f"episodes/{symbol}/{symbol}_episode_{datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime('%Y%m%d%H%M%S')}.csv")
            # and then generate a fresh empty current episode csv file
            with open(f"episodes/{symbol}/{symbol}_episode_current.csv", 'w+', newline='', encoding='utf-8') as episode_file:
                pass