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
    view_count
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


def artist_tracks(item_to_query):
    # Returns All Tracks by Artist

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
	   time_signature
FROM spotify_tracks sp
INNER JOIN tracks_artists ta
ON sp.s_id = ta.s_id
INNER JOIN artist_names an
ON ta.artistid = an.artistid
INNER JOIN audio_features af
ON sp.featuresid = af.featuresid
WHERE artistname IN('""" + item_to_query + """')
    """)
    cur.execute(query)
    return pd.read_sql(query, con=conn)


def channel_tracks(item_to_query):
    # Returns All Tracks by Channel

    query = ("""SELECT channelname,
	   datepublished,
	   view_count,
	   sp.s_id, 
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
	   time_signature
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
WHERE channelname IN('""" + item_to_query + """')
    """)
    cur.execute(query)
    return pd.read_sql(query, con=conn)


def spotify_date(date1, date2):
    # Returns All Tracks in timeframe by Spotify release years

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
	   time_signature
FROM spotify_tracks sp
INNER JOIN tracks_artists ta
ON sp.s_id = ta.s_id
INNER JOIN artist_names an
ON ta.artistid = an.artistid
INNER JOIN audio_features af
ON sp.featuresid = af.featuresid
WHERE sp.s_release_date BETWEEN '""" + date1 + """' AND '""" + date2 + """'
    """)
    cur.execute(query)
    return pd.read_sql(query, con=conn)


def youtube_date(date1, date2):
    # Returns All Tracks in timeframe by Youtube published date

    query = ("""SELECT channelname,
	   datepublished,
	   view_count,
	   sp.s_id, 
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
	   time_signature
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
WHERE yt.datepublished BETWEEN '""" + date1 + """' AND '""" + date2 + """'
    """)
    cur.execute(query)
    return pd.read_sql(query, con=conn)