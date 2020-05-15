import json, dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import geopandas as gpd
from django_plotly_dash import DjangoDash
# from django_pandas.io import read_frame
from mec.models import District, Contribution
from django.db.models import Avg, Count

# from .urls import app_name
data = pd.DataFrame()
mec = DjangoDash('MEC')

mec.layout = html.Div([
    dcc.RadioItems(
        id='district_type',
        options=[
            {'label': 'MO House', 'value': 'SLD.L'},
            {'label': 'MO Senate', 'value': 'SLDU'},
            {'label': 'US House', 'value': 'USH'},
            # {'label': 'STL Wards', 'value': 'stl'},
        ],
        value='SLDL',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Dropdown(id='district_number'),
    html.P(id='data'),
    # html.H4('Donations:'),
    # dash_table.DataTable(
    #     id='donations'
    # )
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
    [dash.dependencies.Input('district_type', 'value'),
     dash.dependencies.Input('district_number', 'value')]
)
def update_data(district_type, district_number):
    type_labels = {'SLDU':'LU','SLDL':'LL','USH':'C2'}
    district = District.objects.get(district_type=type_labels[district_type], number=district_number)
    addresses = district.address_set.all()
    donations = Contribution.objects.filter(contributor__address__in=addresses)
    # donation_data = read_frame(donations)
    # donation_data = donation_data.sort_values(by='Amount', ascending=False)
    # columns = [{"name": i, "id": i} for i in donation_data.columns]
    # print(len(donations))
    # donation_aggs = donations.aggregate(Avg('amount'))
    # avg_donation = donation_aggs['amount__avg']
    # return (f'Found {donations.count()} donations averaging ${avg_donation:.2f} from n donors in {district.name}')
    return (f'Found {donations.count()} donations from {district.name}')