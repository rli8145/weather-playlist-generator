import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_model(max_iter = 1000):
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=max_iter)),
        ]
    )

def predict_weather(model, features):
    return pd.Series(model.predict(features), index=features.index, name="weather")