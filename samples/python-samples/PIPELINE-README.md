# Build an Airbnb Analysis Pipeline with GitHub Copilot

> **Workshop exercise for econometrics and analytics teams.**
> Use GitHub Copilot's Chat panel, Agent mode, and Plan mode to build a
> Python analysis pipeline — step by step — without writing code from scratch.

This guide walks you through using Copilot to create a script similar to
[`airbnb_analysis_pipeline.py`](./airbnb_analysis_pipeline.py). That file is
the "finished product" — a reference you can compare against as you build
your own version.

---

## Prerequisites

| Requirement | Details |
|---|---|
| **VS Code** with **GitHub Copilot** extension | [Install guide](../00-quick-start/README.md) |
| **Python 3.10+** and `.venv` activated | Run the setup cell in `air-bnb-workshop.ipynb` first |
| **Copilot Chat panel open** | `Cmd+Option+I` (Mac) / `Ctrl+Alt+I` (Windows) |
| Familiarity with the workshop notebook | Open `samples/air-bnb-workshop.ipynb` and run the first two cells |

---

## How to use this guide

Each section below gives you:

1. **The goal** — what this part of the pipeline does, in plain English
2. **A Copilot prompt** — copy it into the Chat panel (Agent mode recommended)
3. **What to check** — how to verify the output is correct
4. **Stretch prompts** — optional follow-ups to refine the result

> **Tip:** Switch Copilot to **Agent mode** (dropdown at the top of Chat) so
> it can create and edit files directly. If you want to plan first before
> generating code, try **Plan mode** — Copilot will outline its approach and
> ask for your approval before making changes.

---

## Step 0 — Plan the pipeline

Before writing any code, ask Copilot to help you plan.

**Switch to Plan mode** in the Chat dropdown, then paste:

```
I want to create a Python script called samples/my_analysis_pipeline.py
that does an end-to-end analysis of Airbnb listing data for five cities:
New York, London, Paris, Amsterdam, and Barcelona.

The script should:
1. Download CSV data from Inside Airbnb
2. Clean the price column and add derived columns (price_tier, rental_type)
3. Print a data quality overview
4. Run SQL queries using DuckDB on the DataFrame
5. Generate matplotlib/seaborn charts and save them as PNG files
6. Build a summary table and export everything to CSV

Please read #AGENTS.md for the project conventions and data schema.
Outline a step-by-step plan for this script before writing any code.
```

**What to check:** Copilot should produce a numbered plan. Review it and ask
it to adjust anything before moving on.

Once happy, **switch to Agent mode** and say:

```
Go ahead and implement the plan. Create the file samples/my_analysis_pipeline.py.
```

---

## Step 1 — Download and combine data

If you prefer to build the script piece by piece, start with the data
download function.

**Copilot prompt:**

```
Create a Python file samples/my_analysis_pipeline.py.

Start with a function called download_city_data() that:
- Downloads Airbnb listing CSVs from Inside Airbnb for New York, London,
  Paris, Amsterdam, and Barcelona
- Paris needs the gzip-compressed full data file (data/listings.csv.gz)
  because the visualisations extract doesn't include price
- Samples 2,000 rows per city (random_state=42)
- Normalises the neighbourhood column name
- Returns a single combined pandas DataFrame

Add a main() function that calls this and prints the shape of the result.
Read #AGENTS.md for the data schema and URL structure.
```

**What to check:**
- The script runs without errors: `python samples/my_analysis_pipeline.py`
- Output shows ~10,000 rows (2,000 per city)
- Paris data includes a price column

**Stretch prompt:**

```
Add a --cities command-line argument so I can run the script for just
one or two cities, e.g.: python samples/my_analysis_pipeline.py --cities London Paris
```

---

## Step 2 — Clean and enrich the data

**Copilot prompt:**

```
Add a function called clean_and_enrich(df) to my pipeline script that:
- Strips currency symbols ($, £, €) from the price column if it's stored as text
- Converts price to float
- Adds a has_price boolean column (True where price is not null and > 0)
- Caps price outliers at the 99th percentile per city into a price_capped column
- Classifies minimum_nights into rental_type: Short-term (< 7), Weekly+ (7–29),
  Long-term (30+)
- Adds a price_tier column: Budget / Mid-range / Luxury based on the 33rd and
  66th percentile of each city's price distribution

Call this function in main() after downloading the data.
```

**What to check:**
- `df.columns` includes `has_price`, `price_capped`, `rental_type`, `price_tier`
- `df["price_tier"].value_counts()` shows a reasonable distribution
- No errors when running on all five cities

---

## Step 3 — Data overview

**Copilot prompt:**

```
Add a function called print_data_overview(df) that prints:
- The DataFrame shape
- Listings per city
- A table showing each column's data type and percentage of missing values
- A visual bar showing price availability by city (using block characters)
```

**What to check:** Output is readable and matches what you see in the notebook.

---

## Step 4 — SQL analysis with DuckDB

This step is especially relevant for analysts who already know SQL.

**Copilot prompt:**

```
Add a function called run_sql_analyses(df) that uses DuckDB to run these
queries directly on the DataFrame and prints the results:

1. Count of listings per city, ordered by count descending
2. Room type breakdown per city with percentage share (using a window function)
3. Top 15 neighbourhoods by average reviews (minimum 5 listings)
4. Short-term vs long-term rental mix by city, with average reviews and availability

Use duckdb.query("...").df() syntax. Return the results as a dictionary of DataFrames.
Read #AGENTS.md for DuckDB conventions.
```

**What to check:**
- All four queries run without errors
- Results match what the notebook produces
- The SQL uses DuckDB syntax (e.g., window functions work)

**Stretch prompt:**

```
Add a fifth query: use a CTE to find listings with above-average reviews
AND above-average availability for their city. Count them per city.
```

---

## Step 5 — Charts and visualisations

**Copilot prompt:**

```
Add chart functions to my pipeline that save PNG files to an output directory:

1. plot_overview_charts(df, output_dir) — bar charts of listings per city
   and room type distribution (side by side, figsize 15x5)
2. plot_price_charts(df, output_dir) — box plots of price by city and
   price by room type + city (skip if no price data)
3. plot_reviews_availability(df, output_dir) — median reviews bar chart
   and availability KDE distribution

Use seaborn with whitegrid style and muted palette.
Always call plt.tight_layout() before saving.
Save each chart as a PNG file in the output directory.
```

**What to check:**
- PNG files appear in the output directory
- Charts are readable with proper titles and labels
- No errors for cities with missing price data

**Stretch prompt:**

```
Add an interactive Plotly chart showing room-type share per city as a
stacked bar chart. Save it as an HTML file in the output directory.
```

---

## Step 6 — Summary functions and export

**Copilot prompt:**

```
Add these functions:

1. city_summary(df, city) — returns a dictionary with total listings,
   top room type, median availability, median reviews, top neighbourhood,
   and median price (if available). Add type hints and a docstring.

2. build_summary_table(df) — aggregates key metrics for every city into
   a single DataFrame.

3. export_results(df, sql_results, summary, output_dir) — saves the
   cleaned dataset, summary table, and all SQL results to CSV files.

Wire them all into the main pipeline.
```

**What to check:**
- CSV files appear in the output directory
- `city_summary()` returns sensible values for each city
- The summary table matches the one at the bottom of the notebook

---

## Step 7 — Run the full pipeline

```bash
python samples/my_analysis_pipeline.py
```

Or for a quick test with just two cities:

```bash
python samples/my_analysis_pipeline.py --cities London Amsterdam --output-dir test_output/
```

Compare your output against the reference file:

```
Look at #airbnb_analysis_pipeline.py — compare it with my version in
#my_analysis_pipeline.py. What differences are there? Are there any
improvements I should make?
```

---

## Going further — automation with custom instructions

Once your pipeline works, you can teach Copilot to run it automatically in
future sessions. There are three approaches available at Sky:

### Option A: Custom instructions file

The file at `.github/copilot-instructions.md` is read automatically by
Copilot in every chat session. You can add pipeline-specific conventions:

```
Ask Copilot:

Read #.github/copilot-instructions.md — add a section about the analysis
pipeline script at samples/airbnb_analysis_pipeline.py. Include the
command to run it, the expected outputs, and any conventions about the
output directory structure.
```

### Option B: Agent instructions file (AGENTS.md)

The `AGENTS.md` file in the project root gives AI tools broader context.
Ask Copilot to update it:

```
Read #AGENTS.md and add a section called "Analysis Pipeline" that describes:
- The purpose of samples/airbnb_analysis_pipeline.py
- How to run it (with and without city filters)
- The output files it generates
- The key functions and what they do
```

### Option C: Skill file

A skill file is a focused instruction document for a specific task. Create
one that Copilot can reference when you want to run or modify the pipeline:

```
Create a file at .github/skills/analysis-pipeline/SKILL.md that teaches
Copilot how to:
1. Run the Airbnb analysis pipeline
2. Add new cities to the pipeline
3. Add new chart types
4. Add new SQL queries
5. Export results in different formats

Read #.github/skills/duckdb-query/SKILL.md for an example of the format.
```

Then in future sessions, reference it:

```
#.github/skills/analysis-pipeline/SKILL.md — Run the analysis pipeline
for London and Paris only, and add a correlation heatmap to the charts.
```

---

## Copilot features used in this exercise

| Feature | How it helps |
|---|---|
| **Plan mode** | Outlines the pipeline structure before writing code |
| **Agent mode** | Creates and edits files, runs terminal commands |
| **`#file` context** | Points Copilot at the notebook, AGENTS.md, or SKILL.md for context |
| **Inline completions** | Suggests code as you type inside the script |
| **Copilot: Explain** | Right-click any function to understand what it does |
| **Custom instructions** | `.github/copilot-instructions.md` sets project-wide conventions |
| **Skill files** | `.github/skills/*/SKILL.md` teaches Copilot reusable task patterns |

---

## Sky environment notes

| Feature | Status |
|---|---|
| Copilot Chat + Agent mode | Available |
| Plan mode | Available |
| Inline completions | Available |
| `#file` context | Available |
| `.github/copilot-instructions.md` | Available |
| AGENTS.md | Available (reference manually with `#AGENTS.md`) |
| Skill files | Available (reference manually with `#` in Chat) |
| Copilot CLI | Not available (public preview, blocked by policy) |
| MCP servers | Not available in our environment |
