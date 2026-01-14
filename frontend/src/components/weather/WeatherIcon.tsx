import { motion } from "framer-motion";
import { Sun, Cloud, CloudRain, Snowflake, CloudLightning, Wind, CloudFog, CloudSun } from "lucide-react";
import type { WeatherType } from "./WeatherBackground";

interface WeatherIconProps {
  weather: WeatherType;
  size?: number;
  className?: string;
  showLabel?: boolean;
}

const weatherConfig: Record<WeatherType, { 
  icon: typeof Sun; 
  label: string; 
  colorClass: string;
}> = {
  sunny: { icon: Sun, label: "Sunny", colorClass: "text-weather-sunny" },
  clear: { icon: Sun, label: "Clear", colorClass: "text-weather-sunny" },
  cloudy: { icon: Cloud, label: "Cloudy", colorClass: "text-weather-cloudy" },
  rainy: { icon: CloudRain, label: "Rainy", colorClass: "text-weather-rainy" },
  snowy: { icon: Snowflake, label: "Snowy", colorClass: "text-weather-snowy" },
  thunder: { icon: CloudLightning, label: "Thunder", colorClass: "text-weather-thunder" },
  windy: { icon: Wind, label: "Windy", colorClass: "text-weather-windy" },
  foggy: { icon: CloudFog, label: "Foggy", colorClass: "text-weather-foggy" },
  mixed: { icon: CloudSun, label: "Mixed", colorClass: "text-weather-sunny" },
  default: { icon: Cloud, label: "Unknown", colorClass: "text-muted-foreground" },
};

export const WeatherIcon = ({ 
  weather, 
  size = 48, 
  className = "",
  showLabel = false 
}: WeatherIconProps) => {
  const config = weatherConfig[weather] || weatherConfig.default;
  const Icon = config.icon;

  return (
    <motion.div 
      className={`flex flex-col items-center gap-2 ${className}`}
      initial={{ scale: 0.8, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ type: "spring", stiffness: 200 }}
    >
      <motion.div
        animate={weather === "sunny" || weather === "clear" ? { 
          rotate: [0, 360],
          scale: [1, 1.1, 1]
        } : weather === "windy" ? {
          x: [-2, 2, -2]
        } : weather === "snowy" ? {
          y: [-2, 2, -2],
          rotate: [0, 180, 360]
        } : {}}
        transition={{ 
          duration: weather === "sunny" ? 20 : 2,
          repeat: Infinity,
          ease: "linear"
        }}
      >
        <Icon 
          size={size} 
          className={`${config.colorClass} drop-shadow-lg`}
          strokeWidth={1.5}
        />
      </motion.div>
      {showLabel && (
        <span className={`text-sm font-medium ${config.colorClass}`}>
          {config.label}
        </span>
      )}
    </motion.div>
  );
};

export default WeatherIcon;