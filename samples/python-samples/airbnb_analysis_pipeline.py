#!/usr/bin/env python3
"""
Airbnb Listings — End-to-End Analysis Pipeline
================================================
Downloads, cleans, analyses, and visualises Airbnb listing data for five
cities: New York, London, Paris, Amsterdam, and Barcelona.

This script is a standalone equivalent of the workshop Jupyter notebook
(samples/air-bnb-workshop.ipynb). It demonstrates the kind of reusable
analysis pipeline that a team of analysts could build with the help of
GitHub Copilot — even without deep Python experience.

Usage
-----
    python samples/airbnb_analysis_pipeline.py [--output-dir OUTPUT_DIR] [--cities CITY ...]

Examples
--------
    python samples/airbnb_analysis_pipeline.py
    python samples/airbnb_analysis_pipeline.py --cities London Paris
    python samples/airbnb_analysis_pipeline.py --output-dir results/
"""

from __future__ import annotations

import argparse
import io
import warnings
from pathlib import Path
from typing import Any

import duckdb
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import seaborn as sns

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns", None)
pd.set_option("display.float_format", "{:,.2f}".format)
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams["figure.dpi"] = 110

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SAMPLE_PER_CITY = 2_000

CITY_SOURCES: dict[str, tuple[str, bool]] = {
    "New York": (
        "https://data.insideairbnb.com/united-states/ny/new-york-city/"
        "2026-02-13/visualisations/listings.csv",
        False,
    ),
    "London": (
        "https://data.insideairbnb.com/united-kingdom/england/london/"
        "2025-09-14/visualisations/listings.csv",
        False,
    ),
    "Paris": (
        "https://data.insideairbnb.com/france/ile-de-france/paris/"
        "2025-09-12/data/listings.csv.gz",
        True,
    ),
    "Amsterdam": (
        "https://data.insideairbnb.com/the-netherlands/north-holland/amsterdam/"
        "2025-09-11/visualisations/listings.csv",
        False,
    ),
    "Barcelona": (
        "https://data.insideairbnb.com/spain/catalonia/barcelona/"
        "2025-12-14/visualisations/listings.csv",
        False,
    ),
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"
    ),
    "Referer": "https://insideairbnb.com/",
}

KEEP_COLS = [
    "id", "name", "host_id", "host_name",
    "neighbourhood_cleansed", "neighbourhood",
    "latitude", "longitude",
    "room_type", "price",
    "minimum_nights", "number_of_reviews",
    "reviews_per_month", "calculated_host_listings_count",
    "availability_365",
]

# ---------------------------------------------------------------------------
# Step 1 — Download and combine data
# ---------------------------------------------------------------------------


def download_city_data(
    cities: list[str] | None = None,
    sample_per_city: int = SAMPLE_PER_CITY,
) -> pd.DataFrame:
    """Download Airbnb listing CSVs from Inside Airbnb and combine into one DataFrame."""
    selected = {
        k: v for k, v in CITY_SOURCES.items() if cities is None or k in cities
    }
    if not selected:
        raise ValueError(f"No matching cities. Choose from: {list(CITY_SOURCES)}")

    frames: list[pd.DataFrame] = []
    for city, (url, is_gzip) in selected.items():
        print(f"  Downloading {city} ...", end=" ", flush=True)
        try:
            r = requests.get(url, timeout=120, headers=HEADERS)
            r.raise_for_status()
            compression = "gzip" if is_gzip else None
            df_tmp = pd.read_csv(
                io.BytesIO(r.content), compression=compression, low_memory=False
            )
            df_tmp["city"] = city
            cols = [c for c in KEEP_COLS if c in df_tmp.columns] + ["city"]
            df_tmp = df_tmp[cols]
            if (
                "neighbourhood_cleansed" in df_tmp.columns
                and "neighbourhood" not in df_tmp.columns
            ):
                df_tmp = df_tmp.rename(
                    columns={"neighbourhood_cleansed": "neighbourhood"}
                )
            df_tmp = df_tmp.sample(
                min(sample_per_city, len(df_tmp)), random_state=42
            )
            frames.append(df_tmp)
            print(f"OK  {len(df_tmp):,} rows")
        except (requests.RequestException, pd.errors.ParserError, ValueError) as exc:
            print(f"FAILED: {exc}")

    if not frames:
        raise RuntimeError("No data could be downloaded.")
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------------------
# Step 2 — Clean and enrich
# ---------------------------------------------------------------------------


def clean_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Clean price data, add derived columns (price_tier, rental_type, has_price)."""
    df = df.copy()

    # Clean price — strip currency symbols if stored as text
    if df["price"].dtype == object:
        df["price"] = (
            df["price"]
            .str.replace(r"[$,£€]", "", regex=True)
            .str.strip()
            .replace("", np.nan)
            .astype(float)
        )

    df["has_price"] = df["price"].notna() & (df["price"] > 0)

    # Cap outliers at 99th percentile per city
    p99 = df.groupby("city")["price"].transform(lambda x: x.quantile(0.99))
    df["price_capped"] = df["price"].clip(upper=p99)

    # Coerce numeric columns
    for col in [
        "number_of_reviews", "reviews_per_month",
        "calculated_host_listings_count", "availability_365", "minimum_nights",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Rental duration classification
    df["rental_type"] = df["minimum_nights"].apply(_classify_rental)

    # Price tier — relative to each city's distribution
    df["price_tier"] = _assign_price_tiers(df)

    return df


def _classify_rental(min_nights: float) -> str:
    """Classify a listing as Short-term, Weekly+, or Long-term based on minimum nights."""
    if pd.isna(min_nights):
        return "Unknown"
    if min_nights >= 30:
        return "Long-term (30+ nights)"
    if min_nights >= 7:
        return "Weekly+"
    return "Short-term"


def _assign_price_tiers(df: pd.DataFrame) -> pd.Series:
    """Assign Budget / Mid-range / Luxury tiers using city-level 33rd/66th percentiles."""
    tiers: list[pd.Series] = []
    for _city, group in df.groupby("city"):
        prices = group["price"].dropna()
        if len(prices) < 10:
            tiers.append(pd.Series("Unknown", index=group.index))
            continue
        p33, p66 = prices.quantile(0.33), prices.quantile(0.66)
        tiers.append(
            group["price"].apply(
                lambda p, lo=p33, hi=p66: (
                    "Unknown" if pd.isna(p)
                    else "Budget" if p <= lo
                    else "Mid-range" if p <= hi
                    else "Luxury"
                )
            )
        )
    return pd.concat(tiers).reindex(df.index)


# ---------------------------------------------------------------------------
# Step 3 — Data overview
# ---------------------------------------------------------------------------


def print_data_overview(df: pd.DataFrame) -> None:
    """Print shape, column types, missing-value rates, and per-city counts."""
    print(f"\nDataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"\nListings per city:\n{df['city'].value_counts().to_string()}")

    missing = (df.isnull().sum() / len(df) * 100).rename("missing_%").round(1)
    dtypes = df.dtypes.rename("dtype")
    overview = pd.concat([dtypes, missing], axis=1).sort_values(
        "missing_%", ascending=False
    )
    print(f"\nColumn quality:\n{overview.to_string()}")

    if df["has_price"].any():
        print("\nPrice availability by city:")
        price_avail = df.groupby("city")["has_price"].mean().mul(100).round(1)
        for city, pct in price_avail.items():
            bar = "\u2588" * int(pct / 5)
            print(f"  {city:<12} {bar:<20} {pct}%")


# ---------------------------------------------------------------------------
# Step 4 — SQL analysis with DuckDB
# ---------------------------------------------------------------------------


def run_sql_analyses(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Run a set of DuckDB SQL queries against the DataFrame and return results."""
    results: dict[str, pd.DataFrame] = {}

    results["listings_by_city"] = duckdb.query("""
        SELECT city, COUNT(*) AS listings
        FROM df
        GROUP BY city
        ORDER BY listings DESC
    """).df()

    results["room_type_share"] = duckdb.query("""
        SELECT
            city,
            room_type,
            COUNT(*) AS listings,
            ROUND(
                COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY city),
            1) AS pct_of_city
        FROM df
        GROUP BY city, room_type
        ORDER BY city, listings DESC
    """).df()

    results["top_neighbourhoods"] = duckdb.query("""
        SELECT
            city,
            neighbourhood,
            COUNT(*)                          AS listings,
            ROUND(AVG(number_of_reviews), 1)  AS avg_reviews,
            ROUND(AVG(availability_365), 0)   AS avg_availability_days
        FROM df
        WHERE neighbourhood IS NOT NULL
        GROUP BY city, neighbourhood
        HAVING COUNT(*) >= 5
        ORDER BY avg_reviews DESC
        LIMIT 15
    """).df()

    results["rental_mix"] = duckdb.query("""
        SELECT
            city,
            CASE
                WHEN minimum_nights >= 30 THEN 'Long-term (30+ nights)'
                WHEN minimum_nights >= 7  THEN 'Weekly+'
                ELSE 'Short-term'
            END AS rental_category,
            COUNT(*)                         AS listings,
            ROUND(AVG(number_of_reviews), 1) AS avg_reviews,
            ROUND(AVG(availability_365), 0)  AS avg_availability
        FROM df
        WHERE minimum_nights IS NOT NULL
        GROUP BY city, rental_category
        ORDER BY city, listings DESC
    """).df()

    for name, result_df in results.items():
        print(f"\n{'='*60}")
        print(f"  {name}")
        print(f"{'='*60}")
        print(result_df.to_string(index=False))

    return results


# ---------------------------------------------------------------------------
# Step 5 — Visualisations
# ---------------------------------------------------------------------------


def plot_overview_charts(df: pd.DataFrame, output_dir: Path) -> None:
    """Listings per city and room-type distribution bar charts."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    city_counts = df["city"].value_counts().reset_index()
    city_counts.columns = ["City", "Listings"]
    sns.barplot(
        data=city_counts, x="City", y="Listings",
        hue="City", palette="viridis", legend=False, ax=axes[0],
    )
    axes[0].set_title(
        "Listings per City (sample of 2,000)", fontsize=13, fontweight="bold"
    )
    axes[0].set_xlabel("")
    axes[0].yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
    )

    room_counts = df["room_type"].value_counts().reset_index()
    room_counts.columns = ["Room Type", "Count"]
    sns.barplot(
        data=room_counts, x="Room Type", y="Count",
        hue="Room Type", palette="Set2", legend=False, ax=axes[1],
    )
    axes[1].set_title(
        "Room Type Distribution — All Cities", fontsize=13, fontweight="bold"
    )
    axes[1].set_xlabel("")
    axes[1].yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{int(x):,}")
    )

    plt.tight_layout()
    fig.savefig(output_dir / "01_overview.png", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_dir / '01_overview.png'}")


def plot_price_charts(df: pd.DataFrame, output_dir: Path) -> None:
    """Box plots for price by city and by room type + city."""
    df_price = df[df["has_price"]].copy()
    if df_price.empty:
        print("  Skipping price charts — no price data available.")
        return

    cities = sorted(df_price["city"].unique())
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    city_data = [
        df_price.loc[df_price["city"] == c, "price_capped"].dropna().values
        for c in cities
    ]
    bp = axes[0].boxplot(
        city_data, patch_artist=True, labels=cities,
        medianprops=dict(color="black", linewidth=1.5),
    )
    pastel = plt.colormaps["Pastel1"].colors
    for patch, color in zip(bp["boxes"], pastel[: len(cities)]):
        patch.set_facecolor(color)
    axes[0].set_title(
        "Nightly Price by City (capped at 99th pctl)",
        fontsize=12, fontweight="bold",
    )
    axes[0].set_ylabel("Nightly Price (local currency)")
    axes[0].tick_params(axis="x", rotation=20)

    sns.boxplot(
        data=df_price, x="room_type", y="price_capped", hue="city", ax=axes[1]
    )
    axes[1].set_title("Price by Room Type & City", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("")
    axes[1].set_ylabel("Nightly Price")
    axes[1].legend(title="City", bbox_to_anchor=(1.01, 1), loc="upper left")

    plt.tight_layout()
    fig.savefig(output_dir / "02_price_analysis.png", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_dir / '02_price_analysis.png'}")


def plot_reviews_availability(df: pd.DataFrame, output_dir: Path) -> None:
    """Median reviews by city and availability KDE distribution."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    med_reviews = (
        df.groupby("city")["number_of_reviews"]
        .median()
        .sort_values(ascending=False)
    )
    med_reviews.plot(kind="bar", ax=axes[0], color="steelblue", edgecolor="white")
    axes[0].set_title(
        "Median Number of Reviews by City", fontsize=12, fontweight="bold"
    )
    axes[0].set_xlabel("")
    axes[0].set_ylabel("Median Reviews")
    axes[0].tick_params(axis="x", rotation=30)

    for city in df["city"].unique():
        sub = df[df["city"] == city]["availability_365"].dropna()
        if len(sub) >= 2 and sub.std() > 0:
            sub.plot.kde(ax=axes[1], label=city)
    axes[1].set_title(
        "Availability (Days/Year) Distribution", fontsize=12, fontweight="bold"
    )
    axes[1].set_xlabel("Days Available per Year")
    axes[1].legend()
    axes[1].set_xlim(0, 365)

    plt.tight_layout()
    fig.savefig(output_dir / "03_reviews_availability.png", bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {output_dir / '03_reviews_availability.png'}")


def plot_interactive_room_share(df: pd.DataFrame, output_dir: Path) -> None:
    """Interactive stacked bar chart of room-type share per city (saved as HTML)."""
    room_share = (
        df.groupby(["city", "room_type"]).size().reset_index(name="count")
    )
    room_share["pct"] = room_share.groupby("city")["count"].transform(
        lambda x: x / x.sum() * 100
    ).round(1)

    fig = px.bar(
        room_share, x="city", y="pct", color="room_type",
        barmode="stack",
        title="Room Type Share per City (%)",
        labels={"pct": "Share (%)", "city": "", "room_type": "Room Type"},
        template="plotly_white",
        height=450,
        text="pct",
    )
    fig.update_traces(texttemplate="%{text:.0f}%", textposition="inside")
    out = output_dir / "04_room_type_share.html"
    fig.write_html(str(out))
    print(f"  Saved: {out}")


# ---------------------------------------------------------------------------
# Step 6 — Reusable summary functions
# ---------------------------------------------------------------------------


def city_summary(df: pd.DataFrame, city: str) -> dict[str, Any]:
    """Return key metrics for a single city as a dictionary."""
    subset = df[df["city"] == city]
    if subset.empty:
        return {"error": f"No data found for city: {city}"}

    nbh_col = (
        "neighbourhood_cleansed"
        if "neighbourhood_cleansed" in df.columns
        else "neighbourhood"
    )
    top_room = subset["room_type"].value_counts().idxmax()
    top_nbh = (
        subset[nbh_col].value_counts().idxmax()
        if nbh_col in subset.columns
        else "N/A"
    )

    result: dict[str, Any] = {
        "city": city,
        "total_listings": len(subset),
        "top_room_type": top_room,
        "median_availability": round(float(subset["availability_365"].median()), 0),
        "median_reviews": round(float(subset["number_of_reviews"].median()), 1),
        "top_neighbourhood": top_nbh,
    }
    if subset["has_price"].any():
        result["median_price"] = round(
            float(subset.loc[subset["has_price"], "price"].median()), 2
        )
    return result


def build_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate key metrics for every city into a single summary table."""
    summary = df.groupby("city").agg(
        Total_Listings=("id", "count"),
        Pct_Entire_Home=(
            "room_type",
            lambda x: round((x == "Entire home/apt").mean() * 100, 1),
        ),
        Median_Reviews=("number_of_reviews", "median"),
        Avg_Availability_Days=(
            "availability_365",
            lambda x: round(x.mean(), 0),
        ),
    ).sort_values("Total_Listings", ascending=False)

    if df["has_price"].any():
        price_stats = (
            df[df["has_price"]]
            .groupby("city")["price"]
            .agg(Median_Price="median")
            .round(1)
        )
        summary = summary.join(price_stats, how="left")

    return summary


# ---------------------------------------------------------------------------
# Step 7 — Export results
# ---------------------------------------------------------------------------


def export_results(
    df: pd.DataFrame,
    sql_results: dict[str, pd.DataFrame],
    summary: pd.DataFrame,
    output_dir: Path,
) -> None:
    """Write the cleaned dataset, SQL results, and summary to CSV files."""
    df.to_csv(output_dir / "cleaned_listings.csv", index=False)
    print(f"  Saved: {output_dir / 'cleaned_listings.csv'}")

    summary.to_csv(output_dir / "city_summary.csv")
    print(f"  Saved: {output_dir / 'city_summary.csv'}")

    for name, result_df in sql_results.items():
        path = output_dir / f"sql_{name}.csv"
        result_df.to_csv(path, index=False)
        print(f"  Saved: {path}")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def run_pipeline(cities: list[str] | None = None, output_dir: str = "output") -> None:
    """Execute the full analysis pipeline end to end."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 60)
    print("  STEP 1 — Downloading data")
    print("=" * 60)
    df = download_city_data(cities)

    print("\n" + "=" * 60)
    print("  STEP 2 — Cleaning and enriching")
    print("=" * 60)
    df = clean_and_enrich(df)
    print("  Done.")

    print("\n" + "=" * 60)
    print("  STEP 3 — Data overview")
    print("=" * 60)
    print_data_overview(df)

    print("\n" + "=" * 60)
    print("  STEP 4 — SQL analyses (DuckDB)")
    print("=" * 60)
    sql_results = run_sql_analyses(df)

    print("\n" + "=" * 60)
    print("  STEP 5 — Generating charts")
    print("=" * 60)
    plot_overview_charts(df, out)
    plot_price_charts(df, out)
    plot_reviews_availability(df, out)
    plot_interactive_room_share(df, out)

    print("\n" + "=" * 60)
    print("  STEP 6 — City summaries")
    print("=" * 60)
    for city in sorted(df["city"].unique()):
        s = city_summary(df, city)
        print(f"\n  {s['city']}")
        for k, v in s.items():
            if k != "city":
                print(f"    {k:<22} {v}")

    summary = build_summary_table(df)
    print(f"\n{summary.to_string()}")

    print("\n" + "=" * 60)
    print("  STEP 7 — Exporting results")
    print("=" * 60)
    export_results(df, sql_results, summary, out)

    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print(f"  All outputs saved to: {out.resolve()}")
    print("=" * 60 + "\n")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Airbnb listings analysis pipeline"
    )
    parser.add_argument(
        "--cities",
        nargs="+",
        default=None,
        help="Cities to include (default: all five)",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for output files (default: output/)",
    )
    args = parser.parse_args()
    run_pipeline(cities=args.cities, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
