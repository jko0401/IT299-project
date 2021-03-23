import dash
import dash_core_components as dcc, dash_table
import dash_html_components as html
from dash.dependencies import Input, Output
from sklearn.decomposition import PCA
import plotly.express as px
import db
import pandas as pd
from labels import FEATURES, SUMMARY, SCATTER

app = dash.Dash(__name__)
server = app.server

df = db.main_db()
df = df.convert_dtypes()
df['datepublished'] = pd.to_datetime(df['datepublished'])
df['s_release_date'] = pd.to_datetime(df['s_release_date'])


def create_options(name, list):
    name = []
    for a in list:
        name.append({'label': a, 'value': a})
    return name


artist_options = create_options('artist_options', df[~(df['channelname'] == 'BassMusicMovement')]['artistname'].unique())
channel_options = create_options('channel_options', df[~(df['channelname'] == 'BassMusicMovement')]['channelname'].unique())
features = [
    {"label": str(FEATURES[feature]), "value": str(feature)} for feature in FEATURES
]
scatter = [
    {"label": str(SCATTER[feature]), "value": str(feature)} for feature in SCATTER
]
summary = [
    {"label": str(SUMMARY[feature]), "value": str(feature)} for feature in SUMMARY
]
audio_features = ['danceability', 'energy', 'music_key', 'loudness', 'music_mode', 'speechiness',
                  'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
                  'time_signature']

min_s_date = '2009-1-1'
max_s_date = max(df['s_release_date'])
min_y_date = min(df['datepublished'])
max_y_date = max(df['datepublished'])

color_scheme = ['#00adb5', '#E74C3C', '#3498DB', '#F39C12', '#9B59B6']

app.layout = html.Div([
    html.Div(id='main-header', children=[
        html.Header([
            html.H1('Trap and Dubstep Exploration through YouTube and Spotify Data')
        ])
    ], className='container'),
    html.Div(id='main-app', children=[
        dcc.Tabs([
            dcc.Tab(id='intro-tab', label='Introduction', children=[
                html.Div([
                    html.H2('Welcome!'),
                    html.P('This dashboard allows you to explore the electronic bass music genres of Trap and Dubstep '
                           'through YouTube and Spotify data. Tracks related to these genres were gathered by scraping '
                           'five popular music-discovering channels on YouTube: TrapNation, TrapCity, BassNation, '
                           'UKFDubstep, and DubRebellion. Audio features data was tied to those that could be found in '
                           'Spotify’s library. Brief explanations of each section of the dashboard below.'),
                    html.H5('Filters:'),
                    html.P('Choose to filter the dataset by artists or channels, and through different time ranges by YouTube publish or Spotify release dates. Data points can be differentiated by color through artists or channels.'),
                    html.H5('Feature Summary:'),
                    html.P('Compare the mean, max, min of a specific feature for each artist.'),
                    html.H5('Compare Features:'),
                    html.P('Select any two features to compare and see if there is a correlation between them.'),
                    html.H5('Feature Distributions:'),
                    html.P('A set of histograms to help visualize the frequency and distribution of audio features pertaining to the tracks of the artists or channels selected. Follow the link below to Spotify\'s explanation of each feature.'),
                    html.A('Audio Features', href='https://developer.spotify.com/documentation/web-api/reference/#object-audiofeaturesobject'),
                    html.H5('Similar Tracks:'),
                    html.P('Tracks that are similar in terms of their audio features are grouped together through principal component analysis. The closer the tracks, the more similar they are.'),
                    html.H5('Selected Track:'),
                    html.P('Click on any data point on the Similar Tracks graph to load an embedded YouTube video and listen to the track. Some tracks may have embedding disabled and must be played on YouTube.'),
                    html.H5('Limitations:'),
                    html.P('> The dataset does not automatically update. The most recent data was from the end of January when everything was scraped.'),
                    html.P('> Not all tracks uploaded to YouTube could be found on Spotify. Many SoundCloud-only tracks, unofficial releases, remixes that also represent the genres were not included in this dataset.'),
                    html.P('> Not all Spotify tracks of artists in this dataset were included, only those uploaded and shared by the five YouTube channels were selected.'),
                    html.P(''),
                    html.Div([
                        html.P(''),
                        html.A(html.Img(src='/assets/github.png'), href='https://github.com/jko0401/IT299-project'),
                        html.A(html.Img(src='/assets/website.png'), href='https://jko0401.github.io/')
                    ], className='offset-by-five columns')
                ], className='six columns pretty_container offset-by-three columns')
            ]),
            dcc.Tab(id='dash-tab', label='Dashboard', children=[
                # Filters, Popularity Plots, Video
                html.Div([
                    html.Div([
                        html.Div([
                            html.H5('Filters'),
                            html.Div([
                                html.P('Artists:'),
                                html.Div([
                                    dcc.Dropdown(id='artists',
                                                 options=artist_options,
                                                 multi=True,
                                                 value=['RL Grime', 'TroyBoi', 'Eptic'],
                                                 ),
                                ]),
                            ]),
                        ], className='row'),
                        html.Div([
                            html.Div([
                                html.P('Channels:'),
                                dcc.Dropdown(id='channels',
                                             options=channel_options,
                                             multi=True,
                                             value=['TrapNation', 'TrapCity', 'BassNation', 'UKFDubstep', 'DubRebellion']
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
                        html.H5('Feature Summary'),
                        dcc.Dropdown(id='summary',
                                     options=summary,
                                     value='popularity'
                                     ),
                        html.Div(id='div-summary')
                    ], className='pretty_container'),
                    html.Div(id='div-video')
                ], className='three columns'),

                # Scatter Plots
                html.Div([
                    html.Div([
                        html.H5('Compare Features'),
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
                        html.H5('Similar Tracks'),
                        html.Div(dcc.Graph(id='pca'))
                    ], className='pretty_container')
                ], className='five columns'),

                # Histograms
                html.Div([
                    html.Div([
                        html.H5('Feature Distributions'),
                        html.Div(id='div-figures'),
                        html.Div(id='filtered-data-hidden', style={'display': 'none'})
                    ], className='pretty_container')
                ], className='four columns')
            ])
        ])
    ]),
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
        df_filtered = df[df['artistname'].isin(artists[:5]) &
                         df['channelname'].isin(channels) &
                         df['s_release_date'].isin(pd.date_range(start_s, end_s)) &
                         df['datepublished'].isin(pd.date_range(start_y, end_y))]
    elif not channels:
        df_filtered = df[df['artistname'].isin(artists[:5]) &
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
     Input('color', 'value'),
     Input('artists', 'value'),
     Input('channels', 'value')]
)
def plot_data(df, color, artists, channels):
    dff = pd.read_json(df, orient='split')
    figures = []
    if artists and channels:
        color = color
    elif not artists:
        color = 'channelname'
    elif not channels:
        color = 'artistname'
    else:
        color = None
    for feature in FEATURES.keys():
        if feature == 'music_key':
            bin_size = 22
        elif feature == 'valence':
            bin_size = 2
        else:
            bin_size = 20
        f = px.histogram(dff, x=feature, nbins=bin_size, height=300, color=color,
                         color_discrete_sequence=color_scheme[:len(artists)])
        f.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#393e46",
            showlegend=False,
            font_color="#eeeeee",
            xaxis_title=FEATURES[feature]
        )
        figures.append(dcc.Graph(figure=f))
    return figures




@app.callback(
    Output('div-summary', 'children'),
    [Input('filtered-data-hidden', 'children'),
     Input('color', 'value'),
     Input('summary', 'value')]
)
def summary_table(df, color, summary):
    dff = pd.read_json(df, orient='split')
    test_sum = dff.groupby('artistname').agg({summary: ['mean', 'min', 'max']}).round(2).transpose()
    test_sum = pd.DataFrame(test_sum).reset_index().drop(columns=['level_0']).rename(columns={'level_1': ''})
    figures = dash_table.DataTable(
        data=test_sum.to_dict('records'),
        sort_action='native',
        columns=[{'name': str(i), 'id': str(i)} for i in test_sum.columns],
        style_header={'backgroundColor': '#00adb5'},
        style_cell={
            'backgroundColor': '#222831',
            'color': '#eeeeee'
        },
    )
    return figures


@app.callback(
    Output('scatter', 'figure'),
    [Input('filtered-data-hidden', 'children'),
     Input('feature-1', 'value'),
     Input('feature-2', 'value'),
     Input('color', 'value'),
     Input('artists', 'value'),
     Input('channels', 'value')]
)
def graph_scatter(df, feature_1, feature_2, color, artists, channels):
    dff = pd.read_json(df, orient='split')
    if artists and channels:
        color = color
    elif not artists:
        color = 'channelname'
    elif not channels:
        color = 'artistname'
    else:
        color = None
    figure = px.scatter(dff, x=feature_1, y=feature_2, custom_data=['videoid'],
                        hover_name='s_track_name', color=color, color_discrete_sequence=color_scheme[:len(artists)],
                        height=1000)
    if color == 'artistname':
        legend_title = 'Artist'
    else:
        legend_title = 'Channel'
    figure.update_layout(
        paper_bgcolor="#393e46",
        showlegend=True,
        font_color="#eeeeee",
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
            ),
            title=legend_title
        )
    )
    return figure


@app.callback(
    Output('pca', 'figure'),
    [Input('filtered-data-hidden', 'children'),
     Input('artists', 'value'),
     Input('channels', 'value')]
)
def pca(df, artists, channels):
    if not artists or not channels:
        return dash.no_update

    dff = pd.read_json(df, orient='split')
    X = dff[audio_features].to_numpy(dtype='float')
    X_id = pd.merge(dff[['s_track_name', 's_id']], dff[audio_features], left_index=True, right_index=True)
    pca = PCA(n_components=2)
    components = pca.fit_transform(X)
    figure = px.scatter(components, x=0, y=1, hover_name=X_id['s_track_name'], height=1000)
    figure.update_layout(
        paper_bgcolor="#393e46",
        showlegend=False,
        font_color="#eeeeee",
        xaxis_title='Principal Component 1',
        yaxis_title='Principal Component 2'
    )
    figure.update_traces(marker=dict(color='#00adb5'))
    return figure


@app.callback(
    Output('div-video', 'children'),
    Input('pca', 'clickData'))
def display_selected_data(selectedData):
    if not selectedData:
        return html.Div([
                    html.H5('Selected Track'),
                    html.Div(id='div-video'),
                    html.P('(Click on a datapoint on the Similar Tracks graph to listen to the track)')
                ], className='pretty_container')
    else:
        dff = db.track_id(selectedData['points'][0]['hovertext'])
        vid_link = "https://www.youtube.com/embed/" + dff['videoid'][0]
        return html.Div([
                    html.Iframe(src=vid_link, className='video')
                ], className='video-container')


if __name__ == '__main__':
    app.run_server(debug=True)
