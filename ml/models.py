import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def naive_bayes():
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", GaussianNB()),
        ]
    )

def logistic_regression(max_iter = 1000):
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=max_iter)),
        ]
    )

def random_forest():
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", RandomForestClassifier()),
        ]
    )