# 🌦️ Weather Data Project

## 🧭 Overview
The **Weather Data Project** is a full data engineering and visualization pipeline for collecting, storing, analyzing, and visualizing **weather data**.  
It automates data ingestion from weather APIs, performs data cleaning and aggregation, stores results in a **PostgreSQL** database, and visualizes insights through an **Apache Superset** dashboard.

### 🎯 Who is it for?
- Data engineers and analysts learning weather data pipelines  
- Students or researchers studying climate or environmental data  
- Developers building weather-aware applications or dashboards  

### 🧰 Main Technologies
- **Python** – Data collection and processing (Pandas, Requests, SQLAlchemy)  
- **PostgreSQL** – Relational database for storage  
- **Apache Superset** – Interactive BI dashboard  
- **Docker & Docker Compose** – Containerized environment  
- **Plotly** – Data visualization  

---

## 🌟 Features
- 🌍 Fetches **real-time** and **forecast** weather data from APIs  
- 🕒 Supports **historical** data ingestion and analysis  
- 🧹 Cleans, normalizes, and aggregates data (daily averages, trends)  
- 💾 Stores data in **PostgreSQL** for persistence  
- 📊 Visualizes KPIs, distributions, and trends using Superset or Plotly  
- ⚙️ Configurable data sources and ETL scripts  
- 🧩 Extensible and open-source design  

---

## 🗂️ Project Structure
```bash
weather-data-project/
├── README.md
├── requirements.txt
├── docker-compose.yml
├── .env.example
├── src/
│   ├── api.py            # Flask API (optional)
│   ├── db.py             # Database connection (SQLAlchemy)
│   └── utils.py          # Helper functions
├── scripts/
│   ├── ingest.py         # Fetch weather data<img width="958" height="472" alt="Screenshot 2025-10-02 145951" src="https://github.com/user-attachments/assets/163f0f03-ffb5-4815-af3b-71e37052ff72" />

│   └── etl.py            # Transform & aggregate data
├── dashboards/           # Superset dashboard exports (.json)
├── notebooks/            # Jupyter notebooks for analysis
└── tests/                # Unit tests

