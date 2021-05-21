from connection import Connection
import queries as sql

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

conn = Connection("./conn_data.json")

#queries

conn.openConnection()

print("SALES TABLE")
query = pd.read_sql_query(sql.getSales(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

