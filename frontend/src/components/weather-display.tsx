import { CloudRain, MapPin, Thermometer } from "lucide-react";

interface WeatherDisplayProps {
  location: string;
  temperature: number;
  condition: string;
}

const WeatherDisplay = ({ location, temperature, condition }: WeatherDisplayProps) => {
  return (
    <div className="flex items-center gap-4 text-foreground/80 animate-fade-in">
      <div className="flex items-center gap-2">
        <MapPin className="w-4 h-4 text-accent" />
        <span className="text-sm font-medium">{location}</span>
      </div>
      
      <div className="w-px h-4 bg-foreground/20" />
      
      <div className="flex items-center gap-2">
        <CloudRain className="w-4 h-4 text-rain" />
        <span className="text-sm">{condition}</span>
      </div>
      
      <div className="w-px h-4 bg-foreground/20" />
      
      <div className="flex items-center gap-2">
        <Thermometer className="w-4 h-4 text-accent" />
        <span className="text-sm">{temperature}°C</span>
      </div>
    </div>
  );
};

export default WeatherDisplay;
