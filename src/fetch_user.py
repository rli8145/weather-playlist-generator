import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import date

load_dotenv()

def get_user_spotify_client():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIFY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-top-read playlist-modify-public playlist-modify-private",
            cache_path=".spotify_cache"
        )
    )

sp = get_user_spotify_client()
user_id = sp.current_user()["id"]
top_tracks = sp.current_user_top_tracks(limit=50, time_range="medium_term")
track_ids = [item["id"] for item in top_tracks["items"]]

#if option pressed
username = sp.current_user()["display_name"]
date_today = date.today().strftime("%Y-%m-%d")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date_today} : {username}'s Weather-Based Playlist",
    public=False
)

sp.playlist_add_items(
    playlist_id=playlist["id"],
    items=weather_playlist[:5]
)
