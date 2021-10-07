from . import api_v1
from .v1_sql import *
from .v1_helps import *


def _dms_lpr_asset(schema, engine, table='dms_lpr_asset'):
    asset_list = list()
    with engine.connect() as conn:
        if conn.execute(q_is_table.format(schema=schema, table='dms_lpr_asset')):
            q = f"""SELECT cctv_id FROM {schema}.{table} ;"""
            asset_list = [id[0] for id in conn.execute(q).fetchall()]
    return asset_list

def _dms_lpr_data_part_miryang(df, schema, tables, engine):
    def _set_area3(df):
        if df['use_strnghld_area1'] and df['use_strnghld_area2']:
            return df['use_strnghld_area1'] + '.' + df['use_strnghld_area2']
        elif df['use_strnghld_area1']:
            return df['use_strnghld_area1']
        else:
            return ''
    pk_list = pk_list = ['day_hour_part', 'vhcty_asort_nm', 'vims_prpos_se_nm', 'use_strnghld_area1', 'use_strnghld_area2', 'use_strnghld_area3']
    query = q_dms_lpr_data_part_miryang.format(schema=schema, table=tables)
    asset_list = _dms_lpr_asset(schema, engine)
    df_ = df[df['cctv_id'].isin(asset_list)]
    df_['day_hour_part'] = (pd.to_datetime(df_['regi_at']) + timedelta(hours=9)).dt.strftime('%Y-%m-%d')
    df_['use_strnghld_area3'] = df_[['use_strnghld_area1', 'use_strnghld_area2']].apply(_set_area3, axis=1)
    df_res = df_.groupby(by=pk_list).agg( cnt = ('car_num','count') ).reset_index()
    df_res['db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return df_res, query, pk_list

def _dms_lpr_data_part_yeoncheon(df, schema, tables, engine):
    def _set_area4(df):
        if df['use_strnghld_area1'] and df['use_strnghld_area2'] and df['use_strnghld_area3']:
            return df['use_strnghld_area1'] + '.' + df['use_strnghld_area2'] + '.' + df['use_strnghld_area3']
        elif df['use_strnghld_area1'] and df['use_strnghld_area2']:
            return df['use_strnghld_area1'] + '.' + df['use_strnghld_area2']
        elif df['use_strnghld_area1']:
            return df['use_strnghld_area1']
        else:
            return ''
        
    pk_list = pk_list = ['day_hour_part', 'vhcty_asort_nm', 'vims_prpos_se_nm', 'use_strnghld_area1', 'use_strnghld_area2', 'use_strnghld_area3', 'use_strnghld_area4', 'cctv_id']
    query = q_dms_lpr_data_part_yeoncheon.format(schema=schema, table=tables)
    asset_list = _dms_lpr_asset(schema, engine)
    df_ = df[df['cctv_id'].isin(asset_list)]
    df_['day_hour_part'] = (pd.to_datetime(df_['regi_at']) + timedelta(hours=9)).dt.strftime('%Y-%m-%d')
    df_['use_strnghld_area4'] = df_[['use_strnghld_area1', 'use_strnghld_area2', 'use_strnghld_area3']].apply(_set_area4, axis=1)
    df_res = df_.groupby(by=pk_list).agg( cnt = ('car_num','count') ).reset_index()
    df_res['db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return df_res, query, pk_list

# API ROUTE
#############################################################################################################################################
@api_v1.route('/vurixdms/history/<tables>', methods=['POST'])
def dms_history(tables):
    '''
    Functions : VURIXDMS History API
    TABLES : Drop and Create
    COMMON BATCH : 0 */1 * * * 
    '''
    # Connect sql engine
    engine = sql_engine()
    start = datetime.now()

    # Download azure blob
    save_path, schema = blob_download(request) 
    # save_path, schema = '/home/anna_data-spark/data/dmsbi/vurixdms/miryang01/lpr_data_part', 'miryang01'
    # save_path, schema = '/home/anna-data-spark/data/dmsbi/vurixdms/yeongcheon01/lpr_data_part', 'yeongcheon01'

    if not save_path:
        return jsonify({'INFO':'NOT FOUND JSON FILE(FAILED DOWNLOADS BLOB)'})

    # Json to Dataframe
    df = bi_json_to_df(save_path)

    # Data parse
    if tables=='dms_lpr_data_part' and schema=='miryang01':
        df_res, query, pk_list = _dms_lpr_data_part_miryang(df, schema, tables, engine)


    elif tables=='dms_lpr_data_part' and schema=='yeongcheon01':
        df_res, query, pk_list = _dms_lpr_data_part_yeoncheon(df, schema, tables, engine)    
        
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
