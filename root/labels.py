FEATURES = dict(
    popularity='Popularity',
    s_release_date='Spotify Release Date',
    datepublished='YouTube Publish Date',
    tempo='Tempo',
    energy='Energy',
    danceability='Danceability',
    loudness='Loudness',
    valence='Positiveness',
    speechiness='Speechiness',
    acousticness='Acousticness',
    instrumentalness='Instrumentalness',
    liveness='Liveness',
    music_key='Key',
    view_count='YouTube Play Count'
)

FIGURES = {f: 'figure_'+f[0:2] for f in FEATURES.keys()}
