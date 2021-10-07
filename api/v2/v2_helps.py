# a
import asyncio
from azure.storage.blob.aio import BlobServiceClient

# d
from datetime import datetime, timedelta

# f
from functools import wraps
from flask import jsonify, request

# j
import json

# m
from math import ceil, floor

# n
import numpy as np

# o
import os

# p
import pandas as pd

# s
import sys
from sqlalchemy import create_engine

# u
from urllib.parse import quote_plus
from uuid import uuid4



# Data path of Azure blob storage files
data_parents_path = '/data/'

# Azure SQL-Server(MS-SQL) config
host = 'dms-bi-db-service.database.windows.net'
port = '1433'
db = 'site'
user = 'lance'
pwd = '[P@ssw0rd][P@ssw0rd]'

# ODBC config
odbc_driver = 'ODBC Driver 17 for SQL Server'
odbc_url = f'DRIVER={odbc_driver};SERVER=tcp:{host},{port};DATABASE={db};UID={user};PWD={pwd}'
odbc_url_qp = quote_plus(odbc_url)
odbc_engine_url = f'mssql+pyodbc:///?odbc_connect={odbc_url_qp}'

##### Helps Decorator
def engine_manager(origin):
    '''
    # Function : Before origin(Create sqlalchemy engine) / After origin(Dispose sqlalchemy engine)
    # Params : 
        1. origin : function
    # Return : function
    '''
    @wraps(origin)
    def _wrapper():
        global odbc_engine_url
        engine = create_engine(odbc_engine_url, fast_executemany=True, encoding='utf-8', pool_size=50, max_overflow=0)
        conn = engine.connect()
        trans = conn.begin()
        result = origin(conn, trans)
        conn.close()
        engine.dispose()
        return result
    return _wrapper


##### Helps Functions
def pre_raise_error(result):
    if result is None:
        msg = {"RESULT":"ERROR", "ERROR":"NO SEARCH BLOB or DataFrame"}
    else:
        msg = {"RESULT":"ERROR", "MESSAGE":str(result)}
    return msg

def set_scheam(conn_str):
    return [ item.split('=')[1] for item in conn_str.split(';') if 'AccountName' in item ][0] 

def make_time_dirs(start_time:str, end_time:str):
    '''
    # Function : Make time directory list(range : start_time <= item <= end_time)
    # Params :
        1. start_time : str
        2. end_time : str
    # Return : list
    '''
    date_fmt = '%Y-%m-%d %H:00:00'
    start_time = datetime.strptime(start_time, date_fmt)
    end_time = datetime.strptime(end_time, date_fmt)

    dir_fmt = '%Y/%m/%d/%H'
    result = list()
    sub_time = end_time - start_time
    sub_sec = sub_time.total_seconds()
    sub_hour = floor(sub_sec/3600)

    for hour in range(0,sub_hour+1):
        dir = (end_time - timedelta(hours=hour)).strftime(dir_fmt)
        result.append(dir)  
    return result


async def stream_blob(params, time_dir, target):
    '''
    # Function : Asyncio execution, download 'blob client'
    # Params :
        1. form : werkzeug.local.LocalProxy
        2. time_dir : str
    # Return : str
    '''
    # from azure.storage.blob.aio import BlobServiceClient
    conn_str = params['conn_str']
    container = params['container']
    service = params['service']
    myblob = os.path.join(service, time_dir, target)
    
    result = ''
    try :
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        
        async with blob_service_client:
            container_client = blob_service_client.get_container_client(container)
            blob_client = container_client.get_blob_client(myblob)

            # Block blob files of downloading
            lease = blob_client.acquire_lease(lease_duration=-1)
            
            if await blob_client.exists():
                stream = await blob_client.download_blob()
                data = await stream.readall()
                result = data.decode('utf-8')
        
        # Break block lease
        # lease.break_lease()
    except Exception as e:
        print("ERROR>>",e)
    return result


async def stream_main(params):
    '''
    # Function : Asyncio execution main function for download 'blob client'
    # Params :
        1. form : werkzeug.local.LocalProxy
    # Return : str
    '''
    start_time = params['start_time']
    end_time = params['end_time']
    time_dirs = make_time_dirs(start_time, end_time)

    futures = []
    for target in params['target']:
        for time_dir in time_dirs:
            futures.append(asyncio.ensure_future(stream_blob(params, time_dir, target))) 
    # futures  = [asyncio.ensure_future(stream_blob(params, time_dir)) for time_dir in time_dirs]
    results = await asyncio.gather(*futures)

    return "".join(filter(None, results))


def make_df(params):
    '''
    # Function : Run stream_main function and Make dataframe
    # Params :
        1. form : werkzeug.local.LocalProxy
    # Return : Dataframe
    '''
    result = None
    data = asyncio.run(stream_main(params))
    if len(data):
        data = '[{0}]'.format(data.replace('\n', ',')[:-1])
        data_ls = list(map(lambda x : x['data'], json.loads(data)))
        result = pd.json_normalize(data_ls)
    return result

def replace_to_sql(df_res, schema, table, query, conn, trans):
    '''
    # Function : Try : Drop table and create table. finally : Append to sql of pandas dataframe
    # Params :
        1. df_res : Pandas dataframe
        2. schema : str
        3. table : str
        4. query : str
        5. conn : sqlalchemy.engine.base.Connection
        6. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : Result message of Preprocessing 
    '''
    try:
        conn.execute(query)
        df_res.to_sql(schema=schema, name=table, con=conn, if_exists='append',  index=False, index_label=None, chunksize=10000)
        trans.commit()
        result = {"RESULT":"OK"}
    except Exception as e:
        trans.rollback()
        result = {"RESULT":"ERROR", "ERROR":str(e)}
        if 'Cannot insert duplicate key in object' in str(e):
            result = {"RESULT":"ERROR", "ERROR":"Cannot insert duplicate key in object"}
    return result


def append_to_sql(df_res, schema, table, query, conn, trans, time_column='db_update_time' , hours=24):
    '''
    # Function : Try : Create table if not exists and append new dataframe. finally : Delete from table where db_update_time < now() - 24H
    # Params :
        1. df_res : Pandas dataframe
        2. schema : str
        3. table : str
        4. query : str
        5. conn : sqlalchemy.engine.base.Connection
        6. trans : sqlalchemy.engine.base.RootTransaction
        7. time_column : 
        8. hours : int() -> 24
    # Return : str : Result message of Preprocessing 
    '''
    try:
        time_line = datetime.now() - timedelta(hours=hours)
        time_line_str = time_line.strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(query)
        df_res.to_sql(schema=schema, name=table, con=conn, if_exists='append',  index=False, index_label=None, chunksize=10000)
        conn.execute(
            f""" DELETE FROM {schema}.{table} WHERE {time_column} < '{time_line_str}' """
        )
        trans.commit()
        result = {"RESULT":"OK"}
    except Exception as e:
        trans.rollback()
        result = {"RESULT":"ERROR", "ERROR":str(e)}
        if 'Cannot insert duplicate key in object' in str(e):
            result = {"RESULT":"ERROR", "ERROR":"Cannot insert duplicate key in object"}
    return result


def append_only_to_sql(df_res, schema, table, query, conn, trans):
    '''
    # Function : Try : Create table if not exists and append new dataframe.
    # Params :
        1. df_res : Pandas dataframe
        2. schema : str
        3. table : str
        4. query : str
        5. conn : sqlalchemy.engine.base.Connection
        6. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : Result message of Preprocessing 
    '''
    try:
        conn.execute(query)
        df_res.to_sql(schema=schema, name=table, con=conn, if_exists='append',  index=False, index_label=None, chunksize=10000)
        trans.commit()
        result = {"RESULT":"OK"}
    except Exception as e:
        trans.rollback()
        result = {"RESULT":"ERROR", "ERROR":str(e)}
        if 'Cannot insert duplicate key in object' in str(e):
            result = {"RESULT":"ERROR", "ERROR":"Cannot insert duplicate key in object"}
    return result
