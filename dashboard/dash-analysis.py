import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

data = pd.read_csv('./sensor_data.csv')

#ver la temperatura con el area inferior que tiene
tempFig = px.area(data, x="timestamp", y="temp")

#ver la temperatura como solo una linea
tempFig2 = px.line(data, x="timestamp", y="temp")

#ver todos en uno mismo plot
tempFig3 = go.Figure()
tempFig3.add_trace(go.Scatter(x=list(data["timestamp"]), y=list(data["temp"]), mode='lines+markers', name='Temperatura'))
tempFig3.add_trace(go.Scatter(x=list(data["timestamp"]), y=list(data["hum"]), mode='lines+markers', name='Humedad'))
tempFig3.add_trace(go.Scatter(x=list(data["timestamp"]), y=list(data["pressure"]), mode='lines+markers', name='Presión Atmosférica'))
tempFig3.add_trace(go.Scatter(x=list(data["timestamp"]), y=list(data["lux"]), mode='lines', name='Lux'))

#subplot de 1 columna y 4 filas
tempFig4  =  make_subplots(rows=4, cols=1, shared_xaxes=False, vertical_spacing=0.05)

tempFig4.add_trace(go.Scatter(x=list(data["timestamp"]), y=list(data["temp"]), mode='lines',
                    name='Temperatura', marker = dict(color='#ff4340')), row = 1, col=1)
tempFig4.add_trace(go.Scatter(x=list(data["timestamp"]), y=list(data["hum"]), mode='lines',
                    name='Humedad', marker = dict(color='#4b69ed')), row = 2, col=1)
tempFig4.add_trace(go.Scatter(x=list(data["timestamp"]), y=list(data["pressure"]), mode='lines',
                    name='Presión Atmosférica', marker = dict(color='#6CD1DB')), row = 3, col=1)  #69ed4b -> verde clarito
tempFig4.add_trace(go.Scatter(x=list(data["timestamp"]), y=list(data["lux"]), mode='lines',
                    name='Lux', marker = dict(color='#eed04d')), row = 4, col=1)

tempFig4.update_layout(height=1000, width=1000, title="Reporte de Variables del cultivo :>")
tempFig4.update_layout(paper_bgcolor="#161B29", plot_bgcolor="#161B29")

app.layout = html.Div(children=[
    html.H1(children='Proyecto de Bases de Datos :D'),

    html.Div(children='''
        Prueba sencilla con dash
    '''),

    dcc.Graph(
        id='Temperatura',
        figure=tempFig4
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)


#ejemplos de interactividad interesantes:
#1) https://plotly.com/python/histograms/

#linea más puntos y otros modos de hacer scatters con plotly
#1) https://plotly.com/python/line-charts/

#manejar atributos extra de los plots
#1) https://plotly.com/python/reference/layout/#layout-paper_bgcolor

#manejar pandas dataframe a partir de queries de data Bases
#esto permite no usar csv sino directamente usar bases de datos 
#1) https://datatofish.com/sql-to-pandas-dataframe/

#maybe para grafos:
#1) https://plotly.com/python/scatter-plots-on-maps/
