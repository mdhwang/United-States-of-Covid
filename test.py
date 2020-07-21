import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import numpy as np

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


states = np.sort(state_data.state.unique())

print(states)
print(len(states))

fig = make_subplots(rows = 11, 
                    cols = 5,
                    subplot_titles = states)

for i,each in enumerate(states):
    plus = i + 1
    row = i // 5 + 1
    col = i % 5 + 1
    data = state_data[state_data.state == each]
    fig.add_trace(go.Scatter(x = data.date, 
                             y = data.cases,
                            name = 'Case Load Over Time for {}'.format(each)
                            ),
        row=row, 
        col=col
    ),

fig.update_layout(
    width = 1200,
    height = 2400,
    showlegend = False
)
fig.show()