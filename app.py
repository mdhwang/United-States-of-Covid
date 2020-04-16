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
days_since_outbreak = (latest_dt - datetime.strptime('2019-12-31', '%Y-%m-%d')).days
days_since_USA = (latest_dt - datetime.strptime('2020-01-21', '%Y-%m-%d')).days
day_prior = datetime.strftime((latest_dt - timedelta(days=1)),'%Y-%m-%d')
two_prior = datetime.strftime((latest_dt - timedelta(days=2)),'%Y-%m-%d')

confirmed_cases = county_data.query("date=={}".format("'" + latestDate + "'")).cases.sum()
cases_day_prior = county_data.query("date=={}".format("'" + day_prior + "'")).cases.sum()
cases_two_prior = county_data.query("date=={}".format("'" + two_prior + "'")).cases.sum()

case_rate = (confirmed_cases - cases_day_prior) / cases_day_prior
case_prior_rate = (cases_day_prior - cases_two_prior) / cases_two_prior
case_rate_delta = (case_rate - case_prior_rate) / case_prior_rate
if case_rate_delta < 0:
    case_rate_delta_s = '{:.2%}'.format(case_rate_delta)
else:
    case_rate_delta_s = '+ {:.2%}'.format(case_rate_delta)
    
case_delta = confirmed_cases - cases_day_prior
case_percent_diff = (case_delta) / cases_day_prior


confirmed_deaths = county_data.query("date=={}".format("'" + latestDate + "'")).deaths.sum()
death_day_prior = county_data.query("date=={}".format("'" + day_prior + "'")).deaths.sum()
death_two_prior = county_data.query("date=={}".format("'" + two_prior + "'")).deaths.sum()

death_rate = (confirmed_deaths - death_day_prior) / death_day_prior
death_prior_rate = (death_day_prior - death_two_prior) / death_two_prior
death_rate_delta = (death_rate - death_prior_rate) / death_prior_rate
if death_rate_delta < 0:
    death_rate_delta_s = '{:.2%}'.format(death_rate_delta)
else:
    death_rate_delta_s = '+ {:.2%}'.format(death_rate_delta)
    

death_delta = confirmed_deaths - death_day_prior
death_percent_diff = (death_delta) / death_day_prior



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
                            
                            As of **{}**, there are **{:,d}** confirmed cases in the USA.'''.format(latestDate, confirmed_cases),
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
                                  
                                  html.H2(style={'textAlign': 'center',
                                                 'fontWeight': 'bold', 'color': '#2674f6'},
                                               children=[
                                                   html.P(style={'color': '#2674f6', 'padding': '.5rem'},
                                                              children='Days Since Outbreak'),
                                                   '{}'.format(days_since_outbreak),
                                               ]),

                                    html.Br(),
                                    html.H4(style={'textAlign': 'center', 'fontWeight': 'bold','color': '#2674f6', 'padding': '.1rem'},
                                        children="{}".format(days_since_USA)),
                                    html.H5(style={'textAlign': 'center', 'color': '#2674f6', 'padding': '.1rem'},
                                        children="Days since first case occurance in USA".format(days_since_USA))
                                       ]),
                     html.Div(
                         style={'width': '32%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                                'marginRight': '.8%', 'verticalAlign': 'top', 
                                'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee','border-top': '#d7191c solid .2rem',},
                              children=[
                                  html.H4(style={'textAlign': 'center',
                                                 'fontWeight': 'bold', 'color': '#d7191c'},
                                                children=[
                                                    html.P(style={'padding': '.5rem'},
                                                              children='+ {:,d} cases in the past 24h ({:.2%}) increase in cases'.format(case_delta, case_percent_diff)),
                                                    html.P(style={'padding': '.5rem'},
                                                              children='({}) change in rate'.format(case_rate_delta_s)),
                                                              
                                                        '{:,d}'.format(confirmed_cases)
                                                         ]),
                                  html.H5(style={'textAlign': 'center', 'color': '#d7191c', 'padding': '.1rem'},
                                               children="confirmed cases")
                                       ]),
                     html.Div(
                         style={'width': '32%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                                'verticalAlign': 'top', 
                                'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee','border-top': '#6c6c6c solid .2rem',},
                              children=[
                                  html.H4(style={'textAlign': 'center',
                                                       'fontWeight': 'bold', 'color': '#6c6c6c'},
                                                children=[
                                                    html.P(style={'padding': '.5rem'},
                                                              children='+ {:,d} deaths in the past 24h ({:.2%}) increase in deaths'.format(death_delta, death_percent_diff)),
                                                    html.P(style={'padding': '.5rem'},
                                                              children='({}) change in rate'.format(death_rate_delta_s)),
                                                             
                                                    '{:,d}'.format(confirmed_deaths)
                                                ]),
                                  html.H5(style={'textAlign': 'center', 'color': '#6c6c6c', 'padding': '.1rem'},
                                               children="death cases")
                                       ]),
                      html.Hr(),    
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
                    html.Br(),
                    html.Br(),
                    html.Hr(),
                    html.P('This is my first Dash App - project was heavily influenced by the below repo'),
                    html.A('Perishleaf Project', href='https://github.com/Perishleaf/data-visualisation-scripts/tree/master/dash-2019-coronavirus',target='_blank'),
                ]
            )

])

if __name__ == '__main__':
    # change host from the default to '0.0.0.0' to make it publicly available
    app.server.run(port=8000, host='127.0.0.1')
    app.run_server(debug=True)