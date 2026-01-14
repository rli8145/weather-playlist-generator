# Weather Playlist Generator

Generate playlists that match the weather by predicting how long a song should be saved based on its audio features.

## ML Component (Core)

The ML pipeline predicts a weather-related label from song audio features and powers the playlist logic.

### Data

- Source: `data/track_data.csv`
- Features used: `energy`, `valence`, `tempo`, `acousticness`, `loudness`
- Target: `weather`

### Models

Implemented in `ml/models.py`:

- Naive Bayes
- Logistic Regression
- Random Forest
- Gradient Boosting (default example model)

### Training

Train all models and return a dictionary of trained estimators:

```bash
python ml/train.py
```

### Evaluation

`ml/evaluate.py` runs:

- Weighted F1 on a holdout split
- Stratified cross-validated F1
- Permutation feature importance
- Confusion matrices (visualized)

```bash
python ml/evaluate.py
```

### Prediction Flow

`ml/model_sample.py` prompts for audio features, builds a single-row dataframe, and predicts the weather label to decide how long to save a song.

```bash
python ml/model_sample.py
```

## APIs

- Spotify Web API (song lookup)
- OpenWeatherMap API (weather context)
- ReccoBeats API (audio features)

## Local Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the ML scripts above.

## Issues

- As of Nov. 2024, Spotify API denies access to song features
- ReccoBeats API, which provided alternative access to song features, had very slow response times. Future improvement may involve caching audio features when possible.
