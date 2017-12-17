
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# 
# The dashboard will have two graphs: 
# 
# The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators.
# 

# In[3]:


import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


# In[4]:



eurodata = pd.read_csv("nama_10_gdp_1_Data.csv")

available_indicators = eurodata['NA_ITEM'].unique()

available_countries = eurodata['GEO'].unique()


# # Dashboard for Graph 1 and Graph 2

# In[ ]:



#app = dash.Dash()

app = dash.Dash(__name__)

server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#Creating DataFrame for the units

eurodata1 = eurodata[eurodata['UNIT'] == 'Current prices, million euro']



app.layout = html.Div([

#Graph 1    

    html.Div([
#I create the layout of the first dropdown and set the default value for my graph - Gross domestic product at market prices
        html.Div([
            dcc.Dropdown( 
# name of the x-axis is: xaxis-columns, and same for the yaxis = yaxiscolumns 

                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown( 
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries'
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),

#first graph name = graph1
    dcc.Graph(id='graph1'),

    html.Div(dcc.Slider( 
        id='year--slider',
        min=eurodata['TIME'].min(),
        max=eurodata['TIME'].max(),
        value=eurodata['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in eurodata['TIME'].unique()},
    
    ), style={'marginRight': 50, 'marginLeft': 110},),

#Second chart
    
    html.Div([
        
        html.Div([
            dcc.Dropdown( 
#
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown( 
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "Spain"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
# Second graph name is id graph2
     dcc.Graph(id='graph2'),


])

#This is the call back function for the first graph

@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])



def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):

#Dataframe for the time
    eurodataperyear = eurodata[eurodata['TIME'] == year_value]
    


    return {
        'data': [go.Scatter(
            x=eurodataperyear[eurodataperyear['NA_ITEM'] == xaxis_column_name]['Value'],
            y=eurodataperyear[eurodataperyear['NA_ITEM'] == yaxis_column_name]['Value'],
            text=eurodataperyear[eurodataperyear['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },

            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }

#This is the call back function for the second chart
@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

#As here I have all of the years I just have to update the column names of the chart

def update_graph(xaxis_column_name, yaxis_column_name):
    


    eurodataperyear = eurodata1[eurodata1['GEO'] == yaxis_column_name]
    


    return {
        'data': [go.Scatter(
            x=eurodataperyear['TIME'].unique(),
            y=eurodataperyear[eurodataperyear['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }



if __name__ == '__main__':
    app.run_server()

