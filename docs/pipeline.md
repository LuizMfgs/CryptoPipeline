# ETL Pipeline

## Overview

The pipeline follows the traditional ETL architecture:

```text
Extract → Transform → Load
```

The objective is to collect cryptocurrency market data, prepare it for analytical use, and store historical snapshots in PostgreSQL.

## Extract

The extraction process communicates with the CoinGecko API.

The API request uses configurable parameters such as:

```text
vs_currency
order
per_page
page
```

Pagination allows multiple API pages to be extracted during a single execution.

### Retry Strategy

Temporary HTTP failures are handled through the configured retry mechanism.

The extraction layer uses:

* retry attempts
* exponential backoff
* HTTP status validation
* request timeout
* `Retry-After` support
* controlled request delays

This reduces the impact of temporary API failures and rate limiting.

### Response Validation

Each API response is checked before being added to the extraction result.

The pipeline expects the API response to contain a list of cryptocurrency records.

Unexpected responses are logged and skipped.

## Transform

The transformation stage converts raw API data into the structure expected by PostgreSQL.

The process consists of:

```text
Raw Data
   ↓
Column Validation
   ↓
Column Selection
   ↓
Column Standardization
   ↓
Data Cleaning
   ↓
Duplicate Removal
   ↓
Metric Calculation
   ↓
ETL Timestamp
   ↓
Transformed Data
```

### Duplicate Removal

Duplicates within the current extraction are removed before loading.

This prevents the same cryptocurrency from being unnecessarily inserted multiple times during one extraction.

### Derived Metrics

The pipeline calculates:

```text
liquidity_ratio =
(total_volume / market_cap) × 100
```

The result is rounded to two decimal places.

### ETL Timestamp

Each transformed record receives an `etl_timestamp`.

This timestamp identifies when the ETL execution produced the snapshot.

It also enables historical data preservation.

## Load

The Load stage receives the transformed DataFrame and delegates persistence to:

```text
CryptoRepository.insert_snapshots()
```

The repository converts DataFrame records into SQLAlchemy model objects and persists them using a database transaction.

## Empty Data

If the transformation or extraction produces an empty DataFrame, the pipeline does not attempt unnecessary database operations.

The condition is logged and the load operation returns:

```text
0
```

## Transaction Handling

Database operations use transactional behavior.

If any record in a batch violates a database constraint, the transaction fails and the complete batch is rolled back.

This prevents partial loads.

## Historical Data Cleanup

The repository also provides functionality for removing snapshots older than a configured number of days.

The cleanup operation validates the number of days before executing.

Invalid values such as:

```text
0
-1
-7
```

are rejected.

## Complete Execution

A normal execution follows:

```text
1. Start pipeline
2. Extract cryptocurrency data
3. Validate API response
4. Transform dataset
5. Calculate liquidity ratio
6. Add ETL timestamp
7. Load snapshots
8. Log execution result
```

The resulting PostgreSQL table can then be used for historical analysis and visualization.
