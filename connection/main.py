from connection_real import Connection
import queries as sql

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

conn = Connection(".\conn_data.json")

#queries

conn.openConnection()

print("MEASUREMENT TABLE")
query = pd.read_sql_query(sql.getMeasurements(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

conn.openConnection()

print("CROP TABLE")
query = pd.read_sql_query(sql.getCrop(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

conn.openConnection()

print("EXP CATEGORY TABLE")
query = pd.read_sql_query(sql.getExpCategory(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

conn.openConnection()

print("EXPENSES TABLE")
query = pd.read_sql_query(sql.getExpenses(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

conn.openConnection()

print("OPT CONDITIONS TABLE")
query = pd.read_sql_query(sql.getOptCondition(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

conn.openConnection()

print("SALES TABLE")
query = pd.read_sql_query(sql.getSales(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

conn.openConnection()

print("SENS INFO TABLE")
query = pd.read_sql_query(sql.getSensInfo(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

conn.openConnection()

print("UNIT TABLE")
query = pd.read_sql_query(sql.getUnit(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

conn.openConnection()

print("ZONE TABLE")
query = pd.read_sql_query(sql.getZone(), conn.connection)
conn.closeConnection()
print(query)
print("\n")

conn.openConnection()

print("PRODUCTION TABLE")
query = pd.read_sql_query(sql.getProduction(), conn.connection)
conn.closeConnection()
print(query)
print("\n")




#external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"]
#
## Inicializacion app dash
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#
## Layout 
#app.layout = html.Div(children=[
#    html.H1(children='Dashboard Covid 19 '),
#    html.H2(children='Casos por país'),
#    dcc.Graph(
#        id='barCasesByCountry',
#        figure=figBarCases
#    )  
#])
#
#
