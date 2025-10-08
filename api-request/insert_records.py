import psycopg2
from api_request import fetch_weather_data
from transform_data import transform_weather_data

DB_CONFIG = {
    "host": "db",
    "port": 5432,
    "dbname": "db",
    "user": "db_user",
    "password": "db_password"
}

def connect_to_db():
    """Create a connection to PostgreSQL"""
    print("🔌 Connecting to PostgreSQL database...")
    return psycopg2.connect(**DB_CONFIG)

def create_table(cursor):
    """Create table if it doesn't exist"""
    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS dev;

        CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
            id SERIAL PRIMARY KEY,
            city TEXT,
            time TIMESTAMP,
            temperature FLOAT,
            wind_speed FLOAT,
            humidity FLOAT,
            pressure FLOAT,
            cloudcover FLOAT,
            precipitation FLOAT,
            dewpoint FLOAT,
            weathercode INT,
            inserted_at TIMESTAMP DEFAULT NOW(),
            inserted_at_local TIMESTAMP,
            utc_offset TEXT
        );
    """)
    print("✅ Table ensured (created if not exists)")

def insert_data(cursor, df):
    """Insert records into PostgreSQL"""
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dev.raw_weather_data (
                city, time, temperature, wind_speed, humidity, pressure,
                cloudcover, precipitation, dewpoint, weathercode, inserted_at_local, utc_offset
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (
            row.get("city"),
            row.get("time"),
            row.get("temperature_2m"),
            row.get("wind_speed_10m"),
            row.get("relative_humidity_2m"),
            row.get("pressure_msl"),
            row.get("cloudcover"),
            row.get("precipitation"),
            row.get("dewpoint_2m"),
            row.get("weathercode"),
            row.get("inserted_at_local"),  
            row.get("utc_offset")          
        ))


def main():
    print("Fetching weather data from Open-Meteo API ...")
    data = fetch_weather_data()
    print("API response succeeded")

    df = transform_weather_data(data)
    print(f"✅ Transformed {len(df)} hourly records for {df['city'].iloc[0]}")

    with connect_to_db() as conn:
        with conn.cursor() as cur:
            create_table(cur)
            insert_data(cur, df)
        conn.commit()

    print("🎉 Data successfully inserted into PostgreSQL!")

if __name__ == "__main__":
    main()






