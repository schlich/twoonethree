import json
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd
from django_plotly_dash import DjangoDash

# from .urls import app_name
data = pd.DataFrame()
mec = DjangoDash('MEC')

mec.layout = html.Div([
    dcc.RadioItems(
        id='district_type',
        options=[
            {'label': 'MO House', 'value': 'SLDL'},
            {'label': 'MO Senate', 'value': 'SLDU'},
            {'label': 'US House', 'value': 'USH'},
            {'label': 'STL Wards', 'value': 'stl'},
        ],
        value='SLDL',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Dropdown(id='district_number', value=78),
    html.P(id='data'),
    html.H4('Donations:'),
    dash_table.DataTable(
        id='donations'
    )
],)

@mec.callback(
    dash.dependencies.Output('district_number', 'options'),
    [dash.dependencies.Input('district_type', 'value')]
)
def update_district_list(district_type):
    n = {'SLDL': 163, 'SLDU': 34, 'USH': 8, 'stl': 28}
    return [{'label': i+1, 'value': i+1} for i in list(range(n[district_type]))]

@mec.callback(
    dash.dependencies.Output('data', 'children'),
    #  dash.dependencies.Output('donations', 'columns'),
    #  dash.dependencies.Output('donations', 'data')],
    [dash.dependencies.Input('district_type', 'value'),
     dash.dependencies.Input('district_number', 'value')]
)
def update_data(district_type, district_number):
    district_data = data[data[district_type] == district_number]
    donation_data = district_data[['First Name', 'Last Name', 'Address 1', 'City', 'Date', 'Amount']]
    donation_data = donation_data.sort_values(by='Amount', ascending=False)
    columns = [{"name": i, "id": i} for i in donation_data.columns]

    n_donations = len(district_data)

    donors = district_data.groupby(['First Name', 'Last Name', 'Address 1', 'City', 'State', 'Zip'])
    n_donors = len(donors)

    return (f'Found {n_donations} donations from {n_donors} donors in District {district_number}')
