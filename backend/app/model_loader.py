"""
ML Model loader and prediction handler
"""
import joblib
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Handles loading and inference for weather classification models
    Supports: Logistic Regression, Random Forest, Gradient Boosting, Naive Bayes
    """

    def __init__(self, models_dir: str = "models"):
        """
        Initialize model loader

        Args:
            models_dir: Directory containing model files
        """
        self.models_dir = Path(models_dir)
        self.model = None
        self.scaler = None
        self.model_type = None
        self.expected_features = [
            "energy",
            "valence",
            "tempo",
            "acousticness",
            "loudness"
        ]
        self.weather_labels = ["sunny", "cloudy", "rainy", "snowy"]

    def load(self, model_filename: str = "model.pkl", scaler_filename: str = "scaler.pkl"):
        """
        Load the trained model and optional scaler

        Args:
            model_filename: Name of the model file
            scaler_filename: Name of the scaler file (optional)
        """
        model_path = self.models_dir / model_filename
        scaler_path = self.models_dir / scaler_filename

        # Load model
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model file not found: {model_path}\n"
                f"Please place your trained model at backend/models/{model_filename}"
            )

        self.model = joblib.load(model_path)
        self.model_type = type(self.model).__name__
        logger.info(f"Loaded model: {self.model_type} from {model_path}")

        # Load scaler if it exists
        if scaler_path.exists():
            self.scaler = joblib.load(scaler_path)
            logger.info(f"Loaded scaler from {scaler_path}")
        else:
            logger.info("No scaler found - predictions will use raw features")

    def predict(self, features: np.ndarray) -> Tuple[str, float]:
        """
        Make a weather prediction from audio features

        Args:
            features: numpy array of shape (1, 5) containing:
                      [energy, valence, tempo, acousticness, loudness]

        Returns:
            Tuple of (weather_label, confidence_score)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load() first.")

        # Validate feature shape
        if features.shape != (1, 5):
            raise ValueError(
                f"Expected features shape (1, 5), got {features.shape}. "
                f"Features should be: {self.expected_features}"
            )

        # Apply scaling if scaler exists
        if self.scaler is not None:
            features = self.scaler.transform(features)

        # Get prediction
        prediction = self.model.predict(features)[0]

        # Get confidence score
        confidence = self._get_confidence(features)

        # Map prediction to weather label
        if isinstance(prediction, (int, np.integer)):
            weather = self.weather_labels[prediction]
        else:
            weather = prediction

        return weather, confidence

    def _get_confidence(self, features: np.ndarray) -> float:
        """
        Extract confidence score from model prediction

        Args:
            features: Preprocessed feature array

        Returns:
            Confidence score between 0 and 1
        """
        try:
            # Try to get probability predictions
            if hasattr(self.model, "predict_proba"):
                probabilities = self.model.predict_proba(features)[0]
                confidence = float(np.max(probabilities))
            elif hasattr(self.model, "decision_function"):
                # For models with decision_function (like some SVMs)
                decision = self.model.decision_function(features)[0]
                # Normalize to 0-1 range (rough approximation)
                confidence = float(1 / (1 + np.exp(-np.max(decision))))
            else:
                # Fallback for models without probability estimates
                confidence = 1.0
                logger.warning(
                    f"Model {self.model_type} doesn't support probability predictions. "
                    "Returning confidence=1.0"
                )
        except Exception as e:
            logger.warning(f"Error getting confidence: {e}. Returning 1.0")
            confidence = 1.0

        return confidence

    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        if self.model is None:
            return {"loaded": False}

        return {
            "loaded": True,
            "type": self.model_type,
            "features": self.expected_features,
            "labels": self.weather_labels,
            "scaler_loaded": self.scaler is not None
        }
