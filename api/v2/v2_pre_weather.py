from . import api_v2
from .v2_sql import *
from .v2_helps import * 


# API ROUTE
#############################################################################################################################################

# # Use replace_to_sql() ####################################
@api_v2.route('/weather/weather_localinfo', methods=['POST'])
@engine_manager
def weather_localinfo(conn, trans):
    '''
    # Function : "weather.weather_localinfo" Data preprocessing
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
        df_ = df.drop_duplicates(['SLOCALNAME'], keep='last')
        df_.rename(columns={
            'SLOCALCODE':'slocal_code', 'SLOCALNAME':'slocal_name',
            'LSENSORTYPE':'lsensor_type', 'LMODELTYPE':'lmodel_type', 
            'LLINETYPE':'lline_type', 'BAVRTYPE':'bavr_type',
            'LASTCALLTIME_KST':'last_call_time_kst', 'GATH_TURM':'gath_turm',
            }, inplace=True)
        del df_["LASTCALLTIME"]
        df_.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_weather_localinfo.format(schema=schema, table=table)
    result = replace_to_sql(df_, schema, table, query, conn, trans)

    return result

# Use append_only_to_sql() ####################################
@api_v2.route('/weather/weather_atmo', methods=['POST'])
@engine_manager
def weather_atmo(conn, trans):
    '''
    # Function : "weather.weather_atmo" Data preprocessing
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
        df_ = df.drop_duplicates(['SLOCALCODE', 'ATMODATE_KST'], keep='last')
        df_.rename(columns={
            'SLOCALCODE':'slocal_code',
            'ATMODATE_KST':'atmo_date_kst', 'BTYPE':'btype', 
            'LAVR':'lavr', 'LMIN':'lmin', 'LMAX':'lmax',
            'BRTUSTATE':'brtu_state'}, inplace=True)
        df_.drop(["SLOCALNAME", "LASTCALLTIME_KST", "TABLE_NAME"], axis=1, inplace=True)
        df_.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_weather_atmo.format(schema=schema, table=table)
    result = append_only_to_sql(df_, schema, table, query, conn, trans)
    
    return result


@api_v2.route('/weather/weather_humi', methods=['POST'])
@engine_manager
def weather_humi(conn, trans):
    '''
    # Function : "weather.weather_humi" Data preprocessing
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
        df_ = df.drop_duplicates(['SLOCALCODE', 'HUMIDATE_KST'], keep='last')
        df_.rename(columns={
            'SLOCALCODE':'slocal_code',
            'HUMIDATE_KST':'humi_date_kst', 'BTYPE':'btype', 
            'LAVR':'lavr', 'LMIN':'lmin', 'LMAX':'lmax',
            'BRTUSTATE':'brtu_state'}, inplace=True)
        df_.drop(["SLOCALNAME", "LASTCALLTIME_KST", "TABLE_NAME"], axis=1, inplace=True)
        df_.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_weather_humi.format(schema=schema, table=table)
    result = append_only_to_sql(df_, schema, table, query, conn, trans)
    
    return result


@api_v2.route('/weather/weather_rain', methods=['POST'])
@engine_manager
def weather_rain(conn, trans):
    '''
    # Function : "weather.weather_rain" Data preprocessing
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
        df_ = df.drop_duplicates(['SLOCALCODE', 'RAINDATE_KST'], keep='last')
        df_.rename(columns={
            'SLOCALCODE':'slocal_code',
            'RAINDATE_KST':'rain_date_kst', 'BTYPE':'btype', 
            'lValue':'lvalue', 'bSensing':'bsensing'}, inplace=True)
        df_.drop(["SLOCALNAME", "LASTCALLTIME_KST", "TABLE_NAME"], axis=1, inplace=True)
        df_.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_weather_rain.format(schema=schema, table=table)
    result = append_only_to_sql(df_, schema, table, query, conn, trans)
    
    return result


@api_v2.route('/weather/weather_temp', methods=['POST'])
@engine_manager
def weather_temp(conn, trans):
    '''
    # Function : "weather.weather_temp" Data preprocessing
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
        df_ = df.drop_duplicates(['SLOCALCODE', 'TEMPDATE_KST'], keep='last')
        df_.rename(columns={
            'SLOCALCODE':'slocal_code',
            'TEMPDATE_KST':'temp_date_kst', 'BTYPE':'btype', 
            'LAVR':'lavr', 'LMIN':'lmin', 'LMAX':'lmax',
            'MINTIME':'min_time', 'MAXTIME':'max_time',
            'BRTUSTATE':'brtu_state'}, inplace=True)
        df_.drop(["SLOCALNAME", "LASTCALLTIME_KST", "TABLE_NAME"], axis=1, inplace=True)
        df_.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_weather_temp.format(schema=schema, table=table)
    result = append_only_to_sql(df_, schema, table, query, conn, trans)
    
    return result


@api_v2.route('/weather/weather_wind', methods=['POST'])
@engine_manager
def weather_wind(conn, trans):
    '''
    # Function : "weather.weather_wind" Data preprocessing
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
        df_ = df.drop_duplicates(['SLOCALCODE', 'WINDDATE_KST'], keep='last')
        df_.rename(columns={
            'SLOCALCODE':'slocal_code',
            'WINDDATE_KST':'wind_date_kst', 'BTYPE':'btype', 
            'LAVRDEG1':'lavr_deg1', 'LAVRVEL1':'lavr_vel1', 'LAVRDEG2':'lavr_deg2',
            'LAVRVEL2':'lavr_vel2', 'LMAXDEG':'lmax_deg', 'LMAXVEL':'lmax_vel',
            'MAXVELTIME':'max_vel_time',
            'BRTUSTATE':'brtu_state'}, inplace=True)
        df_.drop(["SLOCALNAME", "LASTCALLTIME_KST", "TABLE_NAME"], axis=1, inplace=True)
        df_.loc[:,'db_update_time_utc'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(df_)
    except Exception as e:
       return pre_raise_error(e)
    
    # SQL
    query = q_weather_wind.format(schema=schema, table=table)
    result = append_only_to_sql(df_, schema, table, query, conn, trans)
    
    return result