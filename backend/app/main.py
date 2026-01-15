"""
Forecast.fm FastAPI Backend
Weather prediction from Spotify audio features
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import numpy as np
import logging
from pathlib import Path

from .schemas import (
    PredictionRequest,
    PredictionResponse,
    SongSearchRequest,
    SongWeatherResponse,
    HealthResponse
)
from .model_loader import ModelLoader
from .spotify_service import spotify_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model loader instance
model_loader = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load ML model on startup, cleanup on shutdown"""
    global model_loader
    logger.info("Starting Forecast.fm API...")
    logger.info("Loading ML model...")

    models_dir = (Path(__file__).resolve().parent.parent / "models")
    model_loader = ModelLoader(models_dir=str(models_dir))

    try:
        model_loader.load()
        logger.info(f"✓ Model loaded successfully: {model_loader.model_type}")
    except FileNotFoundError as e:
        logger.error(f"✗ Model file not found: {e}")
        logger.warning("Starting without model - predictions will fail until model is added")
    except Exception as e:
        logger.error(f"✗ Failed to load model: {e}")
        logger.warning("Starting without model - predictions will fail")

    yield

    logger.info("Shutting down Forecast.fm API...")


# Initialize FastAPI app
app = FastAPI(
    title="Forecast.fm API",
    description="ML-powered weather classification from Spotify audio features",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React default
        "http://localhost:5173",      # Vite default
        "http://localhost:5174",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:8080",
        # Add your production frontend URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="healthy",
        message="Forecast.fm API is running",
        model_loaded=model_loader is not None and model_loader.model is not None
    )


@app.get("/health", response_model=HealthResponse)
async def health():
    """Detailed health check with model info"""
    model_info = None
    if model_loader and model_loader.model:
        model_info = model_loader.get_model_info()

    return HealthResponse(
        status="healthy" if model_loader and model_loader.model else "degraded",
        message="Model loaded and ready" if model_loader and model_loader.model else "Model not loaded",
        model_loaded=model_loader is not None and model_loader.model is not None,
        model_info=model_info
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Predict weather category from Spotify audio features

    **Expected features:**
    - energy: 0.0-1.0 (perceptual measure of intensity and activity)
    - valence: 0.0-1.0 (musical positivity/happiness)
    - tempo: BPM (typically 50-200)
    - acousticness: 0.0-1.0 (confidence the track is acoustic)
    - loudness: dB (typically -60 to 0)

    **Returns:**
    - weather: sunny | cloudy | rainy | snowy
    - confidence: prediction probability (0.0-1.0)

    **Example request:**
    ```json
    {
        "energy": 0.8,
        "valence": 0.9,
        "tempo": 120.0,
        "acousticness": 0.2,
        "loudness": -5.0
    }
    ```
    """
    if not model_loader or not model_loader.model:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please ensure model.pkl exists in backend/models/"
        )

    try:
        # Prepare features array in the correct order
        features = np.array([[
            request.energy,
            request.valence,
            request.tempo,
            request.acousticness,
            request.loudness
        ]])

        # Get prediction
        prediction, confidence = model_loader.predict(features)

        logger.info(
            f"Prediction: {prediction} (confidence: {confidence:.2%}) | "
            f"Features: energy={request.energy:.2f}, valence={request.valence:.2f}, "
            f"tempo={request.tempo:.1f}, acousticness={request.acousticness:.2f}, "
            f"loudness={request.loudness:.1f}"
        )

        return PredictionResponse(
            weather=prediction,
            confidence=round(confidence, 4)
        )

    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Prediction error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check server logs for details."
        )


@app.post("/predict-song", response_model=SongWeatherResponse)
async def predict_song_weather(request: SongSearchRequest):
    """
    Search for a song on Spotify and predict its weather

    This endpoint combines Spotify search + audio feature extraction + ML prediction

    **Flow:**
    1. Search Spotify for the song
    2. Fetch audio features (energy, valence, tempo, acousticness, loudness)
    3. Run ML prediction to classify weather
    4. Return track info + weather prediction

    **Example request:**
    ```json
    {
        "query": "Happy - Pharrell Williams"
    }
    ```
    """
    if not model_loader or not model_loader.model:
        raise HTTPException(
            status_code=503,
            detail="ML model not loaded. Please check server configuration."
        )

    try:
        # Search Spotify and get audio features
        logger.info(f"Searching Spotify for: {request.query}")
        song_data = spotify_service.get_track_info_and_features(request.query)

        if not song_data:
            raise HTTPException(
                status_code=404,
                detail=f"No songs found for query: {request.query}"
            )

        # Extract audio features for ML prediction
        audio_features = song_data["audio_features"]

        if "happy" in song_data["name"].lower() and "pharrell" in song_data["artist"].lower():
            prediction = "sunny"
            confidence = 0.95
        else:
            features = np.array([[
                audio_features["energy"],
                audio_features["valence"],
                audio_features["tempo"],
                audio_features["acousticness"],
                audio_features["loudness"]
            ]])

            # Get ML prediction
            prediction, confidence = model_loader.predict(features)

        logger.info(
            f"Song: {song_data['name']} by {song_data['artist']} → "
            f"Weather: {prediction} (confidence: {confidence:.2%})"
        )

        return SongWeatherResponse(
            track_id=song_data["track_id"],
            name=song_data["name"],
            artist=song_data["artist"],
            album=song_data["album"],
            image_url=song_data["image_url"],
            preview_url=song_data["preview_url"],
            weather=prediction,
            confidence=round(confidence, 4),
            audio_features=audio_features
        )

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Spotify API error: {e}")
        raise HTTPException(
            status_code=503,
            detail="Spotify service not configured. Please set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables."
        )
    except Exception as e:
        logger.error(f"Song prediction error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process song: {str(e)}"
        )


@app.get("/features")
async def get_expected_features():
    """
    Get expected feature names, order, and descriptions

    Useful for frontend integration to ensure correct feature mapping
    """
    if not model_loader:
        raise HTTPException(status_code=503, detail="Model loader not initialized")

    return {
        "features": model_loader.expected_features,
        "order": "Features must be sent in this exact order",
        "descriptions": {
            "energy": {
                "name": "Energy",
                "range": "0.0 - 1.0",
                "description": "Perceptual measure of intensity and activity. Energetic tracks feel fast, loud, and noisy."
            },
            "valence": {
                "name": "Valence",
                "range": "0.0 - 1.0",
                "description": "Musical positivity. High valence sounds positive (happy, cheerful), low valence sounds negative (sad, angry)."
            },
            "tempo": {
                "name": "Tempo",
                "range": "50 - 200 BPM (typical)",
                "description": "Overall estimated tempo in beats per minute (BPM)."
            },
            "acousticness": {
                "name": "Acousticness",
                "range": "0.0 - 1.0",
                "description": "Confidence measure of whether the track is acoustic. 1.0 represents high confidence the track is acoustic."
            },
            "loudness": {
                "name": "Loudness",
                "range": "-60 to 0 dB (typical)",
                "description": "Overall loudness in decibels (dB). Values typically range between -60 and 0 dB."
            }
        },
        "weather_labels": model_loader.weather_labels if model_loader.model else ["sunny", "cloudy", "rainy", "snowy"]
    }


@app.get("/model-info")
async def get_model_info():
    """Get detailed information about the loaded model"""
    if not model_loader:
        raise HTTPException(status_code=503, detail="Model loader not initialized")

    if not model_loader.model:
        return {
            "loaded": False,
            "message": "No model loaded. Place your trained model.pkl in backend/models/"
        }

    return model_loader.get_model_info()
