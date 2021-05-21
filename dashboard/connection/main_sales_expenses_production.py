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

##### Creación de las gráficas

# Total de ingresos por cultivo
conn.openConnection()
query = pd.read_sql_query(sql.getTotalIncomeByCrop(), conn.connection)
conn.closeConnection()
dfTotalIncomebyCrop = pd.DataFrame(query, columns = ["crop", "total_income"])

figBarIncome = px.bar(dfTotalIncomebyCrop, x = "crop", y = "total_income",
                      text = 'total_income', color_discrete_sequence =['turquoise']*len(dfTotalIncomebyCrop))
figBarIncome.update_traces(texttemplate='%{text:.2s}', textposition='outside')
figBarIncome.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')


# Total en toneladas vendido por cultivo.
conn.openConnection()
query = pd.read_sql_query(sql.getTotalProdSoldByCrop(), conn.connection)
conn.closeConnection()
dfTotalProdSoldbyCrop = pd.DataFrame(query, columns = ["crop", "total_tons"])
figBarProd1 = px.bar(dfTotalProdSoldbyCrop, x = "crop", y = "total_tons",
                      text = 'total_tons', color_discrete_sequence =['springgreen']*len(dfTotalProdSoldbyCrop))
figBarProd1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
figBarProd1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')



#Layout
app.layout = html.Div(children = [
        html.H1(children = 'Sales Analysis', className = 'text-center'),
        html.Div(className = "container-fluid", children =[
                
                html.Div(className="row mt-4", children=[
                        html.Div(className="col-12 col-xl-6", children=[ ##grid division bootstrap
                                html.Div(className="card border", children=[
                                        html.Div(className="card-header bg-success text-light", children=[
                                                html.H3(children="Total Income by Crop"),
                        
                        ]),
                        html.Div(className = "card-body", children = [
                                dcc.Graph(
                                        id = 'barIncome1',
                                        figure = figBarIncome
                                        ),
                                ]),
                            ]),
                        ]),
                                        
                html.Div(className="col-12 col-xl-6", children=[
                        html.Div(className="card border", children=[
                                html.Div(className="card-header bg-success text-light", children=[
                                        html.H3(children="Total Production Sold by Crop"),
                                ]),
                                html.Div(className="card-body", children=[
                                        dcc.Graph(
                                                id = "barProd1",
                                                figure = figBarProd1
                                        ),
                                ]),
                            ]),
                        ]),
                    ]), ## cerrar pareja
        html.Footer(className = "text-muted text-center", children = "Alejandra")
            ]),
        ])
    
        
if __name__ == '__main__':
    app.run_server(debug = True)

