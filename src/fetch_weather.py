import os
import requests

#temperature, precipitation, cloud cover

def fetch_weather_by_coords(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric"
    }
    data = requests.get(url, params=params).json()
    return data["weather"]["main"]
