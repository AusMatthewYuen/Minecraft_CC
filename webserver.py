from flask import Flask
from flask import request
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
    
    mining_coordinates = "-91,20,147,4,4,4"
    
    return mining_coordinates