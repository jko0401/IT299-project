import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import datetime as dt
import plotly.graph_objects as go
import plotly.express as px
import db
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df = db.main_db()
df = df.convert_dtypes()
df['datepublished'] = pd.to_datetime(df['datepublished'])
df['s_release_date'] = pd.to_datetime(df['s_release_date'])


def create_options(name, list):
    name = []
    for a in list:
        name.append({'label': a, 'value': a})
    return name


artist_options = create_options('artist_options', df['artistname'].unique())
channel_options = create_options('channel_options', df['channelname'].unique())


min_s_date = min(df['s_release_date'])
max_s_date = max(df['s_release_date'])
min_y_date = min(df['datepublished'])
max_y_date = max(df['datepublished'])

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(id='artists',
                         options=artist_options,
                         multi=True,
                         value=['RL Grime', 'TroyBoi', 'Eptic'],
                         ),
        ], className='six columns'),
    ], className='row'),
    html.Div([
        html.Div([
            dcc.DatePickerRange(id='s_date',
                                start_date=min_s_date,
                                end_date=max_s_date,
                                display_format='Y/M/D'
                                )
        ], className='six columns'),
    ], className='row'),
    html.Div([
        html.Div([
            dcc.DatePickerRange(id='y_date',
                                start_date=min_y_date,
                                end_date=max_y_date,
                                display_format='Y/M/D'
                                )
        ], className='six columns'),
    ], className='row'),
    html.Div([
        html.Div([
            dcc.Dropdown(id='channels',
                         options=channel_options,
                         multi=True,
                         value=['TrapNation', 'TrapCity', 'BassNation', 'UKFDubstep',
                                'BassMusicMovement', 'DubRebellion']
                         ),
        ], className='six columns'),
    ], className='row'),

    html.Div(id='data-table-id')
])


@app.callback(
    Output('data-table-id', 'children'),
    [Input('artists', 'value'),
     Input('channels', 'value'),
     Input('s_date', 'start_date'),
     Input('s_date', 'end_date'),
     Input('y_date', 'start_date'),
     Input('y_date', 'end_date')]
)
def filter_df(artists, channels, start_s, end_s, start_y, end_y):
    if artists:
        df_filtered = df[df['artistname'].isin(artists) &
                         df['channelname'].isin(channels) &
                         df['s_release_date'].isin(pd.date_range(start_s, end_s)) &
                         df['datepublished'].isin(pd.date_range(start_y, end_y))]
    else:
        df_filtered = df[df['channelname'].isin(channels) &
                         df['s_release_date'].isin(pd.date_range(start_s, end_s)) &
                         df['datepublished'].isin(pd.date_range(start_y, end_y))]
    data = df_filtered.to_dict('records')
    columns = [{"name": i, "id": i} for i in df_filtered.columns]
    return dash_table.DataTable(data=data, columns=columns)


if __name__ == '__main__':
    app.run_server(debug=True)
