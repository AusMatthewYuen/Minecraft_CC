from flask import Flask
from flask import request
from datetime import datetime
app = Flask(__name__)

import psycopg2
import pandas as pd
import numpy as np

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
    
@app.route('/mining_job_server_allocation')
def mining_server_finder():
    
    x = int(request.args.get('x')) #if key doesn't exist, returns None
    y = int(request.args.get('y'))
    z = int(request.args.get('z'))
    
    sql_query = """
    select 
    object_label

    from "Mining".infrastructure_locations INFRA
    where object_type = 'Docking_Station'
    
    order by 
    
    abs(cast({0} as int) - cast(x as int)) 
    + abs(cast({1} as int) - cast(y as int)) 
    + abs(cast({2} as int) - cast(z as int))  asc
    
    limit 1
    """.format(x,y,z)
    
    df_mining_server = pd.read_sql_query(con = engine, sql = sql_query)
    
    if df_mining_server.empty == True:
        return str("error, no docking point available")
    
    returned_string = df_mining_server['object_label'][0]
        
    return returned_string

    
@app.route('/mining_path')
def mining_request():
    
    mining_job_server = str(request.args.get('mining_job_server'))
    
    sql_query = """
    
    select * from "Mining".mining_jobs_allocated 
    where object_label = '{0}'
    order by time desc limit 1
    
    """.format(mining_job_server)
    
    df_mining_result = pd.read_sql_query(con = engine, sql = sql_query)
    
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
    delete from "Mining".mining_jobs_allocated 
    where x = '{0}' 
    and y = '{1}' 
    and z = '{2}' 
    and time = '{3}'
    and object_label = '{4}'
    """.format(x,y,z,time,mining_job_server))
    
    returned_string = str((x,y,z,x_quarry,y_quarry,z_quarry))
    
    returned_string = returned_string.replace('(' , "" )
    returned_string = returned_string.replace(')' , "" )
    returned_string = returned_string.replace("'" , "" )
    returned_string = returned_string.replace(" " , "" )
    
    return returned_string


@app.route('/mining_jobs_available')
def mining_jobs_check():
    
    mining_job_server = request.args.get('mining_job_server')
    
    sql_query = """
    
    select count(*) as count from "Mining".mining_jobs_allocated
    where object_label = '{0}'
    
    """.format(mining_job_server)

    df_count_result = pd.read_sql_query(con = engine, sql = sql_query)
    
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
    mining_job_power_zone_check()
    mining_job_queue_allocator()
    
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
        
@app.route('/powerline_one_step_expansion')
def powerline_one_step_expansion():
    
    powerline_creation_request()
    
    return "jobs added to queue"

@app.route('/powerline_jobs_available')
def powerline_jobs_available():
    
    sql_query = """
    select 
    count(*) as counter
    
    from "Mining".powerline_available_jobs
    
    """
    
    df_powerline_job_counter = pd.read_sql_query(con = engine, sql = sql_query)
    
    if df_powerline_job_counter.empty == True:
        return 0
    else:
        return str(df_powerline_job_counter['counter'][0])
    

@app.route('/powerline_update')
def powerline_placement_location():
    x = int(request.args.get('x')) #if key doesn't exist, returns None
    y = 98
    z = int(request.args.get('z'))
    
    sql_query = """
    insert into "Mining".infrastructure_locations
    values (1,'Worldspike','Worldspike','{0}','{1}','{2}','Overworld')

    """.format(x,y,z)
        
    return 'powerline added to database'
    

@app.route('/powerline_path')
def powerline_job():
    
    sql_query = """
    select 
      coordinate_job_x
    , coordinate_job_z
    
    from "Mining".powerline_available_jobs
    
    limit 1
    """
    
    df_powerline_job = pd.read_sql_query(con = engine, sql = sql_query)
    
    if df_powerline_job.empty == True:
        return 'no jobs'
        
    x = df_powerline_job['coordinate_job_x'][0]
    z = df_powerline_job['coordinate_job_z'][0]
    
    engine.execute("""
    delete from "Mining".powerline_available_jobs 
    where coordinate_job_x = '{0}' 
    and coordinate_job_z = '{1}' 
    """.format(x,z))
    
    returned_string = str((x,z))
    
    returned_string = returned_string.replace('(' , "" )
    returned_string = returned_string.replace(')' , "" )
    returned_string = returned_string.replace("'" , "" )
    returned_string = returned_string.replace(" " , "" )
    
    return returned_string


def mining_job_splitter(x, y ,z , xquarry = 50 ,yquarry = 1,zquarry = 1,numbots = 4):
    
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
            mining_jobs.append(('mining', x+(i * multiple + multiple), y, z,remainder  ,yquarry ,zquarry))
        else:
            mining_jobs.append(('mining', x+(i * multiple + multiple), y, z,multiple  ,yquarry ,zquarry))

    df = pd.DataFrame(mining_jobs,columns = headers)

    df.to_sql( schema = 'Mining', name = 'mining_jobs',con = engine, if_exists = 'replace')
    
def mining_job_queue_allocator():
    print('pi')
    
    sql_query = """
    
    with mining_queue_allocator as 
    
        (
            select
            MINING.*
            , INFRA.object_label
            , rank() OVER (
            				PARTITION BY MINING.x, MINING.y, MINING.z ORDER BY    
            			      abs(cast(MINING.x as int) - cast(INFRA.x as int)) 
                			+ abs(cast(MINING.y as int) - cast(INFRA.y as int)) 
                			+ abs(cast(MINING.z as int) - cast(INFRA.z as int))
							, object_label asc 
            			  ) as mining_rank
            FROM "Mining".mining_within_powered_grid_zones MINING
            
            CROSS JOIN "Mining".infrastructure_locations INFRA
            WHERE INFRA.object_type = 'Docking_Station'
        )
        
    select * from mining_queue_allocator
    where mining_rank = 1 
    
    """
    
    df = pd.read_sql_query(con = engine, sql = sql_query)
    
    df.to_sql( schema = 'Mining', name = 'mining_jobs_allocated',con = engine, if_exists = 'append')
    
    
def mining_job_power_zone_check():
    
    sql_query_worldspike_range = """
    
    select 
      cast(INFRA.x as double precision) / 16.0 as xchunk
    , cast(INFRA.z as double precision) / 16.0 as zchunk
    
    from "Mining".infrastructure_locations INFRA where object_type = 'Worldspike'

    """
    
    df_worldspikes = pd.read_sql_query(con = engine, sql = sql_query_worldspike_range)
    
    df_worldspikes['xchunk'] = df_worldspikes['xchunk'].apply(np.floor)
    df_worldspikes['zchunk'] = df_worldspikes['zchunk'].apply(np.floor)
    
    df_worldspikes['xmin_chunk'] = df_worldspikes['xchunk'] - 1 
    df_worldspikes['xmax_chunk'] = df_worldspikes['xchunk'] + 1 
    df_worldspikes['zmin_chunk'] = df_worldspikes['zchunk'] - 1 
    df_worldspikes['zmax_chunk'] = df_worldspikes['zchunk'] + 1 
        
    df_worldspikes.to_sql( schema = 'Mining', name = 'powered_grid_zones',con = engine, if_exists = 'replace')
    
    sql_query_power_zone_check = """
    
    select 
    mining.*
    from "Mining".mining_jobs mining
    
    cross join "Mining".powered_grid_zones power
    
    where mining.x/16 between power.xmin_chunk and power.xmax_chunk
    and (mining.x + x_quarry) / 16 between power.xmin_chunk and power.xmax_chunk
    and mining.z/16 between power.zmin_chunk and power.zmax_chunk
    and (mining.z + z_quarry) / 16 between power.zmin_chunk and power.zmax_chunk
    

    """
    
    df_worldspikes_zone_check = pd.read_sql_query(con = engine, sql = sql_query_power_zone_check)
    
    df_worldspikes_zone_check.to_sql(schema = 'Mining', name = 'mining_within_powered_grid_zones',con = engine, if_exists = 'replace')
    

def powerline_creation_request():
    
    df_list = []
    
    sql_query_worldspike_range = """
    
    
    select xchunk, zchunk from "Mining".powered_grid_zones 
    
    """
    
    df_worldspikes = pd.read_sql_query(con = engine, sql = sql_query_worldspike_range)
    
    worldspike_list = [list(df_worldspikes['xchunk']),list(df_worldspikes['zchunk'])] 
    
    def powerline_chunk_job_plus_one(base_chunk):
        
        chunk_job_x = []
        chunk_job_z = []
        coordinate_job_x = []
        coordinate_job_z = []
        
        chunk_job_x.append(base_chunk[0] + 1)
        chunk_job_z.append(base_chunk[1])
        
        chunk_job_x.append(base_chunk[0] - 1)
        chunk_job_z.append(base_chunk[1])
        
        chunk_job_x.append(base_chunk[0])
        chunk_job_z.append(base_chunk[1] + 1)
    
        chunk_job_x.append(base_chunk[0])
        chunk_job_z.append(base_chunk[1] - 1)
        
        chunk_job_x.append(base_chunk[0] + 1)
        chunk_job_z.append(base_chunk[1] + 1)
    
        chunk_job_x.append(base_chunk[0] - 1)
        chunk_job_z.append(base_chunk[1] - 1)
        
        chunk_job_x.append(base_chunk[0] + 1)
        chunk_job_z.append(base_chunk[1] - 1)
    
        chunk_job_x.append(base_chunk[0] - 1)
        chunk_job_z.append(base_chunk[1] + 1)
        
        coordinate_job_x.append(list(map(lambda x : x * 16, chunk_job_x)))
        coordinate_job_z.append(list(map(lambda x : x * 16, chunk_job_z))) 
    
        return(chunk_job_x, chunk_job_z,coordinate_job_x,coordinate_job_z)

    job_map = list(map(powerline_chunk_job_plus_one,worldspike_list))
  
    for i in job_map:
        print(i)
        q = zip(i[0],i[1],i[2][0],i[3][0])
        headers = ['chunk_job_x', 'chunk_job_z', 'coordinate_job_x', 'coordinate_job_z']
        df = pd.DataFrame(q,columns = headers)        
        df_list.append(df)
        
    df = pd.concat(df_list)
    
    df.to_sql( schema = 'Mining', name = 'powerline_intermediate_jobs',con = engine, if_exists = 'replace')

    sql_query_valid_powerline_jobs = """
    
     with temp_table_job_validity as 
     
     	(
        select 
    	 case when chunk_job_x = xchunk and chunk_job_z = zchunk then 0 else 1 end as valid_job
    	, jobs.chunk_job_x
    	, jobs.chunk_job_z
    	, cast(jobs.coordinate_job_x as int)
    	, cast(jobs.coordinate_job_z as int)
    	
    	from "Mining".powerline_intermediate_jobs jobs
        
        cross join "Mining".powered_grid_zones zones
        
        where chunk_job_x between xmin_chunk and xmax_chunk
        and chunk_job_z between zmin_chunk and zmax_chunk
    	 )
    
    select distinct
      chunk_job_x
    , chunk_job_z
    , coordinate_job_x
    , coordinate_job_z
    from temp_table_job_validity 
    where valid_job = 1
    
    """
    
    df_powerline_jobs = pd.read_sql_query(con = engine, sql = sql_query_valid_powerline_jobs)
    
    df_powerline_jobs.to_sql(schema = 'Mining', name = 'powerline_available_jobs',con = engine, if_exists = 'replace')
    
    