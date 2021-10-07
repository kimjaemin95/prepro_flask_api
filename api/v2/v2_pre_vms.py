from . import api_v2
from .v2_sql import *
from .v2_helps import * 


# API ROUTE
#############################################################################################################################################
# Use replace_to_sql() ####################################

@api_v2.route('/vms/dms_layer_cctv', methods=['POST'])
@engine_manager
def dms_layer_cctv(conn, trans):
    '''
    # Function : "vms.dms_layer_cctv" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)

    # Data Preprocessing
    try:
        df.drop_duplicates(['name'], keep='last', inplace=True)
        df.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
       return pre_raise_error(e)

    # SQL
    if schema == "hadong01":
        query = q_dms_layer_cctv_2nd.format(schema=schema, table=table)
    else:
        query = q_dms_layer_cctv.format(schema=schema, table=table)
    result = replace_to_sql(df, schema, table, query, conn, trans)

    return result


@api_v2.route('/vms/vms_device', methods=['POST'])
@engine_manager
def vms_device(conn, trans):
    '''
    # Function : "vms.vms_device" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)

    # Data Preprocessing
    try:
        df_ = df.drop(['dev_property'], axis=1).drop_duplicates(['dev_serial'], keep='last')
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_vms_device.format(schema=schema, table=table)
    result = replace_to_sql(df_, schema, table, query, conn, trans)

    return result

    
@api_v2.route('/vms/vms_device_channel', methods=['POST'])
@engine_manager
def vms_device_channel(conn, trans):
    '''
    # Function : "vms.vms_device_channel" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)

    # Data Preprocessing
    try:
        df_ = df.drop_duplicates(['dch_id'], keep='last')
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_vms_device_channel.format(schema=schema, table=table)
    result = replace_to_sql(df_, schema, table, query, conn, trans)

    return result


@api_v2.route('/vms/vms_device_media', methods=['POST'])
@engine_manager
def vms_device_media(conn, trans):
    '''
    # Function : "vms.vms_device_media" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)

    # Data Preprocessing
    try:
        df_ = df.drop_duplicates(['dchm_id'], keep='last')
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_vms_device_media.format(schema=schema, table=table)
    result = replace_to_sql(df_, schema, table, query, conn, trans)

    return result


@api_v2.route('/vms/vms_device_model', methods=['POST'])
@engine_manager
def vms_device_model(conn, trans):
    '''
    # Function : "vms.vms_device_model" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)

    # Data Preprocessing
    try:
        df_ = df.drop_duplicates(['model_id'], keep='last')
        df_.loc[:,'company'] = df_['model_property'].apply(lambda x : json.loads(x)['company'])
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_ = df_.drop(['model_property'], axis=1)
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_vms_device_model.format(schema=schema, table=table)
    result = replace_to_sql(df_, schema, table, query, conn, trans)
    
    return result


@api_v2.route('/vms/vms_servers', methods=['POST'])
@engine_manager
def vms_servers(conn, trans):
    '''
    # Function : "vms.vms_servers" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)

    # Data Preprocessing
    try:
        df_ = df.drop_duplicates(['srv_id'], keep='last')
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_vms_servers.format(schema=schema, table=table)
    result = replace_to_sql(df_, schema, table, query, conn, trans)
    
    return result


# Use append_to_sql() ####################################

@api_v2.route('/vms/vms_user_log', methods=['POST'])
@engine_manager
def vms_user_log(conn, trans):
    '''
    # Function : "vms.vms_user_log" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)
    
    # Data Preprocessing
    try:
        df_ = df.drop_duplicates(['log_id', 'ins_time'], keep='last')
        df_.loc[:,'uuid'] = [uuid4() for _ in range(len(df_.index))]
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(df_)
        # print(df_.columns)
        # print(df_.dtypes)
    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_vms_user_log.format(schema=schema, table=table)
    result = append_to_sql(df_, schema, table, query, conn, trans, time_column='log_time')
    
    return result

@api_v2.route('/vms/vms_vfs_history', methods=['POST'])
@engine_manager
def vms_vfs_history(conn, trans):
    '''
    # Function : "vms.vms_vfs_history" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)

    # Data Preprocessing
    try:
        df_ = df.drop_duplicates(['srv_serial', 'dev_serial', 'dch_ch', 'rec_time'], keep='last')
        df_.loc[:,'history_serial'] = [uuid4() for _ in range(len(df_.index))]
        df_.loc[:,'rec_time'] = pd.to_datetime(df_['rec_time'], format='%Y%m%d%H')
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_vms_vfs_history.format(schema=schema, table=table)
    result = append_to_sql(df_, schema, table, query, conn, trans, time_column='rec_time')
    
    return result


@api_v2.route('/vms/vms_vfs_fail_history', methods=['POST'])
@engine_manager
def vms_vfs_fail_history(conn, trans):
    '''
    # Function : "vms.vms_vfs_fail_history" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)

    # Data Preprocessing
    try:
        df_ = df.drop_duplicates(['dev_serial', 'dch_ch', 'srv_serial', 'rec_min'], keep='last')
        df_.loc[:,'rec_min'] = pd.to_datetime(df_['rec_min'], format='%Y%m%d%H%M')
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_vms_vfs_fail_history.format(schema=schema, table=table)
    result = append_to_sql(df_, schema, table, query, conn, trans, time_column='rec_min')
    
    return result


@api_v2.route('/vms/vms_server_status', methods=['POST'])
@engine_manager
def vms_server_status(conn, trans):
    '''
    # Function : "vms.vms_server_status" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    schema = set_scheam(params['conn_str'])
    table = params['table']

    # Make pandas dataframe
    df = make_df(params)
    if df is None:
        return pre_raise_error(df)

    # Data Preprocessing
    try:
        df_ = pd.json_normalize(df['param.servers'].explode('param.servers'), record_path = 'groups', meta=['srv_name', 'srv_serial']).explode('items').reset_index(drop=True)
        df_items = pd.json_normalize(df_['items'])
        df_cc = pd.concat([df_, df_items], axis=1).drop('items', axis=1)
        df_cc.loc[:,'item_time'] = pd.to_datetime(df_cc['item_time']/10000000 - 11644473600, unit='s').astype('datetime64[s]')
        df_cc.loc[:,'item_param'] = df_cc['item_param'].apply(lambda x : 'null' if 'null' in x else list(json.loads(x).values())[0])
        df_cc.loc[:,'item_value_str'] = df_cc['item_value'].apply(lambda x : np.nan if x.replace('.','').isdecimal() and x.count('.') <= 1 else x)
        df_cc.loc[:,'item_value']= df_cc['item_value'].apply(lambda x : pd.to_numeric(x) if x.replace('.','').isdecimal() and x.count('.') <= 1 else np.nan)
        df_cc = df_cc.rename(columns={'group_id':'groups_id'})
        df_res= df_cc.groupby(['srv_name', 'srv_serial', 'groups_id', 'item_id', 'item_param'], dropna=False).agg(
            recv_count = ('srv_name', 'count'),
            item_min_time = ('item_time', 'min'),
            item_max_time = ('item_time', 'max'),
            item_value = ('item_value', 'mean'),
            item_value_str = ('item_value_str', 'first')
        ).reset_index().round(3)
        df_res.loc[:,'history_serial'] = [uuid4() for _ in range(len(df_res.index))]
        df_res.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
        return pre_raise_error(e)
    
    # SQL
    query = q_vms_server_status.format(schema=schema, table=table)
    result = append_to_sql(df_res, schema, table, query, conn, trans, time_column='item_min_time')
    
    return result