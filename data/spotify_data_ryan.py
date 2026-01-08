import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

features = ["energy", "valence", "tempo", "acousticness", "loudness"]

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

def get_tracks(playlist_id):
    res = sp.playlist_items(playlist_id, limit=100, offset=0, additional_types=["track"])
    track_ids = []
    for item in res["items"]:
        t = item.get("track")
        if t and t.get("id"): #track can be unavailable
            track_ids.append(t["id"])
    return track_ids

def get_features(track_ids, weather_label):
    features = sp.audio_features(track_ids)
    rows = []
    for f in features:
        if f is None:
            continue
        rows.append({
            "weather": weather_label,
            "energy": f["energy"],
            "valence": f["valence"],
            "tempo": f["tempo"],
            "acousticness": f["acousticness"],
            "loudness": f["loudness"],
        })
    return pd.DataFrame(rows)

df = pd.DataFrame()

def add_to_df(playlist_ids, weather_label):
    for id in playlist_ids:
        track_ids = get_tracks(id)
        df_feats = get_features(track_ids, weather_label)
    df = pd.concat([df, df_feats], ignore_index=True)

add_to_df(rain_ids, "rainy")
add_to_df(sun_ids, "sunny")
add_to_df(cloud_ids, "cloudy")
add_to_df(snow_ids, "snowy")

df.to_csv("data/ryan.csv", index=False)
#csv with columns weather, energy, valence, tempo, acousticness, loudness