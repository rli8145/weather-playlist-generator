import { useState, useEffect } from "react";
import { CloudRain, Sun, Cloud, Snowflake, Headphones } from "lucide-react";
import WeatherBackground, { WeatherType } from "@/components/WeatherBackground";
import PlaylistCard from "@/components/PlaylistCard";
import RatingStars from "@/components/RatingStars";
import WeatherDisplay from "@/components/WeatherDisplay";
import WeatherSelector from "@/components/WeatherSelector";
import LocationPermissionCard from "@/components/LocationPermissionCard";
import { playlists, weatherMoods, weatherTemperatures } from "@/data/playlists";
import { useGeolocation } from "@/hooks/useGeolocation";
import { fetchWeatherByCoordinates, mapConditionToWeatherType } from "@/services/weatherService";

// Import all cover images
import rainyCover from "@/assets/rainy-playlist-cover.jpg";
import sunnyCover from "@/assets/sunny-playlist-cover.jpg";
import cloudyCover from "@/assets/cloudy-playlist-cover.jpg";
import snowyCover from "@/assets/snowy-playlist-cover.jpg";

const coverImages: Record<WeatherType, string> = {
  rainy: rainyCover,
  sunny: sunnyCover,
  cloudy: cloudyCover,
  snowy: snowyCover,
};

const weatherIcons: Record<WeatherType, typeof Sun> = {
  sunny: Sun,
  cloudy: Cloud,
  rainy: CloudRain,
  snowy: Snowflake,
};

const weatherConditions: Record<WeatherType, string> = {
  rainy: "Rainy",
  sunny: "Sunny",
  cloudy: "Cloudy",
  snowy: "Snowy",
};

interface WeatherData {
  location: string;
  temperature: number;
  condition: string;
}

const Index = () => {
  const [weather, setWeather] = useState<WeatherType>("rainy");
  const [userRating, setUserRating] = useState<number | null>(null);
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [hasRequestedLocation, setHasRequestedLocation] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const {
    latitude,
    longitude,
    isLoading: isLoadingLocation,
    error: locationError,
    permissionState,
    requestLocation,
  } = useGeolocation();

  // Fetch weather when coordinates are available
  useEffect(() => {
    if (latitude && longitude) {
      setApiError(null);
      fetchWeatherByCoordinates({ latitude, longitude })
        .then((data) => {
          setWeatherData({
            location: data.location,
            temperature: data.temperature,
            condition: data.condition,
          });
          setWeather(data.weatherType || mapConditionToWeatherType(data.condition));
        })
        .catch((err) => {
          console.error("Weather API error:", err);
          setApiError("Failed to fetch weather data");
          // Keep using default/manual weather selection
        });
    }
  }, [latitude, longitude]);

  const handleRate = (rating: number) => {
    setUserRating(rating);
    console.log(`User rated ${weather} playlist: ${rating} stars`);
  };

  const handleWeatherChange = (newWeather: WeatherType) => {
    setWeather(newWeather);
    setUserRating(null);
  };

  const handleRequestLocation = () => {
    setHasRequestedLocation(true);
    requestLocation();
  };

  const handleSkipLocation = () => {
    setHasRequestedLocation(true);
  };

  const showLocationPrompt = !hasRequestedLocation && permissionState !== "granted";

  const currentPlaylist = playlists[weather];
  const WeatherIcon = weatherIcons[weather];

  return (
    <div className="relative min-h-screen flex flex-col">
      <WeatherBackground weather={weather} />

      {/* Main Content */}
      <main className="relative z-10 flex-1 flex flex-col items-center justify-center px-4 py-12">
        {/* Header */}
        <div className="text-center mb-6 animate-fade-in">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Headphones className="w-8 h-8 text-accent" />
            <h1 className="text-3xl md:text-4xl font-bold text-foreground">
              MoodPlay
            </h1>
          </div>
          <p className="text-muted-foreground max-w-md mx-auto">
            Music that matches your moment. Curated playlists based on your weather and vibe.
          </p>
        </div>

        {/* Location Permission or Weather Selector */}
        {showLocationPrompt ? (
          <div className="mb-6">
            <LocationPermissionCard
              isLoading={isLoadingLocation}
              error={locationError}
              onRequestLocation={handleRequestLocation}
              onSkip={handleSkipLocation}
            />
          </div>
        ) : (
          <>
            {/* Weather Selector - always show for manual override */}
            <div className="mb-6 animate-fade-in animation-delay-200">
              <WeatherSelector currentWeather={weather} onWeatherChange={handleWeatherChange} />
            </div>

            {/* Weather Info */}
            <div className="mb-6">
              <WeatherDisplay
                location={weatherData?.location || "Select Weather"}
                temperature={weatherData?.temperature ?? weatherTemperatures[weather]}
                condition={weatherData?.condition || weatherConditions[weather]}
              />
            </div>
          </>
        )}

        {/* Current Weather Mood */}
        <div className="flex items-center gap-2 mb-8 px-4 py-2 rounded-full bg-secondary/50 backdrop-blur-sm animate-fade-in animation-delay-200">
          <WeatherIcon className="w-5 h-5 text-accent" />
          <span className="text-sm font-medium text-foreground">
            {weatherMoods[weather]}
          </span>
        </div>

        {/* Playlist Card */}
        <PlaylistCard
          key={weather}
          name={currentPlaylist.name}
          description={currentPlaylist.description}
          trackCount={currentPlaylist.trackCount}
          coverImage={coverImages[weather]}
          tracks={currentPlaylist.tracks}
        />

        {/* Rating Section */}
        <div className="mt-8">
          <RatingStars key={`rating-${weather}`} onRate={handleRate} />
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 text-center py-6 text-muted-foreground text-xs">
        <p>Powered by weather data • Playlists update in real-time</p>
      </footer>
    </div>
  );
};

export default Index;
