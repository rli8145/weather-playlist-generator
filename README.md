# Weather-Conditioned Music Classification Engine

Predict a suitable weather category given a song's audio features.

## Two Demo Paths

### Option 1: Run the Website Locally

This starts the FastAPI backend + the Vite frontend.

1. Backend setup:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Set Spotify credentials (go to Spotify Web API):

```bash
export SPOTIPY_CLIENT_ID="your_spotify_client_id"
export SPOTIPY_CLIENT_SECRET="your_spotify_client_secret"
```

3. Start the API (uses `backend/models/model.pkl` if present):

```bash
uvicorn backend.app.main:app --reload --port 8000
```

4. Start the frontend in a second terminal:

```bash
cd frontend
npm install
npm run dev
```

5. Open the app using the given `localhost` server.

Video: https://drive.google.com/file/d/1nc7trHjiscxEsSmc9bRy0GR-1T8RSImB/view?usp=sharing

### Option 2: Manual Features via the ML Script

This runs a simple prompt-driven predictor and does not use the web app.

1. Ensure the Python environment is ready (same as Demo 1).
2. Run the script and enter features when prompted:

```bash
python 'ml/features->weather.py'
```

The user will be prompted for `energy [0.0, 1.0]`, `valence [0.0, 1.0]`, `tempo (BPM)`, `acousticness [0.0, 1.0]`, and `loudness (dB)` in order, and the predicted weather category is printed.

## Tech Stack
- Python - `scikit-learn`, `pandas`, `matplotlib`, `FastAPI` (served via `Uvicorn`)
- React, Typescript, Tailwind CSS

## APIs Used
- Spotify Web API (song lookup)
- ReccoBeats API (audio features)
- OpenWeatherMap API (real-time weather context) (NOT USED IN CURRENT VERSION)

## ML Component

- Data source: `data/track_data.csv`. 
- Features: `energy`, `valence`, `tempo`, `acousticness`, `loudness`. `StandardScalar` was used to standardize each feature.
- Target label: `weather`: one of `sunny`, `cloudy`, `rainy`, `snowy` 
- Models in `ml/models.py`, trained using `Pipeline` to avoid data leakage: Naive Bayes, Logistic Regression (baseline), Random Forest, Gradient Boosting (production)

Training and evaluation scripts:

```bash
python ml/train.py
python ml/evaluate.py
```

Evaluation metrics and diagnostics used in `ml/evaluate.py`:

- Weighted F1 on a simple holdout split was initially used, and we improved to Stratified K-Fold cross-validation with weighted F1
- Permutation feature importance (PFI)
- Confusion matrices (visualized using matplotlib)

![Confusion matrices](ml/results/confusion_matrices.png)
see `ml/results/evaluate_results.txt` for other final diagnostics

## Issues

- As of Nov. 2024, Spotify API does not provide access to audio features. ReccoBeats was thus added for audio features but API experienced high latency. In the future we can experiment with caching song information for faster response times.
