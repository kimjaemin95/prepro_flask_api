from pandas.io.pytables import dropna_doc
from sqlalchemy.sql.expression import label
from .v1_sql import *
from azure.storage.blob import BlobClient
from datetime import datetime, timedelta
from flask import jsonify, request
from glob import glob
import json
from math import ceil, floor, floor
import numpy as np
import os
import pandas as pd
from pandas.io.json import json_normalize
import sys
import shutil
from sqlalchemy import create_engine, text, types
from urllib.parse import quote_plus
from uuid import uuid1, uuid4


# Save path of Azure Blob json 
data_path = '/home/anna-data-spark/data/'

# ODBC url
odbc_driver = 'ODBC Driver 17 for SQL Server'
odbc_url = f'DRIVER={odbc_driver};SERVER=tcp:dms-bi-db-service.database.windows.net,1433;DATABASE=site;UID=lance;PWD=[P@ssw0rd][P@ssw0rd]'
odbc_url_qp = quote_plus(odbc_url)
odbc_engine_url = f'mssql+pyodbc:///?odbc_connect={odbc_url_qp}'


# HELP DECORATOR
#############################################################################################################################################
def running_time(origin):
    def running_time_wrapper(*args, **kwargs):
        start = datetime.now()
        res = origin(*args, **kwargs)
        end = datetime.now()
        print('Running time :', end-start)
        return res
    return running_time_wrapper


# HELP FUNCTIONS
#############################################################################################################################################
def sql_engine():
    '''
    Functions : Create SQLAlchemy engine
    '''
    # Create engine
    return create_engine(odbc_engine_url, fast_executemany=True, encoding='utf-8', pool_size=30, max_overflow=0)

def _set_time_dirs(start_time:str, end_time:str):
    '''
    Function : _set_time_dirs
    Contents : Set dir's range -> end_time - start_time 
    '''
    date_fmt   = '%Y-%m-%d %H:00:00'
    start_time = datetime.strptime(start_time, date_fmt)
    end_time   = datetime.strptime(end_time, date_fmt)

    dir_fmt   = '%Y/%m/%d/%H'
    dir_list  = list()
    sub_time   = end_time - start_time
    sub_sec    = sub_time.total_seconds()
    sub_hour = floor(sub_sec/3600)

    for hour in range(0,sub_hour+1):
        dir = (end_time - timedelta(hours=hour)).strftime(dir_fmt)
        dir_list.append(dir)  
    return dir_list

def _make_dirs(path):
    '''
    Function : _make_dirs
    Contents : Delete directories when If exists this and Makes directories
    '''
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"""{{INFO : DELETE DIRECTORIES -> {path}}}""")
    os.makedirs(path)
    print(f"""{{INFO : MAKE DIRECTORIES -> {path}}}""")
    return path

def _remove_dirs(path):
    shutil.rmtree(path)
    print(f"""{{INFO : DELETE DIRECTORIES -> {path}}}""")
    return path

def blob_download(request):
    '''
    Function : blob_download
    Contents : Download azure blob storage files until end of time dirs ranges
    '''
    conn_str   = request.values.get('conn_str')
    start_time = request.values.get('start_time')
    end_time   = request.values.get('end_time')
    container  = request.values.get('container')
    service    = request.values.get('service')
    target     = request.values.get('target')

    # Set time dirs
    time_dirs = _set_time_dirs(start_time, end_time)

    # Set save path
    conn_conf    = { item.split('=')[0]:item.split('=')[1] for item in conn_str.split(';') }
    account_name = conn_conf['AccountName']
    save_path    = os.path.join(data_path, container, service, account_name, target)
    
    # Make dirs 
    _make_dirs(save_path)

    # Downloads azure blob files
    downloas_check = list()
    target_name  = target + '.json'
    for dir in time_dirs:
        target_blob = os.path.join(service, dir, target_name)
        blob_client = BlobClient.from_connection_string(conn_str=conn_str, container_name=container, blob_name=target_blob)
        
        save_file   = os.path.join(save_path, target_blob.replace('/', '_'))
        if blob_client.exists():
            with open(save_file, 'wb') as my_blob:
                wb_blob = blob_client.download_blob()
                my_blob.write(wb_blob.readall())
                print(f"""{{INFO : SUCCESS DOWNLOAD -> {save_file}}}""")
                downloas_check.append(1)
        else:
            # 나중에 예외처리로 수정할 것
            print(f"""{{INFO : NOT FOUND BLOB AND FAIL DOWNLOAD -> {save_file}}}""")
            if not os.path.isdir('/home/anna-data-spark/log/'):
                os.makedirs('/home/anna-data-spark/log/')
            with open('/home/anna-data-spark/log/data_error.log', 'a', encoding='utf-8') as f:
                f.write(f'{{ERROR : NO DATA {account_name}, {target_blob}}}\n')

    if len(downloas_check):
        return save_path, account_name
    else:
        _remove_dirs(save_path)
        return None, None
 

def json_to_df(save_path):
    '''
    Function : json_to_df
    Contents : Json files in 'path' to Dataframes and concat
    '''
    json_path = os.path.join(save_path, '*.json')
    df_list   = [ pd.read_json(file, lines=True, chunksize=100) for file in glob(json_path) ]
    df_all    = pd.concat(df_list, ignore_index=True)
    return df_all

def json_to_df(save_path):
    '''
    Function : json_to_df
    Contents : Json files in 'path' to Dataframes and concat
    '''
    json_path = os.path.join(save_path, '*.json')
    df_list   = [ pd.read_json(file, lines=True) for file in glob(json_path) ]
    df_all    = pd.concat(df_list, ignore_index=True)
    return df_all

def bi_json_to_df(save_path):
    '''
    Function : bi_json_to_df
    Contents : Read json files in save_path to Datafrme and select columns site, data
    '''
    json_path = os.path.join(save_path, '*.json')
    df_list   = [ pd.read_json(file, lines=True) for file in glob(json_path) ]
    df_all    = pd.concat(df_list, ignore_index=True)
    df_flat   = pd.concat([df_all['site'], pd.json_normalize(df_all['data'])], axis=1)\
                  .drop(['site'], axis=1)
    df_flat['db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return df_flat




