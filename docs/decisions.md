# Technical Decisions

## Overview

This document records the main technical decisions made during the development of the Crypto ETL Pipeline.

## Python

Python was selected as the primary language because of its ecosystem for data processing, API integration, automation, and testing.

The project uses:

* Pandas
* Requests
* SQLAlchemy
* Pydantic Settings
* Pytest

## PostgreSQL

PostgreSQL was selected as the persistence layer because the project requires:

* relational data modeling
* constraints
* indexes
* transactions
* historical querying
* reliable data integrity

The database is executed through Docker for easier environment setup and reproducibility.

## SQLAlchemy

SQLAlchemy is used as the database abstraction layer.

The ORM allows the project to represent database entities as Python models while keeping database operations organized inside a repository layer.

## Repository Pattern

Database operations are centralized in:

```text
CryptoRepository
```

This avoids placing SQL/database logic directly inside the ETL orchestration code.

The separation makes the application easier to maintain and test.

## Historical Snapshots

The project intentionally preserves historical observations instead of updating existing cryptocurrency records.

The snapshot identity is:

```text
coin_id + etl_timestamp
```

This design allows the database to answer historical questions such as:

```text
How did the market data change between ETL executions?
```

while still preventing duplicate snapshots.

## Data Validation

Validation is implemented at multiple levels.

### Application Level

The transformation layer validates:

* required columns
* data structure
* duplicates
* derived metrics

### Database Level

PostgreSQL constraints validate important numerical fields.

This creates defense in depth: invalid data should be detected before or during persistence.

## Transaction Management

Database writes are transactional.

If a batch contains invalid data, the entire operation is rolled back.

This was chosen to prevent partial datasets from being persisted.

## API Retry Strategy

The extraction layer uses retries and backoff for temporary API failures.

This improves resilience against:

* temporary server errors
* connection failures
* rate limiting

Request timeouts are also configured to prevent indefinitely hanging requests.

## Pagination

Pagination was implemented so the extraction process is not restricted to a single API page.

The number of pages is configurable through application settings.

This allows the pipeline to scale the number of extracted cryptocurrencies without changing the extraction logic.

## Configuration Management

Configuration is centralized using Pydantic Settings and environment variables.

This prevents environment-specific values from being hardcoded into application modules.

Examples include:

```text
API configuration
Database configuration
Pagination
Timeouts
Retry parameters
Request delays
```

## Testing Strategy

Pytest was selected to validate critical business and infrastructure behavior.

The tests prioritize:

```text
Data quality
Database integrity
Transaction behavior
Historical preservation
Input validation
Transformation correctness
```

The final test suite contains 31 passing tests.

## Future Improvements

Potential improvements include:

* GitHub Actions CI/CD
* Code coverage reporting
* Alembic database migrations
* Pipeline orchestration
* Monitoring and alerting
* Structured logging
* Analytical database views
* Dashboard integration
* Apache Airflow evaluation

These improvements are intentionally separated from the current implementation to keep the core project focused and maintainable.
