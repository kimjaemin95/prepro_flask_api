import sys
import os
import ast 
import asyncio
import aiohttp
import json
import sqlite3
import random
from datetime import datetime, timedelta


# Global Arguments 
batch_start = datetime.now()
set_hours = sys.argv[1]

def set_times(site_id, service):
    now = datetime.now()
    if (set_hours == '1' and site_id == 'hadong01' and service == 'weather') or \
        (set_hours == '1' and  site_id == 'hadong01' and service == 'forest'):

        start_time = (now - timedelta(hours=1)).strftime('%Y-%m-%d %H:00:00')
        end_time = start_time

    elif set_hours == '1': # Target normal 1H cron
        start_time = (now - timedelta(hours=2)).strftime('%Y-%m-%d %H:00:00')
        end_time = start_time

    elif set_hours == '24': # Target normal 24 cron
        start_time = (now - timedelta(days=1)).strftime('%Y-%m-%d 15:00:00')
        end_time = now.strftime('%Y-%m-%d 14:00:00')

    return start_time, end_time

# Functions 
async def fetch(app):
    config = dict(app)
    site_id = config['site_id']
    conn_str = config['conn_str']
    conatiner = config['container']
    service = config['service']
    table = config['table']
    target = ast.literal_eval(config['target'])
    api_path = config['api_path']
    url = 'http://0.0.0.0:5000/api/v2/data' + api_path

    start_time, end_time = set_times(site_id, service)
    
    data = { 
        'conn_str': conn_str, 'container': conatiner, 'service':service, 'table':table, 'target':target, 'start_time':start_time, 'end_time':end_time
        } 
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=data) as response:
                    result = await response.text()
                    msg = result.replace('\n', '').replace('  ','')
                    print(msg, url, site_id, start_time, sep=' | ' )
                    # print('-'*100)
                    await asyncio.sleep(1)
            # except asyncio.TimeoutError as e:
            except asyncio.TimeoutError as e:
                print('-'*150)
                print({'RESULT':'ERROR', 'ERROR':'Asyncio time out error'}, url, site_id, start_time, sep=' | ')

async def main(apps):
    futures = [asyncio.ensure_future(fetch(app)) for app in apps]
    result = await asyncio.gather(*futures)
    return len(result)


# Set Configure of asyncio 
task_count = 30
semaphore = asyncio.Semaphore(task_count)

# Connection Sqlite3
db_name = 'bi_data_flask.db'
path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(path, db_name)

conn = sqlite3.connect(db_path, isolation_level=None)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
apps = cursor.execute(
    "SELECT * FROM view_anna_apps WHERE cron = {0} ".format(set_hours)
    ).fetchall()

# Create asyncio event loop
random.shuffle(apps)
for n in range(0, len(apps), task_count):
    asyncio.run(main(apps[n:n+task_count]))

batch_end = datetime.now()
print("Run time :", batch_end - batch_start)