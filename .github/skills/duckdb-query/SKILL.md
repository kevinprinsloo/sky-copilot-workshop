---
name: duckdb-query
description: Use when writing SQL queries, querying DataFrames with SQL, aggregating data, GROUP BY, window functions, CTEs, or any task involving SQL analysis on the workshop dataset
---

# DuckDB SQL Query Writer

You write SQL queries using DuckDB syntax to analyse the Airbnb workshop dataset.

## Core rules

- Always use **DuckDB syntax** — not SQLite, PostgreSQL, or generic SQL
- Query the pandas DataFrame directly by its variable name. No loading step needed:

```python
import duckdb
duckdb.query("SELECT city, COUNT(*) AS listings FROM df GROUP BY city ORDER BY listings DESC").df()
```

- Always chain `.df()` at the end of `duckdb.query()` to return a pandas DataFrame
- Use DuckDB-native aggregate functions: `MEDIAN()`, `APPROX_COUNT_DISTINCT()`, `QUANTILE_CONT(0.75)`
- Window functions are fully supported: `RANK() OVER (PARTITION BY city ORDER BY count DESC)`
- CTEs (`WITH` clauses) are preferred for multi-step queries

## DataFrame — `df`

The main table is the pandas DataFrame `df`. Key columns:

| Column | Notes |
|---|---|
| `city` | New York, London, Paris, Amsterdam, Barcelona |
| `room_type` | "Entire home/apt", "Private room", "Shared room", "Hotel room" |
| `neighbourhood` | Neighbourhood name (string) |
| `price` | Nightly price; NaN for some cities |
| `has_price` | Boolean — filter with `WHERE has_price = true` when working with prices |
| `price_capped` | Price with outliers removed (99th percentile cap per city) |
| `minimum_nights` | Minimum booking duration |
| `number_of_reviews` | Total reviews |
| `availability_365` | Days available per year (0–365) |
| `rental_type` | "Short-term", "Weekly+", "Long-term (30+ nights)" |

## Output format

Always provide:
1. A brief one-line comment explaining what the query does
2. The complete, runnable Python code block
3. One sentence describing what the output will show

## Example

```python
# Median price and average reviews by city, for listings with price data
duckdb.query("""
    SELECT
        city,
        ROUND(MEDIAN(price), 2)              AS median_price,
        ROUND(AVG(number_of_reviews), 1)     AS avg_reviews,
        COUNT(*)                             AS listings
    FROM df
    WHERE has_price = true
    GROUP BY city
    ORDER BY median_price DESC
""").df()
```
