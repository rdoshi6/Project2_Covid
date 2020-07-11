## First Example

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

def zipcode_lookup(zipcode):
    global state
    global county
    global lat
    global lng
    state_abb = {'AL': 'Alabama',
 'AK': 'Alaska',
 'AS': 'American Samoa',
 'AZ': 'Arizona',
 'AR': 'Arkansas',
 'CA': 'California',
 'CO': 'Colorado',
 'CT': 'Connecticut',
 'DE': 'Delaware',
 'DC': 'District of Columbia',
 'FL': 'Florida',
 'GA': 'Georgia',
 'GU': 'Guam',
 'HI': 'Hawaii',
 'ID': 'Idaho',
 'IL': 'Illinois',
 'IN': 'Indiana',
 'IA': 'Iowa',
 'KS': 'Kansas',
 'KY': 'Kentucky',
 'LA': 'Louisiana',
 'ME': 'Maine',
 'MD': 'Maryland',
 'MA': 'Massachusetts',
 'MI': 'Michigan',
 'MN': 'Minnesota',
 'MS': 'Mississippi',
 'MO': 'Missouri',
 'MT': 'Montana',
 'NE': 'Nebraska',
 'NV': 'Nevada',
 'NH': 'New Hampshire',
 'NJ': 'New Jersey',
 'NM': 'New Mexico',
 'NY': 'New York',
 'NC': 'North Carolina',
 'ND': 'North Dakota',
 'MP': 'Northern Mariana Islands',
 'OH': 'Ohio',
 'OK': 'Oklahoma',
 'OR': 'Oregon',
 'PA': 'Pennsylvania',
 'PR': 'Puerto Rico',
 'RI': 'Rhode Island',
 'SC': 'South Carolina',
 'SD': 'South Dakota',
 'TN': 'Tennessee',
 'TX': 'Texas',
 'UT': 'Utah',
 'VT': 'Vermont',
 'VI': 'Virgin Islands',
 'VA': 'Virginia',
 'WA': 'Washington',
 'WV': 'West Virginia',
 'WI': 'Wisconsin',
 'WY': 'Wyoming'}
    df = pd.read_csv("zip_code_database.csv")
    outdf = df.loc[df['zip'] == zipcode]
    try:
        county = outdf['county'].values[0]
        county = county[:-7]
        state = outdf['state'].values[0]
        state = state_abb[state]
        lat = outdf['latitude'].values[0]
        lng = outdf['longitude'].values[0]
    except:
        return(f'Zipcode not in our Database...')

def confirmed(county,state):
    confirmed_cases_file_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
    confirmed_df = pd.read_csv(confirmed_cases_file_link)
    confirmed_df = confirmed_df.loc[confirmed_df['Admin2'] == county]
    confirmed_df = confirmed_df.loc[confirmed_df['Province_State'] == state]
    confirmed_df = confirmed_df.drop(['UID','iso2','iso3','code3','FIPS','Country_Region','Lat','Long_','Admin2','Province_State','Combined_Key'], axis=1)
    confirmed_df = confirmed_df.T
    confirmed_df['Dates'] = confirmed_df.index
    confirmed_df = confirmed_df[confirmed_df["Dates"]>= '2020-03-01']
    confirmed_df.rename(columns={ confirmed_df.columns[0]: "number" }, inplace = True)
    confirmed_df = confirmed_df.reset_index(drop=True)
    return(confirmed_df)

def deaths(county,state):
    death_cases_file_link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
    deaths_df = pd.read_csv(death_cases_file_link)
    deaths_df = deaths_df.loc[deaths_df['Admin2'] == county]
    deaths_df = deaths_df.loc[deaths_df['Province_State'] == state]
    deaths_df = deaths_df.drop(['Population','UID','iso2','iso3','code3','FIPS','Country_Region','Lat','Long_','Admin2','Province_State','Combined_Key'], axis=1)
    deaths_df = deaths_df.T
    deaths_df['Dates'] = deaths_df.index
    deaths_df = deaths_df[deaths_df["Dates"]>= '2020-03-01']
    deaths_df.rename(columns={ deaths_df.columns[0]: "number" }, inplace = True)
    deaths_df = deaths_df.reset_index(drop=True)
    return(deaths_df)

def daily(county,state):
    confirmed_df2 = confirmed(county,state)
    daily_df = confirmed_df2
    daily_df['increase'] = daily_df['number']
    daily_df = daily_df[['number','increase','Dates']]
    for i in range(1, len(daily_df)):
        daily_df.loc[i, 'increase'] = daily_df.loc[i,'number'] - daily_df.loc[i-1, 'number']
    daily_df = daily_df[['increase','Dates']]
    return(daily_df)


app = dash.Dash()

county = "Cook"
state = "Illinois"


app.layout = html.Div(
    html.Div([
        html.H1('Enter in your Zipcode!'), 
        dcc.Input(id="input1", type="number", placeholder="Zipcode"),
        html.Div(id='output-graph')
    ])
)

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input1', component_property='value')]
)
def multi_output(input_data) :
    zipcode_lookup(input_data)
    confirmed_df = confirmed(county,state)
    deaths_df = deaths(county,state)
    daily_df = daily(county,state)
    return dcc.Graph(
    id='graph',
    figure={
        'data': [
            {'x': confirmed_df['Dates'].tolist(), 'y': confirmed_df['number'].tolist(), 'type': 'graph', 'name': 'Confirmed Cases'},
       ],
        'layout': {
            'title': f'Total Cases for {county}, {state}'
            }
        }
    ), dcc.Graph(
    id='graph2',
    figure={
        'data': [
            {'x': daily_df['Dates'].tolist(), 'y': daily_df['increase'].tolist(), 'type': 'graph', 'name': 'Daily Increase'},
       ],
        'layout': {
            'title': f'Daily Increase for {county}, {state}'
            }
        }
    ),dcc.Graph(
    id='graph3',
    figure={
        'data': [
            {'x': deaths_df['Dates'].tolist(), 'y': deaths_df['number'].tolist(), 'type': 'graph', 'name': 'Deaths'},
       ],
        'layout': {
            'title': f'Number of Deaths for {county}, {state}'
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)