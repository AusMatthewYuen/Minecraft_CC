import psycopg2
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://postgres:password@localhost/Minecraft', echo=False)

headers = ['type','id','x','y','z','label','rednet_class']
data = [
['Computer', '12', '-143', '172', '241', 'gps0003_over', 'GPS_Over'],
['Computer', '13', '-132', '176', '229', 'gps0004_over', 'GPS_Over'],
['Computer', '10', '-142', '180', '236', 'gps0005_over', 'GPS_Over'],
['Computer', '11', '-141', '172', '218', 'gps0002_over', 'GPS_Over'],
['Computer', '14', '-153', '164', '226', 'gps0001_over', 'GPS_Over']
        ]

df = pd.DataFrame(data,columns = headers)

df.to_sql(schema = 'Mining', name = 'gps_computer',con = engine, if_exists = 'replace')

df_gps_result = pd.read_sql_query(con = engine, sql = """  select x,y,z from "Mining".gps_computer
    where id = '12'""")