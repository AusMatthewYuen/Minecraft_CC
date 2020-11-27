from flask import Flask
from flask import request
from datetime import datetime
app = Flask(__name__)

import psycopg2
import pandas as pd

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:password@localhost/Minecraft', echo=False)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/GPS_Setup')
def gps_link():
    computer_id = request.args.get('computer_id') #if key doesn't exist, returns None
    
    sql_query = """
    
    select X,Y,Z from "Mining".gps_computer
    where ID = '{0}'
    
    """.format(computer_id)
    
    location = pd.read_sql_query(con = engine, sql = sql_query)
    
    if location.empty:
        return 'No PC Registered'
    else:
        return_string = str(location['x'][0] +',' + location['y'][0] + ',' + location['z'][0])
        return return_string
    
@app.route('/mining_path')
def mining_request():
    df_mining_result = pd.read_sql_query(con = engine, sql = """  select * from "Mining".mining_jobs order by time desc limit 1""")
    
    x = df_mining_result['x'][0]
    y = df_mining_result['y'][0]
    z = df_mining_result['z'][0]
    x_quarry = df_mining_result['x_quarry'][0]
    y_quarry = df_mining_result['y_quarry'][0]
    z_quarry = df_mining_result['z_quarry'][0]
    time = df_mining_result['time'][0]
    
    engine.execute("""
    delete from "Mining".mining_jobs 
    where x = '{0}' 
    and y = '{1}' 
    and z = '{2}' 
    and time = '{3}'
    """.format(x,y,z,time))
    
    return str((x,y,z,x_quarry,y_quarry,z_quarry))


def mining_job_splitter(x, y ,z , xquarry = 10 ,yquarry = 5,zquarry = 5,numbots = 1):
    
    remainder = xquarry % numbots
    multiple = xquarry // numbots
    
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    headers = ['job','x','y','z','x_quarry','y_quarry','z_quarry','time']
    
    mining_jobs = []
    mining_range = range(numbots - 1)
    
    for i in mining_range:
        mining_jobs.append(('mining', x+(i * multiple), y, z,multiple  ,yquarry ,zquarry, timestamp))
        
    if remainder != 0:
        mining_jobs.append(('mining', x+(i * multiple), y, z,remainder  ,yquarry ,zquarry, timestamp))
        
    df = pd.DataFrame(mining_jobs,columns = headers)

    df.to_sql( schema = 'Mining', name = 'mining_jobs',con = engine, if_exists = 'append')

miner = mining_job_splitter(-100,57,23)
