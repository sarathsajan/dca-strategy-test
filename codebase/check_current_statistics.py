import csv
import pathlib
import datetime

# Get list of coin pairs to check
# symbol_list = ['ethinr', 'adainr', 'linkinr', 'uniinr', 'algoinr', 'nearinr', 'lunainr', 'manainr', 'xlminr', 'dotinr', 'btcinr']
# symbol_list = ['btcinr']
with open("symbol_list.csv", 'r', newline='', encoding='utf-8') as symbol_list_file:
    symbol_list = (list(csv.reader(symbol_list_file)))[0]

# get the list of completed episode files of each coin pair
# to consolidate the data
for symbol in symbol_list:
    episode_file_path_list = list(pathlib.Path(f'episodes/{symbol}').glob('*.*'))
    # traverse through each completed episode and extract the necessary data
    # only if there is atleast 1 completed episode for that symbol
    # So if there is atleast 1 completed episode the length of the list will be greater than 1
    # that id current episode file plus completed episode file
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
        with open(f'statistics/{symbol}_statistics.csv', 'w', newline='', encoding='utf-8') as statistics_file:
            writer = csv.writer(statistics_file)
            # the columns in the statistics file are [ 'DATE', 'BUY', 'SELL'])
            writer.writerow([datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y%m%d%H%M%S"), total_amount_BUY, total_amount_SELL])