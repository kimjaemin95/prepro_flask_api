from . import api_v1
from .v1_sql import *
from .v1_helps import * 



def _vms_device(df, schema, tables):
    df_res = df.drop(['dev_property'], axis=1).drop_duplicates(['dev_serial'], keep='last')
    query = q_vms_device.format(schema=schema, table=tables)
    return df_res, query

def _dms_layer_cctv(df, schema, tables):
    df_res = df.drop_duplicates(['name'], keep='last')
    query = q_dms_layer_cctv.format(schema=schema, table=tables)
    return df_res, query 

def _vms_device_channel(df, schema, tables):
    df_res = df.drop_duplicates(['dch_id'], keep='last')
    query = q_vms_device_channel.format(schema=schema, table=tables)
    return df_res, query

def _vms_device_media(df, schema, tables):
    df_res = df.drop_duplicates(['dchm_id'], keep='last')
    query = q_vms_device_media.format(schema=schema, table=tables)
    return df_res, query

def _vms_device_model(df, schema, tables):
    def _json_model_property(df):
        try:
            return json.loads(df)
        except:
            return json.loads(df.split('\n')[0])
    df_company = pd.json_normalize(df['model_property'].apply(_json_model_property))['company']
    df_ = pd.concat([df, df_company], axis=1)
    df_res = df_.drop_duplicates(['model_id'], keep='last').drop(['model_property'], axis=1)
    query = q_vms_device_model.format(schema=schema, table=tables)
    return df_res, query

def _vms_servers(df, schema, tables):
    df_res = df.drop_duplicates(['srv_serial'], keep='last')
    query = q_vms_servers.format(schema=schema, table=tables)
    return df_res, query

def _vms_user_log(df, schema, tables):
    pk_list = ['log_id', 'ins_time']
    date_column = 'ins_time'
    query = q_vms_user_log.format(schema=schema, table=tables)
    # Data parse
    df['ins_time'] = pd.to_datetime(df['ins_time'], format='%Y-%m-%d %H:%M:%S')
    df['uuid'] = [uuid4() for _ in range(len(df.index))]
    df_new = df.drop(['log_time'], axis=1)
    return df_new, query, pk_list, date_column

def _vms_vfs_history(df, schema, tables):
    pk_list = ['srv_serial', 'dev_serial', 'dch_ch', 'rec_time']
    date_column = 'rec_time'
    query = q_vms_vfs_history.format(schema=schema, table=tables)
    # Data parse
    df['rec_time'] = pd.to_datetime(df['rec_time'], format='%Y%m%d%H')
    df['history_serial'] = [uuid4() for _ in range(len(df.index))]
    df_new = df
    return df_new, query, pk_list, date_column

def _vms_vfs_fail_history(df, schema, tables):
    pk_list = ['dev_serial', 'dch_ch', 'srv_serial', 'rec_min']
    date_column = 'rec_min'
    query = q_vms_vfs_fail_history.format(schema=schema, table=tables)
    # Data parse
    df['rec_min'] = pd.to_datetime(df['rec_min'], format='%Y%m%d%H%M')
    df_new = df
    return df_new, query, pk_list, date_column

def _vms_server_status(df, schema, tables):
    pk_list = ['srv_name', 'srv_serial', 'groups_id', 'item_id', 'item_param']
    date_column = 'item_min_time'
    query = q_vms_server_status.format(schema=schema, table=tables)
    # Data parse
    df_servers = pd.json_normalize(df['param.servers'].explode('param.servers')).explode('groups').reset_index()
    df_groups = pd.json_normalize(df_servers['groups']).drop(['status'], axis=1)
    df_items = pd.concat([df_servers, df_groups], axis=1).explode('items').drop(['groups'], axis=1).reset_index()
    df_ = pd.concat([df_items, pd.json_normalize(df_items['items'])], axis=1)

    df_['item_time'] = pd.to_datetime(df_['item_time']/10000000 - 11644473600, unit='s').astype('datetime64[s]')
    df_['item_param'] = df_['item_param'].apply(lambda x : 'null' if 'null' in x else list(json.loads(x).values())[0])
    df_['item_value_str'] = df_['item_value'].apply(lambda x : np.nan if x.replace('.','').isdecimal() and x.count('.') <= 1 else x)
    df_['item_value']= df_['item_value'].apply(lambda x : pd.to_numeric(x) if x.replace('.','').isdecimal() and x.count('.') <= 1 else np.nan)
    df_['groups_id'] = df_['group_id']

    df_new = df_.groupby(pk_list, dropna=False).agg(
        recv_count = ('srv_name', 'count'),
        item_min_time = ('item_time', 'min'),
        item_max_time = ('item_time', 'max'),
        item_value = ('item_value', 'mean'),
        item_value_str = ('item_value_str', 'first')
    ).reset_index().round(3)
    df_new['db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df_new['history_serial'] = [uuid4() for _ in range(len(df_new.index))]

    pk_list = pk_list + ['item_min_time']
    return df_new, query, pk_list, date_column


# API ROUTE
#############################################################################################################################################
@api_v1.route('/vms/reference/<tables>', methods=['POST'])
def vms_reference(tables):
    '''
    Functions : VMS Reference API
    TABLES : Drop and Create
    COMMON BATCH : 0 */1 * * * 
    '''
    # Connect sql engine
    engine = sql_engine()
    start = datetime.now()

    # Download azure blob
    save_path, schema = blob_download(request)
    if not save_path:
        return jsonify({'INFO':'NOT FOUND JSON FILE(FAILED DOWNLOADS BLOB)'})

    # Json to Dataframe
    df = bi_json_to_df(save_path)

    query, df_res = None, None
    # Data parse
    if tables == 'vms_device':
        df_res, query = _vms_device(df, schema, tables)

    elif tables == 'dms_layer_cctv':
        df_res, query = _dms_layer_cctv(df, schema, tables)
    
    elif tables == 'vms_device_channel':
        df_res, query = _vms_device_channel(df, schema, tables)

    elif tables == 'vms_device_media':
        df_res, query = _vms_device_media(df, schema, tables)

    elif tables == 'vms_device_model':
        df_res, query = _vms_device_model(df, schema, tables)

    elif tables == 'vms_servers':
        df_res, query = _vms_servers(df, schema, tables)
    else:
        return jsonify({'INFO':'PLEASE CHECK <tables> of URL'})

    with engine.connect() as conn:
        # Drop table if exists
        conn.execute(query)
        # APPEND or REPLACE sql
        try:
            df_res.to_sql( schema=schema, name = tables, con = conn, if_exists = 'append',  index = False, index_label = None, chunksize = 10000 )
        except Exception as e:
            return jsonify({'ERROR':str(e)})

    engine.dispose()
    end = datetime.now()
    data = dict(request.values)
    data['table'] = tables
    data['schema'] = schema
    data['info'] = 'success'
    data['running time'] = str(end-start)
    return jsonify(data)


@api_v1.route('/vms/history/<tables>', methods=['POST'])
def vms_history(tables):
    '''
    Functions : VMS History API
    TABLES : Drop and Create
    COMMON BATCH : 0 */1 * * * 
    '''
    try:
        # Connect sql engine
        engine = sql_engine()
        start = datetime.now()

        # Download azure blob
        save_path, schema = blob_download(request)
        if not save_path:
            return jsonify({'INFO':'NOT FOUND JSON FILE(FAILED DOWNLOADS BLOB)'})

        # Json to Dataframe
        df = bi_json_to_df(save_path)

        query, df_res, pk_list = None, None, None
        # Data parse
        if tables == 'vms_user_log':
            df_new, query, pk_list, date_column = _vms_user_log(df, schema, tables)

        elif tables == 'vms_vfs_history':
            df_new, query, pk_list, date_column = _vms_vfs_history(df, schema, tables)

        elif tables == 'vms_vfs_fail_history':
            df_new, query, pk_list, date_column = _vms_vfs_fail_history(df, schema, tables)

        elif tables == 'vms_server_status':
            df_new, query, pk_list, date_column = _vms_server_status(df, schema, tables)

        else:
            return jsonify({'INFO':'PLEASE CHECK <tables> OF URL'})

        with engine.connect() as conn:
            # Check table exists
            if conn.execute(q_is_table.format(schema=schema, table=tables)).fetchone():
                q = f""" SELECT * FROM {schema}.{tables} """
                df_old = pd.read_sql_query(q, conn)
                df_res = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates(pk_list)
            else:
                df_res = df_new.drop_duplicates(pk_list)

            # Where range 24 hours
            date_24h = datetime.now() - timedelta(hours=24)
            df_res = df_res.loc[(df_res[date_column] >= date_24h)]

            # Drop table if exists
            conn.execute(query)
            # APPEND or REPLACE sql
            try:
                df_res.to_sql( schema=schema, name = tables, con = conn, if_exists = 'append',  index = False, index_label = None, chunksize = 10000 )
            except Exception as e:
                return jsonify({'ERROR':str(e)})
        
        engine.dispose()
        end = datetime.now()
        data = dict(request.values)
        data['table'] = tables
        data['schema'] = schema
        data['info'] = 'success'
        data['running time'] = str(end-start)
        return jsonify(data)
    except Exception as e:
        return str(e)

