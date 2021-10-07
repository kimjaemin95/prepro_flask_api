from . import api_v2
from .v2_sql import *
from .v2_helps import * 


# API ROUTE
#############################################################################################################################################
# Use replace_to_sql() ####################################

@api_v2.route('/videotransfer/videotransfer_csafer', methods=['POST'])
@engine_manager
def videotransfer_csafer(conn, trans):
    '''
    # Function : "videotransfer.videotransfer_csafer" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    # site :
        1. seodaemun01
        2. guri01
        3. cheonan01
        4. asan01
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
        df_ = df.drop_duplicates(['request_id', 'child_request_id', 'request_date'], keep='last')
        df_.loc[df_.child_request_id.isnull(),'child_request_id'] = df_['request_id']
        df_.loc[:,'db_update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print(df_)
    except Exception as e:
       return pre_raise_error(e)

    # SQL
    query = q_videotransfer_csafer.format(schema=schema, table=table)
    result = replace_to_sql(df_, schema, table, query, conn, trans)

    return result