# Architecture

## Overview

The Crypto ETL Pipeline is organized into separate layers responsible for data extraction, transformation, loading, database access, and configuration.

The main workflow is:

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

## Application Layers

### Extract

`app/Extract.py`

Responsible for retrieving cryptocurrency market data from the CoinGecko API.

Main responsibilities:

* API communication
* Pagination
* Request timeout
* Retry strategy
* Temporary API failure handling
* Response validation
* Session management

The extraction layer uses `requests.Session` with an `HTTPAdapter` and retry configuration.

### Transform

`app/Transform.py`

Responsible for preparing raw API data for database storage.

The transformation workflow is:

```text
Validate columns
      ↓
Select required columns
      ↓
Standardize column names
      ↓
Clean data
      ↓
Remove duplicates
      ↓
Calculate metrics
      ↓
Add ETL timestamp
```

The transformation layer also calculates the `liquidity_ratio` metric.

### Load

`app/Load.py`

Responsible for loading the transformed DataFrame into PostgreSQL.

The loading process delegates database persistence to `CryptoRepository`.

Empty DataFrames are ignored and logged without attempting a database insertion.

### Database

The database layer is divided into:

```text
app/database/
├── Database.py
├── Models.py
└── Repository.py
```

#### Database.py

Responsible for:

* SQLAlchemy engine configuration
* Database sessions
* Transaction management

#### Models.py

Defines the SQLAlchemy database models and constraints.

#### Repository.py

Contains database operations such as:

* inserting cryptocurrency snapshots
* removing old snapshots

This separation keeps database operations independent from the ETL orchestration logic.

### Configuration

`config/settings.py`

Application configuration is centralized using Pydantic Settings.

Configuration values include:

* CoinGecko API URL
* API currency
* API ordering
* records per page
* number of pages
* request timeout
* request delay
* retry configuration
* database configuration

Environment-specific values are loaded through environment variables.

## Data Flow

A complete pipeline execution follows:

```text
1. Extract raw data from CoinGecko
2. Validate API response
3. Transform the raw dataset
4. Calculate derived metrics
5. Add ETL execution timestamp
6. Load snapshots into PostgreSQL
7. Preserve historical records
```

## Design Principles

The architecture follows several principles:

* Separation of responsibilities
* Centralized configuration
* Repository pattern for database operations
* Explicit data validation
* Transactional database operations
* Historical data preservation
* Logging and error propagation
* Testable application components

The goal is to keep each layer focused on a specific responsibility while allowing the complete pipeline to operate as a single workflow.
