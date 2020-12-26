import psycopg2
import pandas as pd
from sqlalchemy import create_engine

from datetime import datetime

engine = create_engine('postgresql+psycopg2://postgres:password@localhost/Minecraft', echo=False)

headers = ['object_type','x','y','z','world_type']

data = [
['Docking_Station', '-100', '69', '160', 'Overworld'],
['Drop_Point', '-92', '69', '152', 'Overworld']
        ]

df = pd.DataFrame(data,columns = headers)

df.to_sql( schema = 'Mining', name = 'infrastructure_locations',con = engine, if_exists = 'replace')

df_mining_result = pd.read_sql_query(con = engine, sql = """  select * from "Mining".infrastructure_locations""")

df_mining_result