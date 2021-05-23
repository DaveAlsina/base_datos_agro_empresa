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

external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"]
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([

    html.Div(
    children = [
        html.Div(
            className = "center row mt-4",
            children = [
            
                #dropdown menú para seleccionar de qué cultivo se quieren ver y analizar los datos

                html.Div(
                    className = "col-12 col-xl-6",
                    children = [
                        html.Div(className = "card-border",
                            children = [
                            html.Div(children="Selección de cultivo", className="card-header bg-dark text-light"),

                        
                            html.Div(className = "menu", children = [
                                    dcc.Dropdown(
                                        id = "opciones_crop_meas_disp",
                                        options = options_crop_measurement_display ,
                                            value = 'cilantro',
                                            placeholder = "Seleccione un cultivo",
                                            multi = False,
                                            className = "dropdown bg-dark"
                                    ),                
                                ])
                            ]),
                    ]),

                html.Div(
                    className = "col-12 col-xl-6",
                    children = [
                    html.Div(
                        #dropdown menú para seleccionar de qué cultivo se quieren ver y analizar los datos
                        children = [
                            html.Div(className = "card-border",
                                children = [
                                    html.Div(children = "Selección de fecha de cultivo", className="card-header bg-dark text-light"),
                                    dcc.Dropdown(
                                        id = "opts_fechas_crop",
                                            value = None,
                                            placeholder = "Seleccione una fecha de cultivo",
                                            multi = False,
                                    ),
                                ]),
                        ]),

                    ]),

            ]),

    html.Div(className = "row mt-4", children = []),

    html.Div(className = "card-border",
        children = [
            #seleccionar que variables ambientales del cultivo se quieren visualizar
            html.Div(children = "Selección de variables ambientales", className = "card-header bg-dark text-center text-light"),
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
        ]),

    #grafico de mediciones de sensor para las variables seleccionadas por el usuario
    html.Div([
        dcc.Graph(id = 'grafico_variables_amb', animate=True)
    ], id = 'grafico_form_variables_amb'),
    
    ],className = "body")
],className = "bg-light")


@app.callback(
    dash.dependencies.Output(component_id = 'opts_fechas_crop', component_property='options'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value')]
)

def display_date_opts(crop_name):
    
    if crop_name != None:

        opt_data = []

        #toma las tuplas del dataframe que tienen el nombre del cultivo 
        #que el usuario ha seleccionado
        dates_for_crop = query[ query['crop_name'] == crop_name]

        for date in dates_for_crop['date_']:            #crea la lista de diccionarios de opciones 
            local_dict = {}                             #para actualizar en la gui
            local_dict['label'] = date
            local_dict['value'] = date
            
            opt_data.append(local_dict)

        return opt_data

    else: 

        #en caso de que se rompa la funcionalidad aunque es muy poco posible
        return [{'label' : 'No hay opciones disponibles', 'value' : 0}]

@app.callback(
    dash.dependencies.Output(component_id = 'opts_fechas_crop', component_property='disabled'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value')]
)

#callback para blockear la selección de qué condicion ambiental buscar
#si no se especifica de cuál es la fecha del cultivo se va a buscar
def crop_date_gui_restriction(value):

    print(value)

    if value == None:
        return True
    
    return False 


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
    dash.dependencies.Output(component_id = 'grafico_form_variables_amb', component_property='hidden'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value'),
    dash.dependencies.Input(component_id = 'opts_fechas_crop', component_property='value')]
)

def show_hide_measure_grap(crop_name, date):
    
    print("aaaa esto es para el hidden: ", crop_name, date)

    if ((crop_name != None) and (date != None)):
        return False 
    else:
        return True
 

#callback para generar la figura que contiene todos las variables ambientales ploteadas 
#que pidió el usuario
@app.callback(
    dash.dependencies.Output(component_id = 'grafico_variables_amb', component_property='figure'),
    [dash.dependencies.Input(component_id = 'opciones_measure', component_property='value'),
    dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value'),
    dash.dependencies.Input(component_id = 'opts_fechas_crop', component_property='value')]
)

def build_graph_measurements(op_elegidas, crop_name, date):

    print("Opciones seleccionadas: ", op_elegidas)
    print("Clase del objeto: ", type(op_elegidas))
    print("Tipo de cultivo recibido: ", crop_name)
    
    fig = go.Figure()
    max_height = 600
    
    if (crop_name == None) or (date == None):

        print("aaaaa")

    else:

        row_counter = len(op_elegidas)
        individual_height = int(max_height/row_counter)

        conn.openConnection()
        measure = pd.read_sql_query(sql.getMeasurements(crop_name, date), conn.connection)
        conn.closeConnection()

        print(measure)
        opts = {'humidity': ('Humedad', '#4b69ed'), 
                'temperature' :('Temperatura', '#ff4340'),
                'pressure': ('Presión Atm.' ,'#6CD1DB'),
                'lux': ('Lux','#eed04d')}


        if (row_counter == 1):
            
            local_fig = go.Scatter(x = list(measure["time_"]), y = list(measure[op_elegidas[0]]), 
                        mode = 'lines', name=opts[op_elegidas[0]][0], 
                        marker = dict(color=opts[op_elegidas[0]][1]))
            fig.add_trace(local_fig)
            fig.update_layout(title=opts[op_elegidas[0]][0])

        elif (row_counter > 1):

            fig = make_subplots(rows = row_counter, cols = 1, shared_xaxes = False, vertical_spacing = 0.15, row_heights = [ individual_height for i in op_elegidas])
            count = 1

            for opt in op_elegidas:

                local_fig = go.Scatter(x = list(measure["time_"]), y = list(measure[opt]), 
                        mode = 'lines', name=opts[opt][0], marker = dict(color=opts[opt][1]))
                fig.add_trace(local_fig, row=count, col=1)
                count += 1
    

    fig.update_layout(paper_bgcolor = "#161B29", plot_bgcolor = "#161B29", height = max_height)

    return fig 

#-------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)



