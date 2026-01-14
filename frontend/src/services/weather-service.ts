import { WeatherType } from "@/components/WeatherBackground";

interface WeatherResponse {
  location: string;
  temperature: number;
  condition: string;
  weatherType: WeatherType;
}

interface FetchWeatherParams {
  latitude: number;
  longitude: number;
}

// Placeholder for your backend API endpoint
const WEATHER_API_ENDPOINT = "/api/weather";

export const fetchWeatherByCoordinates = async (
  params: FetchWeatherParams
): Promise<WeatherResponse> => {
  const response = await fetch(WEATHER_API_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      latitude: params.latitude,
      longitude: params.longitude,
    }),
  });

  if (!response.ok) {
    throw new Error(`Weather API error: ${response.status}`);
  }

  return response.json();
};

// Helper to map weather conditions to WeatherType
export const mapConditionToWeatherType = (condition: string): WeatherType => {
  const lowerCondition = condition.toLowerCase();
  
  if (lowerCondition.includes("rain") || lowerCondition.includes("drizzle") || lowerCondition.includes("shower")) {
    return "rainy";
  }
  if (lowerCondition.includes("snow") || lowerCondition.includes("sleet") || lowerCondition.includes("blizzard")) {
    return "snowy";
  }
  if (lowerCondition.includes("clear") || lowerCondition.includes("sunny")) {
    return "sunny";
  }
  // Default to cloudy for overcast, mist, fog, clouds, etc.
  return "cloudy";
};
