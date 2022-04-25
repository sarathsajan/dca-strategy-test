import csv
import pathlib

# Get list of coin pairs to check
# symbol_list = ['ethinr', 'adainr', 'linkinr', 'uniinr', 'algoinr', 'nearinr', 'lunainr', 'manainr', 'xlminr', 'dotinr', 'btcinr']
# symbol_list = ['btcinr', 'ethinr', 'adainr']
with open("symbol_list.csv", 'r', newline='', encoding='utf-8') as symbol_list_file:
    symbol_list = (list(csv.reader(symbol_list_file)))[0]

# check if nescessary files exist in price_data folder
# if not, create them
for symbol in symbol_list:
    price_data_folder = pathlib.Path(f"price_data")
    if not price_data_folder.is_dir():
        price_data_folder.mkdir()
    price_data_file = pathlib.Path(f"price_data/{symbol}.csv")
    if not price_data_file.is_file():
        with open(f"price_data/{symbol}.csv", 'w+', newline='', encoding='utf-8') as price_data_file:
            pass

# check if nescessary files and sub folders exist in episodes/symbol folder
# if not, create them
for symbol in symbol_list:
    episode_folder = pathlib.Path(f"episodes")
    if not episode_folder.is_dir():
        episode_folder.mkdir()
    episode_symbol_folder = pathlib.Path(f"episodes/{symbol}")
    if not episode_symbol_folder.is_dir():
        episode_symbol_folder.mkdir()
    episode_file = pathlib.Path(f"episodes/{symbol}/{symbol}_episode_current.csv")
    if not episode_file.is_file():
        with open(f"episodes/{symbol}/{symbol}_episode_current.csv",'w+', newline='', encoding='utf-8') as episode_file:
            pass