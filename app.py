
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

# In[1]:


import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


# In[2]:


#First we import the files and create the coresponding indicators for the values and the countries

euro_data = pd.read_csv("Eurostat_file.csv")

available_indicators = euro_data['NA_ITEM'].unique()

available_countries = euro_data['GEO'].unique()


# ### My Dashboard

# In[4]:


#We start with creating the app itself

#app = dash.Dash()

app = dash.Dash(__name__)

server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

#Here I create the dataframe for the units that will be used

euro_data1 = euro_data[euro_data['UNIT'] == 'Current prices, million euro']

#Now I start designing the layout of my app

app.layout = html.Div([

#Since we need to put two graphs on the same dashboard this part will be for graph 1    

    html.Div([
#I create the layout of the first dropdown and set the default value for my graph - Gross domestic product at market prices
        html.Div([
            dcc.Dropdown( 
#Note that I have given a unique axis name here xaxis-column1, as if I use the same one in both graphs 
#the dropdown will affect both graphs, I do the same for the yaxis
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),
#Here I repeat the same steps as for the x axis, but I put the default value to Wages and Salaries
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries'
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),

#I give my graph a unique name grph1 in order to be able to have both graphs on my dashboard
    dcc.Graph(id='grph1'),
#Finally I create my slider, in order to manipulate it's position I have made it as a html and with style I aligned it with 
#the graph itself
    html.Div(dcc.Slider( 
        id='year--slider',
        min=euro_data['TIME'].min(),
        max=euro_data['TIME'].max(),
        value=euro_data['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in euro_data['TIME'].unique()},
    
    ), style={'marginRight': 50, 'marginLeft': 110},),

#Here I start creating the environment for my second chart folowing the same steps as I did for my previous one with some minor
#alterations
    
    html.Div([
        
        html.Div([
            dcc.Dropdown( 
#Note how here I use xaxis-column2 as my id to prevent the dropdown from my previous graph to interact with this 
#axis and vice-versa
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),
# The bigest change from the previous chart is here, where I use available_countries as the option for my dropdown
# and I set Spain as the default value
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "Spain"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
# Finally I give my second graph a unique id graph2
     dcc.Graph(id='grph2'),


])

#Here I create the callback which updates the first graph according to the value in the fropdown boxes
#I start by setting my imputs and outputs
@app.callback(
    dash.dependencies.Output('grph1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

#Then I define the function
def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):

#I create the dataframe which will match the coresponding value with the year that is chosen
    euro_data_yearly = euro_data[euro_data['TIME'] == year_value]
#And finally I create the output, in addition to the values on the x and y axis, I add the text marker which shows the country,
#when you hover over the coresponding scatter value with the cursor
    return {
        'data': [go.Scatter(
            x=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == yaxis_column_name]['Value'],
            text=euro_data_yearly[euro_data_yearly['NA_ITEM'] == yaxis_column_name]['GEO'],
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
# I set the margins for both of the charts to be the same for a neater look of my dashboard
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }

#Here I create the call back for the second chart, starting with defining the input and output using the id's I have assigned
#to my second graph and the coresponding ones for the x and y axis
@app.callback(
    dash.dependencies.Output('grph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])
#As here I have all of the years I just have to update the column names of the chart
def update_graph(xaxis_column_name, yaxis_column_name):
#I create a dataframe which will mach the country or country group with the coresponding x axis value    
    euro_data_yearly = euro_data1[euro_data1['GEO'] == yaxis_column_name]

#Finally I create my output, using mode='lines' to create a linechart. Note that here I do not need text= as there is nothing to
#label on the chart area itself, as it will show values for only the country chosen in the dropdown
    return {
        'data': [go.Scatter(
            x=euro_data_yearly['TIME'].unique(),
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
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

#Finally I run the server for my dashboard

if __name__ == '__main__':
    app.run_server()

