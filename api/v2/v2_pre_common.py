# After change pyspark...

from sqlalchemy import engine
from . import api_v2
from .v2_sql import *
from .v2_helps import * 


# API ROUTE
#############################################################################################################################################

@api_v2.route('/common/blob/jsonify', methods=['POST'])
@engine_manager
def blob_jsonify(conn, trans):
    '''
    # Function : "common.blob.jsonify" Data preprocessing
    # Params :
        1. conn : sqlalchemy.engine.base.Connection
        2. trans : sqlalchemy.engine.base.RootTransaction
    # Return : str : result
    '''
    # Set config
    params = request.get_json()
    conn_str = params.get('conn_str')
    container = params.get('container')
    service = params.get('service')
    target_blob = params.get('target_blob')

    # Check required param
    if conn_str is None or container is None:
        return {"RESULT":"ERROR", "ERROR":"'conn_str' and 'container' are required input values."}
    
    # Make target blob
    if service is None and target_blob is None:
        return {"RESULT":"ERROR", "ERROR":"'service' or 'target_blob' are required input values."}

    if target_blob is None:
        target_blob = '{0}/{1}'.format(service, datetime.now().strftime('%Y/%m/%d/%H/'))
        
    # Import azure
    from azure.storage.blob import ContainerClient
    from azure.storage.blob import BlobClient

    # Connect azure blob storage container
    container_client = ContainerClient.from_connection_string(conn_str, container_name=container)
    blob_list = container_client.list_blobs(name_starts_with=target_blob)  

    # Blob data load
    data_ls = []
    for b in blob_list:
        blob_name = b.name   # blob 이름
        blob_client = BlobClient.from_connection_string(conn_str=conn_str, container_name=container, blob_name=blob_name)
        if blob_client.exists():
            stream = blob_client.download_blob()
            data = stream.readall()
            data_str = data.decode('utf-8')
            if data_str[-1] == '\n':
                data_ls.append(data_str)
            else:
                data_ls.append(data_str+'\n')

    result = []
    # Json to DataFrame
    if len(data_ls):
        data = "".join(filter(None, data_ls))
        data = '[{0}]'.format(data.replace('\n', ',')[:-1])
        result = list(map(lambda x : x['data'], json.loads(data)))
        # pd_res = pd.json_normalize(result)
    else:
        result = {"RESULT":"OK", "ERROR":"NOT EXISTS BLOB FILES."}

    return jsonify(result)

