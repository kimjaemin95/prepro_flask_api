from . import api_v1
from .v1_sql import *
from .v1_helps import * 



def _videotransfer_csafer(df, schema, tables):
    date_column = 'request_date'
    pk_list = ['dev_serial', 'request_date']
    df_new = df.drop_duplicates(pk_list, keep='last')
    df_new[date_column] = df_new[date_column].astype('datetime64[s]')
    query = q_videotransfer_csafer.format(schema=schema, table=tables)
    return df_new, query, pk_list, date_column


# API ROUTE
#############################################################################################################################################
@api_v1.route('/videotransfer/history/<tables>', methods=['POST'])
def videotransfer_history(tables):
    '''
    Functions : videotransfer History API
    TABLES : Drop and Create
    COMMON BATCH : 0 */1 * * * 
    '''
    try:
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
        if tables == 'videotransfer_csafer':
            df_new, query, pk_list, date_column = _videotransfer_csafer(df, schema, tables)
        else:
            return jsonify({'INFO':'PLEASE CHECK <tables> OF URL'})

        with engine.connect() as conn:
            # Check table exists
            if conn.execute(q_is_table.format(schema=schema, table=tables)).fetchone():
                q = f""" SELECT * FROM {schema}.{tables} """
                df_old = pd.read_sql_query(q, conn)
                df_res = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates(pk_list)
            else:
                df_res = df_new.drop_duplicates(pk_list)

            # Where range 30 days
            # date_30d = datetime.now() - timedelta(days=30)
            # df_res = df_res.loc[(df_res[date_column] >= date_30d)]

            # Drop table if exists
            conn.execute(query)
            # APPEND or REPLACE sql
            try:
                df_res.to_sql( schema=schema, name = tables, con = conn, if_exists = 'append',  index = False, index_label = None, chunksize = 10000)
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
    except Exception as e:
        return str(e)
