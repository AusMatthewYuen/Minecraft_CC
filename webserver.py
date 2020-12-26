from flask import Flask
from flask import request
from datetime import datetime
from flask import stream_with_context
app = Flask(__name__)

import psycopg2
import pandas as pd

from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:password@localhost/Minecraft', echo=False)

@app.route('/')
def hello_world():
    return 'Mining Server Online!'

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
    
    if df_mining_result.empty == True:
        return str("no jobs")
    
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
    
    returned_string = str((x,y,z,x_quarry,y_quarry,z_quarry))
    
    returned_string = returned_string.replace('(' , "" )
    returned_string = returned_string.replace(')' , "" )
    returned_string = returned_string.replace("'" , "" )
    returned_string = returned_string.replace(" " , "" )
    
    return returned_string


@app.route('/mining_jobs_available')
def mining_jobs_check():
    df_count_result = pd.read_sql_query(con = engine, sql = """select count(*) as count from "Mining".mining_jobs""")
    
    if df_count_result.empty == True:
        return str("0")
    
    num_jobs = str(df_count_result['count'][0])
        
    return num_jobs

@app.route('/mining_request')
def mining_queue_add():
    x = int(request.args.get('x')) #if key doesn't exist, returns None
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))
    xquarry = int(request.args.get('xquarry'))
    yquarry = int(request.args.get('yquarry'))
    zquarry = int(request.args.get('zquarry'))
    numbots = int(request.args.get('numbots'))
    
    mining_job_splitter(x,y,z,xquarry,yquarry,zquarry,numbots)
    
    return ('job added to queue')

@app.route('/drop_point_location')
def drop_point_location():
    x = int(request.args.get('x')) #if key doesn't exist, returns None
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))
    
    sql_query = """
    select 
      x
    , y 
    , z
    
    from "Mining".infrastructure_locations INFRA
    where object_type = 'Drop_Point'
    
    order by 
    
    abs(cast({0} as int) - cast(x as int)) 
    + abs(cast({1} as int) - cast(y as int)) 
    + abs(cast({2} as int) - cast(z as int))  asc
    
    limit 1
    """.format(x,y,z)
    
    df_closest_drop_point = pd.read_sql_query(con = engine, sql = sql_query)
    
    x = df_closest_drop_point['x'][0]
    y = df_closest_drop_point['y'][0]
    z = df_closest_drop_point['z'][0]
    
    returned_string = str((x,y,z))
    
    returned_string = returned_string.replace('(' , "" )
    returned_string = returned_string.replace(')' , "" )
    returned_string = returned_string.replace("'" , "" )
    returned_string = returned_string.replace(" " , "" )
    
    return returned_string

@app.route('/docking_station_location')
def docking_station_location():
    x = int(request.args.get('x')) #if key doesn't exist, returns None
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))
    
    sql_query = """
    select 
      x
    , y 
    , z
    
    from "Mining".infrastructure_locations INFRA
    where object_type = 'Docking_Station'
    
    order by 
    
    abs(cast({0} as int) - cast(x as int)) 
    + abs(cast({1} as int) - cast(y as int)) 
    + abs(cast({2} as int) - cast(z as int))  asc
    
    limit 1
    """.format(x,y,z)
    
    df_closest_docking_station = pd.read_sql_query(con = engine, sql = sql_query)
    
    x = df_closest_docking_station['x'][0]
    y = df_closest_docking_station['y'][0]
    z = df_closest_docking_station['z'][0]
    
    returned_string = str((x,y,z))
    
    returned_string = returned_string.replace('(' , "" )
    returned_string = returned_string.replace(')' , "" )
    returned_string = returned_string.replace("'" , "" )
    returned_string = returned_string.replace(" " , "" )
    
    return returned_string
        

def mining_job_splitter(x, y ,z , xquarry = 50 ,yquarry = 1,zquarry = 1,numbots = 2):
    
    remainder = xquarry % numbots
    multiple = xquarry // numbots
    
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    headers = ['job','x','y','z','x_quarry','y_quarry','z_quarry','time']
    
    mining_jobs = []
    mining_range = range(numbots)
    
    for i in mining_range:
        mining_jobs.append(('mining', x+(i * multiple), y, z,multiple  ,yquarry ,zquarry, timestamp))
        
    if numbots != 1:
        if remainder != 0:
            mining_jobs.append(('mining', x+(i * multiple + 1 + multiple), y, z,remainder  ,yquarry ,zquarry, timestamp))
        else:
            mining_jobs.append(('mining', x+(i * multiple + 1 + multiple), y, z,multiple  ,yquarry ,zquarry, timestamp))
        
    df = pd.DataFrame(mining_jobs,columns = headers)

    df.to_sql( schema = 'Mining', name = 'mining_jobs',con = engine, if_exists = 'append')

