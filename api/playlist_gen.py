import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import date
from api.fetch_weather import fetch_weather_by_coords

import pandas as pd
import requests
from ml.data import load_data, features as model_features
from ml.models import gradient_boosting

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
top_tracks = sp.current_user_recently_played(limit=100)
track_ids = [
    item["track"]["id"]
    for item in top_tracks["items"]
    if item.get("track") and item["track"].get("id")
]

BASE_URL = "https://api.reccobeats.com"

def spotify_to_recco(track_id, session):
    resp = session.get(
        f"{BASE_URL}/v1/track",
        params={"ids": track_id},
        timeout=30
    )
    resp.raise_for_status()
    data = resp.json()
    tracks = data.get("data", [])
    if not tracks:
        return None
    return tracks[0].get("id")

def fetch_audio_features(recco_id, session):
    resp = session.get(
        f"{BASE_URL}/v1/track/{recco_id}/audio-features",
        timeout=30
    )
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    data = resp.json()
    features = {f: data.get(f) for f in model_features}
    if any(value is None for value in features.values()):
        return None
    return features

def build_weather_playlist(candidate_track_ids, target_weather):
    X, y = load_data()
    model = gradient_boosting()
    model.fit(X, y)
    classes = list(model.named_steps["classifier"].classes_)
    target_key = target_weather.lower()
    if target_key not in classes:
        target_key = classes[0]
    target_idx = classes.index(target_key)

    session = requests.Session()
    scored_tracks = []
    for track_id in candidate_track_ids:
        recco_id = spotify_to_recco(track_id, session)
        if not recco_id:
            continue
        feats = fetch_audio_features(recco_id, session)
        if not feats:
            continue
        df = pd.DataFrame([feats], columns=model_features)
        score = model.predict_proba(df)[0][target_idx]
        scored_tracks.append((track_id, score))
    scored_tracks.sort(key=lambda item: item[1], reverse=True)
    return [track_id for track_id, _ in scored_tracks]

personal_playlist = build_weather_playlist(track_ids, weather)



username = sp.current_user()["display_name"]
date_today = date.today().strftime("%Y-%m-%d")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date_today} : {username}'s {weather} Day Playlist",
    public=False
)

if personal_playlist:
    sp.playlist_add_items(
        playlist_id=playlist["id"],
        items=personal_playlist[:5]
    )
