# workaround to run python script every hour in pythonanywhere's free tier servers
import datetime
import time
import importlib

# initial run, initiated by external trigger/scheduler at 12 AM
print('run  - ', 0)
print('time - ', datetime.datetime.now())
time.sleep(5)
import app
time.sleep(60*56) # sleep for 56 minutes

# subsequent runs approximately every hour(i.e after sleeping for 56 minutes)
# subsequent runs ideally start from run at 1 AM and end with the 11PM run
# ironically the 11PM run will also include the 56 minute sleep. Then the for completes 
# and the scripts stops.
for run in range(1,24):
    print('run  - ', run)
    print('time - ', datetime.datetime.now())
    time.sleep(5)
    importlib.reload(app)
    time.sleep(60*55) # sleep for 56 minutes

print("ALL 24 RUNS COMPLETED FOR THE DAY")