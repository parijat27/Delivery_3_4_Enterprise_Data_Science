#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import dash
dash.__version__
from dash import dcc
from dash import html
from dash.dependencies import Input, Output,State
import plotly.graph_objects as go
import os
print(os.getcwd())
df_input_large=pd.read_csv('data/processed/COVID_final_set.csv',sep=';')


fig = go.Figure()

app = dash.Dash()
app.layout = html.Div([

    dcc.Markdown('''
    # Enterprise Data Science Delivery 3
    ##  Applied Data Science on COVID-19 data
    
    The aim of this delivery is to get a better understanding of the applied data science concepts 
    which includes automated data pooling, transforming raw data into useful data, defining and applying 
    various filters for doubling rate and confirmed cases and greating a dynamic dashboard to view statistics
    of various countries.

    '''),

    dcc.Markdown('''
    ## Select countries to display the covid cases data
    '''),


    dcc.Dropdown(
        id='country_drop_down',
        options=[ {'label': each,'value':each} for each in df_input_large['country'].unique()],
        value=['US','India','Italy'],
        multi=True
    ),

    dcc.Markdown('''
        ## Select Timeline from the dropdown for confirmed COVID-19 cases or approximated doubling time of cases
        '''),

    dcc.Dropdown(
    id='doubling_time',
    options=[
        {'label': 'Confirmed cases timeline ', 'value': 'confirmed'},
        {'label': 'Confirmed filtered cases timeline', 'value': 'confirmed_filtered'},
        {'label': 'Doubling Rate timeline', 'value': 'confirmed_DR'},
        {'label': 'Doubling Rate filtered timeline', 'value': 'confirmed_filtered_DR'},
    ],
    value='confirmed',
    multi=False
    ),

    dcc.Graph(figure=fig, id='main_window_slope')
])

@app.callback(
    Output('main_window_slope', 'figure'),
    [Input('country_drop_down', 'value'),
    Input('doubling_time', 'value')])
def update_figure(country_list,show_doubling):

    if 'doubling_rate' in show_doubling:
        my_yaxis={'type':"log",
               'title':'Approximated doubling rate over 3 days (larger numbers are better #stayathome)'
              }
    else:
        my_yaxis={'type':"log",
                  'title':'Confirmed infected people (source johns hopkins csse, log-scale)'
              }


    traces = []
    for each in country_list:

        df_plot=df_input_large[df_input_large['country']==each]

        if show_doubling=='confirmed_DR':
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.mean).reset_index()
        else:
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.sum).reset_index()

        traces.append(dict(x=df_plot.date,
                                y=df_plot[show_doubling],
                                mode='markers+lines',
                                line_width = 0.5, 
                                marker_size = 0.005,
                                opacity=0.9,
                                name=each
                        )
                )

    return {
            'data': traces,
            'layout': dict (
                width=1400,
                height=600,

                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      },

                yaxis=my_yaxis
        )
    }

if __name__ == '__main__':

    app.run_server(debug=True, use_reloader=False)


# In[ ]:




