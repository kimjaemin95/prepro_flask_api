from sqlalchemy import engine
from . import api_v2
from .v2_sql import *
from .v2_helps import * 


# API ROUTE
#############################################################################################################################################

# Use replace_to_sql() ####################################
@api_v2.route('/aruba/dms_layer_ap', methods=['POST'])
@engine_manager
def dms_layer_ap(conn, trans):
    '''
    # Function : "aruba.dms_layer_ap" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    # site :
        1. dongnae01
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
        df_ = df.drop_duplicates(['name'], keep='last')
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_dms_layer_ap.format(schema=schema, table=table)
    result = replace_to_sql(df_, schema, table, query, conn, trans)

    return result


# Use append_only_to_sql() ####################################
@api_v2.route('/aruba/aruba_count_hourly', methods=['POST'])
@engine_manager
def aruba_count_hourly(conn, trans):
    '''
    # Function : "aruba.aruba_count_hourly" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    # site :
        1. dongnae01
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
        df_ = df.drop_duplicates(['loc', 'id', 'time'], keep='last')
        df_.loc[:,'dt_hour'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:00:00')
        df_res = df_.groupby(['loc', 'dt_hour']).agg(
            cnt = ('id', 'count')
        ).reset_index()
        df_res.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_aruba_count_hourly.format(schema=schema, table=table)
    result = append_only_to_sql(df_res, schema, table, query, conn, trans)

    return result


@api_v2.route('/aruba/aruba_count_daily', methods=['POST'])
@engine_manager
def aruba_count_daily(conn, trans):
    '''
    # Function : "aruba.aruba_count_daily" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    # site :
        1. dongnae01
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
        df_ = df.drop_duplicates(['loc', 'id', 'time'], keep='last')

        # Filter dms_layer_ap 
        q = f""" SELECT name, sublayer_id, ap_serial FROM {schema}.dms_layer_ap; """
        asset_ls = [id[0] for id in conn.execute(q).fetchall()]
        df_ap = pd.read_sql_query(q, conn)

        # Columns settings
        df_.loc[:,'dt'] = (pd.to_datetime(df['time']) + timedelta(hours=9)).dt.strftime('%Y-%m-%d')
        df_gp = df_.groupby(['loc', 'id', 'dt']).agg(
            cnt = ('id', 'count'),
            start_time = ('time', 'min'),
            end_time = ('time', 'max'),
            avg_signal = ('signal', 'mean')
        ).reset_index().round(0)
        df_gp.loc[:,'stay_time'] = round((pd.to_datetime(df_gp['end_time']) - pd.to_datetime(df_gp['start_time'])).dt.seconds/60, 0)
        df_gp.loc[:,'avg_interval_time'] = round(df_gp['stay_time']/df_gp['cnt'], 0)
        df_gp['stay_rate'] = round(df_gp['cnt']/df_gp['stay_time'], 5)
        df_mg = pd.merge(df_gp, df_ap, left_on='loc', right_on='ap_serial', how='inner')
        df_rp = df_mg.replace([np.inf, -np.inf], 0)
        df_rp.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df_res = df_rp.drop(['loc', 'name', 'ap_serial'], axis=1)

    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_aruba_count_daily.format(schema=schema, table=table)
    result = append_only_to_sql(df_res, schema, table, query, conn, trans)

    return result