import { useState } from "react";
import { motion } from "framer-motion";
import { Radio } from "lucide-react";
import { WeatherBackground, type WeatherType } from "@/components/weather/WeatherBackground";
import SongWeather from "@/components/SongWeather";

const Index = () => {
  const [activeWeather, setActiveWeather] = useState<WeatherType>("default");

  return (
    <div className="relative min-h-screen overflow-hidden">
      {/* Dynamic Weather Background */}
      <WeatherBackground weather={activeWeather} />

      {/* Content */}
      <div className="relative z-10 min-h-screen flex flex-col">
        {/* Header */}
        <motion.header 
          className="pt-8 pb-4 px-6"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="max-w-4xl mx-auto flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="relative">
                <Radio className="w-8 h-8 text-primary" />
                <motion.div
                  className="absolute inset-0"
                  animate={{ scale: [1, 1.5, 1], opacity: [0.5, 0, 0.5] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  <Radio className="w-8 h-8 text-primary" />
                </motion.div>
              </div>
              <div>
                <h1 className="text-2xl font-display font-bold text-foreground glow-text">
                  Forecast.fm
                </h1>
                <p className="text-xs text-muted-foreground">
                  Matching songs to weather conditions
                </p>
              </div>
            </div>
          </div>
        </motion.header>

        {/* Main Content */}
        <main className="flex-1 flex flex-col items-center justify-center px-6 pb-12">
          {/* Hero Text */}
          <motion.div 
            className="text-center mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <h2 className="text-4xl md:text-5xl font-display font-bold text-foreground mb-4">
              Feel the <span className="text-primary">MUSIC</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-md mx-auto">
              A Weather-Conditioned Music Classification Engine
            </p>
          </motion.div>

          {/* Song Weather Feature */}
          <div className="w-full max-w-lg">
            <SongWeather onWeatherChange={setActiveWeather} />
          </div>
        </main>

        {/* Footer */}
        <motion.footer 
          className="py-6 text-center text-sm text-muted-foreground"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <p>Built by Daniel Kwan and Ryan Li</p>
        </motion.footer>
      </div>
    </div>
  );
};

export default Index;
