# 🌤️ Weather Data Engineering Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A production-ready, end-to-end data engineering pipeline that automates weather data collection, transformation, modeling, and visualization. Built with modern data stack: **Apache Airflow**, **DBT**, **PostgreSQL**, **Docker**, and **Apache Superset**.

---

## 📊 Live Dashboard Preview

![Dashboard Overview](docs/dashboard/dashboard_overview.jpg)

**Interactive Analytics Dashboard**: [http://127.0.0.1:8088/superset/dashboard/p/RLj1oydXdkB/](http://127.0.0.1:8088/superset/dashboard/p/RLj1oydXdkB/)

### Key Metrics & Visualizations
- 🌡️ Real-time temperature and humidity trends
- 🌬️ Wind speed and atmospheric pressure analysis
- ☁️ Cloud cover and precipitation monitoring
- 📈 Multi-dimensional correlation heatmaps
- 📊 Dynamic KPI gauges and time-series charts

---

## 🏗️ Architecture Overview

![Architecture Diagram](docs/images/weather-data.png)

### Data Flow
1. **Extract**: Fetch real-time weather data from Open-Meteo API
2. **Transform**: Clean and standardize data using Pandas
3. **Load**: Persist to PostgreSQL database
4. **Model**: Transform with DBT (staging → marts)
5. **Orchestrate**: Schedule and monitor via Apache Airflow
6. **Visualize**: Interactive dashboards in Apache Superset

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Orchestration** | Apache Airflow 2.x | Workflow automation and scheduling |
| **Data Transformation** | DBT Core | SQL-based modeling and testing |
| **Database** | PostgreSQL 14+ | Data warehouse |
| **Visualization** | Apache Superset | BI dashboards and analytics |
| **Containerization** | Docker & Docker Compose | Environment consistency |
| **API** | Open-Meteo API | Weather data source |
| **Language** | Python 3.8+ | ETL scripts |

---

## 📁 Project Structure

```
weather-data-project/
├── airflow/
│   └── dags/
│       └── weather_pipeline_dag.py    # Orchestration logic
├── api-request/
│   ├── api_request.py                 # API client
│   ├── transform_data.py              # Data cleaning
│   └── insert_records.py              # Database loader
├── dbt/
│   ├── my_project/
│   │   ├── models/
│   │   │   ├── staging/               # Raw data models
│   │   │   └── marts/                 # Business logic models
│   │   ├── tests/                     # Data quality tests
│   │   └── dbt_project.yml
│   └── profiles.yml                   # DBT connection config
├── docker/
│   ├── docker-bootstrap.sh            # Initialization script
│   ├── docker-init.sh                 # Service setup
│   └── superset_config.py             # Superset configuration
├── postgres/
│   ├── airflow_init.sql               # Airflow metadata DB
│   └── superset_init.sql              # Superset metadata DB
├── docs/
│   └── images/                        # Documentation assets
├── docker-compose.yml                 # Multi-container setup
├── requirements.txt                   # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Docker Desktop (v20.10+)
- Docker Compose (v2.0+)
- 8GB RAM minimum
- Ports available: 8080 (Airflow), 8088 (Superset), 5432 (PostgreSQL)

### Installation

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/noran-salm/weather-data-project.git
cd weather-data-project
```

#### 2️⃣ Start All Services
```bash
docker-compose up --build -d
```

**Services Starting:**
- PostgreSQL (port 5432)
- Apache Airflow Webserver (port 8080)
- Apache Airflow Scheduler
- DBT Container
- Apache Superset (port 8088)

⏱️ **Wait 2-3 minutes** for services to initialize completely.

#### 3️⃣ Verify Service Health
```bash
docker-compose ps
```

All services should show `healthy` or `running` status.

---

## 🔐 Access Credentials

| Service | URL | Username | Password |
|---------|-----|----------|----------|
| **Airflow** | http://localhost:8080 | `admin` | Check terminal logs |
| **Superset** | http://localhost:8088 | `admin` | `123456` |

---

## ⚙️ Configuration & Setup

### Initialize Superset (First-Time Only)
```bash
# Create admin user
docker exec -it superset_container superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@superset.com \
  --password 123456

# Upgrade database
docker exec -it superset_container superset db upgrade

# Initialize Superset
docker exec -it superset_container superset init
```

### Configure Database Connections

**Superset Connection String:**
```
postgresql://airflow:airflow@postgres:5432/airflow
```

**DBT Profile (`dbt/profiles.yml`):**
```yaml
my_project:
  target: dev
  outputs:
    dev:
      type: postgres
      host: postgres
      port: 5432
      user: db_user  
      password: db_password
      dbname: db
      schema: dev
      threads: 4
```

---

## 🎯 Running the Pipeline

### Option A: Airflow UI (Recommended)
1. Navigate to http://localhost:8080
2. Login with credentials
3. Locate `weather-api-dbt-orchestrator` DAG
4. Toggle **ON** to enable
5. Click **▶ Trigger DAG**

### Option B: Manual Execution
```bash
# Run ETL script
docker exec -it airflow_container python /opt/airflow/api-request/insert_records.py

# Run DBT models
docker exec -it dbt_container dbt run --project-dir /dbt/my_project

# Run DBT tests
docker exec -it dbt_container dbt test --project-dir /dbt/my_project
```

### Option C: Scheduled Execution
The DAG runs automatically based on the schedule defined in `weather_pipeline_dag.py`:
```python
schedule_interval='@hourly'  # Adjust as needed
```

---

## 📊 Using the Dashboard

1. Open http://localhost:8088
2. Navigate to **Dashboards** → **Weather Report**
3. Use filters to:
   - Select specific cities
   - Adjust date ranges
   - Compare metrics across regions
4. Export charts as PNG/PDF for reports

---

## 🧪 Data Quality & Testing

### Run DBT Tests
```bash
docker exec -it dbt_container dbt test --project-dir /dbt/my_project
```

### Available Tests
- **Schema validation**: Column types and constraints
- **Null checks**: Required fields completeness
- **Uniqueness**: Primary key integrity
- **Referential integrity**: Foreign key relationships
- **Range validation**: Temperature/humidity bounds

---

## 📈 Performance Optimization

### Database Indexing
```sql
-- Add indexes for frequent queries
CREATE INDEX idx_weather_city ON weather_data(city);
CREATE INDEX idx_weather_time ON weather_data(weather_time_local);
CREATE INDEX idx_weather_city_time ON weather_data(city, weather_time_local);
```

### DBT Incremental Models
```sql
-- models/staging/stg_weather_incremental.sql
{{ config(materialized='incremental', unique_key='id') }}

SELECT * FROM {{ source('raw', 'weather_data') }}
{% if is_incremental() %}
WHERE weather_time_local > (SELECT MAX(weather_time_local) FROM {{ this }})
{% endif %}
```

### API Rate Limiting
```python
# api-request/api_request.py
import time
from functools import wraps

def rate_limit(max_per_minute=60):
    min_interval = 60.0 / max_per_minute
    def decorator(func):
        last_called = [0.0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait = min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator
```

---

## 🔔 Monitoring & Alerts

### Configure Airflow Email Alerts
```python
# airflow/dags/weather_pipeline_dag.py
default_args = {
    'email': ['your-email@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}
```

### View Logs
```bash
# Airflow logs
docker exec -it airflow_container cat /opt/airflow/logs/scheduler/latest/*.log

# DBT logs
docker exec -it dbt_container cat /dbt/logs/dbt.log

# Application logs
tail -f logs/pipeline.log
```

---

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Find and kill process using port 8080
lsof -ti:8080 | xargs kill -9
```

**Database Connection Failed**
```bash
# Restart PostgreSQL container
docker-compose restart postgres

# Check database health
docker exec -it postgres psql -U airflow -d airflow -c "SELECT 1;"
```

**DBT Models Not Running**
```bash
# Debug DBT connection
docker exec -it dbt_container dbt debug --project-dir /dbt/my_project
```

**Airflow DAG Not Appearing**
```bash
# Refresh DAGs
docker exec -it airflow_container airflow dags list

# Check for syntax errors
docker exec -it airflow_container python -m py_compile /opt/airflow/dags/*.py
```

---

## 🧹 Cleanup

### Stop All Services
```bash
docker-compose down
```

### Remove Volumes (Full Reset)
```bash
docker-compose down -v
```

### Remove Images
```bash
docker-compose down --rmi all
```
---

## 📚 Additional Resources

- 📖 [Open-Meteo API Documentation](https://open-meteo.com/en/docs)
- 🛠️ [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- 🔧 [DBT Documentation](https://docs.getdbt.com/)
- 📊 [Apache Superset Documentation](https://superset.apache.org/docs/intro)
- 🐳 [Docker Compose Documentation](https://docs.docker.com/compose/)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Noran Salm**

- GitHub: [@noran-salm](https://github.com/noran-salm)
- LinkedIn: [Connect with me](https://www.linkedin.com/in/noran-salm)

---

## ⭐ Show Your Support

If this project helped you, please give it a ⭐️!

---

