# After change pyspark...

from sqlalchemy import engine
from . import api_v2
from .v2_sql import *
from .v2_helps import * 


# API ROUTE
#############################################################################################################################################

# Use append_only_to_sql() ####################################
@api_v2.route('/vurixdms/dms_lpr_data_part/yeongcheon01', methods=['POST'])
@engine_manager
def dms_lpr_data_part_yeongcheon01(conn, trans):
    '''
    # Function : "vurixdms.dms_lpr_data_part" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    # site :
        1. yeongcheon01
        2. miryang01
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
        df_ = df.drop_duplicates(['id'], keep='last')
        
        # Filter dms_lpr_asset 
        q = f""" SELECT cctv_id FROM {schema}.dms_lpr_asset; """
        asset_ls = [id[0] for id in conn.execute(q).fetchall()]
        df_ = df_[df_['cctv_id'].isin(asset_ls)]

        # group by
        df_res = df_.groupby(['cctv_id', 'day_hour_part', 'vhcty_asort_nm', 'vims_prpos_se_nm', 'use_strnghld_area1', 'use_strnghld_area2']).agg(
            cnt = ('car_num','count')
        ).reset_index()
        df_res.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_dms_lpr_data_part_yeongcheon01.format(schema=schema, table=table)
    result = append_only_to_sql(df_res, schema, table, query, conn, trans)

    return result


@api_v2.route('/vurixdms/dms_lpr_data_part/miryang01', methods=['POST'])
@engine_manager
def dms_lpr_data_part_miryang01(conn, trans):
    '''
    # Function : "vurixdms.dms_lpr_data_part" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    # site :
        1. yeongcheon01
        2. miryang01
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
        df_ = df.drop_duplicates(['id'], keep='last')

        # Filter dms_lpr_asset 
        q = f""" SELECT cctv_id FROM {schema}.dms_lpr_asset; """
        asset_ls = [id[0] for id in conn.execute(q).fetchall()]
        df_ = df_[df_['cctv_id'].isin(asset_ls)]

        # group by
        df_res = df_.groupby(['day_hour_part', 'vhcty_asort_nm', 'vims_prpos_se_nm', 'use_strnghld_area1', 'use_strnghld_area2']).agg(
            cnt = ('car_num','count')
        ).reset_index()
        df_res.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_dms_lpr_data_part_miryang01.format(schema=schema, table=table)
    result = append_only_to_sql(df_res, schema, table, query, conn, trans)

    return result


@api_v2.route('/vurixdms/dms_plpr_data_part', methods=['POST'])
@engine_manager
def dms_plpr_data_part(conn, trans):
    '''
    # Function : "vurixdms.dms_plpr_data_part" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    # site :
        1. yeongcheon01
        2. miryang01
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
        df_ = df.drop_duplicates(['id'], keep='last')

        # Filter dms_lpr_asset 
        q = f""" SELECT cctv_id FROM {schema}.dms_plpr_layer_cctv; """
        asset_ls = [id[0] for id in conn.execute(q).fetchall()]
        df_ = df_[df_['cctv_id'].isin(asset_ls)]

        # group by
        df_res = df_.groupby(['cctv_id', 'day_hour_part', 'arrear_type']).agg(
                    cnt = ('id', 'count'),
                    arrear_sum = ('arrear', 'sum'),
                    arrear_min = ('arrear', 'min'),
                    arrear_max = ('arrear', 'max'),
                    arrear_count_sum = ('arrear_count', 'sum'),
                    cctv_name = ('cctv_name', 'first'),
                    hjd_name = ('hjd_name', 'last'),
                    longitude = ('longitude', 'last'),
                    latitude = ('latitude', 'last'),
        ).reset_index()
        df_res.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(df_res.columns)
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_dms_plpr_data_part.format(schema=schema, table=table)
    result = append_only_to_sql(df_res, schema, table, query, conn, trans)

    return result

