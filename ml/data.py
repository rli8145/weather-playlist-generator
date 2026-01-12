import pandas as pd

features = ["energy", "valence", "tempo", "acousticness", "loudness"]

def load_data(path: str = "data/track_data.csv") -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(path)
    X = df[features]
    y = df["weather"]
    return X, y