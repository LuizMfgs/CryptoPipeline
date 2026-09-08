# Crypto ETL Pipeline

ETL pipeline for cryptocurrency market data using **Python, CoinGecko API and PostgreSQL**.

The project extracts market data, transforms and validates the dataset, calculates derived metrics, and stores historical snapshots in PostgreSQL.

## Architecture

```text
CoinGecko API
      ↓
   Extract
      ↓
  Transform
      ↓
     Load
      ↓
 PostgreSQL
```

## Features

* CoinGecko API extraction with pagination
* HTTP retries and timeout handling
* Data validation and cleaning
* Duplicate removal
* Liquidity ratio calculation
* Historical cryptocurrency snapshots
* PostgreSQL constraints and indexes
* Transaction rollback
* Old snapshot cleanup
* Dockerized PostgreSQL
* Automated tests

## Tech Stack

* Python 3.13
* Pandas
* Requests
* PostgreSQL
* SQLAlchemy
* Pydantic Settings
* Pytest
* Docker

## Project Structure

```text
Cripto-ETL/
├── app/
│   ├── Extract.py
│   ├── Transform.py
│   ├── Load.py
│   └── database/
│       ├── Database.py
│       ├── Models.py
│       └── Repository.py
├── config/
│   └── settings.py
├── tests/
├── docker-compose.yml
├── .env.example
├── LICENSE
└── README.md
```

## Installation

Create the virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Configure the environment variables using `.env.example`.

## Database

Start PostgreSQL with Docker:

```powershell
docker compose up -d
```

Check the container:

```powershell
docker compose ps
```

## Running the Pipeline

```powershell
python -m app.Pipeline
```

The pipeline executes:

```text
Extract → Transform → Load
```

## Testing

Run the complete test suite:

```powershell
python -m pytest tests -v
```

Current test status:

```text
31 passed
```

The tests cover:

* Database connectivity
* Database constraints
* Transaction rollback
* Batch rollback
* Duplicate snapshots
* Multiple historical snapshots
* Empty DataFrames
* Data cleanup
* Extraction validation
* Data transformation
* Duplicate removal
* Liquidity ratio calculation
* ETL timestamp validation

## Historical Snapshots

The pipeline preserves historical cryptocurrency observations instead of overwriting previous records.

Snapshots are identified by:

```text
coin_id + etl_timestamp
```

This allows the same cryptocurrency to be stored across multiple ETL executions while preventing duplicate snapshots.

## Future Improvements

* Add CI/CD with GitHub Actions
* Add code coverage reporting
* Add database migrations with Alembic
* Add pipeline scheduling
* Add monitoring and alerting
* Add analytical views for historical data
* Add a data visualization dashboard
* Evaluate orchestration with Apache Airflow
* Improve observability with structured logging

## Documentation

Additional technical documentation can be found in the `docs/` directory:

* `architecture.md` — system architecture
* `data-model.md` — database structure
* `pipeline.md` — ETL workflow
* `testing.md` — testing strategy
* `decisions.md` — main technical decisions

## Author

**Luiz Miguel Fernandes**

Data / Infrastructure Engineering

## License

MIT License.
