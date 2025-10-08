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

