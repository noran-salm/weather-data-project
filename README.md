# 🌤️ Weather Data Pipeline Project

A full **end-to-end Data Engineering pipeline** that automates weather data collection, transformation, modeling, and visualization using **Python, DBT, Airflow, Superset, PostgreSQL, and Docker**.

---

## 🧩 Project Structure

.
├── README.md
├── __pycache__
│   └── api_request.cpython-312.pyc
├── airflow
│   └── dags
├── api-request
│   ├── __pycache__
│   ├── api_request.py
│   ├── insert_records.py
│   └── transform_data.py
├── dashboards
│   ├── dashboard_export_20251006T190505.zip
│   └── dashboard_overview.jpg
├── dbt
│   ├── logs
│   ├── my_project
│   └── profiles.yml
├── docker
│   ├── docker-bootstrap.sh
│   ├── docker-init.sh
│   └── superset_config.py
├── docker-compose.yml
├── logs
│   └── dbt.log
├── postgres
│   ├── airflow_init.sql
│   └── superset_init.sql
├── var
│   └── run
└── venv
    ├── bin
    ├── include
    ├── lib
    ├── lib64 -> lib
    └── pyvenv.cfg

## ⚙️ Key Components

| Component | Description |
|------------|-------------|
| **API Layer** | Fetches real-time weather data using Open-Meteo API |
| **Transform Layer** | Cleans and prepares the API response for database storage |
| **Load Layer** | Inserts the transformed data into PostgreSQL |
| **DBT Layer** | Models the raw data into analytics-ready tables |
| **Airflow Layer** | Automates the entire process via a DAG |
| **Visualization Layer** | Dashboards in Superset display key metrics |

---

## 🧠 Examples for Each Stage

### 1️⃣ API Request (Extract)

**File:** `api-request/api_request.py`
python
import requests

def fetch_weather_data(api_url):
    print('Fetching weather data from Open-Meteo API ...')
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        print('✅ API response succeeded')
        return response.json()
    except requests.exceptions.RequestException as e:
        print('❌ An error occurred:', e)
        raise
🧩 This script pulls hourly weather data for Cairo and prints it in JSON format.

2️⃣ Data Transformation
File: api-request/transform_data.py

python
Copy code
import pandas as pd

def transform_weather_data(data, city="New York"):
    """Transform raw JSON from Open-Meteo into a clean DataFrame"""
    if not data or "hourly" not in data:
        raise ValueError("Invalid API response: 'hourly' field missing")

    hourly = data["hourly"]
    df = pd.DataFrame(hourly)

    df["city"] = city
    df["inserted_at_local"] = pd.Timestamp.now()

    print(f"✅ Transformed {len(df)} hourly records for {city}")
    return df
🧩 Cleans and converts timestamps, adds city name, and standardizes columns.

3️⃣ Insert into Database (Load)
File: api-request/insert_records.py

python
Copy code
def insert_data(cursor, df):
    """Insert records into PostgreSQL"""
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dev.raw_weather_data (
                city, time, temperature, wind_speed, humidity, pressure,
                cloudcover, precipitation, dewpoint, weathercode,
                inserted_at_local, utc_offset
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
🧩 Loads the cleaned weather data into PostgreSQL.

4️⃣ DBT Modeling
Example: dbt/my_project/models/mart/daily_average.sql

sql
Copy code
{{ config(materialized='table') }}

SELECT
    city,
    DATE(weather_time_local) AS date,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temperature,
    ROUND(AVG(wind_speed)::numeric, 2) AS avg_wind_speed,
    ROUND(AVG(humidity)::numeric, 2) AS avg_humidity,
    ROUND(AVG(pressure)::numeric, 2) AS avg_pressure,
    ROUND(AVG(cloudcover)::numeric, 2) AS avg_cloudcover,
    ROUND(AVG(precipitation)::numeric, 2) AS avg_precipitation,
    ROUND(AVG(dewpoint)::numeric, 2) AS avg_dewpoint,
    ROUND(AVG(weathercode)::numeric, 0) AS avg_weathercode
FROM {{ ref('stg_weather_data') }}
GROUP BY city, DATE(weather_time_local)
ORDER BY city, DATE(weather_time_local)
🧩 Aggregates hourly weather data into daily averages for dashboard use.

5️⃣ Airflow DAG (Automation)
File: airflow/dags/orchestrator.py

python
Copy code
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
import sys

sys.path.append('/opt/airflow/api-request')

def safe_main_callable():
    from insert_records import main
    return main()

default_args = {
    'owner': 'airflow',
    'retries': 3,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
    dag_id='weather-api-dbt-orchestrator',
    default_args=default_args,
    description='A DAG to orchestrate data',
    start_date=datetime(2025, 9, 27),
    schedule=timedelta(minutes=5),
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='ingest_data_task',
        python_callable=safe_main_callable
    )

    task2 = DockerOperator(
        task_id='transform_data_task',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir='/usr/app',
        mounts=[
            Mount(source=f'{HOST_PROJECT_PATH}/dbt/my_project', target='/usr/app', type='bind'),
            Mount(source=f'{HOST_PROJECT_PATH}/dbt/profiles.yml', target='/root/.dbt/profiles.yml', type='bind', read_only=True)
        ],
        network_mode='weather-data-project_my_network',
        docker_url='unix:///var/run/docker.sock',
        environment={'DBT_PROFILES_DIR': '/root/.dbt'},
        auto_remove='success',
        retrieve_output=True,
        mount_tmp_dir=False,
    )

    task1 >> task2
🧩 Automates your API → DBT transformation every 5 minutes.

6️⃣ Superset Dashboard Charts
Temperature & Humidity Trend

Cloud Cover Gauge

Temperature Distribution Histogram

Correlation Heatmap

🧩 All exported dashboards are in /dashboards/dashboard_export_*.zip

🚀 How to Run the Full Project
🪄 Step 1: Clone the Repo
bash
Copy code
git clone https://github.com/noran-salm/weather-data-project.git
cd weather-data-project
🐍 Step 2: (Optional) Create Virtual Env
bash
Copy code
python -m venv venv
source venv/bin/activate
🐳 Step 3: Build Docker Containers
bash
Copy code
docker-compose up --build
🧭 Step 4: Access the Services
Service	URL	Default Credentials
Airflow	http://localhost:8080	admin / (generated password)
Superset	http://localhost:8088	admin / 123456

🧰 Step 5: Initialize Superset (first run only)
bash
Copy code
docker exec -it superset_container superset fab create-admin
docker exec -it superset_container superset db upgrade
docker exec -it superset_container superset init
⚙️ Step 6: Run DBT Models
bash
Copy code
docker exec -it dbt_container dbt run
📅 Step 7: Trigger Airflow DAG
Go to Airflow UI → enable weather-api-dbt-orchestrator → “Trigger DAG”.

📊 Step 8: View Dashboards
Open Superset → Dashboards → Weather Report → enjoy live weather metrics 🌦️

📊 Dashboard Preview

📚 References
Open-Meteo API Docs

Apache Airflow Docs

DBT Core Docs

Apache Superset Docs

Docker Documentation

🧾 License
MIT License © 2025 Noran Salm

yaml
Copy code

---

### 📸 For your repo visuals
Add 1–3 screenshots under:
dashboards/dashboard_image/

markdown
Copy code
Example names:
- `dashboard_overview.jpg`
- `temperature_trend.png`
- `correlation_heatmap.png`

Then reference them like:
```markdown
![Dashboard Overview](dashboards/dashboard_image/dashboard_overview.jpg)
