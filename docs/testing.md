# Testing

## Overview

The project uses **Pytest** to validate the main ETL, database, and data-quality behaviors.

The complete test suite currently contains:

```text
31 passed
```

Run the complete suite with:

```powershell
python -m pytest tests -v
```

## Test Structure

Tests are organized in the `tests/` directory.

The test suite covers the following areas.

## Database Connectivity

Validates that the application can establish a connection with PostgreSQL.

```text
test_connection.py
```

## Database Constraints

Validates that invalid numerical values are rejected by database constraints.

Examples include:

```text
current_price < 0
market_cap < 0
market_cap_rank < 1
total_volume < 0
liquidity_ratio < 0
```

## Duplicate Snapshots

Validates that the database rejects duplicate combinations of:

```text
coin_id + etl_timestamp
```

This protects the historical snapshot model.

## Multiple Snapshots

Validates that multiple snapshots of the same cryptocurrency can coexist when their ETL timestamps are different.

Example:

```text
coin_id = bitcoin
timestamp = T1

coin_id = bitcoin
timestamp = T2
```

Both records must remain available.

## Transaction Rollback

Validates that failed database operations are rolled back correctly.

The test ensures that invalid data does not remain persisted after a transaction failure.

## Batch Rollback

Validates transactional integrity when a batch contains multiple records and one of them is invalid.

Expected behavior:

```text
Valid record
Valid record
Invalid record
      ↓
Transaction failure
      ↓
Complete rollback
```

No partial batch should remain in the database.

## Empty DataFrame

Validates that inserting an empty DataFrame does not create unnecessary database operations.

Expected result:

```text
0 records inserted
```

## Data Cleanup

Validates that old cryptocurrency snapshots can be removed while recent snapshots remain available.

The cleanup test verifies that only records older than the configured retention period are deleted.

## Cleanup Validation

Validates that invalid cleanup periods are rejected.

Examples:

```text
0
-1
-7
```

## Extraction Validation

Validates the extraction parameter:

```text
total_pages
```

Invalid values such as:

```text
0
-1
-7
```

must raise a validation error.

## Transformation

Transformation tests validate:

* successful transformation of valid data
* duplicate removal
* missing required column detection
* liquidity ratio calculation
* ETL timestamp generation

## Testing Philosophy

The test suite focuses on critical failure scenarios rather than only testing successful execution.

Important properties validated include:

```text
Data integrity
Transaction integrity
Validation
Historical preservation
Duplicate prevention
Transformation correctness
```

This helps ensure that the pipeline behaves predictably when receiving invalid data or encountering database errors.
