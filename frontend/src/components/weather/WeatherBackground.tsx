import { motion, AnimatePresence } from "framer-motion";
import { useMemo } from "react";

export type WeatherType = 
  | "sunny" 
  | "cloudy" 
  | "rainy" 
  | "snowy" 
  | "thunder" 
  | "windy" 
  | "foggy" 
  | "mixed"
  | "clear"
  | "default";

interface WeatherBackgroundProps {
  weather: WeatherType;
  className?: string;
}

const Raindrop = ({ delay, left, duration }: { delay: number; left: string; duration: number }) => (
  <motion.div
    className="absolute w-0.5 h-8 bg-gradient-to-b from-transparent via-weather-rainy to-transparent rounded-full opacity-40"
    style={{ left }}
    initial={{ y: "-100vh", opacity: 0 }}
    animate={{ y: "100vh", opacity: [0, 0.6, 0.3] }}
    transition={{ 
      duration,
      delay,
      repeat: Infinity,
      ease: "linear"
    }}
  />
);

const Snowflake = ({ delay, left, size, duration }: { delay: number; left: string; size: number; duration: number }) => (
  <motion.div
    className="absolute rounded-full bg-weather-snowy opacity-80"
    style={{ left, width: size, height: size }}
    initial={{ y: "-10vh", x: 0, rotate: 0, opacity: 0 }}
    animate={{ 
      y: "110vh", 
      x: [0, 30, -20, 40, 0],
      rotate: 360,
      opacity: [0, 1, 0.8, 0.5]
    }}
    transition={{ 
      duration,
      delay,
      repeat: Infinity,
      ease: "linear"
    }}
  />
);

const Cloud = ({ delay, top, scale, duration }: { delay: number; top: string; scale: number; duration: number }) => (
  <motion.div
    className="absolute opacity-20"
    style={{ top }}
    initial={{ x: "-200px" }}
    animate={{ x: "calc(100vw + 200px)" }}
    transition={{ 
      duration,
      delay,
      repeat: Infinity,
      ease: "linear"
    }}
  >
    <div 
      className="bg-weather-cloudy rounded-full blur-xl"
      style={{ 
        width: 200 * scale, 
        height: 80 * scale 
      }}
    />
  </motion.div>
);

const LightningFlash = () => (
  <motion.div
    className="absolute inset-0 bg-weather-thunder/20"
    initial={{ opacity: 0 }}
    animate={{ opacity: [0, 1, 0, 0.5, 0] }}
    transition={{ 
      duration: 0.3,
      repeat: Infinity,
      repeatDelay: Math.random() * 5 + 3
    }}
  />
);

const SunGlow = () => (
  <motion.div
    className="absolute top-10 right-10 w-40 h-40 rounded-full"
    style={{
      background: "radial-gradient(circle, hsl(var(--sunny-glow)) 0%, transparent 70%)"
    }}
    animate={{ 
      scale: [1, 1.2, 1],
      opacity: [0.6, 0.9, 0.6]
    }}
    transition={{ 
      duration: 4,
      repeat: Infinity,
      ease: "easeInOut"
    }}
  />
);

const FogLayer = ({ delay, opacity }: { delay: number; opacity: number }) => (
  <motion.div
    className="absolute inset-0"
    style={{
      background: "linear-gradient(90deg, transparent, hsl(var(--foggy-primary) / 0.3), transparent)"
    }}
    initial={{ x: "-100%", opacity: 0 }}
    animate={{ 
      x: ["0%", "100%"],
      opacity: [0, opacity, 0]
    }}
    transition={{ 
      duration: 20,
      delay,
      repeat: Infinity,
      ease: "linear"
    }}
  />
);

const WindParticle = ({ delay, top }: { delay: number; top: string }) => (
  <motion.div
    className="absolute h-0.5 bg-gradient-to-r from-transparent via-weather-windy/50 to-transparent rounded-full"
    style={{ top, width: Math.random() * 100 + 50 }}
    initial={{ x: "-100px", opacity: 0 }}
    animate={{ x: "calc(100vw + 100px)", opacity: [0, 0.6, 0] }}
    transition={{ 
      duration: 2 + Math.random(),
      delay,
      repeat: Infinity,
      ease: "linear"
    }}
  />
);

// Mountain silhouette component for default background
const MountainSilhouette = () => (
  <div className="absolute bottom-0 left-0 right-0 h-[40%] pointer-events-none">
    {/* Far mountains - lighter, smaller */}
    <svg 
      className="absolute bottom-0 w-full h-[60%] opacity-[0.08]" 
      viewBox="0 0 1440 320" 
      preserveAspectRatio="none"
    >
      <path 
        fill="currentColor" 
        className="text-primary"
        d="M0,320 L0,200 Q180,120 360,180 Q540,100 720,160 Q900,80 1080,140 Q1260,60 1440,120 L1440,320 Z"
      />
    </svg>
    
    {/* Mid mountains - medium opacity */}
    <svg 
      className="absolute bottom-0 w-full h-[75%] opacity-[0.12]" 
      viewBox="0 0 1440 320" 
      preserveAspectRatio="none"
    >
      <path 
        fill="currentColor" 
        className="text-primary"
        d="M0,320 L0,220 Q120,160 240,200 Q420,80 600,160 Q780,60 960,140 Q1140,40 1320,100 Q1380,80 1440,90 L1440,320 Z"
      />
    </svg>
    
    {/* Near mountains - darker, larger */}
    <svg 
      className="absolute bottom-0 w-full h-full opacity-[0.18]" 
      viewBox="0 0 1440 320" 
      preserveAspectRatio="none"
    >
      <path 
        fill="currentColor" 
        className="text-primary"
        d="M0,320 L0,240 Q100,180 200,220 Q350,100 500,180 Q650,60 800,140 Q950,40 1100,120 Q1250,20 1440,80 L1440,320 Z"
      />
    </svg>
  </div>
);

// Floating ambient particles for default
const AmbientParticle = ({ delay, size, x, duration }: { delay: number; size: number; x: string; duration: number }) => (
  <motion.div
    className="absolute rounded-full bg-primary/20 blur-sm"
    style={{ left: x, width: size, height: size, bottom: "20%" }}
    initial={{ y: 0, opacity: 0 }}
    animate={{ 
      y: [0, -100, -50, -150],
      opacity: [0, 0.4, 0.2, 0],
    }}
    transition={{ 
      duration,
      delay,
      repeat: Infinity,
      ease: "easeInOut"
    }}
  />
);

// Subtle stars for default night sky feel
const Star = ({ x, y, size, delay }: { x: string; y: string; size: number; delay: number }) => (
  <motion.div
    className="absolute rounded-full bg-primary"
    style={{ left: x, top: y, width: size, height: size }}
    animate={{ 
      opacity: [0.2, 0.6, 0.2],
      scale: [1, 1.2, 1],
    }}
    transition={{ 
      duration: 3 + Math.random() * 2,
      delay,
      repeat: Infinity,
      ease: "easeInOut"
    }}
  />
);

export const WeatherBackground = ({ weather, className = "" }: WeatherBackgroundProps) => {
  const raindrops = useMemo(() => 
    Array.from({ length: 50 }, (_, i) => ({
      id: i,
      delay: Math.random() * 2,
      left: `${Math.random() * 100}%`,
      duration: 0.8 + Math.random() * 0.4
    })), []
  );

  const snowflakes = useMemo(() => 
    Array.from({ length: 60 }, (_, i) => ({
      id: i,
      delay: Math.random() * 5,
      left: `${Math.random() * 100}%`,
      size: 4 + Math.random() * 8,
      duration: 6 + Math.random() * 4
    })), []
  );

  const clouds = useMemo(() => 
    Array.from({ length: 5 }, (_, i) => ({
      id: i,
      delay: i * 4,
      top: `${10 + Math.random() * 30}%`,
      scale: 0.5 + Math.random() * 1,
      duration: 25 + Math.random() * 15
    })), []
  );

  const windParticles = useMemo(() =>
    Array.from({ length: 15 }, (_, i) => ({
      id: i,
      delay: i * 0.3,
      top: `${Math.random() * 100}%`
    })), []
  );

  const ambientParticles = useMemo(() =>
    Array.from({ length: 8 }, (_, i) => ({
      id: i,
      delay: i * 1.5,
      size: 6 + Math.random() * 10,
      x: `${10 + Math.random() * 80}%`,
      duration: 8 + Math.random() * 4
    })), []
  );

  const stars = useMemo(() =>
    Array.from({ length: 20 }, (_, i) => ({
      id: i,
      x: `${Math.random() * 100}%`,
      y: `${5 + Math.random() * 40}%`,
      size: 1 + Math.random() * 2,
      delay: Math.random() * 3
    })), []
  );

  const getGradientClass = () => {
    switch (weather) {
      case "sunny":
      case "clear":
        return "weather-gradient-sunny";
      case "cloudy":
        return "weather-gradient-cloudy";
      case "rainy":
        return "weather-gradient-rainy";
      case "snowy":
        return "weather-gradient-snowy";
      case "thunder":
        return "weather-gradient-thunder";
      case "foggy":
        return "weather-gradient-foggy";
      case "windy":
        return "weather-gradient-windy";
      case "mixed":
        return "weather-gradient-rainy";
      default:
        return "bg-background";
    }
  };

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={weather}
        className={`fixed inset-0 overflow-hidden ${className}`}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 1 }}
      >
        {/* Base gradient */}
        <div className={`absolute inset-0 ${getGradientClass()} opacity-30`} />
        
        {/* Weather-specific effects */}
        {(weather === "sunny" || weather === "clear") && <SunGlow />}
        
        {weather === "cloudy" && clouds.map(cloud => (
          <Cloud key={cloud.id} {...cloud} />
        ))}
        
        {weather === "rainy" && (
          <>
            {raindrops.map(drop => (
              <Raindrop key={drop.id} {...drop} />
            ))}
            {clouds.slice(0, 3).map(cloud => (
              <Cloud key={cloud.id} {...cloud} />
            ))}
          </>
        )}
        
        {weather === "snowy" && snowflakes.map(flake => (
          <Snowflake key={flake.id} {...flake} />
        ))}
        
        {weather === "thunder" && (
          <>
            <LightningFlash />
            {raindrops.map(drop => (
              <Raindrop key={drop.id} {...drop} />
            ))}
          </>
        )}
        
        {weather === "foggy" && (
          <>
            <FogLayer delay={0} opacity={0.4} />
            <FogLayer delay={5} opacity={0.3} />
            <FogLayer delay={10} opacity={0.5} />
          </>
        )}
        
        {weather === "windy" && windParticles.map(particle => (
          <WindParticle key={particle.id} {...particle} />
        ))}

        {weather === "mixed" && (
          <>
            <SunGlow />
            {raindrops.slice(0, 20).map(drop => (
              <Raindrop key={drop.id} {...drop} />
            ))}
          </>
        )}

        {/* Default background with mountains, stars, and ambient particles */}
        {weather === "default" && (
          <>
            {stars.map(star => (
              <Star key={star.id} {...star} />
            ))}
            {ambientParticles.map(particle => (
              <AmbientParticle key={particle.id} {...particle} />
            ))}
            <MountainSilhouette />
          </>
        )}

        {/* Overlay for depth */}
        <div className="absolute inset-0 bg-gradient-to-b from-background/80 via-background/40 to-background/90" />
      </motion.div>
    </AnimatePresence>
  );
};

export default WeatherBackground;