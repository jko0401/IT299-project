import psycopg2
import pandas as pd
from config import config


# set up SQl connection
params = config()
conn = psycopg2.connect(**params)
cur = conn.cursor()


def main_db():
    query = ("""SELECT sp.s_id, 
    sp.s_release_date, 
    sp.s_track_name, 
    artistname, 
    sp.featuresid, 
    popularity, 
    danceability, 
    energy, 
    music_key, 
    loudness, 
    music_mode, 
    speechiness, 
    acousticness, 
    instrumentalness, 
    liveness, 
    valence, 
    tempo, 
    time_signature,
    channelname,
    datepublished,
    view_count,
    videoid
    FROM youtube_videos yt
    INNER JOIN channel_names cn
    ON yt.channelid = cn.channelid
    INNER JOIN spotify_tracks sp
    ON yt.s_id = sp.s_id 
    INNER JOIN tracks_artists ta
    ON sp.s_id = ta.s_id
    INNER JOIN artist_names an
    ON ta.artistid = an.artistid
    INNER JOIN audio_features af
    ON sp.featuresid = af.featuresid
    """)
    cur.execute(query)
    return pd.read_sql(query, con=conn)


def track_id(trackname):
    query = ("""SELECT sp.s_id, 
    yt.videoid
    FROM youtube_videos yt
    INNER JOIN spotify_tracks sp
    ON yt.s_id = sp.s_id 
    WHERE sp.s_track_name IN ('""" + trackname + """')
    """)
    cur.execute(query)
    return pd.read_sql(query, con=conn)
