# Data Model

## Overview

The project stores cryptocurrency market snapshots in PostgreSQL.

The main table is:

```text
cryptocurrencies
```

Each record represents the state of a cryptocurrency at a specific ETL execution time.

## Table: cryptocurrencies

| Column                        | Type       | Description                                      |
| ----------------------------- | ---------- | ------------------------------------------------ |
| `id`                          | Integer    | Primary key                                      |
| `coin_id`                     | String     | CoinGecko cryptocurrency identifier              |
| `symbol`                      | String     | Cryptocurrency symbol                            |
| `name`                        | String     | Cryptocurrency name                              |
| `current_price`               | Float      | Current market price                             |
| `market_cap`                  | BigInteger | Market capitalization                            |
| `market_cap_rank`             | Integer    | Market capitalization ranking                    |
| `total_volume`                | BigInteger | 24-hour trading volume                           |
| `price_change_percentage_24h` | Float      | 24-hour price change                             |
| `ath_change_percentage`       | Float      | Percentage change from all-time high             |
| `liquidity_ratio`             | Float      | Trading volume relative to market capitalization |
| `etl_timestamp`               | DateTime   | ETL execution timestamp                          |

## Liquidity Ratio

The pipeline calculates liquidity ratio as:

```text
(total_volume / market_cap) × 100
```

The resulting value is rounded to two decimal places.

This metric provides a relative measure of trading activity compared with the cryptocurrency's market capitalization.

## Historical Snapshots

Historical observations are preserved instead of updating a single record for each cryptocurrency.

The database uses:

```text
coin_id + etl_timestamp
```

as the snapshot identity.

A unique constraint named `uq_coin_snapshot` prevents the same cryptocurrency from being inserted twice with the same ETL timestamp.

This allows multiple observations of the same cryptocurrency over time.

Example:

```text
bitcoin | 2026-08-09 18:05
bitcoin | 2026-08-09 18:10
bitcoin | 2026-08-09 18:15
```

Each record represents a different historical snapshot.

## Database Constraints

The model includes validation constraints for important numerical fields.

```text
current_price >= 0
market_cap >= 0
market_cap_rank >= 1
total_volume >= 0
liquidity_ratio >= 0
```

These constraints prevent invalid numerical values from being persisted.

Required fields include:

```text
coin_id
name
symbol
current_price
market_cap
etl_timestamp
```

## Indexes

Indexes are defined for frequently queried fields:

```text
coin_id
symbol
market_cap
market_cap_rank
etl_timestamp
symbol + etl_timestamp
```

These indexes support common analytical and historical queries.

## Transaction Integrity

Database writes are executed inside transactions.

If an insertion fails, the transaction is rolled back, preventing partially inserted batches.

This guarantees that a failed batch does not leave inconsistent records in the database.
