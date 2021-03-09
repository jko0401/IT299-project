import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from sklearn.decomposition import PCA
import plotly.express as px
import db
import pandas as pd
from labels import FEATURES, POPULARITY, SCATTER

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
scatter = [
    {"label": str(SCATTER[feature]), "value": str(feature)} for feature in SCATTER
]
audio_features = ['danceability', 'energy', 'music_key', 'loudness', 'music_mode', 'speechiness',
                  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                  'time_signature']

min_s_date = '2009-1-1'
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
                html.P('Differentiate Data Points By:'),
                dcc.RadioItems(
                    id='color',
                    options=[
                        {'label': 'Artists', 'value': 'artistname'},
                        {'label': 'Channels', 'value': 'channelname'},
                    ],
                    value='artistname',
                    labelStyle={'display': 'inline-block'})
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
            html.Div(id='div-popularity')
        ], className='pretty_container'),
        html.Div([
            html.H3('Selected Track'),
            html.Div(id='div-video')
        ], className='pretty_container')
    ], className='three columns'),

    html.Div([
        html.Div([
            html.H3('Compare Features'),
            html.Div([
                html.Div([
                    html.P('X-Axis'),
                    dcc.Dropdown(id='feature-1',
                                 options=scatter,
                                 value='popularity'
                                 ),
                ], className='six columns'),
                html.Div([
                    html.P('Y-Axis'),
                    dcc.Dropdown(id='feature-2',
                                 options=scatter,
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
        html.Div(id='div-figures'),
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
    return df_filtered.to_json(date_format='iso', orient='split')


@app.callback(
    Output('div-figures', 'children'),
    [Input('filtered-data-hidden', 'children'),
     Input('color', 'value')]
)
def plot_data(df, color):
    dff = pd.read_json(df, orient='split')
    figures = []
    for feature in FEATURES.keys():
        if feature == 'music_key':
            bin_size = 22
        elif feature == 'valence':
            bin_size = 2
        else:
            bin_size = 20
        f = px.histogram(dff, x=feature, nbins=bin_size, height=300, color=color)
        f.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#4e4e50",
            showlegend=False,
            font_color="white",
            xaxis_title=FEATURES[feature]
        )
        figures.append(dcc.Graph(figure=f))
    return figures


@app.callback(
    Output('div-popularity', 'children'),
    [Input('filtered-data-hidden', 'children'),
     Input('color', 'value')]
)
def plot_pop(df, color):
    dff = pd.read_json(df, orient='split')
    figures = []
    for feature in POPULARITY.keys():
        if feature == 'popularity':
            bin_size = 20
        else:
            bin_size = 200
        f = px.histogram(dff, x=feature, nbins=bin_size, color=color, height=400)
        f.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#4e4e50",
            showlegend=False,
            font_color="white",
            xaxis_title=POPULARITY[feature]
        )
        figures.append(dcc.Graph(figure=f))
    return figures


@app.callback(
    Output('scatter', 'figure'),
    [Input('filtered-data-hidden', 'children'),
     Input('feature-1', 'value'),
     Input('feature-2', 'value'),
     Input('color', 'value')]
)
def graph_scatter(df, feature_1, feature_2, color):
    dff = pd.read_json(df, orient='split')
    figure = px.scatter(dff, x=feature_1, y=feature_2, custom_data=['videoid'],
                        hover_name='s_track_name', color=color, height=1000)
    figure.update_layout(
        paper_bgcolor="#4e4e50",
        showlegend=False,
        font_color="white",
        xaxis_title=SCATTER[feature_1],
        yaxis_title=SCATTER[feature_2],
        legend=dict(
            orientation="h",
            yanchor="middle",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(
                size=12,
            )
        )
    )
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
    figure = px.scatter(components, x=0, y=1, hover_name=X_id['s_track_name'], height=1000)
    figure.update_layout(
        paper_bgcolor="#4e4e50",
        showlegend=False,
        font_color="white",
        xaxis_title='Principal Component 1',
        yaxis_title='Principal Component 2'
    )
    return figure


@app.callback(
    Output('div-video', 'children'),
    Input('pca', 'clickData'))
def display_selected_data(selectedData):
    if not selectedData:
        return html.P('(Click on a datapoint on the Similar Tracks graph to listen to the track)')
    else:
        dff = db.track_id(selectedData['points'][0]['hovertext'])
        vid_link = "https://www.youtube.com/embed/" + dff['videoid'][0]
        return html.Iframe(src=vid_link)


if __name__ == '__main__':
    app.run_server(debug=True)
