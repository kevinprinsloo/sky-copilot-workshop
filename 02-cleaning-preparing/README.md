![Data Analysis with GitHub Copilot — Sky Workshop](../images/Picture%201.png)

# Chapter 02 — Cleaning & Preparing Data 🧹

> **Real-world data is always messy. Copilot is remarkably good at diagnosing data quality problems and writing the code to fix them.**

Before you can trust any analysis, you need to know your data is clean. Missing values, wrong data types, outliers, inconsistent formatting — these are the invisible problems that lead to wrong conclusions. Copilot can spot them and fix them faster than doing it by hand.

> ⚠️ **Prerequisites:** Complete [Chapter 01](../01-understanding-data/README.md).

> ❌ **Sky environment note:** This chapter includes optional "Copilot CLI" examples. **Ignore those sections** — the CLI is not available in our GitHub Enterprise environment. All core exercises use VS Code Chat only.

## 🎯 Learning Objectives

By the end of this chapter you'll be able to:

- Ask Copilot to diagnose and fix data quality issues
- Generate new derived columns from plain-English descriptions
- Use Agent mode to make edits directly in the notebook
- Understand when Copilot's code needs reviewing before running

> ⏱️ **Estimated time:** ~35 minutes (10 min reading + 25 min hands-on)

---

## 🧩 Real-World Analogy: The Audit Before the Report

A good financial analyst doesn't build a model on unaudited data. You check the source, reconcile the totals, and flag anything that looks off — before the numbers go anywhere near a stakeholder.

Data cleaning is the same discipline applied to a dataset. Copilot doesn't remove the need for that judgement — but it does the tedious parts faster, and often catches things you'd miss.

---

## See It In Action

### Demo 1: Diagnose a data quality problem

Run the cleaning section of the notebook (Section 5). Then ask:

**💬 VS Code Chat UI:**

> *"The price column in our Airbnb dataset is missing for 72% of rows after cleaning. Write Python code to investigate whether the missingness is random or follows a pattern by city or room_type. Show the results as a formatted table."*

**What happens:** Copilot writes a groupby analysis that shows exactly which cities are missing prices. You discover it's not random — it follows the city. That's a data quality finding worth documenting.

**🖥️ Copilot CLI:**
```bash
copilot
> The price column in our Airbnb dataset is missing for 72% of rows. Write Python code to check whether missingness patterns vary by city or room_type.
```

---

### Demo 2: Generate a derived column

**💬 VS Code Chat UI:**

> *"Add a new column called `price_tier` that categorises each listing as 'Budget', 'Mid-range', or 'Luxury' based on the 33rd and 66th price percentiles within each city. Return 'Unknown' if price is missing. Write this as a reusable function."*

**What happens:** Copilot writes a `groupby().apply()` pattern that calculates per-city percentiles and assigns tiers. You get a function rather than inline code — reusable for any new city added to the dataset.

---

### Demo 3: Use Agent mode to edit the notebook

Switch to **Agent mode** (dropdown in Chat → **Agent**) and try:

> *"In the notebook samples/air-bnb-workshop.ipynb, add a cell after the price cleaning section that shows a summary table: for each city, show the number of listings with valid prices, the number without, and the percentage with. Format it clearly."*

**What happens:** Agent mode reads the notebook, identifies the right location, and adds the cell. You review and accept the change.

> 💡 **Tip:** Agent mode can edit files directly. Always read the proposed change before accepting — Copilot is usually right, but you're the analyst.

---

## ▶️ Your Turn

### Exercise 1 — Outlier detection

> 💬 *"Write code to identify outlier listings in the price column using the IQR method. Show how many outliers there are per city and what the threshold values are."*

### Exercise 2 — Classification column

> 💬 *"Add a column called `host_type` that classifies hosts as 'Individual' if they have 1–2 listings, 'Small operator' if they have 3–10 listings, or 'Professional' if they have more than 10. Use the `calculated_host_listings_count` column."*

### Exercise 3 — Document the cleaning steps

After running the cleaning cells, ask Copilot to write a summary:

> 💬 *"Write a brief data quality summary documenting the cleaning steps we applied to the Airbnb dataset. Format it as a markdown table with columns: Issue, Action Taken, Impact. Write it for a finance manager reviewing the methodology."*

---

## 📝 Assignment

The examples above cleaned the Airbnb dataset. Now apply the same thinking to a scenario from your own work:

1. Think of a data quality problem you've encountered (missing values, duplicates, inconsistent formats)
2. Ask Copilot to write the diagnostic code — the code that *finds* the problem, not just fixes it
3. Then ask it to write the fix
4. Finally, ask it to write a one-paragraph explanation of both steps for a non-technical stakeholder

**Success criteria:** You can move from "I suspect there's a problem" to "here's the problem, here's the fix, here's the plain-English explanation" — with Copilot doing the heavy lifting.

---

## 🔑 Key Takeaways

1. **Diagnose before fixing** — ask Copilot to show you the problem, then ask it to fix it. Two steps is safer than one.
2. **Ask for functions, not inline code** — reusable functions are more useful than one-off fixes
3. **Agent mode edits files** — use it for making changes directly in the notebook; review each change before accepting
4. **Always review generated code** — Copilot is fast but not infallible. You're the analyst; you make the call.

---

**[← Back to Chapter 01](../01-understanding-data/README.md)** | **[Continue to Chapter 03 →](../03-explore-visualise/README.md)**
