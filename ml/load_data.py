import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

df = pd.read_csv("data/track_data.csv")

X = df[["energy", "valence", "tempo", "acousticness", "loudness"]]
y = df["weather"]