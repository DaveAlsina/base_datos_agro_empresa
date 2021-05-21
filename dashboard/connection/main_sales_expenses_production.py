from connection import Connection
import queries as sql

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

conn = Connection("./conn_data.json") #datos para la conexión

#estilo de bootstrap
external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"]

#instancia de Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Total de ingresos por cultivo
conn.openConnection()
query = pd.read_sql_query(sql.getTotalIncomeByCrop(), conn.connection)
conn.closeConnection()
dfTotalIncomebyCrop = pd.DataFrame(query, columns = ["crop", "total_income"])
figBarIncome = px.bar(dfTotalIncomebyCrop, x = "crop", y = "total_income")


#Layout
app.layout = html.Div(children = [
        html.H1(children = 'Sales Analysis'),
        html.H2(children = 'Total Income by Crop'),
        dcc.Graph(
                id = 'barIncome1',
                figure = figBarIncome),
        ])
        
if __name__ == '__main__':
    app.run_server(debug = True)

