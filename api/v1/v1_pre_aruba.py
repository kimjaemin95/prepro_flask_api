from . import api_v1
from .v1_sql import *
from .v1_helps import * 


def _list_up_dongnae_wifi_ap(schema, engine):
    with engine.connect() as conn:
        if conn.execute(q_is_table.format(schema=schema, table='dms_layer_ap')):
            q = f"""SELECT name, sublayer_id, ap_serial FROM {schema}.dms_layer_ap ;"""
            df_ap = pd.read_sql_query(q, conn)
    return df_ap

def _dms_layer_ap(df, schema, tables):
    df_res = df.drop_duplicates(['name'], keep='last')
    df_res['x'] = df_res['x'].astype(str)
    df_res['y'] = df_res['y'].astype(str)
    query = q_dms_layer_ap.format(schema=schema, table=tables)
    return df_res, query

def _aruba_count_daily(df, schema, tables, engine):
    pk_list = ['sublayer_id', 'id', 'dt']
    query = q_aruba_count_daily.format(schema=schema, table=tables)
    # Data parse
    df_ap = _list_up_dongnae_wifi_ap(schema, engine)
    df['dt'] = (pd.to_datetime(df['time']) + timedelta(hours=9)).dt.strftime('%Y-%m-%d')
    df_ = pd.merge(df, df_ap, left_on='loc', right_on='ap_serial', how='inner').drop(['name', 'loc', 'ap_serial'], axis=1)\
            .groupby(pk_list)\
            .agg(
                cnt = ('id','count'),
                start_time = ('time', 'min'),
                end_time = ('time', 'max'),
                avg_signal = ('signal', 'mean')
            ).reset_index().round(0)
    df_['stay_time'] = round((pd.to_datetime(df_['end_time']) - pd.to_datetime(df_['start_time'])).dt.seconds/60, 0)
    df_['avg_interval_time'] = round(df_['stay_time']/df_['cnt'], 0)
    df_['stay_rate'] = round(df_['cnt']/df_['stay_time'], 5)
    df_res = df_.replace([np.inf, -np.inf], 0)
    df_res['db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return df_res, query, pk_list

def _aruba_count_hourly(df, schema, tables):
    pk_list = ['loc', 'dt_hour']
    query = q_aruba_count_hourly.format(schema=schema, table=tables)
    df['dt_hour'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d %H:00:00')
    df_res = df.drop_duplicates(['id', 'dt_hour'], keep='last')\
                .groupby(pk_list)\
                .agg(
                    cnt = ('loc','count'),
                ).reset_index()
    df_res['db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return df_res, query, pk_list


# API ROUTE
#############################################################################################################################################
@api_v1.route('/aruba/reference/<tables>', methods=['POST'])
def vurixdms_reference(tables):
    '''
    Functions : VURIXDMS Reference API
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
    if tables == 'dms_layer_ap':
        df_res, query = _dms_layer_ap(df, schema, tables)
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


@api_v1.route('/aruba/history/<tables>', methods=['POST'])
def aruba_history(tables):
    # Connect sql engine
    engine = sql_engine()
    start = datetime.now()

    # Download azure blob
    save_path, schema = blob_download(request)  # save_path, schema = '/home/anna_data/data/dmsbi/aruba/dongnae01/wifi-visit', 'dongnae01'
    
    if not save_path:
        return jsonify({'INFO':'NOT FOUND JSON FILE(FAILED DOWNLOADS BLOB)'})

    # Json to Dataframe
    df = bi_json_to_df(save_path)

    # Data parse
    if tables=='aruba_count_daily':
        df_res, query, pk_list = _aruba_count_daily(df, schema, tables, engine)
    
    elif tables == 'aruba_count_hourly':
        df_res, query, pk_list = _aruba_count_hourly(df, schema, tables)

    else:
        return jsonify({'INFO':'PLEASE CHECK <tables> of URL'})
    
    with engine.connect() as conn:
        # Create table if not exists
        if not conn.execute(q_is_table.format(schema=schema, table=tables)).fetchone():
            conn.execute(query)

        # Data append
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

