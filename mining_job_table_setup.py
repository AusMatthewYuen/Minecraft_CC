import psycopg2
import pandas as pd
from sqlalchemy import create_engine

from datetime import datetime

engine = create_engine('postgresql+psycopg2://postgres:password@localhost/Minecraft', echo=False)

headers = ['job','x','y','z','x_quarry','y_quarry','z_quarry','time']


data = []

df = pd.DataFrame(data,columns = headers)

df.to_sql( schema = 'Mining', name = 'mining_jobs',con = engine, if_exists = 'replace')

df_mining_result = pd.read_sql_query(con = engine, sql = """  select * from "Mining".mining_jobs order by time desc""")

df_mining_result