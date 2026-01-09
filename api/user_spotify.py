import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import date
from api.fetch_weather import fetch_weather_by_coords

load_dotenv()

# Get weather via frontend (IP-based geolocation)
weather = fetch_weather_by_coords(37.7749, -122.4194)

def get_user_spotify():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("RYAN_SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("RYAN_SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-top-read playlist-modify-public playlist-modify-private",
            cache_path=".spotify_cache"
        )
    )

sp = get_user_spotify()
user_id = sp.current_user()["id"]
top_tracks = sp.current_user_top_tracks(limit=50, time_range="medium_term")
track_ids = [item["id"] for item in top_tracks["items"]]

########## Save playlist to profile
#if option pressed
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
