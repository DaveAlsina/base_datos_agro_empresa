from connection import Connection
import queries as sql

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


conn = Connection("./conn_data.json")

#obtiene las opciones de qué cultivos poseen datos de sensores
#para crear con esto un menú de selección en la interfaz
conn.openConnection()
query = pd.read_sql_query(sql.createMeasurement_selection_menu(), conn.connection)
conn.closeConnection()

#sección de creación de variables para display en la interfaz

#menú de que cultivos poseen mediciones 
options_crop_measurement_display = []

for cropname in query['crop_name']:
    local_dict = {}
    local_dict['label'] = cropname
    local_dict['value'] = cropname
    
    options_crop_measurement_display.append(local_dict)



########
########
# sección de dash
########
########

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([

    html.Div(
    children = [
        html.Div(
            #dropdown menú para seleccionar de qué cultivo se quieren ver y analizar los datos
            children = [
                html.Div(children="Selección de cultivo", className="menu-title"),
                dcc.Dropdown(
                    id = "opciones_crop_meas_disp",
                    options = options_crop_measurement_display ,
                        value = 'cilantro',
                        placeholder = "Seleccione un cultivo",
                        multi = False,
                ),
            ]
        ),
        html.Div(
            #dropdown menú para seleccionar de qué cultivo se quieren ver y analizar los datos
            children = [
                html.Div(children="Selección de cultivo", className="menu-title"),
                dcc.Dropdown(
                    id = "opciones_crop_meas",
                    options = options_crop_measurement_display ,
                        value = 'cilantro',
                        placeholder = "Seleccione un cultivo",
                        multi = False,
                ),
            ]
        ),
    ], className = 'menu'),



    #seleccionar que variables ambientales del cultivo se quieren visualizar
    dcc.Dropdown(
        id = 'opciones_measure',
        options = [
                {'label': 'Temperatura', 'value': 'humidity'},
                {'label': 'Humedad', 'value': 'temperature'},
                {'label': 'Presión Atmosférica', 'value': 'pressure'},
                {'label': 'Luz', 'value': 'lux'}
            ],
            value = ['humidity', 'temperature', 'pressure', 'lux'],
            placeholder = "Seleccione una variable",
            multi = True,
    ),

    #grafico de mediciones de sensor para las variables seleccionadas por el usuario
    html.Div([
    dcc.Graph(id = 'grafico', animate=True)
    ]),
    
],
className = "mainp")


#callback para blockear la selección de qué condicion ambiental buscar
#si no se especifica de qué cultivo se va a buscar
@app.callback(
    dash.dependencies.Output(component_id = 'opciones_measure', component_property='disabled'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value')]
)

def crop_name_gui_restriction(value):

    print(value)

    if value == None:
        return True
    
    return False 



#callback para generar la figura que contiene todos las variables ambientales ploteadas 
#que pidió el usuario
@app.callback(
    dash.dependencies.Output(component_id = 'grafico', component_property='figure'),
    [dash.dependencies.Input(component_id = 'opciones_measure', component_property='value'),
    dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value')]
)

def build_graph_measurements(op_elegidas, crop_name):

    print("Opciones seleccionadas: ", op_elegidas)
    print("Clase del objeto: ", type(op_elegidas))
    print("Tipo de cultivo recibido: ", crop_name)
    
    fig = go.Figure()
    
    if (crop_name == None):

        print("aaaaa")

    else:

        conn.openConnection()
        measure = pd.read_sql_query(sql.getMeasurements(), conn.connection)
        conn.closeConnection()

        print(measure)
        opts = {'humidity': ('Humedad', '#4b69ed'), 
                'temperature' :('Temperatura', '#ff4340'),
                'pressure': ('Presión Atm.' ,'#6CD1DB'),
                'lux': ('Lux','#eed04d')}

        row_counter = len(op_elegidas)

        if (row_counter == 1):
            
            local_fig = go.Scatter(x = list(measure["time"]), y = list(measure[op_elegidas[0]]), 
                        mode = 'lines', name=opts[op_elegidas[0]][0], 
                        marker = dict(color=opts[op_elegidas[0]][1]))
            fig.add_trace(local_fig)
            fig.update_layout(title=opts[op_elegidas[0]][0])

        elif (row_counter > 1):

            fig = make_subplots(rows = row_counter, cols = 1, shared_xaxes = False, vertical_spacing = 0.05)
            count = 1

            for opt in op_elegidas:

                local_fig = go.Scatter(x = list(measure["time"]), y = list(measure[opt]), 
                        mode = 'lines', name=opts[opt][0], marker = dict(color=opts[opt][1]))
                fig.add_trace(local_fig, row=count, col=1)
                count += 1
    

    fig.update_layout(paper_bgcolor = "#161B29", plot_bgcolor = "#161B29")

    return fig 

#-------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)



