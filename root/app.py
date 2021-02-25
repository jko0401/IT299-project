import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from sklearn.decomposition import PCA
import plotly.express as px
import db
import pandas as pd
from labels import FEATURES

app = dash.Dash(__name__)

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
features = [
    {"label": str(FEATURES[feature]), "value": str(feature)} for feature in FEATURES
]
audio_features = ['danceability', 'energy', 'music_key', 'loudness', 'music_mode', 'speechiness',
                  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                  'time_signature']

min_s_date = min(df['s_release_date'])
max_s_date = max(df['s_release_date'])
min_y_date = min(df['datepublished'])
max_y_date = max(df['datepublished'])

app.layout = html.Div([
    html.Div([
       html.H1('Visualizing Trap and Dubstep through YouTube and Spotify Data')
    ]),
    html.Div([
        html.Div([
            html.Div([
                html.H3('Filters'),
                html.Div([
                    html.P('Artists:'),
                    dcc.Dropdown(id='artists',
                                 options=artist_options,
                                 multi=True,
                                 value=['RL Grime', 'TroyBoi', 'Eptic'],
                                 ),
                ]),
            ], className='row'),
            html.Div([
                html.Div([
                    html.P('Channels:'),
                    dcc.Dropdown(id='channels',
                                 options=channel_options,
                                 multi=True,
                                 value=['TrapNation', 'TrapCity', 'BassNation', 'UKFDubstep',
                                        'BassMusicMovement', 'DubRebellion']
                                 ),
                ]),
            ], className='row'),
            html.Div([
                html.Div([
                    html.P('Spotify Release Date Range:'),
                    dcc.DatePickerRange(id='s_date',
                                        start_date=min_s_date,
                                        end_date=max_s_date,
                                        display_format='Y/M/D'
                                        )
                ]),
            ], className='row'),
            html.Div([
                html.Div([
                    html.P('YouTube Publish Date Range:'),
                    dcc.DatePickerRange(id='y_date',
                                        start_date=min_y_date,
                                        end_date=max_y_date,
                                        display_format='Y/M/D'
                                        )
                ]),
            ], className='row'),
        ], className='pretty_container'),
        html.Div([
            html.H3('Popularity'),
            html.P('Spotify Popularity'),
            html.Div(dcc.Graph(id='popularity')),
            html.P('YouTube Plays'),
            html.Div(dcc.Graph(id='yt-views'))
        ], className='pretty_container')
    ], className='three columns'),

    html.Div([
        html.Div([
            html.H3('Compare Features'),
            html.Div([
                html.Div([
                    html.P('X-Axis'),
                    dcc.Dropdown(id='feature-1',
                                 options=features,
                                 value='popularity'
                                 ),
                ], className='six columns'),
                html.Div([
                    html.P('Y-Axis'),
                    dcc.Dropdown(id='feature-2',
                                 options=features,
                                 value='energy'
                                 ),
                ], className='six columns'),
            ], className='row'),
            html.Div(dcc.Graph(id='scatter')),
        ], className='pretty_container'),
        html.Div([
            html.H3('Similar Tracks'),
            html.Div(dcc.Graph(id='pca'))
        ], className='pretty_container')
    ], className='five columns'),

    html.Div([
        html.H3('Audio Feature Distributions'),
        # html.Div(dcc.Graph(id='figures')),
        html.Div(dcc.Graph(id='tempo')),
        html.Div(dcc.Graph(id='energy')),
        html.Div(dcc.Graph(id='danceability')),
        html.Div(dcc.Graph(id='loudness')),
        html.Div(dcc.Graph(id='instrumentalness')),
        html.Div(dcc.Graph(id='speechiness')),
        html.Div(dcc.Graph(id='valence')),
        html.Div(dcc.Graph(id='acousticness')),
        html.Div(dcc.Graph(id='liveness')),
        # html.Div(dcc.Graph(id='mode')),
        html.Div(dcc.Graph(id='key')),
        html.Div(id='filtered-data-hidden', style={'display': 'none'})
    ], className='pretty_container four columns')
])


@app.callback(
    Output('filtered-data-hidden', 'children'),
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
    # data = df_filtered.to_dict('records')
    # columns = [{"name": i, "id": i} for i in df_filtered.columns]
    # return dash_table.DataTable(data=data, columns=columns)
    return df_filtered.to_json(date_format='iso', orient='split')


@app.callback(
    # Output('figures', 'figure'),
    [Output('tempo', 'figure'),
     Output('energy', 'figure'),
     Output('danceability', 'figure'),
     Output('loudness', 'figure'),
     Output('instrumentalness', 'figure'),
     Output('speechiness', 'figure'),
     Output('valence', 'figure'),
     Output('acousticness', 'figure'),
     Output('liveness', 'figure'),
     # Output('mode', 'figure'),
     Output('key', 'figure'),
     Output('popularity', 'figure'),
     Output('yt-views', 'figure')],
    [Input('filtered-data-hidden', 'children')]
)
def graph_features(df):
    dff = pd.read_json(df, orient='split')
    # figures = []
    # for feature in FEATURES.keys():
    #     figures.append(px.histogram(dff, x=features, nbins=20))
    figure_t = px.histogram(dff, x="tempo", nbins=20, height=300)
    figure_e = px.histogram(dff, x="energy", nbins=20)
    figure_dance = px.histogram(dff, x="danceability", nbins=20)
    figure_loud = px.histogram(dff, x="loudness", nbins=20)
    figure_i = px.histogram(dff, x="instrumentalness", nbins=20)
    figure_s = px.histogram(dff, x="speechiness", nbins=20)
    figure_v = px.histogram(dff, x="valence", nbins=2)
    figure_a = px.histogram(dff, x="acousticness", nbins=20)
    figure_l = px.histogram(dff, x="liveness", nbins=20)
    # figure_m = px.histogram(dff, x="music_mode", nbins=20)
    figure_k = px.histogram(dff, x="music_key", nbins=22)
    figure_p = px.histogram(dff, x="popularity", nbins=50)
    figure_yt = px.histogram(dff, x="view_count", nbins=50)
    # return figures
    return figure_t, figure_e, figure_dance, figure_loud, figure_i, figure_s, figure_v, figure_a, figure_l, \
        figure_k, figure_p, figure_yt


@app.callback(
    Output('scatter', 'figure'),
    [Input('filtered-data-hidden', 'children'),
     Input('feature-1', 'value'),
     Input('feature-2', 'value')]
)
def graph_scatter(df, feature_1, feature_2):
    dff = pd.read_json(df, orient='split')
    figure = px.scatter(dff, x=feature_1, y=feature_2, hover_name='s_track_name')
    return figure


@app.callback(
    Output('pca', 'figure'),
    [Input('filtered-data-hidden', 'children')]
)
def pca(df):
    dff = pd.read_json(df, orient='split')
    X = dff[audio_features].to_numpy(dtype='float')
    X_id = pd.merge(dff[['s_track_name', 's_id']], dff[audio_features], left_index=True, right_index=True)
    pca = PCA(n_components=2)
    components = pca.fit_transform(X)
    figure = px.scatter(components, x=0, y=1, hover_name=X_id['s_track_name'])
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
