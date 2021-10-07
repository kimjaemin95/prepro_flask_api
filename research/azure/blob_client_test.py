# Normal
import json
import pandas as pd

# Azure
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobClient




conn_str = 'DefaultEndpointsProtocol=https;AccountName=ulsanbuk01;AccountKey=C0CQq8i8VqHmB71n7/s+EoLtkCiHvZf1oxBdHjCJDhbi1447j1dNzRQyFI2iOLk7B94zRUVU9jTlGyArhqh4Uw==;EndpointSuffix=core.windows.net'
container_name = 'dmsbi'
target_blob = 'weather/2021/08/24/01/'

container = ContainerClient.from_connection_string(conn_str, container_name=container_name)
blob_list = container.list_blobs(name_starts_with=target_blob)

res_ls = []
for b in blob_list:
    blob_name = b.name                              # blob 이름
    json_name = blob_name.split("/")[-1]            # 파일 이름(json 확장자 포함)
    file_name = json_name.replace(".json", "")      # 파일 이름(json 확장자 포함 X)

    blob_client = BlobClient.from_connection_string(conn_str=conn_str, container_name=container_name, blob_name=blob_name)
    if blob_client.exists():
        stream = blob_client.download_blob()
        data = stream.readall()
        result = data.decode('utf-8')
        if result[:-1] == '\n':
            res_ls.append(result)
        else:
            res_ls.append(result+'\n')

if res_ls[:2]:
    data = "\n".join(filter(None, res_ls))
    data = '[{0}]'.format(data.replace('\n', ','))
    data_ls = list(map(lambda x : x['data'], json.loads(data)))
    pd_res = pd.json_normalize(data_ls)
    print(pd_res)
