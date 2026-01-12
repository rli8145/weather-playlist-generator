import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

import requests

# next steps: reroute song ids to reccobeats for features

load_dotenv()
# print(os.getenv("SPOTIPY_CLIENT_ID"))
# print(os.getenv("SPOTIPY_CLIENT_SECRET"))
# print(os.getenv("SPOTIPY_REDIRECT_URI"))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-read-private user-read-private",
    open_browser=True
))

features = ["energy", "valence", "tempo", "acousticness", "loudness"]

rain_id = "1N29g8ErSCFpDOcjVKIj9s"
sun_id = "5rF1LIgzA5dyR0VQgqpuSG"
cloud_id = "3YEYVGm9DWFmwtccWIJUZq"
snow_id = "4BEXBnXIG3MWvevMlUM2Io"

BASE_URL = "https://api.reccobeats.com"
def spotify_to_recco(track_id): # spotify track id to recco track id
    r = requests.get(
        f"{BASE_URL}/v1/track",
        params={"ids": track_id},
        timeout=30
    )
    r.raise_for_status()
    data = r.json()

    tracks = data.get("data", [])
    if not tracks:
        return None  # track not found

    return tracks[0]["id"]

def playlist_to_tracks(playlist_id): # returns list of recco track ids corresponding to spotify playlist
    res = sp.playlist_items(playlist_id, limit=100, offset=0, additional_types=["track"])
    tracks = []
    for item in res["items"]:
        t = item.get("track")
        recco_id = spotify_to_recco(t["id"])
        if t and t.get("id") and recco_id: # track may be unavailable, in spotify or recco
            tracks.append(recco_id)
    return tracks

def get_features(playlist_id, weather_label):
    track_ids = playlist_to_tracks(playlist_id)
    rows = []
    for id in track_ids:
        url = f"{BASE_URL}/v1/track/{id}/audio-features"
        resp = requests.get(url, timeout=30)
        if resp.status_code == 404:
            continue 
        resp.raise_for_status()
        data = resp.json()
        rows.append({"weather": weather_label, **{f: data.get(f) for f in features}})
    return pd.DataFrame(rows)

df = pd.DataFrame()

def add_to_df(playlist_id, weather_label):
    global df
    df_feats = get_features(playlist_id, weather_label)
    df = pd.concat([df, df_feats], ignore_index=True)

add_to_df(rain_id, "rainy")
add_to_df(sun_id, "sunny")
add_to_df(cloud_id, "cloudy")
add_to_df(snow_id, "snowy")

df.to_csv("data/ryan.csv", index=False)
#csv with columns weather, energy, valence, tempo, acousticness, loudness