import pandas as pd

def transform_weather_data(data, city="New York"):
    """Transform raw JSON from Open-Meteo into a clean DataFrame"""
    if not data or "hourly" not in data:
        raise ValueError("Invalid API response: 'hourly' field missing")

    hourly = data["hourly"]
    df = pd.DataFrame(hourly)

    # Add metadata
    df["city"] = city
    df["inserted_at_local"] = pd.Timestamp.now()

    print(f"✅ Transformed {len(df)} hourly records for {city}")
    return df
