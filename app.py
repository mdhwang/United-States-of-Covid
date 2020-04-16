# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime, timedelta

################################################################################################
############ GATHER LATEST DATA ################################################################
################################################################################################

try:
    counties_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    states_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    county_data = pd.read_csv(counties_url,dtype={"fips": str})
    state_data = pd.read_csv(states_url,dtype={"fips": str})
    print("Received latest NYT Data")
except:
    county_data = pd.read_csv('data/data/us-counties.csv')
    state_data = pd.read_csv('data/data/us-states.csv')
    print("Could not get latest NYT Data, falling back to local 4-3-20 data")
county_data = county_data.dropna()
state_data = state_data.dropna()



################################################################################################
############ START DASH APP ####################################################################
################################################################################################

BootyStrap = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

app = dash.Dash(__name__, 
                external_stylesheets=[BootyStrap],
                meta_tags=[
                    {"name": "author", "content": "Matt Hwang"}
                ]
            )

app.title = 'United States of COVID-19'

# server = app.server#
# app.config['suppress_callback_exceptions'] = True # This is to prevent app crash when loading since we have plot that only render when user clicks.

# CALCULATED VALUES

latest = county_data.query("date=='2020-04-13'")

latestDate = county_data.date.max()
latest_dt = datetime.strptime(latestDate, '%Y-%m-%d')
latest_dt_day = latest_dt.days
latest_dt_month = latest_dt.month
latest_dt_year = latest_dt.year
confirmedCases = county_data.query("date=={}".format("'"+latestDate+"'")).cases.sum()
daysOutbreak = (latest_dt - datetime.strptime('2019-12-31', '%Y-%m-%d')).days



plusConfirmedNum = 1
plusPercentNum1 = 1
plusDeathNum = 1
plusPercentNum3 = 1
deathsCases = 1




app.layout = html.Div(style={'backgroundColor': '#fafbfd'},
    children=[
            # HEADER START

            html.Div(style={'marginRight': '1.5%',},
                id="header",
                children=[
                    html.H1(
                        children="UNITED STATES OF COIVD",
                        style={
                            'textAlign': 'center',
                    }),

                    html.H4(
                        children='Dashboard tracking number of cases in the USA based on NYT published data.',
                        style={
                            'textAlign': 'center',
                            }
                    ),

                    html.Div(
                        children=[
                            html.A('NYT Github',href='https://github.com/nytimes/covid-19-data')
                        ],
                        style={
                            'textAlign': 'center',
                            }
                    ),

                    html.Hr(style={'marginTop': '.5%'},),

                    html.P(
                        id="description",
                        children=dcc.Markdown(
                        children=(
                            '''
                            On Dec 31, 2019, the World Health Organization (WHO) was informed 
                            an outbreak of “pneumonia of unknown cause” detected in Wuhan, Hubei Province, China. 
                            The virus that caused the outbreak of COVID-19 was lately known as _severe acute respiratory syndrome coronavirus 2_ (SARS-CoV-2). 
                            The WHO declared the outbreak to be a Public Health Emergency of International Concern on 
                            Jan 30, 2020 and recognized it as a pandemic on Mar 11, 2020. 
                            
                            As of **{}**, there are **{:,d}** confirmed cases in the USA.'''.format(latestDate, confirmedCases),
                        )
                        ),
                        style={
                            'textAlign': 'center',
                            }
                    ),

                    html.P(
                        id='time-stamp',
                        children="Last update: {}.".format(latestDate),
                        style={
                            'textAlign': 'center',
                            }
                        ),
                    
                    html.Hr(style={'marginTop': '.5%'},)
                    
                ]),

            # NUMBER BOARD

            html.Div(
            id="number-plate",
            style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '.8%'},
                 children=[
                     #html.Hr(),
                     html.Div(
                         style={'width': '32%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                                'marginRight': '.8%', 'verticalAlign': 'top', 
                                'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee','border-top': '#2674f6 solid .2rem',},
                              children=[
                                  html.H3(style={'textAlign': 'center',
                                                 'fontWeight': 'bold', 'color': '#2674f6'},
                                               children=[
                                                   html.P(style={'color': '#ffffff', 'padding': '.5rem'},
                                                              children='xxxx xx xxx xxxx xxx xxxxx'),
                                                   '{}'.format(daysOutbreak),
                                               ]),
                                  html.H5(style={'textAlign': 'center', 'color': '#2674f6', 'padding': '.1rem'},
                                               children="days since outbreak")
                                       ]),
                     html.Div(
                         style={'width': '32%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                                'marginRight': '.8%', 'verticalAlign': 'top', 
                                'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee','border-top': '#d7191c solid .2rem',},
                              children=[
                                  html.H3(style={'textAlign': 'center',
                                                 'fontWeight': 'bold', 'color': '#d7191c'},
                                                children=[
                                                    html.P(style={'padding': '.5rem'},
                                                              children='+ {:,d} in the past 24h ({:.1%})'.format(plusConfirmedNum, plusPercentNum1)),
                                                    '{:,d}'.format(
                                                        confirmedCases)
                                                         ]),
                                  html.H5(style={'textAlign': 'center', 'color': '#d7191c', 'padding': '.1rem'},
                                               children="confirmed cases")
                                       ]),
                     html.Div(
                         style={'width': '32%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                                'verticalAlign': 'top', 
                                'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee','border-top': '#6c6c6c solid .2rem',},
                              children=[
                                  html.H3(style={'textAlign': 'center',
                                                       'fontWeight': 'bold', 'color': '#6c6c6c'},
                                                children=[
                                                    html.P(style={'padding': '.5rem'},
                                                              children='+ {:,d} in the past 24h ({:.1%})'.format(plusDeathNum, plusPercentNum3)),
                                                    '{:,d}'.format(deathsCases)
                                                ]),
                                  html.H5(style={'textAlign': 'center', 'color': '#6c6c6c', 'padding': '.1rem'},
                                               children="death cases")
                                       ])
                          ]),

            # BODY START

            dcc.Graph(
                id='example-graph',
                figure={
                    'data': [
                        {'x': state_data.state, 'y': state_data.cases, 'type': 'bar', 'name': 'States'},
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }
            ),

            dcc.Graph(
                id='map',
                figure={
                    'data': [
                        {'x': state_data.state, 'y': state_data.cases, 'type': 'chorop', 'name': 'States'},
                    ],
                    'layout': {
                        'title': 'Dash Data Visualization'
                    }
                }
            ),

            # FOOTER START
            html.Div(
                children=[
                    html.P('This is my first Dash App - project was heavily influenced by the below repo'),
                    html.A('Perishleaf Project', href='https://github.com/Perishleaf/data-visualisation-scripts/tree/master/dash-2019-coronavirus',target='_blank'),
                ]
            )

])

if __name__ == '__main__':
    # change host from the default to '0.0.0.0' to make it publicly available
    app.server.run(port=8000, host='127.0.0.1')
    app.run_server(debug=True)