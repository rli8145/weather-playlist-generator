import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

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

# next steps: save own private playlist and change IDs, 
# regenerate track_data.csv,
# train models
def get_tracks(playlist_id):
    res = sp.playlist_items(playlist_id, limit=100, offset=0, additional_types=["track"])
    track_ids = []
    for item in res["items"]:
        t = item.get("track")
        if t and t.get("id"): #track may be unavailable
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

def add_to_df(id, weather_label):
    global df
    track_ids = get_tracks(id)
    df_feats = get_features(track_ids, weather_label)
    df = pd.concat([df, df_feats], ignore_index=True)

add_to_df(rain_id, "rainy")
add_to_df(sun_id, "sunny")
add_to_df(cloud_id, "cloudy")
add_to_df(snow_id, "snowy")

df.to_csv("data/ryan.csv", index=False)
#csv with columns weather, energy, valence, tempo, acousticness, loudness