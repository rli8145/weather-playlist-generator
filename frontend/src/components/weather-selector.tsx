import { CloudRain, Sun, Cloud, Snowflake } from "lucide-react";
import { WeatherType } from "./WeatherBackground";
import { cn } from "@/lib/utils";

interface WeatherSelectorProps {
  currentWeather: WeatherType;
  onWeatherChange: (weather: WeatherType) => void;
}

const weatherOptions: { type: WeatherType; icon: typeof Sun; label: string }[] = [
  { type: "sunny", icon: Sun, label: "Sunny" },
  { type: "cloudy", icon: Cloud, label: "Cloudy" },
  { type: "rainy", icon: CloudRain, label: "Rainy" },
  { type: "snowy", icon: Snowflake, label: "Snowy" },
];

const WeatherSelector = ({ currentWeather, onWeatherChange }: WeatherSelectorProps) => {
  return (
    <div className="flex items-center gap-2 p-1 rounded-full bg-secondary/30 backdrop-blur-sm">
      {weatherOptions.map(({ type, icon: Icon, label }) => (
        <button
          key={type}
          onClick={() => onWeatherChange(type)}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-full transition-all duration-300",
            currentWeather === type
              ? "bg-primary text-primary-foreground shadow-lg"
              : "text-muted-foreground hover:text-foreground hover:bg-white/5"
          )}
        >
          <Icon className="w-4 h-4" />
          <span className="text-sm font-medium hidden sm:inline">{label}</span>
        </button>
      ))}
    </div>
  );
};

export default WeatherSelector;
