import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotify_auth import get_user_spotify_client
from datetime import date

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
