import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-read-private playlist-read-collaborative",
    open_browser=True
))

rain_ids = ["37i9dQZF1E8PMD6A7ERiBj", 
            "47S4MBG0EEXwA0GdJUA4Ur",
            "37i9dQZF1DXbvABJXBIyiY"]
sun_ids = ["37i9dQZF1EIhkGftn1D0Mh", 
             "37i9dQZF1EIh0gn0qhBsTI", 
             "37i9dQZF1E8MmxIK5TAMPP"]
cloud_ids = ["37i9dQZF1EIgxHuuVqSn9D",
             "5L1D0DHxNCvdWkDDrYQIR6",
             "37i9dQZF1E8IoEX35Mj7fO"]
snow_ids = ["37i9dQZF1EIg6jLXpdBRnL",
            "37i9dQZF1DX0Yxoavh5qJV",
            "37i9dQZF1E8M5ITb7fWzqZ"]

def can_access_playlist(sp, playlist_id):
    try:
        sp.playlist_items(playlist_id, limit=1)
        return True
    except Exception as e:
        return False

for id in rain_ids + sun_ids + cloud_ids + snow_ids:
    if can_access_playlist(sp, id):
        print("Accessible")
    else:
        print("Not accessible")