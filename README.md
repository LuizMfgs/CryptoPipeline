Crypto Market ETL & Analytics

An end-to-end Data Engineering project that extracts cryptocurrency market data from the CoinGecko API, validates data quality, stores historical records in PostgreSQL, and provides an interactive dashboard built with Streamlit.

The project demonstrates a complete ETL workflow, including data extraction, transformation, validation, storage, visualization, and automated execution.

---

# Project Overview

This project was developed to simulate a production-ready data pipeline used in financial analytics environments.

The pipeline:

- Extracts cryptocurrency market data from the CoinGecko API
- Cleans and transforms the dataset
- Performs automated data quality validation
- Loads data into PostgreSQL
- Preserves historical records
- Powers an interactive Streamlit dashboard
- Supports scheduled automatic execution

---

# Architecture

```text
CoinGecko API
       │
       ▼
Extract.py
       │
       ▼
Transform.py
       │
       ▼
Quality.py
       │
       ▼
Load.py
       │
       ▼
PostgreSQL
       │
       ▼
Dashboard.py (Streamlit)
```

---



# Technologies

- Python
- Pandas
- SQLAlchemy
- PostgreSQL
- Streamlit
- CoinGecko API
- Requests
- Logging

---

# Dashboard Features

The dashboard includes:

- Market Overview KPIs
- Top 20 Cryptocurrencies
- Top Market Cap
- Highest Liquidity Ratio
- Largest 24h Gains
- Highest Trading Volume
- Automatic Last Update timestamp

---

# Data Quality Validation

Before loading the data, the pipeline automatically validates:

- Empty datasets
- Missing prices
- Missing market capitalization
- Negative prices
- Duplicate records
- Missing values

If any validation fails, the pipeline stops before loading data.

---

# Database

The project uses PostgreSQL for persistent storage.

Historical market snapshots are preserved, allowing time-series analysis.

Old records can be automatically removed after a configurable retention period (default: 7 days).

---

# Automation

The ETL pipeline is designed to run automatically every 30 minutes.

Execution logs are stored in the logs folder.

Each execution:

- extracts new market data
- validates quality
- stores historical records
- updates the dashboard source

---

# Environment Variables

Database credentials are stored securely using a `.env` file.

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto_db
DB_USER=postgres
DB_PASSWORD=your_password
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/LuizMfgs/crypto-etl.git
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate it

Windows

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the ETL Pipeline

```bash
python app/pipeline.py
```

---

# ▶️ Running the Dashboard

```bash
streamlit run app/Dashboard.py
```

---

#  Future Improvements

- Docker support
- Apache Airflow orchestration
- Unit and integration tests
- CI/CD pipeline using GitHub Actions
- Cloud deployment (AWS or Azure)
- Real-time market monitoring
- Email alerts for data quality failures
- REST API for historical data

---

#  Author

**Luiz Miguel Fernandes**

Data Engineering | Python | SQL | PostgreSQL | ETL | Data Analytics
