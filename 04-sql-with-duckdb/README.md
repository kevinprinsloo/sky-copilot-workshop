![Data Analysis with GitHub Copilot - Sky Workshop](../images/Picture%201.png)

# Chapter 04 - SQL with DuckDB 🗄️

> **You already know SQL. This chapter shows you how to use it on any data - no database server, no connection string, no setup.**

DuckDB lets you run SQL queries directly on a pandas DataFrame. If you're writing SQL in a BI tool, a data warehouse, or even just thinking in SQL, you can bring that skill directly into Python - and use Copilot to write the queries for you.

> ⚠️ **Prerequisites:** Complete Chapters 01–03. Have `samples/air-bnb-workshop.ipynb` open and the data loaded.

## 🎯 Learning Objectives

By the end of this chapter you'll be able to:

- Run SQL queries on a pandas DataFrame using DuckDB
- Ask Copilot to write DuckDB SQL queries from plain-English descriptions
- Use window functions and CTEs without memorising the syntax
- Translate existing pandas code into SQL - and vice versa

> ⏱️ **Estimated time:** ~45 minutes (15 min reading + 30 min hands-on)

---

## 🧩 Real-World Analogy: SQL on a Spreadsheet

Imagine being able to write a SQL `GROUP BY` query against an Excel file without importing it into a database. That's DuckDB. It runs entirely in memory, reads your existing Python variables as tables, and returns results as a DataFrame - all in a single line.

For analysts who think in SQL, this is the fastest path from "I have a question about this data" to "here's the answer."

---

## How DuckDB Works

DuckDB treats your pandas DataFrame like a database table. The variable name becomes the table name:

```python
import duckdb

# df is already loaded in the notebook
result = duckdb.query("""
    SELECT city, COUNT(*) AS listings
    FROM df
    GROUP BY city
    ORDER BY listings DESC
""").df()   # .df() returns a pandas DataFrame

result
```

That's it. No connection string. No importing data. No teardown. Run it in a notebook cell, get a DataFrame back.

---

## Why Copilot writes DuckDB automatically

Before we start writing queries, there's something to note. This project includes a **custom instructions file** at `.github/copilot-instructions.md`.

That file tells Copilot to use DuckDB syntax for all SQL queries in this project. You don't have to say "use DuckDB" in every prompt - Copilot reads the instructions file and applies the rule automatically.

We cover exactly how this works in [Chapter 05](../05-custom-instructions-agents/README.md). For now, just know that this is why Copilot knows to write `duckdb.query(...)` instead of generic SQL.

> **Note:** There is also a `.github/skills/duckdb-query/SKILL.md` file in this project. In VS Code, this file is not read automatically by Copilot - it's a reference document you can drag into Chat with `#` to give extra context. The file that Copilot reads automatically is `.github/copilot-instructions.md`.

---

## See It In Action

### Demo 1: Your first query

In a new notebook cell, type this comment and wait for Copilot's inline suggestion:

```python
# Count the number of listings per city, ordered by count descending
```

Copilot should complete it with a DuckDB query. Accept with `Tab`.

Or ask in Chat:

**💬 VS Code Chat UI:**

> *"Write a DuckDB query to count the number of listings per city, ordered from largest to smallest."*

---

### Demo 2: Translate pandas to SQL

You've already written some pandas in the notebook. Ask Copilot to translate it:

**💬 VS Code Chat UI:**

> *"Translate this pandas code into an equivalent DuckDB SQL query: `df.groupby(['city', 'room_type'])['number_of_reviews'].mean().round(1)`"*

**What happens:** Copilot produces:

```python
duckdb.query("""
    SELECT city, room_type, ROUND(AVG(number_of_reviews), 1) AS avg_reviews
    FROM df
    GROUP BY city, room_type
    ORDER BY city, avg_reviews DESC
""").df()
```

**The takeaway:** If you can describe analysis in SQL terms, you never have to learn pandas syntax for that operation.

---

### Demo 3: Window functions without memorising syntax

Window functions are powerful but syntactically fiddly. Ask Copilot to handle them:

**💬 VS Code Chat UI:**

> *"Write a DuckDB query to rank neighbourhoods within each city by their average number_of_reviews. Show the top 3 per city."*

**Expected output:**

```python
duckdb.query("""
    WITH ranked AS (
        SELECT
            city,
            neighbourhood,
            ROUND(AVG(number_of_reviews), 1) AS avg_reviews,
            RANK() OVER (PARTITION BY city ORDER BY AVG(number_of_reviews) DESC) AS rank
        FROM df
        WHERE neighbourhood IS NOT NULL
        GROUP BY city, neighbourhood
        HAVING COUNT(*) >= 5
    )
    SELECT city, neighbourhood, avg_reviews, rank
    FROM ranked
    WHERE rank <= 3
    ORDER BY city, rank
""").df()
```

**The takeaway:** You described what you wanted in plain English. Copilot wrote the window function, the CTE, the `HAVING` clause, and the filter. You just run it.

---

### Demo 4: Explain a query output

After running a query, paste the result back into Chat:

**💬 VS Code Chat UI:**

> *"I ran this DuckDB query on the Airbnb dataset and got this result: [paste result]. What does this tell us? Are there any patterns worth calling out for a business audience?"*

**The takeaway:** Copilot moves from raw numbers to plain-English insight. This is the commentary that goes in a dashboard or a slide.

---

## ✏️ SQL Challenge

Try these in order. For each one, write a Copilot prompt first - then run the result.

### Challenge 1 - Easy

Ask Copilot:

> 💬 *"Write a DuckDB query to find the average availability_365 for each room_type across all cities."*

### Challenge 2 - Medium

Ask Copilot:

> 💬 *"Write a DuckDB query that shows, for each city: total listings, percentage that are 'Entire home/apt', and the median number_of_reviews. Order by total listings descending."*

### Challenge 3 - Hard

Ask Copilot:

> 💬 *"Write a DuckDB SQL query using a CTE to find listings that have both above-average number_of_reviews AND above-average availability_365 for their city. Call these 'high engagement' listings. Show how many there are per city."*

<details>
<summary>💡 Hints</summary>

For Challenge 3, the CTE approach Copilot will likely produce:

```sql
WITH city_averages AS (
    SELECT city,
           AVG(number_of_reviews)  AS avg_reviews,
           AVG(availability_365)   AS avg_availability
    FROM df
    GROUP BY city
),
high_engagement AS (
    SELECT d.city
    FROM df d
    JOIN city_averages c ON d.city = c.city
    WHERE d.number_of_reviews > c.avg_reviews
      AND d.availability_365   > c.avg_availability
)
SELECT city, COUNT(*) AS high_engagement_listings
FROM high_engagement
GROUP BY city
ORDER BY high_engagement_listings DESC
```

If Copilot produces something different, ask: *"Explain what this CTE is doing, step by step."*

</details>

---

## ▶️ Your Turn

### Exercise: Build a neighbourhood report

Using Copilot, write a single DuckDB query that produces a neighbourhood summary table with:

- City
- Neighbourhood
- Number of listings
- Average `number_of_reviews`
- Average `availability_365`
- Percentage of listings that are "Entire home/apt"

Filter to neighbourhoods with at least 10 listings. Order by city, then by listing count descending.

Start with this prompt:

> 💬 *"Write a DuckDB query to summarise neighbourhoods in the Airbnb dataset. Include: city, neighbourhood, listing count, average reviews, average availability, and percentage of entire home listings. Filter to neighbourhoods with at least 10 listings."*

Then ask Copilot to explain what each column tells a property manager looking at this data.

---

## 📝 Assignment

The examples above queried the `df` DataFrame. Now practice the full workflow:

1. Pick a business question you would genuinely want to answer with this data (e.g. "Which city has the most hosts with multiple listings?" or "What is the relationship between minimum_nights and availability?")
2. Write a Copilot prompt that describes your question in plain English
3. Run the resulting query
4. Ask Copilot to explain the output in two sentences suitable for a slide deck

**Success criteria:** You have a working DuckDB query that answers a question you actually cared about, and a plain-English summary of the answer.

---

<details>
<summary>🔧 Troubleshooting</summary>

**"Column 'X' not found"**
Check the actual column names with `df.columns.tolist()`. DuckDB column names are case-sensitive.

**"duckdb.query() returns an error about 'df'"**
Make sure `df` is defined in the notebook kernel (run the data loading cells first). DuckDB reads from the live Python session.

**"Copilot wrote PostgreSQL/SQLite syntax"**
The DuckDB skill should handle this, but if not, add to your prompt: *"Use DuckDB syntax. Wrap with `duckdb.query(\"\"\" ... \"\"\").df()`."*

**"I want to save the result"**
```python
result = duckdb.query("SELECT ...").df()
result.to_csv("output.csv", index=False)
```
Ask Copilot: *"How do I save this DuckDB result to a CSV file?"*

</details>

---

## 🔑 Key Takeaways

1. **DuckDB = SQL on DataFrames** - query your pandas variables directly, no database needed
2. **The instructions file does the work** - `.github/copilot-instructions.md` tells Copilot to use DuckDB syntax automatically - no need to say "use DuckDB" in every prompt
3. **Describe in English, run in SQL** - window functions, CTEs, ranked results - all from a plain-English prompt
4. **Translate both ways** - pandas → SQL for analysts who prefer SQL; SQL → pandas for the reverse

---

## ➡️ What's Next

In **[Chapter 05: Custom Instructions & Agents](../05-custom-instructions-agents/README.md)** you'll learn:

- Why Copilot already knows to use DuckDB in this project (the skill and instructions files)
- How to write your own instruction files and skills for your own team's data and tools
- How to create a specialist data-analyst agent that applies your standards automatically

---

**[← Back to Chapter 03](../03-explore-visualise/README.md)** | **[Continue to Chapter 05 →](../05-custom-instructions-agents/README.md)**
