import ast 
import json
import sqlite3
import requests


conn = sqlite3.connect("anna-data-flask-apps.db", isolation_level=None)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
apps = cursor.execute(''' update anna_data_apps set target = "{}" where site_id= "miryang01" and `table`="dms_lpr_data_part" '''.format(['lpr_data_part.json']))
conn.commit()
conn.close()

