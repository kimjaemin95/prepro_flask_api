from . import api_v1
from .v1_sql import *
from .v1_helps import * 


def _divas_water_flow(df, schema, tables):
    query = q_divas_water_flow.format(schema=schema, table=tables)
    # Data parse
    df['flow_date'] = df['date']
    df['equipment_id'] = df['id']
    df['equipment_name'] = df['name']
    df['last_time'] = df['lasttime']
    df['realtime_flow_value'] = df['flow_value']
    df_res = df.drop(['date', 'id', 'name', 'lasttime', 'flow_value'], axis=1)
    df_res = df_res.drop_duplicates(['code', 'flow_date'], keep='last')
    return df_res, query


# API ROUTE
#############################################################################################################################################
@api_v1.route('/divas/history/<tables>', methods=['POST'])
def divas_reference(tables):
    '''
    Functions : Divas history API
    TABLES : Create if not exists only
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

    # Data parse
    if tables == 'divas_water_flow':
        df_res, query = _divas_water_flow(df, schema, tables)
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
