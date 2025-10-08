# 🌤️ Weather Data Engineering Pipeline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A **production-ready, end-to-end weather data engineering pipeline** that automates extraction, transformation, modeling, and visualization. Built using **Airflow**, **DBT**, **PostgreSQL**, **Docker**, and **Superset**.  

---

## 📊 Live Dashboard Preview

![Dashboard Overview](docs/dashboard/dashboard_overview.jpg)

### Key Metrics & Visualizations
- 🌡️ Temperature & humidity trends (hourly/daily)
- 🌬️ Wind speed & atmospheric pressure analysis
- ☁️ Cloud cover & precipitation monitoring
- 📈 Correlation heatmaps
- 📊 Dynamic KPI gauges & time-series charts

---

## 🏗️ Architecture Overview

![Architecture Diagram](docs/images/architecture_overview.png)

**Data Flow**:

1. **Extract**: Fetch real-time weather data from [Open-Meteo API](https://open-meteo.com/en/docs)  
2. **Transform**: Clean & standardize using Pandas  
3. **Load**: Persist to PostgreSQL database  
4. **Model**: DBT transformations (staging → marts)  
5. **Orchestrate**: Schedule & monitor via Airflow DAGs  
6. **Visualize**: Interactive dashboards in Superset  

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Orchestration | Apache Airflow 2.x | Workflow automation & scheduling |
| Transformation | DBT Core | SQL-based modeling & testing |
| Database | PostgreSQL 14+ | Data warehouse |
| Visualization | Apache Superset 3.x | BI dashboards |
| Containerization | Docker & Compose | Environment consistency |
| API | Open-Meteo API | Weather data source |
| Language | Python 3.8+ | ELT scripts |

---

## 📁 Project Structure

```
.
├── README.md
├── __pycache__
│   └── api_request.cpython-312.pyc
├── airflow
│   └── dags
├── api-request
│   ├── __pycache__
│   ├── api_request.py
│   ├── insert_records.py
│   └── transform_data.py
├── dbt
│   ├── dbt_internal_packages
│   ├── dbt_project.yml
│   ├── logs
│   ├── my_project
│   ├── profiles.yml
│   └── target
├── docker
│   ├── docker-bootstrap.sh
│   ├── docker-init.sh
│   └── superset_config.py
├── docker-compose.yml
├── docs
│   ├── dashboard
│   └── images
├── postgres
│   ├── airflow_init.sql
│   └── superset_init.sql
└── venv
    ├── bin
    ├── lib
    ├── lib64
    └── pyvenv.cfg
```
---

## ⚠️ LF / CRLF Line Endings Issue (Windows)

Previously, working on Windows caused issues with Git and Docker due to inconsistent line endings (CRLF vs LF).  

✅ **Solution Implemented:**
- Created a temporary branch `bugs_LF_CRLF` to fix all line endings.
- Normalized all files to LF for cross-platform compatibility.
- Merged the fix back into `main`.
- Configured Git to handle line endings automatically:
  ```bash
  git config --global core.autocrlf true  # For Windows users
---

## 🚀 Getting Started

### Prerequisites
- Docker Desktop v20.10+  
- Docker Compose v2.0+  
- 8GB RAM minimum  
- Available ports: 8080 (Airflow), 8088 (Superset), 5432 (PostgreSQL)

### Installation

#### 1️⃣ Clone the Repository
```bash
git clone https://github.com/noran-salm/weather-data-project.git
cd weather-data-project

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
- PostgreSQL 
- Apache Airflow Webserver 
- Apache Airflow Scheduler
- DBT Container
- Apache Superset 

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
The DAG runs automatically based on the schedule defined in `orchetstrator.py`:
```python
schedule=timedelta(minutes=5)  # Adjust as needed
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

## 🔔 Monitoring & Alerts

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

## 👤 About the Author

**Noran Salm** – Data & Software Engineering Enthusiast  

- GitHub: [@noran-salm](https://github.com/noran-salm)  
- LinkedIn: [Connect with me](https://www.linkedin.com/in/noran-salm)  
- Passionate about building scalable data pipelines, automation, and modern analytics solutions.  
- Actively contributing to open-source projects and exploring cloud/data engineering tools like Airflow, DBT, PostgreSQL, and Azure.  

⭐ If this project helped you, feel free to give it a star on GitHub!


---
