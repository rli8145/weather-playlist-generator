import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import date
from api.fetch_weather import fetch_weather_by_coords

import requests

load_dotenv()

# Get weather via frontend (IP-based geolocation)
weather = fetch_weather_by_coords(37.7749, -122.4194)

def get_user_spotify():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-read-recently-played playlist-modify-public playlist-modify-private",
            cache_path=".spotify_cache"
        )
    )

sp = get_user_spotify()
user_id = sp.current_user()["id"]
top_tracks = sp.current_user_recently_played(limit=50)
track_ids = [item["id"] for item in top_tracks["items"]]

########## Save playlist to profile
username = sp.current_user()["display_name"]
date_today = date.today().strftime("%Y-%m-%d")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date_today} : {username}'s {weather} Day Playlist",
    public=False
)

sp.playlist_add_items(
    playlist_id=playlist["id"],
    #items=weather_playlist[:5]
)

# next steps: weather playlist 
# use fetch_weather to get weather given user's location
# use sp to get user's recently played tracks, reccobeats to get features, ml model to predict weather
# filter tracks by predicted weather, or order by probability of weather class. top 5 -> playlist