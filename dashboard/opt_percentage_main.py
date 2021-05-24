from connection import Connection
import queries as sql

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

conn = Connection("./conn_data.json") #datos para la conexión

#estilo de bootstrap
external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"]

#instancia de Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#obtiene las opciones de qué cultivos poseen datos de sensores
#para crear con esto un menú de selección en la interfaz
conn.openConnection()
measurementSelectionMenu = pd.read_sql_query(sql.createMeasurement_selection_menu(), conn.connection)
conn.closeConnection()

#sección de creación de variables para display en la interfaz

#menú de que cultivos poseen mediciones 
options_crop_measurement_display = []

for cropname in measurementSelectionMenu['crop_name']:
    local_dict = {}
    local_dict['label'] = cropname
    local_dict['value'] = cropname
    
    options_crop_measurement_display.append(local_dict)


#LAYOUT

app.layout = html.Div([

    html.Div(
    children = [

        html.H1(children = 'Visualización de variables ambientales', className = 'text-center'),
        html.Div(className = "center row mt-4"),

        html.Div(className = 'card text-center', children = [
                html.Div(className = 'card-header', children = [
                        html.H4(children = "Resumen"),
                    ]),
                html.Div(className = 'card-body', children = [
                       html.P(children = ["En esta sección se presentan las variables ambientales de un cultivo particular que tu seleccionas"
                           ]),

                       html.P(children = ["así como un análisis de las condiciones ambientales y su optimalidad para tus plantaciones seleccionadas."
                           ]),
                            
                    ]),
            ]),

        html.Div(className = "center row mt-4"),

        html.Div(
            className = "center row mt-4",
            children = [
            
                #dropdown menú para seleccionar de qué cultivo se quieren ver y analizar los datos

                html.Div(
                    className = "col-12 col-xl-6",
                    children = [
                        html.Div(className = "card-border",
                            children = [
                            html.Div(children="Selección de cultivo", className="card-header bg-success text-light"),

                        
                            html.Div(className = "menu", children = [
                                    dcc.Dropdown(
                                        id = "opciones_crop_meas_disp",
                                        options = options_crop_measurement_display ,
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
                                    html.Div(children = "Selección de fecha de cultivo", className="card-header bg-success text-light"),
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
            html.Div(children = "Selección de variables ambientales", className = "card-header bg-success text-center text-light"),
                dcc.Dropdown(
                    id = 'opciones_measure',
                    options = [
                            {'label': 'Temperatura', 'value': 'temperature'},
                            {'label': 'Humedad', 'value': 'humidity'},
                            {'label': 'Presión Atmosférica', 'value': 'pressure'},
                            {'label': 'Luz', 'value': 'lux'},
                            {'label': 'Electroconductividad', 'value': 'electroconductivity'}
                        ],
                        value = ['humidity', 'temperature', 'pressure', 'lux', 'electroconductivity'],
                        placeholder = "Seleccione una variable",
                        multi = True,
                ),
        ]),

    #grafico de mediciones de sensor para las variables seleccionadas por el usuario
    html.Div([
        dcc.Graph(id = 'grafico_variables_amb', animate=True)
    ], id = 'grafico_form_variables_amb'),
    
    ],className = "body"),

        html.Div(id = "optimum_cond_plot", children = [
            
                html.H1(children = 'Análisis de condiciones óptimas', className = 'text-center'),
                html.Div(className = "container-fluid", children =[ #DESDE AQUÍ                
                html.Div(className = "card-body", children = [
                                    dcc.Graph(
                                            id = 'grafico_opt',
                                            ),
                                    ]),
         #html.Footer(className = "text-muted text-center", children = "")
             ]),
         ]),

],className = "bg-light")



#callback para cambiar las opciones de que fechas escoger en función del nombre 
#de cultivo que ha seleccionado el usuario
@app.callback(
    dash.dependencies.Output(component_id = 'opts_fechas_crop', component_property='options'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value')]
)

def display_date_opts(crop_name):
    
    if crop_name != None:   #en caso de que se haya seleccionado un nombre de cultivo

        opt_data = []

        #toma las tuplas del dataframe que tienen el nombre del cultivo 
        #que el usuario ha seleccionado
        dates_for_crop = measurementSelectionMenu[ measurementSelectionMenu['crop_name'] == crop_name]

        for date in dates_for_crop['date_']:            #crea la lista de diccionarios de opciones 
            local_dict = {}                             #para actualizar en la gui
            local_dict['label'] = date
            local_dict['value'] = date
            
            opt_data.append(local_dict)

        return opt_data

    else: 

        #en caso de que se rompa la funcionalidad aunque es muy poco posible
        return [{'label' : 'No hay opciones disponibles', 'value' : 0}]


#callback para blockear la selección de qué fechas buscar
#si no se especifica de cuál es el cultivo seleccionado
@app.callback(
    dash.dependencies.Output(component_id = 'opts_fechas_crop', component_property='disabled'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value')]
)

def crop_date_gui_restriction(value):

    print("check para bloquear selección de fechas de cultivos, se recibió: ", value)

    if value == None:
        return True
    
    return False 

#callback para poner como valor de fecha de cultivo 
#a None para evitar bugs
@app.callback(
    dash.dependencies.Output(component_id = 'opts_fechas_crop', component_property='value'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value'),
     dash.dependencies.Input(component_id = 'opts_fechas_crop', component_property='value')   
        ]
)

def crop_date_gui_restriction_value(crop_name, date):

    print("check para setear a None selección de fechas de cultivos en caso de que se borre crop_name, se recibió: ", crop_name, date)

    if crop_name == None:
        return None 
    
    return date 

#callback para blockear la selección de qué condicion ambiental buscar
#si no se especifica de qué cultivo se va a buscar y en qué fecha
@app.callback(
    dash.dependencies.Output(component_id = 'opciones_measure', component_property='disabled'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value'),
    dash.dependencies.Input(component_id = 'opts_fechas_crop', component_property='value')]
)

def crop_name_gui_restriction(crop_name, date):

    print("check para bloquear el menú de selección de variables ambientales, se recibió: ", crop_name, date)

    if ((crop_name  == None) or (date == None)):
        return True
    
    return False 


#callback para ocultar la figura en donde se representan
#todas las variables ambientales ploteadas que pidió el usuario
@app.callback(
    dash.dependencies.Output(component_id = 'grafico_form_variables_amb', component_property='hidden'),
    [dash.dependencies.Input(component_id = 'opciones_measure', component_property='value'),
    dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value'),
    dash.dependencies.Input(component_id = 'opts_fechas_crop', component_property='value')]
)

def show_hide_measure_grap(op_elegidas, crop_name, date):
    
    print("check para ocultar gráfica, se recibió: ",op_elegidas, crop_name, date)
    print()

    if ( (op_elegidas == []) or (crop_name == None) or (date == None) ):
        return True

    else:
        return False
 

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
    row_counter = len(op_elegidas)      #cantidad de variables a plotear

    #estos ifs son para ajustar de una mejor forma el tamaño en altura
    #de la gráfica en función de qué tantas variables debe contener la gráfica
    if row_counter > 3:
        max_height = 650

    elif row_counter != 1:
        max_height = 525

    else:
        max_height = 275
    
    if ( (op_elegidas == []) or (crop_name == None) or (date == None) ):

        print("Aún no se puede crear una gráfica de variables ambientales de cultivos, faltan argumentos")

    else:

        #calculo de la altura individual de cada subplot para cada variable
        individual_height = int(max_height/row_counter)

        #query para realizar el plot
        conn.openConnection()
        measure = pd.read_sql_query(sql.getMeasurements(crop_name, date), conn.connection)
        conn.closeConnection()

#        print(measure)

        #diccionario con las opciones de estilo en función del nombre de variable ambiental que metió el usuario
        opts = {'humidity': ('Humedad', '#4b69ed'), 
                'temperature' :('Temperatura', '#ff4340'),
                'pressure': ('Presión Atm.' ,'#6CD1DB'),
                'lux': ('Lux','#eed04d'),
                'electroconductivity': ('Electroconductividad', '#54AB2F')
                }


        if (row_counter == 1):
            
            local_fig = go.Scatter(x = list(measure["time_"]), y = list(measure[op_elegidas[0]]), 
                        mode = 'lines', name = opts[op_elegidas[0]][0], 
                        marker = dict(color = opts[op_elegidas[0]][1]))
            fig.add_trace(local_fig)

            fig.update_layout(title = opts[ op_elegidas[0] ][0])

        elif (row_counter > 1):

            #hace tantas filas de subplots como variables se le hayan pedido graficar, 
            #y les setea el tamaño en altura que cada plot debe tener
            fig = make_subplots(rows = row_counter, cols = 1, shared_xaxes = False, vertical_spacing = 0.1,
                                row_heights = [ individual_height for i in op_elegidas])
            
            #contador para el número de fila del subplot
            count = 1

            for opt in op_elegidas:

                local_fig = go.Scatter(x = list(measure["time_"]), y = list(measure[opt]), 
                        mode = 'lines', name=opts[opt][0], marker = dict(color=opts[opt][1]))
                fig.add_trace(local_fig, row=count, col=1)
                count += 1
    

    #fig.update_layout(paper_bgcolor = "#161B29", plot_bgcolor = "#161B29", height = max_height)
    fig.update_layout(paper_bgcolor = "#e4e8ee", plot_bgcolor = "#e4e8ee", height = max_height)

    return fig 


@app.callback(
    dash.dependencies.Output(component_id = 'grafico_opt', component_property='figure'),
    [dash.dependencies.Input(component_id = 'opciones_measure', component_property='value'),
    dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value'),
    dash.dependencies.Input(component_id = 'opts_fechas_crop', component_property='value')]
)

def crear_tabla_opt(op_elegidas, crop_name, date):
    # QUERIES SIN FECHA
    conn.openConnection()
    querycon = pd.read_sql_query(sql.getMeasurements(), conn.connection)
    conn.closeConnection()

    #SE CREA LA GRÁFICA VACÍA
    figBar = go.Figure()

    if crop_name == "lechuga" and date != None:

        #QUERIES
        conn.openConnection()
        queryhumlech = pd.read_sql_query(sql.getPercHum("lechuga"), conn.connection)
        queryeclech = pd.read_sql_query(sql.getPercEc("lechuga"), conn.connection)
        querylechdia = pd.read_sql_query(sql.getPercTempD("lechuga", date), conn.connection)
        querylechnoche = pd.read_sql_query(sql.getPercTempN("lechuga", date), conn.connection)
        conn.closeConnection()

        #DATAFRAMES
        dflechugahum = pd.DataFrame(queryhumlech, columns = ["crop_name", "percentage"])
        dflechugaec = pd.DataFrame(queryeclech, columns = ["crop_name", "percentage"])
        dflechugadia = pd.DataFrame(querylechdia, columns = ["crop_name", "percentage"])
        dflechuganoche = pd.DataFrame(querylechnoche, columns = ["crop_name", "percentage"])

        #BARRAS
        figBar.add_trace(go.Bar(x = dflechugahum.crop_name, y = dflechugahum.percentage, name='Humedad'))
        figBar.add_trace(go.Bar(x = dflechugaec.crop_name, y = dflechugaec.percentage, name='Electroconductividad'))
        figBar.add_trace(go.Bar(x = dflechugadia.crop_name, y = dflechugadia.percentage, name='Temperatura - día'))
        figBar.add_trace(go.Bar(x = dflechuganoche.crop_name, y = dflechuganoche.percentage, name='Temperatura - noche'))
        

    elif crop_name == "cilantro" and date != None:

        #QUERIES
        conn.openConnection()
        queryhumcil = pd.read_sql_query(sql.getPercHum("cilantro"), conn.connection)
        queryeccil = pd.read_sql_query(sql.getPercEc("cilantro"), conn.connection)
        querycildia = pd.read_sql_query(sql.getPercTempD("cilantro", date), conn.connection)
        querycilnoche = pd.read_sql_query(sql.getPercTempN("cilantro", date), conn.connection)
        conn.closeConnection()

        #DATAFRAMES
        dfcilhum = pd.DataFrame(queryhumcil, columns = ["crop_name", "percentage"])
        dfcilec = pd.DataFrame(queryeccil, columns = ["crop_name", "percentage"])
        dfcilDia = pd.DataFrame(querycildia, columns = ["crop_name", "percentage"])
        dfcilNoche = pd.DataFrame(querycilnoche, columns = ["crop_name", "percentage"])
        
        #BARRAS
        figBar.add_trace(go.Bar(x = dfcilhum.crop_name, y=dfcilhum.percentage, name='Humedad'))
        figBar.add_trace(go.Bar(x = dfcilec.crop_name, y = dfcilec.percentage, name='Electroconductividad'))
        figBar.add_trace(go.Bar(x = dfcilDia.crop_name, y = dfcilDia.percentage, name='Temperatura - día'))
        figBar.add_trace(go.Bar(x = dfcilNoche.crop_name, y = dfcilNoche.percentage, name='Temperatura - noche'))

    return figBar

#callback para ocultar la figura en donde se representan
#los porcentajes de veces en condiciones óptimas para las 
#variables ambientales a las cuales se les puede hacer este análisis
@app.callback(
    dash.dependencies.Output(component_id = 'optimum_cond_plot', component_property='hidden'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value'),
    dash.dependencies.Input(component_id = 'opts_fechas_crop', component_property='value')]
)

def show_hide_measure_grap(crop_name, date):
    
    print("check para ocultar gráfica, se recibió: ", crop_name, date)
    print()

    if ((crop_name == None) or (date == None) ):
        return True

    else:
        return False

#-------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)

