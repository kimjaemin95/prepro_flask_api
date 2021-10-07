### 🚫주의 : 해당 저장소에 기재된 모든 접속 정보 취급 주의
------------------------------------
# 저장소 이름 : bi_data_flask

## [ 요약 ]  
- 내용 : DMS-BI 데이터 정제 소스 코드
- 환경 : Python 3.7.2 - Flask, Blueprint(API)
- 담당자 : 김재민
- 플로우 : 
    1. API 호출 
    2. Azure storage blob json 파일 호출(Python azure client 사용)
    3. 데이터프레임 전처리
    4. Azure SQL-Server 데이터베이스 저장
    5. Microsoft Power BI 데이터 시각화

------------------------------------
## [ git 배포 방법 ]
``` 
# deploy.sh

pkill -9 -ef flask                                    # 기존에 실행중이던 Flask 프로세스 kill
deactivate                                            # 기존에 활성화 했던 Python 가상환경 종료
rm -rf /home/bi_data_flask                            # 기존에 배포 되어 있던 bi_data_flask 레포지토리 삭제
cd /home                                              # /home 경로 이동

# Azure DevOps ANNA-Project 프로젝트의 bi_data_flask 레포지토리 git clone
git clone https://-----

source /home/envs/.bi_data_flask/bin/activate         # Python 가상환경 활성화
pip install -r /home/bi_data_flask/requirements.txt   # Python 가상환경에 모듈 설치
export FLASK_APP=/home/bi_data_flask/run.py           # FLASK_APP 환경변수에 run.py 파일 경로 등록
nohup flask run -h 0.0.0.0                            # nohup을 이용하여 Background 에서 Host가 0.0.0.0인 상태로 Flask 서버 실행
```
------------------------------------
## [ Cron 스케줄 ]
- 요약 :
  - 내용 : 데이터베이스에 저장되어 있는 각 사이트의 서비스 정보를 호출하여 아래와 같이 Crontab에 등록 되어 있는 명령에 따라 정제 API 실행
  - 데이터베이스 위치 : /bi_data_flask/batch/bi_data_flask.db
  - 데이터베이스 종류 : SQLite3
```
# 1시간 마다 실행하는 서비스 앱(매시간 05분 실행)
05 */1 * * *    sudo docker exec anna_flask /home/envs/.anna-data-flask/bin/python3 /home/bi_data_flask/batch/batch_run.py 1  >> /home/devel/logs/batch_run_1_hour.log 2>&1

# 24시간 마다 실행하는 서비스 앱(매일 오전 01시 05분 실행)
05 01 * * *    sudo docker exec anna_flask /home/envs/.anna-data-flask/bin/python3 /home/bi_data_flask/batch/batch_run.py 24  >> /home/devel/logs/batch_run_24_hour.log 2>&1
``` 
------------------------------------
## [ 소스코드 편집 및 git 관리 방법 ]
1. 작업할 영역에서 git clone(Linux 환경에서 실행 권장)
```
$ git clone https://------
```
2. 파이썬 모듈 관리자 pip 업그레이드
```
$ python3 -m pip install --upgrade pip
```
3. 파이썬 가상환경 모듈 설치
```
$ pip install virtualenv
```
4. 파이썬 가상환경 생성
```
$ virtualenv [가상환경 이름]
예) virtualenv .envs
```
5. 파이썬 가상환경 활성화
```
$ source .envs/bin/activate
```
6. bi_data_flask 실행 필수 모듈 설치
```
$ pip install -r bi_data_flask/requirements.txt
```
7. 소스코드 편집
```
# 코드 편집
```
8. git 히스토리 저장
```
$ git add --all                             # 현재 이하의 모든 파일, 디렉토리 등 저장 선언
$ git add .                                 # 현재 이하의 모든 파일, 디렉토리 등 저장 선언
$ git commit -m "first commit message"      # 저장 선언한 모든 히스토리 Commit 과 Commit 메시지 등록
$ git pull origin main                      # git 저장소에서 히스토리 PULL 다운 받기(변경 사항에 대해 자동 Merge 시도함)
$ git push origin main                      # git 저장소에 히스토리 PUSH 밀어 넣기
```
------------------------------------
## [ 자료 구조 ]
- 자료구조 업데이트 시 tree 자료 함께 업데이트 
```
anna-data-flask/
.
|-- README.md
|-- __pycache__
|   `-- run.cpython-37.pyc
|-- api
|   |-- v1
|   |   |-- __init__.py
|   |   |-- v1_helps.py
|   |   |-- v1_pre_aruba.py
|   |   |-- v1_pre_divas.py
|   |   |-- v1_pre_videotransfer.py
|   |   |-- v1_pre_vms.py
|   |   |-- v1_pre_vurixdms.py
|   |   `-- v1_sql.py
|   `-- v2
|       |-- __init__.py
|       |-- __pycache__
|       |   |-- __init__.cpython-37.pyc
|       |   |-- v2_helps.cpython-37.pyc
|       |   |-- v2_pre_aruba.cpython-37.pyc
|       |   |-- v2_pre_common.cpython-37.pyc
|       |   |-- v2_pre_divas.cpython-37.pyc
|       |   |-- v2_pre_forest.cpython-37.pyc
|       |   |-- v2_pre_videotransfer.cpython-37.pyc
|       |   |-- v2_pre_vms.cpython-37.pyc
|       |   |-- v2_pre_vurixdms.cpython-37.pyc
|       |   |-- v2_pre_weather.cpython-37.pyc
|       |   `-- v2_sql.cpython-37.pyc
|       |-- v2_helps.py
|       |-- v2_pre_aruba.py
|       |-- v2_pre_common.py
|       |-- v2_pre_divas.py
|       |-- v2_pre_forest.py
|       |-- v2_pre_videotransfer.py
|       |-- v2_pre_vms.py
|       |-- v2_pre_vurixdms.py
|       |-- v2_pre_weather.py
|       `-- v2_sql.py
|-- batch
|   |-- batch_run.py
|   |-- bi_data_flask.db
|   |-- db_query.py
|   `-- old_db
|       |-- bi_data_flask(20210901).db
|       `-- bi_data_flask(20210923).db
|-- requirements.txt
|-- research
|   |-- azure
|   |   `-- blob_client_test.py
|   `-- common
|       `-- replace_test_01.py
`-- run.py
``` 
------------------------------------
## [ API 사용방법 ]
### 1. Python
```
import requests
import json

url = "http://[호스트]:5000/api/v2/data/vms/vms_device_model"

payload = json.dumps({
  "conn_str": [스토리지연결문자열],
  "container": [컨테이너이름],
  "service": [서비스이름],
  "table": [테이블이름],
  "target": [
    [BLOB JSON 이름],
    [BLOB JSON 이름]...
  ],
  "start_time": [yyyy-MM-dd HH:mm:ss],
  "end_time": [yyyy-MM-dd HH:mm:ss]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

---------------------------------------------------------------------------
import requests
import json

url = "http://127.0.0.1:5000/api/v2/data/vms/vms_device_model"

payload = json.dumps({
  "conn_str": "XXXXX",
  "container": "dmsbi",
  "service": "vms",
  "table": "vms_device_model",
  "target": [
    "device_model.json"
  ],
  "start_time": "2021-08-24 12:00:00",
  "end_time": "2021-08-24 12:00:00"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
``` 

### 2. cURL
```
curl --location --request POST 'http://127.0.0.1:5000/api/v2/data/vms/vms_device_model' \
--header 'Content-Type: application/json' \
--data-raw '{
    "conn_str":"XXXXX",
    "container":"dmsbi",
    "service":"vms",
    "table":"vms_device_model",
    "target":["device_model.json"],
    "start_time":"2021-08-24 03:00:00",
    "end_time":"2021-08-24 12:00:00"
}'
``` 

------------------------------------
## [ 참고 자료 ]
- git 소스코드 보안 : https://github.com/sobolevn/git-secret
