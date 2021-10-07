from sqlalchemy import engine
from . import api_v2
from .v2_sql import *
from .v2_helps import * 


# API ROUTE
#############################################################################################################################################

# Use append_only_to_sql() ####################################
@api_v2.route('/divas/divas_water_flow', methods=['POST'])
@engine_manager
def divas_water_flow(conn, trans):
    '''
    # Function : "divas.divas_water_flow" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    # site :
        1. ulsanbuk01
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
        df_ = df.drop_duplicates(['code', 'date'], keep='last')
        df_.rename(columns={
            'date':'flow_date',
            'id':'equipment_id',
            'name':'equipment_name',
            'lasttime':'last_time',
            'flow_value':'realtime_flow_value'
            }, inplace=True)
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_divas_water_flow.format(schema=schema, table=table)
    result = append_only_to_sql(df_, schema, table, query, conn, trans)

    return result

