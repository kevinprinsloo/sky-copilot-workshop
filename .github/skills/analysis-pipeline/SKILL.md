---
name: analysis-pipeline
description: Use when running the Airbnb analysis pipeline, adding new cities or charts, modifying SQL queries, or exporting results in different formats
---

# Airbnb Analysis Pipeline Runner

You help analysts run, extend, and maintain the Airbnb listings analysis pipeline.

## The pipeline

The script is at `samples/airbnb_analysis_pipeline.py`. It downloads, cleans,
analyses, and visualises Airbnb listing data for up to five cities.

### How to run

```bash
# All five cities — outputs to ./output/
python samples/airbnb_analysis_pipeline.py

# Specific cities only
python samples/airbnb_analysis_pipeline.py --cities London Paris

# Custom output directory
python samples/airbnb_analysis_pipeline.py --output-dir results/q1_2026/
```

### Output files

The pipeline writes these files to the output directory:

| File | Contents |
|---|---|
| `cleaned_listings.csv` | Full cleaned dataset with derived columns |
| `city_summary.csv` | One row per city with key metrics |
| `sql_listings_by_city.csv` | Listing counts per city |
| `sql_room_type_share.csv` | Room type breakdown with percentage shares |
| `sql_top_neighbourhoods.csv` | Top neighbourhoods by review activity |
| `sql_rental_mix.csv` | Short-term vs long-term rental mix |
| `01_overview.png` | Bar charts: listings per city + room type distribution |
| `02_price_analysis.png` | Box plots: price by city and by room type |
| `03_reviews_availability.png` | Median reviews + availability KDE |
| `04_room_type_share.html` | Interactive Plotly stacked bar chart |

## Key functions

| Function | Purpose |
|---|---|
| `download_city_data(cities, sample_per_city)` | Fetch and combine CSVs from Inside Airbnb |
| `clean_and_enrich(df)` | Clean price, add has_price, price_capped, rental_type, price_tier |
| `print_data_overview(df)` | Print shape, missing values, price availability |
| `run_sql_analyses(df)` | Run DuckDB SQL queries and return results dict |
| `plot_overview_charts(df, output_dir)` | Save listings/room-type bar charts |
| `plot_price_charts(df, output_dir)` | Save price box plots |
| `plot_reviews_availability(df, output_dir)` | Save reviews/availability charts |
| `plot_interactive_room_share(df, output_dir)` | Save interactive Plotly chart |
| `city_summary(df, city)` | Return a dict of metrics for one city |
| `build_summary_table(df)` | Aggregate metrics for all cities |
| `export_results(df, sql_results, summary, output_dir)` | Write CSVs |
| `run_pipeline(cities, output_dir)` | Orchestrate all steps end to end |

## Adding a new city

1. Add the city name and Inside Airbnb URL to the `CITY_SOURCES` dict at the top of the script
2. Set the second tuple element to `True` if the URL is gzip-compressed, `False` otherwise
3. The rest of the pipeline handles new cities automatically

## Adding a new chart

1. Create a function following the pattern: `def plot_<name>(df: pd.DataFrame, output_dir: Path) -> None:`
2. Use seaborn with `whitegrid` style and `muted` palette
3. Always call `plt.tight_layout()` before saving
4. Save to `output_dir / "<number>_<name>.png"`
5. Call the function from `run_pipeline()` in the Step 5 section

## Adding a new SQL query

1. Add the query inside `run_sql_analyses()` using `duckdb.query("...").df()` syntax
2. Use DuckDB SQL syntax (not PostgreSQL or SQLite)
3. Reference the DataFrame as `df` — DuckDB queries it directly
4. Add the result to the `results` dict so it gets exported to CSV automatically

## Data schema

The cleaned DataFrame `df` has these columns:

| Column | Type | Notes |
|---|---|---|
| `id` | int | Unique listing ID |
| `name` | str | Listing title |
| `host_id` | int | Host identifier |
| `host_name` | str | Host display name |
| `neighbourhood` | str | Neighbourhood name |
| `city` | str | New York, London, Paris, Amsterdam, or Barcelona |
| `room_type` | str | Entire home/apt, Private room, Shared room, Hotel room |
| `price` | float | Nightly price (local currency); NaN for some cities |
| `price_capped` | float | Price capped at 99th percentile per city |
| `has_price` | bool | True if price is available and > 0 |
| `price_tier` | str | Budget, Mid-range, Luxury, or Unknown |
| `minimum_nights` | float | Minimum booking duration in nights |
| `rental_type` | str | Short-term, Weekly+, or Long-term (30+ nights) |
| `number_of_reviews` | int | Total reviews received |
| `reviews_per_month` | float | Rolling review rate |
| `availability_365` | int | Days available per year (0–365) |
| `calculated_host_listings_count` | int | Number of listings the host manages |

## Conventions

- Use **pandas** for data loading and cleaning
- Use **matplotlib / seaborn** for static charts (`whitegrid` style, `muted` palette)
- Use **plotly.express** for interactive charts (`plotly_white` template)
- Use **DuckDB** for SQL queries — query the DataFrame directly by variable name
- Add type hints to function signatures
- Add a one-line docstring to any function that takes parameters
- Figure size: `(12, 5)` for side-by-side, `(10, 5)` for single charts
