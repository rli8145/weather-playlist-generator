import pandas as pd

features = ["energy", "valence", "tempo", "acousticness", "loudness"]

def load_data(path = "data/track_data.csv"):
    df = pd.read_csv(path)
    X = df[features]
    y = df["weather"]
    return X, y