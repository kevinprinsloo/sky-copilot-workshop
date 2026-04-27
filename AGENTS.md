# Sky Copilot Workshop - Project Instructions

This file is read automatically by GitHub Copilot (and other AI tools) whenever you work in this project.
It gives Copilot the context it needs to give better answers without you having to explain everything each time.

---

## Project context

This is a Python data analysis workshop using Airbnb listing data for five cities:
**New York, London, Paris, Amsterdam, and Barcelona**.

The audience is finance and analytics professionals - not software developers. Explanations should be
clear and practical, using business language rather than engineering jargon where possible.

The data is stored in a pandas DataFrame named `df`, already loaded in `samples/air-bnb-workshop.ipynb`.

---

## SQL - always use DuckDB

- **Always write SQL using DuckDB syntax**, not SQLite, PostgreSQL, or generic SQL
- DataFrames are queried directly by variable name - no loading step needed:

```python
import duckdb
duckdb.query("SELECT city, COUNT(*) FROM df GROUP BY city").df()
```

- Always chain `.df()` at the end of `duckdb.query()` to return a pandas DataFrame
- DuckDB supports: `MEDIAN()`, `APPROX_COUNT_DISTINCT()`, `QUANTILE_CONT()`, window functions, CTEs

---

## DataFrame schema - `df`

| Column | Type | Description |
|---|---|---|
| `id` | int | Unique listing ID |
| `name` | str | Listing title |
| `host_id` | int | Host identifier |
| `host_name` | str | Host display name |
| `neighbourhood` | str | Neighbourhood name |
| `city` | str | New York, London, Paris, Amsterdam, or Barcelona |
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
- Use **matplotlib / seaborn** for static charts (`whitegrid` style, `muted` palette)
- Use **plotly.express** for interactive charts (`plotly_white` template)
- Add type hints to function parameters and return types
- Add a one-line docstring to any function that takes parameters
- Use f-strings for formatted output
- Figure size: `(12, 5)` for side-by-side, `(10, 5)` for single charts
- Always call `plt.tight_layout()` before `plt.show()`

---

## Tone and explanations

- Explain outputs in plain English suitable for a finance or analytics professional
- When generating summaries or comments, avoid technical jargon unless necessary
- When asked to write a function, include a short docstring written for a non-developer audience
