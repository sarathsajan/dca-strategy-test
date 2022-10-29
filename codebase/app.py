from check_file_generator import *
from check_hourly_price import *
from check_buy import *
from check_sell import *
from check_current_statistics import *
import time
import datetime
import os

os.system('cls')
job_start_dttm = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M:%S")
print('job_start_dttm\t-->\t', job_start_dttm)
time.sleep(5)

os.system('cls')
print('step 1/5 checking and validating files...')
time.sleep(5)
file_generator()
time.sleep(5)

os.system('cls')
print('step 2/5 getting current data (hourly)')
time.sleep(5)
hourly_price()
time.sleep(10)

os.system('cls')
print('step 3/5 running conditional checks and creating "BUY limit orders" if conditions are satisfied')
time.sleep(5)
buy()
time.sleep(5)

os.system('cls')
print('step 4/5 running conditional checks and creating "SELL limit orders" if conditions are satisfied')
time.sleep(5)
sell()
time.sleep(5)

os.system('cls')
print('step 5/5 generating stats...')
current_statistics()
time.sleep(5)

os.system('cls')
job_end_dttm = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M:%S")
print('job_start_dttm\t-->\t', job_start_dttm)
print('job_end_dttm\t-->\t', job_end_dttm)