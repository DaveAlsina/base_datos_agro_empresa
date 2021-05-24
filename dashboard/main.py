from connection import Connection
import queries as sql
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

conn = Connection("./conn_data.json") #datos para la conexión

#estilo de bootstrap
external_stylesheets = ["https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css"]

#instancia de Dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

##### Creación de las gráficas


### MEDICIONES

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


#### VENTAS

# Total de ingresos por cultivo
conn.openConnection()
query = pd.read_sql_query(sql.getTotalIncomeByCrop(), conn.connection)
conn.closeConnection()

dfTotalIncomebyCrop = pd.DataFrame(query, columns = ["cultivo", "ingresos_totales"])

figBarIncome1 = px.bar(dfTotalIncomebyCrop, x = "cultivo", y = "ingresos_totales",
                      text = 'ingresos_totales', color_discrete_sequence =['turquoise']*len(dfTotalIncomebyCrop))
figBarIncome1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
figBarIncome1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')


# Total en toneladas vendido por cultivo.
conn.openConnection()
query = pd.read_sql_query(sql.getTotalProdSoldByCrop(), conn.connection)
conn.closeConnection()

dfTotalProdSoldbyCrop = pd.DataFrame(query, columns = ["cultivo", "toneladas_totales"])

figBarProd1 = px.bar(dfTotalProdSoldbyCrop, x = "cultivo", y = "toneladas_totales",
                      text = 'toneladas_totales', color_discrete_sequence =['springgreen']*len(dfTotalProdSoldbyCrop))
figBarProd1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
figBarProd1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

# Serie de tiempo de las ventas

conn.openConnection()
query = pd.read_sql_query(sql.getTimeSeriesSales(), conn.connection)
conn.closeConnection()
dfTimeSeriesSales = pd.DataFrame(query, columns = ["fecha", "ingresos_totales"])
figLineIncome = px.line(dfTimeSeriesSales, x = "fecha", y = "ingresos_totales")

# Serie de tiempo de las toneladas

conn.openConnection()
query = pd.read_sql_query(sql.getTimeSeriesTons(), conn.connection)
conn.closeConnection()
dfTimeSeriesTons = pd.DataFrame(query, columns = ["fecha", "toneladas"])
figLineProd = px.line(dfTimeSeriesTons, x = "fecha", y = "toneladas")

# Ventas por zona

conn.openConnection()
query = pd.read_sql_query(sql.getSalesbyZone(), conn.connection)
conn.closeConnection()
dfSalesbyZone = pd.DataFrame(query, columns = ["zona", "ingresos_totales"])
figPie = px.pie(dfSalesbyZone, values = "ingresos_totales", names = "zona")


# Estadísticas descriptivas de los ingresos
conn.openConnection()
query = pd.read_sql_query(sql.StatIncome(), conn.connection)
conn.closeConnection()

dfStatIncome= pd.DataFrame(query, columns = ["est_des", "ventas"])
figTable = go.Figure(data=[go.Table(
    header=dict(values= dfStatIncome['est_des'],
                line_color='black',
                fill_color='lightskyblue',
                align='center'),
    cells=dict(values= dfStatIncome["ventas"],
               line_color='black',
               fill_color='lightcyan',
               align='center'))
])



#### GASTOS

# total gasto por cultivo

conn.openConnection()
query = pd.read_sql_query(sql.getTotalExpensesByCrop(), conn.connection)
conn.closeConnection()
dfTotalExpensesByCrop = pd.DataFrame(query, columns = ["cultivo", "monto_gasto"])

figBarExp = px.bar(dfTotalExpensesByCrop, x = "cultivo", y = "monto_gasto",
                      text = 'monto_gasto', color_discrete_sequence =['blue']*len(dfTotalIncomebyCrop))

figBarExp.update_traces(texttemplate='%{text:.2s}', textposition='outside')
figBarExp.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
# serie de tiempo gasto

conn.openConnection()
query = pd.read_sql_query(sql.getTimeSeriesExpenses(), conn.connection)
conn.closeConnection()
dfTimeSeriesExpenses = pd.DataFrame(query, columns = ["fecha", "monto_gasto"])

figLineExp = px.line(dfTimeSeriesExpenses, x = "fecha", y = "monto_gasto")


# gastos por categoria

conn.openConnection()
query = pd.read_sql_query(sql.getExpensesCategory(), conn.connection)
conn.closeConnection()
dfExpensesCategory = pd.DataFrame(query, columns = ["categoria", "monto_gasto"])

figPie2 = px.pie(dfExpensesCategory, values = "monto_gasto", names = "categoria")

# gastos por zona

conn.openConnection()
query = pd.read_sql_query(sql.getExpensesbyZone(), conn.connection)
conn.closeConnection()
dfExpensesbyZone = pd.DataFrame(query, columns = ["zona", "monto_gasto"])
figPie3 = px.pie(dfExpensesbyZone, values = "monto_gasto", names = "zona")

# Estadísticas descriptivas de los gastos

conn.openConnection()
query = pd.read_sql_query(sql.StatExpenses(), conn.connection)
conn.closeConnection()

dfStatExpenses= pd.DataFrame(query, columns = ["est_des", "gastos"])
figTable2 = go.Figure(data=[go.Table(
    header=dict(values= dfStatExpenses['est_des'],
                line_color='black',
                fill_color='lightskyblue',
                align='center'),
    cells=dict(values= dfStatExpenses["gastos"],
               line_color='black',
               fill_color='lightcyan',
               align='center'))
])


#### VENTAS VS GASTOS

conn.openConnection()
query = pd.read_sql_query(sql.getTotalSalesExpenses(), conn.connection)
conn.closeConnection()
dfTotalSalesExpenses = pd.DataFrame(query, columns = ["tipo", "total"])

figBar22 = px.bar(dfTotalSalesExpenses, x = "tipo", y = "total",
                      text = 'total', color_discrete_sequence =['orange']*len(dfTotalIncomebyCrop))

figBar22.update_traces(texttemplate='%{text:.2s}', textposition='outside')
figBar22.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')


### produccion

## prod por cultivo

conn.openConnection()
query = pd.read_sql_query(sql.getProdByCrop(), conn.connection)
conn.closeConnection()
dfProdByCrop = pd.DataFrame(query, columns = ["cultivo", "produccion_toneladas"])

figBarProd3 = px.bar(dfProdByCrop, x = "cultivo", y = "produccion_toneladas",
                      text = 'produccion_toneladas', color_discrete_sequence =['blue']*len(dfTotalIncomebyCrop))

figBarProd3.update_traces(texttemplate='%{text:.2s}', textposition='outside')
figBarProd3.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')


## hectareas cosechadas por cultivo

conn.openConnection()
query = pd.read_sql_query(sql.getHaByCrop(), conn.connection)
conn.closeConnection()
dfHaByCrop= pd.DataFrame(query, columns = ["cultivo", "hectareas_cosechadas"])

figBarProd4 = px.bar(dfHaByCrop, x = "cultivo", y = "hectareas_cosechadas",
                      text = 'hectareas_cosechadas', color_discrete_sequence =['blue']*len(dfTotalIncomebyCrop))

figBarProd4.update_traces(texttemplate='%{text:.2s}', textposition='outside')
figBarProd4.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')


## Rendimiento lechuga

conn.openConnection()
query = pd.read_sql_query(sql.RendLechuga(), conn.connection)
conn.closeConnection()
dfRendLechuga = pd.DataFrame(query, columns = ["fecha", "rendimiento_lechuga"])

figLine3 = px.line(dfRendLechuga, x = "fecha", y = "rendimiento_lechuga")


## Rendimiento cilantro

conn.openConnection()
query = pd.read_sql_query(sql.RendCilantro(), conn.connection)
conn.closeConnection()
dfRendCilantro = pd.DataFrame(query, columns = ["fecha", "rendimiento_cilantro"])

figLine4 = px.line(dfRendCilantro, x = "fecha", y = "rendimiento_cilantro")

## prod por zona

conn.openConnection()
query = pd.read_sql_query(sql.ProdByZone(), conn.connection)
conn.closeConnection()
dfProdByZone = pd.DataFrame(query, columns = ["zona", "produccion_toneladas"])
figPie4 = px.pie(dfProdByZone, values = "produccion_toneladas", names = "zona")

## PROD VS VENTAS

conn.openConnection()
query = pd.read_sql_query(sql.ProdVsSales(), conn.connection)
conn.closeConnection()

dfProdVsSales = pd.DataFrame(query, columns = ["cultivo", "produccion_toneladas", "toneladas_vendidas", "perdidas"])

fig123 = go.Figure()
fig123.add_trace(go.Bar(x=dfProdVsSales["cultivo"], y=dfProdVsSales["produccion_toneladas"],
                marker_color='green',
                name='produccion_toneladas'))
fig123.add_trace(go.Bar(x=dfProdVsSales["cultivo"], y=dfProdVsSales["toneladas_vendidas"],
                marker_color='blue',
                name='toneladas_vendidas'
                ))
fig123.add_trace(go.Bar(x=dfProdVsSales["cultivo"], y=dfProdVsSales["perdidas"],
                marker_color='crimson',
                name='perdidas'
                ))
##### CONFIGURACIONES PREVIAS DE PÁGINAS


### SIDEBAR

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Contenido", className="display-6"),
        html.Hr(),
        html.P(
            "Agro-empresa", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Principal", href="/", active="exact"),
                dbc.NavLink("Mediciones", href="/page-1", active="exact"),
                dbc.NavLink("Ventas", href="/page-2", active="exact"),
                dbc.NavLink("Gastos", href="/page-3", active="exact"),
                dbc.NavLink("Ventas vs Gastos", href="/page-4", active="exact"),
                dbc.NavLink("Produccion", href="/page-5", active="exact"),
                dbc.NavLink("Ventas vs Produccion", href="/page-6", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
        
content = html.Div(id="page-content", style=CONTENT_STYLE)

    
### LAYOUT

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


page_mediciones_layout = html.Div([

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
        html.Div(className = "row mt-4", children = []),

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


page_ventas_layout = html.Div(children = [
        html.H1(children = 'Análisis de Ventas', className = 'text-center'),
        html.Div(className = "container-fluid", children =[
                
                html.Div(className= "row mt-4", children=[
                      html.Div(className= "col-12 col-xl-6", children=[
                          html.Div(className = "card border", children=[
                              html.Div(className = "card-header bg-success text-light", children =[
                                      html.H3(children = "Ingresos totales por Cultivo"),
                                      ]),
                              html.Div(className = "card-body", children=[
                                      dcc.Graph(
                                              id = "barI1",
                                              figure = figBarIncome1
                                              ),
                                      ]),
                                ]),
                            ]),
                      html.Div(className= "col-12 col-xl-6", children=[
                          html.Div(className = "card border", children=[
                              html.Div(className = "card-header bg-success text-light", children =[
                                      html.H3(children = "Toneladas vendidas por Cultivo"),
                                      ]),
                              html.Div(className = "card-body", children=[
                                      dcc.Graph(
                                              id = "barProd1",
                                              figure = figBarProd1
                                              ),
                                      ]),
                                ]),
                            ]),
            
                        ]),
                
  
                html.Div(className= "row mt-4", children=[
                      html.Div(className="col-12 col-xl-6", children=[
                              html.Div(className = "card text-black bg-light mb-3", children=[
                                      dbc.Card([
                                              dbc.CardHeader("  "),
                                              dbc.CardBody([
                                                       html.P("Se puede observar en el gráfico de Ingresos totales \
                                                              por Cultivo, que las ganancias del cultivo de lechuga \
                                                              fueron superiores a las ganancias del cultivo de cilantro. \
                                                              Asimismo, en las toneladas vendidas por cultivo, el cultivo \
                                                              con mayor ventas en toneladas fue lechuga.")
                                                      ]),
                                              ]
                                             )
                                     
                                      ]),
                              ]),
                      html.Div(className= "col-12 col-xl-6", children=[
                          html.Div(className = "card border", children=[
                              html.Div(className = "card-header bg-success text-light", children =[
                                      html.H3(children = "Ventas"),
                                      ]),
                              html.Div(className = "card-body", children=[
                                      dcc.Graph(
                                              id = "LineIncome",
                                              figure = figLineIncome
                                              ),
                                      ]),
                                ]),
                            ]),
            
                        ]), ## segunda fila
                 html.Div(className= "row mt-4", children=[
                      html.Div(className= "col-12 col-xl-6", children=[
                          html.Div(className = "card border", children=[
                              html.Div(className = "card-header bg-success text-light", children =[
                                      html.H3(children = "Toneladas Vendidas"),
                                      ]),
                              html.Div(className = "card-body", children=[
                                      dcc.Graph(
                                              id = "LineProd",
                                              figure = figLineProd
                                              ),
                                      ]),
                                ]),
                            ]),
                       html.Div(className="col-12 col-xl-6", children=[
                              html.Div(className = "card text-black bg-light mb-3", children=[
                                      html.P("Se puede observar en el gráfico de Ingresos totales por Cultivo que las ganancias del cultivo de lechuga fueron superiores a las ganancias del cultivo de cilantro.")
                                      ]),
                              ]),                                  
                                     
                        ]), ## tercera fila
            
                 html.Div(className= "row mt-4", children=[
                      html.Div(className= "col-12 col-xl-6", children=[
                          html.Div(className = "card border", children=[
                              html.Div(className = "card-header bg-success text-light", children =[
                                      html.H3(children = "Ingresos por Zona"),
                                      ]),
                              html.Div(className = "card-body", children=[
                                      dcc.Graph(
                                              id = "PieIncome",
                                              figure = figPie
                                              ),
                                      ]),
                                ]),
                            ]),
                      html.Div(className= "col-12 col-xl-6", children=[
                          html.Div(className = "card border", children=[
                              html.Div(className = "card-header bg-success text-light", children =[
                                      html.H3(children = "Estadísticas Descriptivas"),
                                      ]),
                              html.Div(className = "card-body", children=[
                                      dcc.Graph(
                                              id = "Table1",
                                              figure = figTable
                                              ),
                                      ]),
                                ]),
                            ]),

                ]),
            
            #.------------------------------------------
            ]),
        
        ])

                                      
page_gastos_layout = html.Div(children = [
        html.H1(children = 'Análisis de Gastos', className = 'text-center'),
        html.Div(className = "container-fluid", children =[
                
                html.Div(className="row mt-4", children=[
                        html.Div(className="col-12 col-xl-6", children=[ ##grid division bootstrap
                                html.Div(className="card border", children=[
                                        html.Div(className="card-header bg-success text-light", children=[
                                                html.H3(children="Gastos totales por Cultivo"),
                        
                        ]),
                        html.Div(className = "card-body", children = [
                                dcc.Graph(
                                        id = 'barExp1',
                                        figure = figBarExp
                                        ),
                                ]),
                            ]),
                        ]),
                                        
                    html.Div(className="col-12 col-xl-6", children=[
                        html.Div(className="card border", children=[
                                html.Div(className="card-header bg-success text-light", children=[
                                        html.H3(children="Gastos"),
                                ]),
                                html.Div(className="card-body", children=[
                                        dcc.Graph(
                                                id = "LineExp",
                                                figure = figLineExp
                                        ),
                                ]),
                            ]),
                        ]),
                    ]), ## primera linea
                                                
                html.Div(className="row mt-4", children=[
                        html.Div(className="col-12 col-xl-6", children=[ ##grid division bootstrap
                                html.Div(className="card border", children=[
                                        html.Div(className="card-header bg-success text-light", children=[
                                                html.H3(children="Gastos por categoría"),
                        
                        ]),
                        html.Div(className = "card-body", children = [
                                dcc.Graph(
                                        id = 'pie2',
                                        figure = figPie2
                                        ),
                                ]),
                            ]),
                        ]),
                                        
                    html.Div(className="col-12 col-xl-6", children=[
                        html.Div(className="card border", children=[
                                html.Div(className="card-header bg-success text-light", children=[
                                        html.H3(children="Gastos por zona"),
                                ]),
                                html.Div(className="pie3", children=[
                                        dcc.Graph(
                                                id = "LineExp",
                                                figure = figPie3
                                        ),
                                ]),
                            ]),
                        ]),
                    ]), ## primera linea

                html.Div(className="row mt-4", children=[
                        html.Div(className="col-12 col-xl-6", children=[ ##grid division bootstrap
                                html.Div(className="card border", children=[
                                        html.Div(className="card-header bg-success text-light", children=[
                                                html.H3(children="Estadísticas Descriptivas"),
                        
                        ]),
                        html.Div(className = "card-body", children = [
                                dcc.Graph(
                                        id = 'table2',
                                        figure = figTable2
                                        ),
                                ]),
                            ]),
                        ]),
                                        
                    html.Div(className="col-12 col-xl-6", children=[
                        html.Div(className="card border", children=[

                            ]),
                        ]),
                    ]), ## primera linea

                                                
        #----------------------------------------
                ]),
            ])
                            
page_ventasVSgastos_layout = html.Div(children = [
        html.H1(children = 'Ventas vs Gastos', className = 'text-center'),
        html.Div(className = "container-fluid", children =[
                
                html.Div(className="row mt-4", children=[
                        html.Div(className="col-12 col-xl-6", children=[ ##grid division bootstrap
                                html.Div(className="card border", children=[
                                        html.Div(className="card-header bg-success text-light", children=[
                                                html.H3(children="Comparación: Ventas vs Gastos"),
                        
                        ]),
                        html.Div(className = "card-body", children = [
                                dcc.Graph(
                                        id = 'bar22',
                                        figure = figBar22
                                        ),
                                ]),
                            ]),
                        ]),
                                        
                    html.Div(className="col-12 col-xl-6", children=[
                        html.Div(className="card border", children=[

                            ]),
                        ]),
                    ]), ## 
                ]),
            ]), ## 
        
        
page_prod_layout = html.Div(children = [
        html.H1(children = 'Análsis de Producción', className = 'text-center'),
        html.Div(className = "container-fluid", children =[
                
                html.Div(className="row mt-4", children=[
                        html.Div(className="col-12 col-xl-6", children=[ ##grid division bootstrap
                                html.Div(className="card border", children=[
                                        html.Div(className="card-header bg-success text-light", children=[
                                                html.H3(children="Producción por Cultivo"),
                        
                        ]),
                        html.Div(className = "card-body", children = [
                                dcc.Graph(
                                        id = 'barProd2',
                                        figure = figBarProd3
                                        ),
                                ]),
                            ]),
                        ]),
                                        
                    html.Div(className="col-12 col-xl-6", children=[
                        html.Div(className="card border", children=[
                                html.Div(className="card-header bg-success text-light", children=[
                                        html.H3(children="Hectareas cosechadas por Cultivo"),
                                ]),
                                html.Div(className="card-body", children=[
                                        dcc.Graph(
                                                id = "barProd3",
                                                figure = figBarProd4
                                        ),
                                ]),
                            ]),
                        ]),
                    ]), ## primera linea
                                                
                html.Div(className="row mt-4", children=[
                        html.Div(className="col-12 col-xl-6", children=[ ##grid division bootstrap
                                html.Div(className="card border", children=[
                                        html.Div(className="card-header bg-success text-light", children=[
                                                html.H3(children="Rendimiento del Cultivo Lechuga"),
                        
                        ]),
                        html.Div(className = "card-body", children = [
                                dcc.Graph(
                                        id = 'line3',
                                        figure = figLine3
                                        ),
                                ]),
                            ]),
                        ]),
                                        
                    html.Div(className="col-12 col-xl-6", children=[
                        html.Div(className="card border", children=[
                                html.Div(className="card-header bg-success text-light", children=[
                                        html.H3(children="Rendimiento del Cultivo Cilantro"),
                                ]),
                                html.Div(className="pie3", children=[
                                        dcc.Graph(
                                                id = "line3",
                                                figure = figLine4
                                        ),
                                ]),
                            ]),
                        ]),
                    ]), ## primera linea

                html.Div(className="row mt-4", children=[
                        html.Div(className="col-12 col-xl-6", children=[ ##grid division bootstrap
                                html.Div(className="card border", children=[
                                        html.Div(className="card-header bg-success text-light", children=[
                                                html.H3(children="Producción por Zona"),
                        
                        ]),
                        html.Div(className = "card-body", children = [
                                dcc.Graph(
                                        id = 'pie4',
                                        figure = figPie4
                                        ),
                                ]),
                            ]),
                        ]),
                                        
                    html.Div(className="col-12 col-xl-6", children=[
                        html.Div(className="card border", children=[

                            ]),
                        ]),
                    ]), ## primera linea

                                                
        #----------------------------------------
                ]),
            ])
        
page_prodVSventas_layout = html.Div(children = [
        html.H1(children = 'Producción vs Gastos', className = 'text-center'),
        html.Div(className = "container-fluid", children =[
                
                html.Div(className="row mt-4", children=[
                        html.Div(className="col-12 col-xl-6", children=[ ##grid division bootstrap
                                html.Div(className="card border", children=[
                                        html.Div(className="card-header bg-success text-light", children=[
                                                html.H3(children="Comparación: Producción vs Ventas"),
                        
                        ]),
                        html.Div(className = "card-body", children = [
                                dcc.Graph(
                                        id = 'bar123',
                                        figure = fig123
                                        ),
                                ]),
                            ]),
                        ]),
                                        
                    html.Div(className="col-12 col-xl-6", children=[
                        html.Div(className="card border", children=[

                            ]),
                        ]),
                    ]), ## 
                ]),
            ]), ## 
                
                
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

#callback para poner como valor de fecha de cultivo 
#a None para evitar bugs
@app.callback(
    dash.dependencies.Output(component_id = 'opts_fechas_crop', component_property='value'),
    [dash.dependencies.Input(component_id = 'opciones_crop_meas_disp', component_property='value'),]
)

def crop_date_gui_restriction_value(crop_name):

    print("check para setear a None selección de fechas de cultivos en caso de que se borre crop_name, se recibió: ", crop_name)

    if crop_name == None:
        return None 
    

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

def show_hide_measure_grap2(crop_name, date):
    
    print("check para ocultar gráfica, se recibió: ", crop_name, date)
    print()

    if ((crop_name == None) or (date == None) ):
        return True

    else:
        return False
        
                    
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("Hola bb")
    
    elif pathname == "/page-1":
        return page_mediciones_layout
    
    elif pathname == "/page-2":
        return page_ventas_layout
    
    elif pathname == "/page-3":
        return page_gastos_layout

    elif pathname == "/page-4":
        return page_ventasVSgastos_layout

    elif pathname == "/page-5":
        return page_prod_layout

    elif pathname == "/page-6":
        return page_prodVSventas_layout
    
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


       
if __name__ == '__main__':
    app.run_server(debug = True)

