api_url = (
    "https://api.open-meteo.com/v1/forecast?"
    "latitude=40.714&longitude=-74.006"
    "&hourly=temperature_2m,wind_speed_10m,relative_humidity_2m,pressure_msl,cloudcover,"
    "precipitation,dewpoint_2m,weathercode"
    "&timezone=America/New_York"
)

import requests

def fetch_weather_data():
    print('Fetching weather data from Open-Meteo API ...')
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print('API response succeeded')
        return response.json()
    except requests.exceptionpythons.RequestException as e:
        print('An error occurred:', e)
        raise

def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2025-09-24 16:50', 'localtime_epoch': 1758732600, 'utc_offset': '-4.0'}, 'current': {'observation_time': '08:50 PM', 'temperature': 25, 'weather_code': 113, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0001_sunny.png'], 'weather_descriptions': ['Sunny'], 'astro': {'sunrise': '06:46 AM', 'sunset': '06:49 PM', 'moonrise': '09:33 AM', 'moonset': '07:50 PM', 'moon_phase': 'Waxing Crescent', 'moon_illumination': 4}, 'air_quality': {'co': '468.05', 'no2': '115.255', 'o3': '65', 'so2': '19.24', 'pm2_5': '43.845', 'pm10': '44.215', 'us-epa-index': '3', 'gb-defra-index': '3'}, 'wind_speed': 9, 'wind_degree': 161, 'wind_dir': 'SSE', 'pressure': 1018, 'precip': 0, 'humidity': 69, 'cloudcover': 0, 'feelslike': 26, 'uv_index': 2, 'visibility': 14, 'is_day': 'yes'}}

