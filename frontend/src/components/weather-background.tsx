import { useEffect, useState } from "react";

export type WeatherType = "rainy" | "sunny" | "cloudy" | "snowy";

interface Particle {
  id: number;
  left: number;
  delay: number;
  duration: number;
  opacity: number;
  size?: number;
}

interface WeatherBackgroundProps {
  weather: WeatherType;
}

const WeatherBackground = ({ weather }: WeatherBackgroundProps) => {
  const [particles, setParticles] = useState<Particle[]>([]);

  useEffect(() => {
    const count = weather === "sunny" ? 12 : weather === "cloudy" ? 8 : 100;
    const newParticles: Particle[] = Array.from({ length: count }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 3,
      duration: weather === "snowy" ? 3 + Math.random() * 4 : 0.5 + Math.random() * 0.5,
      opacity: 0.2 + Math.random() * 0.5,
      size: weather === "snowy" ? 4 + Math.random() * 6 : undefined,
    }));
    setParticles(newParticles);
  }, [weather]);

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
      {/* Base gradient overlay */}
      <div className={`absolute inset-0 transition-colors duration-1000 ${
        weather === "rainy" ? "bg-gradient-to-b from-weather-rainy via-weather-rainy/95 to-weather-rainy" :
        weather === "sunny" ? "bg-gradient-to-b from-weather-sunny via-weather-sunny/90 to-weather-sunny" :
        weather === "cloudy" ? "bg-gradient-to-b from-weather-cloudy via-weather-cloudy/95 to-weather-cloudy" :
        "bg-gradient-to-b from-weather-snowy via-weather-snowy/95 to-weather-snowy"
      }`} />

      {/* Rain particles */}
      {weather === "rainy" && particles.map((drop) => (
        <div
          key={drop.id}
          className="absolute w-[2px] bg-gradient-to-b from-transparent via-rain to-rain-glow animate-rain"
          style={{
            left: `${drop.left}%`,
            animationDelay: `${drop.delay}s`,
            animationDuration: `${drop.duration}s`,
            opacity: drop.opacity,
            height: "80px",
          }}
        />
      ))}

      {/* Snow particles */}
      {weather === "snowy" && particles.map((flake) => (
        <div
          key={flake.id}
          className="absolute rounded-full bg-white animate-snow"
          style={{
            left: `${flake.left}%`,
            animationDelay: `${flake.delay}s`,
            animationDuration: `${flake.duration}s`,
            opacity: flake.opacity,
            width: `${flake.size}px`,
            height: `${flake.size}px`,
            boxShadow: "0 0 10px rgba(255,255,255,0.8)",
          }}
        />
      ))}

      {/* Sun rays */}
      {weather === "sunny" && (
        <>
          <div className="absolute -top-20 -right-20 w-96 h-96 rounded-full bg-gradient-radial from-yellow-300/40 via-orange-300/20 to-transparent animate-pulse-slow" />
          <div className="absolute -top-10 -right-10 w-64 h-64 rounded-full bg-gradient-radial from-yellow-200/60 via-yellow-300/30 to-transparent animate-pulse-slow" style={{ animationDelay: "0.5s" }} />
          {particles.map((ray) => (
            <div
              key={ray.id}
              className="absolute top-0 right-0 origin-top-right bg-gradient-to-b from-yellow-300/20 to-transparent animate-ray"
              style={{
                width: "3px",
                height: "100vh",
                transform: `rotate(${ray.left * 0.9}deg)`,
                animationDelay: `${ray.delay}s`,
                opacity: ray.opacity * 0.5,
              }}
            />
          ))}
        </>
      )}

      {/* Clouds */}
      {weather === "cloudy" && particles.map((cloud) => (
        <div
          key={cloud.id}
          className="absolute rounded-full bg-gradient-to-b from-gray-300/30 to-gray-400/20 animate-cloud blur-xl"
          style={{
            left: `${cloud.left}%`,
            top: `${10 + (cloud.id % 4) * 15}%`,
            animationDelay: `${cloud.delay}s`,
            animationDuration: `${20 + cloud.duration * 20}s`,
            width: `${150 + cloud.id * 20}px`,
            height: `${80 + cloud.id * 10}px`,
            opacity: cloud.opacity * 0.6,
          }}
        />
      ))}

      {/* Ambient glow */}
      <div className={`absolute inset-0 bg-gradient-radial transition-colors duration-1000 ${
        weather === "rainy" ? "from-accent/5" :
        weather === "sunny" ? "from-yellow-400/10" :
        weather === "cloudy" ? "from-gray-400/5" :
        "from-blue-200/10"
      } via-transparent to-transparent`} />
    </div>
  );
};

export default WeatherBackground;
