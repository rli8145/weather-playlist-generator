import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

features = ["energy", "valence", "tempo", "acousticness", "loudness"]

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        my_id=os.getenv("RYAN_SPOTIFY_CLIENT_ID"),
        my_secret=os.getenv("RYAN_SPOTIFY_CLIENT_SECRET")
    )
)

def get_playlist_tracks(playlist_id):
    tracks = []
    offset = 0

    while True:
        resp = sp.playlist_items(
            playlist_id,
            offset=offset,
            limit=50,
            additional_types=["track"]
        )
        items = resp.get("items", [])
        if not items:
            break

        for it in items:
            t = it.get("track")
            if not t or t.get("id") is None:  # skip local/deleted tracks
                continue
            tracks.append({
                "track_id": t["id"],
                "track_name": t["name"],
                "artist": ", ".join([a["name"] for a in t["artists"]]),
                "album": t["album"]["name"],
                "popularity": t.get("popularity"),
            })

        offset += len(items)
        if resp.get("next") is None:
            break

    return tracks

def add_audio_features(rows):
    track_ids = [r["track_id"] for r in rows]
    # Spotify endpoint supports up to 100 ids at a time
    for i in range(0, len(track_ids), 100):
        batch_ids = track_ids[i:i+100]
        feats = sp.audio_features(batch_ids)  # list aligned with batch_ids
        for r, f in zip(rows[i:i+100], feats):
            if f is None:
                for k in features:
                    r[k] = None
            else:
                for k in features:
                    r[k] = f.get(k)
    return rows

df = pd.read_csv("track_data.csv")
ids = []
for playlist_id in ids:
    rows = get_playlist_tracks(playlist_id)
    rows = add_audio_features(rows)
df = pd.DataFrame(rows)

merged = df.merge(
    df[
        ["track_id", "energy", "valence", "tempo", "acousticness", "loudness"]
    ],
    on="track_id",
    how="left"
)

merged.to_csv("track_data.csv", index=False)