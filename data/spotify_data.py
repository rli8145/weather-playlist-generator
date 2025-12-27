import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

features = ["danceability", "energy", "valence", "tempo", "acousticness", "loudness"]

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        my_id=os.getenv("RYAN_SPOTIFY_CLIENT_ID"),
        my_secret=os.getenv("RYAN_SPOTIFY_CLIENT_SECRET")
    )
)


df.to_csv("data/raw/tracks.csv", index=False)
