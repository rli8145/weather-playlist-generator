import os
import requests
from dotenv import load_dotenv

# [thunderstorm, drizzle, rain], snow, clear, [atmosphere, clouds]

load_dotenv()

def fetch_weather_by_coords(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric"
    }
    data = requests.get(url, params=params).json()

    conditions = data["weather"][0]["main"]
    if conditions in ["Thunderstorm", "Drizzle", "Rain"]:
        return "rain"
    if conditions in ["Atmosphere", "Clouds"]:
        return "clouds"
    else:
        return conditions.lower()
    
# display conditions, temp, cloud cover, precipitation, icon also

