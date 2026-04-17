# GitHub Copilot Instructions — Airbnb Data Workshop

These instructions are loaded automatically by GitHub Copilot whenever you work in this project.
They give Copilot context about the tools, conventions, and data so you get better suggestions
without having to explain everything from scratch each time.

---

## Project context

This is a Python data analysis project working with Airbnb listing data for five cities:
**New York, London, Paris, Amsterdam, and Barcelona**.

The data is stored in a pandas DataFrame named `df` that is already loaded in the notebook.

---

## SQL queries — always use DuckDB

- **Always write SQL using DuckDB syntax**, not SQLite, PostgreSQL, or any other dialect.
- DuckDB can query pandas DataFrames directly by variable name — no loading step needed:

```python
import duckdb
duckdb.query("SELECT * FROM df WHERE city = 'London'").df()
```

- Use DuckDB-native aggregate functions: `MEDIAN()`, `APPROX_COUNT_DISTINCT()`, `QUANTILE_CONT()`
- Window functions are fully supported: `RANK() OVER (PARTITION BY city ORDER BY count DESC)`
- CTEs (`WITH` clauses) are supported and preferred for complex queries
- Always chain `.df()` at the end of `duckdb.query()` to return a pandas DataFrame

---

## Data structure — DataFrame `df`

| Column | Type | Description |
|---|---|---|
| `id` | int | Unique listing ID |
| `name` | str | Listing title |
| `host_id` | int | Host identifier |
| `host_name` | str | Host display name |
| `neighbourhood` | str | Neighbourhood name |
| `city` | str | One of: New York, London, Paris, Amsterdam, Barcelona |
| `room_type` | str | "Entire home/apt", "Private room", "Shared room", "Hotel room" |
| `price` | float | Nightly price (local currency); NaN for some cities |
| `price_capped` | float | Price capped at 99th percentile per city |
| `has_price` | bool | True if price is available and > 0 |
| `price_tier` | str | "Budget", "Mid-range", "Luxury", or "Unknown" |
| `minimum_nights` | float | Minimum booking duration in nights |
| `rental_type` | str | "Short-term", "Weekly+", or "Long-term (30+ nights)" |
| `number_of_reviews` | int | Total reviews received |
| `reviews_per_month` | float | Rolling review rate |
| `availability_365` | int | Days available per year (0–365) |
| `calculated_host_listings_count` | int | Number of listings the host manages |

---

## Python conventions

- Use **pandas** for data loading and cleaning
- Use **matplotlib / seaborn** for static charts (style: `whitegrid`, palette: `muted`)
- Use **plotly.express** for interactive charts (template: `plotly_white`)
- Add **type hints** to all function parameters and return types
- Add a **one-line docstring** to any function that takes parameters
- Prefer explicit column names over positional indexing
- Use f-strings for formatted output

---

## Charting conventions

- Figure size: `(12, 5)` for side-by-side charts, `(10, 5)` for single charts
- Always set a `title`, `xlabel`, and `ylabel`
- Format large numbers with commas: use `mticker.FuncFormatter(lambda x, _: f"{int(x):,}")`
- Use `plt.tight_layout()` before `plt.show()`
