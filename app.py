# -*- coding: utf-8 -*-
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import json
geo_json_path = 'data/geo_data/geojson-counties-fips.json'
with open(geo_json_path,'r') as response:
    counties = json.load(response)


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
    county_data = pd.read_csv('data/data/us-counties.csv',dtype={"fips": str})
    state_data = pd.read_csv('data/data/us-states.csv',dtype={"fips": str})
    print("Could not get latest NYT Data, falling back to local 4-3-20 data")
county_data = county_data.dropna()
state_data = state_data.dropna()


# CALCULATED VALUES

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

latest = county_data.query("date=={}".format("'" + latestDate + "'"))


total = state_data.groupby(state_data.date).sum()
difference = total.diff()
difference = difference.fillna(0)
difference.columns = ['case_increase','death_increase']
new = total.merge(difference, left_index=True, right_index=True)

#Table Summary Data
latest_state_data = state_data.query("date=={}".format("'" + latestDate + "'"))
sum_cols = ['state','cases','deaths']
state_summary = latest_state_data[sum_cols].copy()
state_summary.index = latest_state_data.state

cols = ['state','county','cases','deaths']
county_summary = latest[cols].copy()

################################################################################################
############ GENERATE PLOTS  ###################################################################
################################################################################################

max_cases = latest.cases.max()

fig_map = (px.choropleth_mapbox(latest, geojson=counties, locations='fips', color='cases',
                           color_continuous_scale="matter",
                           range_color=(0, max_cases),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=1,
                           labels={'state':'state',
                                'county':'county',
                                'cases':'cases',
                                'deaths':'deaths'}, 
                          ))
fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



# Cumulative Chart
fig_combo = go.Figure()

fig_combo.add_trace(go.Scatter(x=total.index, y=total.cases,
                    mode='lines+markers',
                               name='Total Cases USA',
                         marker=dict(size=2, color='#d7191c',
                                            line=dict(width=.5, color='#e36209')),
                                hovertext=['Total Cases<br>{:,d}<br>'.format(
                                    i) for i in total.cases],
                                hovertemplate='%{hovertext}' + '<extra></extra>'    
                        ))

fig_combo.add_trace(go.Scatter(x=total.index, y=total.deaths,
                    mode='lines+markers',
                               name = 'Total Deaths USA',
                         marker=dict(size=2, color='#626262',
                                            line=dict(width=.5, color='#626262')),
                                hovertext=['Total Deaths<br>{:,d}<br>'.format(
                                    i) for i in total.deaths],
                                hovertemplate='%{hovertext}' + '<extra></extra>' 
                              ))
fig_combo.update_layout(
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis=dict(
        showline=False, linecolor='#272e3e',
        zeroline=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
    ),
    xaxis=dict(
        showline=False, linecolor='#272e3e',
        showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode='x unified',
    legend_orientation="h",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
)

# Daily Increase Chart

fig_daily = go.Figure()

fig_daily.add_trace(go.Scatter(x=new.index, y=new.case_increase,
                    mode='lines+markers',
                    name='New Cases USA',
                    marker=dict(size=2, color='#d7191c',
                                line=dict(width=.5, color='#e36209')),
                    hovertext=['New Cases<br>{:,d}<br>'.format(
                                int(i)) for i in new.case_increase],
                    hovertemplate='%{hovertext}' + '<extra></extra>' 
                        
                        
                        
                        ))

fig_daily.add_trace(go.Scatter(x=new.index, y=new.death_increase,
                    mode='lines+markers',
                               name = 'New Deaths USA',
                         marker=dict(size=2, color='#626262',
                                            line=dict(width=.5, color='#626262')),
                                text=total.index,
                                hovertext=['New Deaths<br>{:,d}<br>'.format(
                                    int(i)) for i in new.death_increase],
                                hovertemplate='%{hovertext}' + '<extra></extra>' 
                              ))
fig_daily.update_layout(
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis=dict(
        showline=False, linecolor='#272e3e',
        zeroline=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
    ),
#    yaxis_title="Total Confirmed Case Number",
    xaxis=dict(
        showline=False, linecolor='#272e3e',
        showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode='x unified',
    legend_orientation="h",
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
)


census = pd.read_csv('data/co-est2019-alldata.csv',encoding = 'latin-1',dtype={"STATE": str,"COUNTY":str})
census = census.query('COUNTY!="000"')
census["fips"] = census.STATE + census.COUNTY
pop = census[['POPESTIMATE2019']].copy()
pop.columns = ['Population']
pop.index = census.fips
county_pop = pop.to_dict()

county_data = county_data.merge(pop, how='inner',on='fips')

county_data['percent_pop'] = round(10*county_data.cases/county_data.Population,2)
latest2 = county_data.query("date=={}".format("'" + latestDate + "'"))
top = latest2.percent_pop.max()


fig_pop = px.choropleth_mapbox(latest2, geojson=counties, locations='fips', color='percent_pop',
                           color_continuous_scale="matter",
                           range_color=(0,top),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=1,
                          )
fig_pop.update_layout(margin={"r":0,"t":0,"l":0,"b":0})



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
server = app.server

# app.config['suppress_callback_exceptions'] = True # This is to prevent app crash when loading since we have plot that only render when user clicks.



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
            style={'textAlign': 'center','marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '.8%'},
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

            html.Div(
            id='dcc-map',
            style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'backgroundColor': '#ffffff',
                   'marginBottom': '.8%', 'marginTop': '.5%',
                   'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'
                },
                 children=[
                     html.Div(
                         style={'width': '97%', 'display': 'inline-block',
                                },
                         children=[
                                  html.H2(
                                    style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                           'color': '#292929', 'padding': '0.5rem', 'marginBottom': '0','marginTop': '0'},
                                    children='Percentage of Population Infected Per County'),
                                  html.H4(
                                    style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                           'color': '#292929', 'padding': '0.5rem', 'marginBottom': '0','marginTop': '0'},
                                    children='''Calculated percent of population per county based on latest confirmed cases 
                                                over estimated population based on 2019 US Census data.'''),
                                  html.Hr(),
                                  dcc.Graph(
                                    style={'height': '600px'}, 
                                    figure=fig_pop),
                                  ]),
                 ]),

            html.Div(
            id='dcc-plot',
            style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'backgroundColor': '#ffffff',
                   'marginBottom': '.8%', 'marginTop': '.5%',
                   'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'
                },
                 children=[
                    html.H2(
                        style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                'color': '#292929', 'paddingTop': '1rem', 'marginBottom': '0','marginTop': '0'},
                        children='COVID Case and Death Trend Timeline'),
                    html.Hr(),
                     html.Div(
                         style={'width': '49.18%', 'display': 'inline-block',
                                'marginRight': '.8%', 
                                },
                         children=[
                                  html.H4(
                                    id='dcc-num-graph-head',
                                    style={'textAlign': 'center', 'text-decoration': 'underline','backgroundColor': '#ffffff',
                                           'color': '#292929', 'padding': '1rem', 'marginBottom': '0','marginTop': '0'},
                                    children='Cases / Deaths USA'),
                                  dcc.Graph(
                                    style={'height': '300px'}, 
                                    figure=fig_combo),
                                    dbc.Tooltip(
                                    '''
                                    This chart represents the cumulative number of cases and deaths reported in the USA due to COVID-19.
                                    ''',
                                              target='dcc-num-graph-head',
                                              style={"font-size":"1em"},
                                             ),
                                  ]),
                     html.Div(
                         style={'width': '49.18%', 'display': 'inline-block',},
                         children=[
                                  html.H4(
                                    id='dcc-rate-graph-head',
                                    style={'textAlign': 'center', 'backgroundColor': '#ffffff','text-decoration': 'underline',
                                           'color': '#292929', 'padding': '.1rem', 'marginBottom': '0','marginTop': '0'},
                                    children='Daily Increases USA'),
                                  dcc.Graph(
                                    style={'height': '300px'}, 
                                    figure=fig_daily),
                                  dbc.Tooltip(
                                    '''
                                    This chart represents the daily number of increases in cases and deaths reported in the USA due to COVID-19.
                                    ''',
                                              target='dcc-rate-graph-head',
                                              style={"font-size":"1em"},
                                             ),
                                  ]),
                     ]),

            html.Div(
            id='dcc-map2',
            style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'backgroundColor': '#ffffff',
                   'marginBottom': '.8%', 'marginTop': '.5%',
                   'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'
                },
                 children=[
                     html.H2(
                        style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                'color': '#292929', 'paddingTop': '1rem', 'marginBottom': '0','marginTop': '0'},
                        children='COVID-19 Case and Death Metrics US Counties'),
                    html.Hr(),
                     html.Div(
                         style={'width': '64%', 'display': 'inline-block',
                                'marginRight': '.8%', 
                                #'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'
                                },
                         children=[
                                  html.H5(
                                    id='dcc-map-graph-head',
                                    style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                           'color': '#292929', 'padding': '.5rem', 'marginBottom': '0','marginTop': '0'},
                                    children='Case Severity Per County'),
                                  dcc.Graph(
                                    style={'height': '500px'}, 
                                    figure=fig_map),
                                    dbc.Tooltip(
                                    '''
                                    This map calculates percentage of population with confirmed cases based on 2019 US census data.
                                    ''',
                                              target='dcc-map-graph-head',
                                              style={"font-size":"1em"},
                                             ),
                                  ]),
                     html.Div(style={'width': '34%', 'display': 'inline-block', 'verticalAlign': 'top',
                                     'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'},
                              children=[
                                  html.H5(style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                                 'color': '#292929', 'padding': '1rem', 'marginBottom': '0', 'marginTop': '0'},
                                               children='Cases Summary by Location'),
                                  dcc.Tabs(
                                      id="tabs-table",
                                      value='States',
                                      parent_className='custom-tabs',
                                      className='custom-tabs-container',
                                      children=[
                                          dcc.Tab(label='States',
                                              value='States',
                                              className='custom-tab',
                                              selected_className='custom-tab--selected',
                                              style={'textAlign':'center',
                                                    'fontWeight': 'bold',},
                                              children=[
                                                  dash_table.DataTable(
                                                      id='datatable-interact-location',
                                                      columns = [{"name": i, "id": i} for i in state_summary.columns],
                                                      data=state_summary.to_dict("rows"),
                                                      sort_action="native",
                                                      style_as_list_view=True,
                                                      style_cell={'font_family': 'Arial',
                                                                  'font_size': '1rem',
                                                                  'padding': '.1rem',
                                                                  'backgroundColor': '#ffffff',
                                                                  'width': '200px',
                                                                  'textAlign':'right', 
                                                                  'overflow': 'hidden',
                                                                    'textOverflow': 'ellipsis',
                                                                    'maxWidth': 0, },
                                                      fixed_rows={
                                                          'headers': True, 'data': 0},
                                                      style_table={'minHeight': '400px',
                                                                   'height': '400px',
                                                                   'maxHeight': '400px',
                                                                   'overflowX': 'scroll',
                                                                   },
                                                      style_header={'backgroundColor': '#ffffff',
                                                                    'fontWeight': 'bold'},
                                                      style_cell_conditional=[
                                                            {'if': {'column_id': 'state'},
                                                            'width': '50%'},
                                                            {'if': {'column_id': 'cases'},
                                                            'width': '25%'},
                                                            {'if': {'column_id': 'deaths'},
                                                            'width': '25%'},
                                                        ]
                                                  )
                                            ]),

                                            dcc.Tab(label='Counties',
                                              value='Counties',
                                              className='custom-tab',
                                              selected_className='custom-tab--selected',
                                              style={'textAlign':'center',
                                                    'fontWeight': 'bold',},
                                              children=[
                                                  dash_table.DataTable(
                                                      id='datatable-interact-location2',
                                                      columns = [{"name": i, "id": i} for i in county_summary.columns],
                                                      data=county_summary.to_dict("rows"),
                                                      sort_action="native",
                                                      style_as_list_view=True,
                                                      style_cell={'font_family': 'Arial',
                                                                  'font_size': '1rem',
                                                                  'padding': '.1rem',
                                                                  'backgroundColor': '#ffffff',
                                                                  'width': '200px,',
                                                                  'textAlign':'right', 
                                                                  'overflow': 'hidden',
                                                                    'textOverflow': 'ellipsis',
                                                                    'maxWidth': 0,},
                                                      fixed_rows={
                                                          'headers': True, 'data': 0},
                                                      style_table={'minHeight': '400px',
                                                                   'height': '400px',
                                                                   'maxHeight': '400px',
                                                                   'overflowX': 'scroll',
                                                                   },
                                                      style_header={'backgroundColor': '#ffffff',
                                                                    'fontWeight': 'bold'},
                                                  )
                                            ]),
                                          ]
                                       )
                                    ]),
                              ]),
                     
            html.Div(style={'textAlign': 'center'},
                children=[
                    html.Br(),
                    html.H3('Stay safe out in them streets.  Keep your distance and most importantly:'),
                    html.H2('Wash 👏 Your 👏 Hands 👏 '),
                    html.A('www.THWDesigns.com',href='https://thwdesigns.com'),
                ]),

            # FOOTER START
            html.Div(style={'textAlign': 'center'},
                children=[
                    html.Br(),
                    html.Br(),
                    html.Hr(),
                    html.P('Shout out to the below GitHub repos for inspiration.'),
                    html.A('Perishleaf Project', href='https://github.com/Perishleaf/data-visualisation-scripts/tree/master/dash-2019-coronavirus',target='_blank'),
                    html.Br(),
                    html.A('NYT Github',href='https://github.com/nytimes/covid-19-data'),
                ]),

])

if __name__ == '__main__':
    # change host from the default to '0.0.0.0' to make it publicly available
    app.server.run(port=8000, host='127.0.0.1')
    app.run_server(debug=True)