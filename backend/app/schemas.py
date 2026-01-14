"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class PredictionRequest(BaseModel):
    """
    Request schema for weather prediction from Spotify audio features
    """
    energy: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Perceptual measure of intensity and activity (0.0-1.0)"
    )
    valence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Musical positivity/happiness (0.0-1.0)"
    )
    tempo: float = Field(
        ...,
        gt=0,
        description="Overall estimated tempo in BPM (typically 50-200)"
    )
    acousticness: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence the track is acoustic (0.0-1.0)"
    )
    loudness: float = Field(
        ...,
        description="Overall loudness in decibels (typically -60 to 0)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "energy": 0.8,
                "valence": 0.9,
                "tempo": 120.0,
                "acousticness": 0.2,
                "loudness": -5.0
            }
        }


class PredictionResponse(BaseModel):
    """
    Response schema for weather prediction
    """
    weather: str = Field(
        ...,
        description="Predicted weather category: sunny, cloudy, rainy, or snowy"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Prediction confidence score"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "weather": "sunny",
                "confidence": 0.85
            }
        }


class HealthResponse(BaseModel):
    """
    Health check response schema
    """
    status: str
    message: str
    model_loaded: bool
    model_info: Optional[Dict[str, Any]] = None
