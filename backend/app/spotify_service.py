"""
Spotify API Service using spotipy
Handles song search and audio feature extraction
"""
import os
from typing import Optional, Dict
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(__name__)


class SpotifyService:
    """
    Service for interacting with Spotify Web API using spotipy
    """

    def __init__(self):
        """Initialize Spotify service with credentials from environment"""
        self.client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.sp: Optional[spotipy.Spotify] = None

        if not self.client_id or not self.client_secret:
            logger.warning(
                "Spotify credentials not configured. "
                "Set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET environment variables."
            )
        else:
            try:
                auth_manager = SpotifyClientCredentials(
                    client_id=self.client_id, client_secret=self.client_secret
                )
                self.sp = spotipy.Spotify(auth_manager=auth_manager)
                logger.info("Spotify service initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Spotify: {e}")

    def search_track(self, query: str, limit: int = 1) -> Optional[Dict]:
        """
        Search for a track on Spotify

        Args:
            query: Search query (song name, artist, etc.)
            limit: Number of results to return (default: 1)

        Returns:
            First track result or None if no results found
        """
        if not self.sp:
            raise ValueError("Spotify service not initialized. Check credentials.")

        try:
            results = self.sp.search(q=query, type="track", limit=limit)
            tracks = results.get("tracks", {}).get("items", [])

            if not tracks:
                logger.info(f"No tracks found for query: {query}")
                return None

            track = tracks[0]
            logger.info(
                f"Found track: {track['name']} by {track['artists'][0]['name']}"
            )

            return track

        except Exception as e:
            logger.error(f"Spotify search failed: {e}")
            raise Exception(f"Failed to search Spotify: {str(e)}")

    def get_audio_features(self, track_id: str) -> Dict[str, float]:
        """
        Get audio features for a specific track

        Args:
            track_id: Spotify track ID

        Returns:
            Dictionary containing audio features needed for ML prediction
        """
        if not self.sp:
            raise ValueError("Spotify service not initialized. Check credentials.")

        try:
            features = self.sp.audio_features([track_id])[0]

            if not features:
                raise Exception(f"No audio features found for track {track_id}")

            # Extract only the features needed for ML prediction
            audio_features = {
                "energy": features["energy"],
                "valence": features["valence"],
                "tempo": features["tempo"],
                "acousticness": features["acousticness"],
                "loudness": features["loudness"],
            }

            logger.info(f"Retrieved audio features for track {track_id}")

            return audio_features

        except Exception as e:
            logger.error(f"Failed to get audio features: {e}")
            raise Exception(f"Failed to get audio features: {str(e)}")

    def get_track_info_and_features(self, query: str) -> Optional[Dict]:
        """
        Search for a track and get its audio features in one call

        Args:
            query: Search query (song name, artist, etc.)

        Returns:
            Dictionary with track info and audio features, or None if not found
        """
        # Search for track
        track = self.search_track(query)

        if not track:
            return None

        # Get audio features
        audio_features = self.get_audio_features(track["id"])

        # Combine track info with audio features
        return {
            "track_id": track["id"],
            "name": track["name"],
            "artist": ", ".join([artist["name"] for artist in track["artists"]]),
            "album": track["album"]["name"],
            "image_url": track["album"]["images"][0]["url"]
            if track["album"]["images"]
            else None,
            "preview_url": track.get("preview_url"),
            "audio_features": audio_features,
        }


# Global instance
spotify_service = SpotifyService()
