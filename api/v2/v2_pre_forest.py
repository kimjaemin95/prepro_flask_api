from . import api_v2
from .v2_sql import *
from .v2_helps import * 


# API ROUTE
#############################################################################################################################################

# # Use replace_to_sql() ####################################
@api_v2.route('/forest/forest_sensor_list', methods=['POST'])
@engine_manager
def forest_sensor_list(conn, trans):
    '''
    # Function : "forest.forest_sensor_list" Data preprocessing
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
        df.sort_values(by="recvDatetime", inplace=True)
        df.drop_duplicates(['no'], keep='last', inplace=True)
        df.rename(columns={
            'deviceType':'device_type', 'recvDatetime':'last_recp_time'
            }, inplace=True)
        df.loc[ (df["voltage"] == "") | (df["voltage"] == "-"), "voltage"] = np.nan
        df.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_forest_sensor_list.format(schema=schema, table=table)
    result = replace_to_sql(df, schema, table, query, conn, trans)

    return result

@api_v2.route('/forest/forest_tree_list', methods=['POST'])
@engine_manager
def forest_tree_list(conn, trans):
    '''
    # Function : "forest.forest_tree_list" Data preprocessing
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
        df.drop_duplicates(['no'], keep='last', inplace=True)
        df.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_forest_tree_list.format(schema=schema, table=table)
    result = replace_to_sql(df, schema, table, query, conn, trans)

    return result


# Use append_to_sql() ####################################
@api_v2.route('/forest/forest_tree', methods=['POST'])
@engine_manager
def forest_tree(conn, trans):
    '''
    # Function : "forest.forest_tree" Data preprocessing
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
        df.drop_duplicates(['no', 'date', 'hour'], keep='last', inplace=True)
        float_col = ["temperature", "humidity", "top", "middle", "bottom", "soil", "voltage"]
        for fc in float_col:
            df.loc[ (df[fc] == "") | (df[fc] == "-"), fc] = np.nan

        df.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_forest_tree.format(schema=schema, table=table)
    result = append_to_sql(df, schema, table, query, conn, trans, time_column='date', hours=24*60)
    
    return result

'''
@api_v2.route('/forest/forest_sensor', methods=['POST'])
@engine_manager
def forest_sensor(conn, trans):
    
    # Function : "forest.forest_sensor" Data preprocessing
    # Params :
    #    1. conn : sqlalchemy.engine.base.Connection
    #    2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    
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
        df.drop_duplicates(['no', 'date', 'hour'], keep='last', inplace=True)
        float_col = ["temperature", "humidity", "top", "middle", "bottom", "soil", "voltage"]
        for fc in float_col:
            df.loc[ (df[fc] == "") | (df[fc] == "-"), fc] = np.nan

        df.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_forest_sensor.format(schema=schema, table=table)
    result = append_to_sql(df, schema, table, query, conn, trans, time_column='date', hours=24*60)
    
    return result
'''
