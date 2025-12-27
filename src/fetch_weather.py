import os
import requests

#temperature, precipitation, cloud cover

def fetch_by_coords(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric"
    }
    return requests.get(url, params=params).json()

def fetch_weather(data):
    return {
        "temperature": data["main"]["temp"],
        "precipitation": data.get("rain", {}).get("1h", 0),
        "cloud_cover": data["clouds"]["all"]
    }