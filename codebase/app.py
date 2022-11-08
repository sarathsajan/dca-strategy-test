from check_file_generator import *
from check_hourly_price import *
from check_open_orders import *
from check_buy import *
from check_sell import *
from check_current_statistics import *
from wazirx_api_test import *
import time
import datetime
import os

try:
    os.system('cls')
except:
    pass
job_start_dttm = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M:%S")
print('job_start_dttm\t-->\t', job_start_dttm)
time.sleep(5)

try:
    os.system('cls')
except:
    pass
print('step 1/6 checking and validating files...')
time.sleep(5)
file_generator()
time.sleep(5)

try:
    os.system('cls')
except:
    pass
print('step 2/6 getting current data (hourly)')
time.sleep(5)
hourly_price()
time.sleep(15)
test_api()
time.sleep(10)

try:
    os.system('cls')
except:
    pass
print('step 3/6 cancelling all pending BUY orders from previous run')
time.sleep(5)
open_orders()
time.sleep(5)

try:
    os.system('cls')
except:
    pass
print('step 4/5 running conditional checks and creating "BUY limit orders" if conditions are satisfied')
time.sleep(5)
buy()
time.sleep(5)

try:
    os.system('cls')
except:
    pass
print('step 5/6 running conditional checks and creating "SELL limit orders" if conditions are satisfied')
time.sleep(5)
sell()
time.sleep(5)

try:
    os.system('cls')
except:
    pass
print('step 6/6 generating stats...')
current_statistics()
time.sleep(5)

try:
    os.system('cls')
except:
    pass
job_end_dttm = datetime.datetime.now(tz=datetime.timezone(offset=datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M:%S")
print('job_start_dttm\t-->\t', job_start_dttm)
print('job_end_dttm\t-->\t', job_end_dttm)