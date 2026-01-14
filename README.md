# Weather Playlist Generator

Predicting a suitable weather category given a song's audio features.

## ML Component (Core)

The ML pipeline predicts a weather-related label from song audio features and powers the playlist logic.

### Data

- Source: `data/track_data.csv`
- Features used: `energy`, `valence`, `tempo`, `acousticness`, `loudness`
- Target: `weather`

### Models

Implemented in `ml/models.py`:

- Naive Bayes 
- Logistic Regression (baseline)
- Random Forest 
- Gradient Boosting (production)

### Training

Train all models and return a dictionary of models after training:

```bash
python ml/train.py
```

### Evaluation

`ml/evaluate.py` runs:

- Weighted F1 on a holdout split
- Stratified cross-validated F1
- Permutation feature importance
- Confusion matrices (visualized using matplotlib)

```bash
python ml/evaluate.py
```

### Prediction Flow

`ml/model_sample.py` prompts for audio features and predicts the matching weather label.

```bash
python ml/model_sample.py
```

## APIs

- Spotify Web API (song lookup)
- OpenWeatherMap API (real-time weather context)
- ReccoBeats API (audio features)

## Local Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the Prediction Flow scripts above.

## Issues

- As of Nov. 2024, Spotify API denies access to song features
- ReccoBeats API, which provided alternative access to song features, had very slow response times. Future improvement may involve caching audio features when possible.
