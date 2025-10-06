

# import psycopg2
# from api_request import fetch_data

# # ---- Connect to PostgreSQL ----
# def connect_to_db():
#     print("Connecting to PostgreSQL database...")
#     try:

#         print("✅ Connected to database")
#         return con
#     except psycopg2.Error as e:    
#         print(f"Database connection failed: {e}")
#         raise

# # ---- Create table ----
# def create_table(con):
#     print('Creating table if not exist...')
#     try:
#         cursor = con.cursor()
#         cursor.execute('''
#             CREATE SCHEMA IF NOT EXISTS dev;
#             CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
#                 id SERIAL PRIMARY KEY,
#                 city TEXT,
#                 time TIMESTAMP,
#                 temperature FLOAT,
#                 wind_speed FLOAT,
#                 humidity FLOAT,
#                 pressure FLOAT,
#                 cloudcover FLOAT,
#                 precipitation FLOAT,
#                 dewpoint FLOAT,
#                 weathercode INT,
#                 inserted_at TIMESTAMP DEFAULT NOW(),
#                 utc_offset TEXT
#             );
#         ''')
#         con.commit()
#         print('✅ Table created or already exists.')
#     except psycopg2.Error as e:
#         print(f'Failed to create table: {e}')
#         raise

# # ---- Insert records ----
# def insert_records(conn, data):
#     print("Inserting weather data into the database...")
    
#     try:
#         cursor = conn.cursor()
#         times = data['hourly']['time']
#         temps = data['hourly']['temperature_2m']
#         winds = data['hourly']['wind_speed_10m']
#         humidity = data['hourly'].get('relative_humidity_2m', [None]*len(times))
#         pressure = data['hourly'].get('pressure_msl', [None]*len(times))
#         cloudcover = data['hourly'].get('cloudcover', [None]*len(times))
#         precipitation = data['hourly'].get('precipitation', [None]*len(times))
#         dewpoint = data['hourly'].get('dewpoint_2m', [None]*len(times))
#         weathercode = data['hourly'].get('weathercode', [None]*len(times))

#         utc_offset = str(data.get('utc_offset_seconds', 0)/3600)
#         city = "New York" 

#         for i in range(len(times)):
#             cursor.execute(
#                 """
#                 INSERT INTO dev.raw_weather_data (
#                     city, time, temperature, wind_speed, humidity, pressure,
#                     cloudcover, precipitation, dewpoint, weathercode, inserted_at, utc_offset
#                 ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s);
#                 """,
#                 (
#                     city,
#                     times[i],
#                     temps[i],
#                     winds[i],
#                     humidity[i],
#                     pressure[i],
#                     cloudcover[i],
#                     precipitation[i],
#                     dewpoint[i],
#                     weathercode[i],
#                     utc_offset
#                 )
#             )

#         conn.commit()
#         print("✅ Data successfully inserted")
#     except psycopg2.Error as e:
#         print(f"❌ Error inserting data: {e}")
#         raise

# # ---- Main flow ----
# def main():
#     try:
#         data = fetch_data()
#         con = connect_to_db()
#         create_table(con)
#         insert_records(con, data)
#         print("Data inserted successfully.")
#         print(data['hourly'].keys())


#     finally:
#         if 'con' in locals():
#             con.close()
#             print("Database connection closed.")
#             print(data['hourly'].keys())


# if __name__ == "__main__":
#     main()


# api-request/insert_records.py
# import psycopg2
# from api_request import fetch_weather_data
# from transform_data import transform_weather_data

# DB_CONFIG = {
#     "host": "localhost",
#     "port": 5000,
#     "dbname": "db",
#     "user": "db_user",
#     "password": "db_password"
# }

# def connect_to_db():
#     """Create a connection to PostgreSQL"""
#     print("🔌 Connecting to PostgreSQL database...")
#     return psycopg2.connect(**DB_CONFIG)

# def create_table(cursor):
#     """Create table if it doesn't exist"""
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
#             id SERIAL PRIMARY KEY,
#             city TEXT,
#             time TIMESTAMP,
#             temperature FLOAT,
#             wind_speed FLOAT,
#             humidity FLOAT,
#             pressure FLOAT,
#             cloudcover FLOAT,
#             precipitation FLOAT,
#             dewpoint FLOAT,
#             weathercode INT,
#             inserted_at TIMESTAMP DEFAULT NOW(),
#             inserted_at_local TIMESTAMP,
#             utc_offset TEXT
#         );
#     """)
#     print("✅ Table ensured (created if not exists)")

# def insert_data(cursor, df):
#     """Insert records into PostgreSQL"""
#     for _, row in df.iterrows():
#         cursor.execute("""
#             INSERT INTO dev.raw_weather_data (
#                 city, time, temperature, wind_speed, humidity, pressure,
#                 cloudcover, precipitation, dewpoint, weathercode, inserted_at_local
#             )
#             VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
#         """, (
#             row["city"],
#             row["time"], 
#             row["temperature_2m"], 
#             row["wind_speed_10m"],
#             row.get("relative_humidity_2m"), 
#             row.get("pressure_msl"),
#             row.get("cloudcover"), 
#             row.get("precipitation"),
#             row.get("dewpoint_2m"), 
#             row.get("weathercode"),
#         ))

# def main():
#     data = fetch_weather_data()
#     df = transform_weather_data(data)

#     with connect_to_db() as conn:
#         with conn.cursor() as cur:
#             create_table(cur)
#             insert_data(cur, df)
#         conn.commit()

#     print("🎉 Data successfully inserted into PostgreSQL!")

# if __name__ == "__main__":
#     main()





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
            row.get("inserted_at_local"),  # ✅ لازم يكون موجود في transform
            row.get("utc_offset")          # ✅ أضفنا العمود الأخير كمان
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






