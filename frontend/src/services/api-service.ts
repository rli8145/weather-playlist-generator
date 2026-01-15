/**
 * API Service for Forecast.fm Backend
 * Handles communication with FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface SongWeatherResponse {
  track_id: string;
  name: string;
  artist: string;
  album: string;
  image_url: string | null;
  preview_url: string | null;
  weather: 'sunny' | 'cloudy' | 'rainy' | 'snowy';
  confidence: number;
  audio_features: {
    energy: number;
    valence: number;
    tempo: number;
    acousticness: number;
    loudness: number;
  };
}

export interface HealthResponse {
  status: string;
  message: string;
  model_loaded: boolean;
  model_info?: {
    type: string;
    features: string[];
    labels: string[];
    scaler_loaded: boolean;
  };
}

class ApiService {
  /**
   * Check if the API is healthy and model is loaded
   */
  async checkHealth(): Promise<HealthResponse> {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
      throw new Error('API health check failed');
    }

    return response.json();
  }

  /**
   * Search for a song and get weather prediction
   *
   * @param query - Song search query (e.g., "Happy - Pharrell Williams")
   * @returns Song info with weather prediction
   */
  async predictSongWeather(query: string): Promise<SongWeatherResponse> {
    const response = await fetch(`${API_BASE_URL}/predict-song`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));

      if (response.status === 404) {
        throw new Error(`No songs found for: ${query}`);
      } else if (response.status === 503) {
        throw new Error('Service unavailable. Please check if the backend is running.');
      } else {
        throw new Error(error.detail || 'Failed to get prediction');
      }
    }

    return response.json();
  }
}

// Export singleton instance
export const apiService = new ApiService();
