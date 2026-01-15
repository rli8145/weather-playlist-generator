import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Music2, Loader2, AlertCircle } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { WeatherIcon } from "./weather/WeatherIcon";
import type { WeatherType } from "./weather/WeatherBackground";
import { apiService } from "@/services/api-service";

interface SongWeatherProps {
  onWeatherChange: (weather: WeatherType) => void;
}

type SongWeatherType = "sunny" | "cloudy" | "rainy" | "snowy";

interface SongResult {
  title: string;
  artist: string;
  weather: SongWeatherType;
  confidence: number;
  imageUrl?: string;
}

export const SongWeather = ({ onWeatherChange }: SongWeatherProps) => {
  const [query, setQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [result, setResult] = useState<SongResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsSearching(true);
    setError(null);

    try {
      // Call the FastAPI backend
      const response = await apiService.predictSongWeather(query);

      const songResult: SongResult = {
        title: response.name,
        artist: response.artist,
        weather: response.weather,
        confidence: response.confidence,
        imageUrl: response.image_url || undefined,
      };

      setResult(songResult);
      onWeatherChange(response.weather);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to analyze song';
      setError(errorMessage);
      console.error('Song search error:', err);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  const getWeatherDescription = (weather: SongWeatherType): string => {
    switch (weather) {
      case "sunny":
        return "Save this song for sunny days!";
      case "cloudy":
        return "Save this song for cloudy days!";
      case "rainy":
        return "Save this song for rainy days!";
      case "snowy":
        return "Save this song for snowy days!";
    }
  };

  return (
    <motion.div 
      className="glass-card p-8 w-full max-w-lg"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="p-3 rounded-xl bg-primary/10">
          <Music2 className="w-6 h-6 text-primary" />
        </div>
        <div>
          <h2 className="text-xl font-display font-semibold text-foreground">Start here</h2>
          <p className="text-sm text-muted-foreground">When should you listen to this song?</p>
        </div>
      </div>

      <div className="flex gap-2 mb-6">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <Input
            placeholder="Search song title..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            className="pl-10 bg-secondary/50 border-border/50 focus:border-primary/50"
          />
        </div>
        <Button 
          onClick={handleSearch} 
          disabled={isSearching || !query.trim()}
          className="bg-primary hover:bg-primary/90 text-primary-foreground"
        >
          {isSearching ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            "Analyze"
          )}
        </Button>
      </div>

      <AnimatePresence mode="wait">
        {isSearching && (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex flex-col items-center py-8"
          >
            <div className="relative">
              <div className="w-16 h-16 rounded-full border-2 border-primary/20 border-t-primary animate-spin" />
              <Music2 className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-6 h-6 text-primary" />
            </div>
            <p className="mt-4 text-sm text-muted-foreground">Analyzing audio features...</p>
          </motion.div>
        )}

        {!isSearching && result && (
          <motion.div
            key="result"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="bg-secondary/30 rounded-xl p-6"
          >
            <div className="flex items-start gap-4">
              {result.imageUrl && (
                <img
                  src={result.imageUrl}
                  alt={result.title}
                  className="w-16 h-16 rounded-lg object-cover"
                />
              )}
              <WeatherIcon weather={result.weather} size={64} showLabel />
              <div className="flex-1">
                <h3 className="font-display font-semibold text-lg text-foreground truncate">
                  {result.title}
                </h3>
                <p className="text-sm text-muted-foreground mb-2">{result.artist}</p>
                <p className="text-sm text-foreground/70 mb-2">
                  {getWeatherDescription(result.weather)}
                </p>
                <p className="text-xs text-muted-foreground">
                  Confidence: {(result.confidence * 100).toFixed(1)}%
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {!isSearching && error && (
          <motion.div
            key="error"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex items-center gap-3 p-4 bg-destructive/10 border border-destructive/20 rounded-lg"
          >
            <AlertCircle className="w-5 h-5 text-destructive flex-shrink-0" />
            <p className="text-sm text-destructive">{error}</p>
          </motion.div>
        )}

        {!isSearching && !result && !error && (
          <motion.div
            key="empty"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-center py-8 text-muted-foreground"
          >
            <p className="text-sm">Try searching for "Happy - Pharrell" or "Someone Like You - Adele"</p>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default SongWeather;
