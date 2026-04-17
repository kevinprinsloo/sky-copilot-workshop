![Data Analysis with GitHub Copilot — Sky Workshop](../images/Picture%201.png)

# Chapter 06 — Putting It All Together 🎯

> **Use everything you've learned to build a complete, reusable analysis pipeline — from data loading to exported report — entirely through Copilot prompts.**

This chapter is a capstone. There's less instruction and more doing. You'll combine custom instructions, the DuckDB skill, the data-analyst agent, and Agent mode to build something you could actually hand to a colleague.

> ⚠️ **Prerequisites:** Complete Chapters 01–05.

## 🎯 Learning Objectives

By the end of this chapter you'll have:

- Built a reusable `city_report.py` script using Agent mode
- Used the full skills + agent + instructions stack together
- Produced an analysis output you could share with a stakeholder
- Reflected on which Copilot features saved the most time

> ⏱️ **Estimated time:** ~60 minutes (10 min reading + 50 min hands-on)

---

## The Scenario

Your manager has asked for a **monthly city performance report** on the Airbnb market across your five cities. They want:

1. A summary table: median price, average reviews, % entire home, average availability
2. A chart: room type share per city
3. A top-10 neighbourhood table for a selected city
4. All of it saved to files so it can be re-run next month

You're going to build this end-to-end using Copilot.

---

## Part 1 — Scaffold the Script with Agent Mode

Switch to **Agent mode** in VS Code Chat (dropdown → **Agent**) and give it the full task:

**💬 VS Code Chat UI — Agent mode:**

> *"Create a Python script called `samples/city_report.py` that:*
> *1. Loads 2,000 rows of Airbnb data per city using the same URLs as air-bnb-workshop.ipynb*
> *2. Cleans the price column and adds has_price and price_capped columns*
> *3. Uses DuckDB to calculate a summary table: city, total listings, median price (where available), average reviews, average availability_365, percentage of entire home listings*
> *4. Creates a stacked bar chart (plotly) showing room type share per city and saves it as reports/room_type_share.html*
> *5. Saves the summary table as reports/city_summary.csv*
> *6. Prints the summary table to the console in a readable format*
> *Create a reports/ directory if it doesn't exist."*

Agent mode will:
1. Create `samples/city_report.py`
2. Create `reports/` directory
3. May run the script to verify it works

Review each file it creates before accepting.

**🖥️ Copilot CLI equivalent:**
```bash
copilot
> /plan Create a city_report.py script that loads Airbnb data, cleans it, produces a DuckDB summary table, a plotly chart saved as HTML, and exports to CSV
# Review the plan
# Accept → Copilot implements step by step
```

---

## Part 2 — Add the Neighbourhood Report

Now extend the script. With Agent mode still active:

> *"Add a function to city_report.py called `neighbourhood_report(df, city, n=10)` that: takes a DataFrame, a city name, and an optional row count; uses DuckDB to find the top N neighbourhoods by average number_of_reviews for that city (minimum 5 listings); prints the result as a table; and saves it as reports/{city}_top_neighbourhoods.csv. Call this function for London after the summary table."*

---

## Part 3 — Use the Data-Analyst Agent for the Narrative

Switch to the **data-analyst agent** (select from the Agent mode dropdown, or `copilot --agent data-analyst` in the CLI):

> *"I've run city_report.py and got these results: [paste your summary table output]. Write a short management commentary — 4 bullet points — that a Head of Analytics could include in a monthly market update. Highlight the most interesting findings and flag anything that needs explanation."*

This is the combination that matters: Agent mode built the code; the data-analyst agent writes the business narrative.

---

## Part 4 — Make It Robust

Ask Copilot to harden the script:

**💬 VS Code Chat UI:**

> *"Review city_report.py for edge cases: what happens if one city download fails? What if the reports/ directory already exists? What if price data is missing for all cities? Add appropriate error handling and informative print statements."*

Then:

> *"Add a command-line argument `--city` so the script can be run for a single city: `python city_report.py --city London`. When a city is specified, skip the global summary and only run the neighbourhood report for that city."*

---

## Part 5 — Document It

Ask Copilot to write documentation:

> *"Write a README section for city_report.py that explains: what it does, how to run it, what outputs it produces, and what to do if a city download fails. Write for a finance analyst who is not a Python developer."*

---

## Reflection: Which Features Saved the Most Time?

Take 5 minutes and consider:

| Feature | Time saved | What it replaced |
|---|---|---|
| `AGENTS.md` / `copilot-instructions.md` | | |
| DuckDB skill | | |
| Data-analyst agent | | |
| Agent mode (file creation/editing) | | |
| Inline suggestions | | |
| Copilot Chat (question-answering) | | |

This is worth discussing as a group. Which features felt most immediately useful for your day-to-day work? Which would need more setup to be worth it?

---

## Bonus: The Copilot CLI Workflow

If you're comfortable in the terminal, try reproducing Part 1 entirely in the CLI:

```bash
# 1. Use the data-analyst agent
copilot --agent data-analyst

# 2. Plan first
> /plan Create city_report.py: loads Airbnb data, cleans, DuckDB summary, plotly chart, CSV export

# 3. Review the plan, then proceed
# 4. Let Copilot implement step by step
# 5. Review diffs with /diff before finalising
> /diff
```

The CLI `/plan` → implement → `/diff` → review workflow is particularly good for larger scripts where you want to see the whole approach before any code is written.

---

## 📝 Final Assignment

Adapt `city_report.py` for a dataset from your own work (or a hypothetical one):

1. Update `AGENTS.md` to describe your own project's data — schema, tools, SQL dialect
2. Modify the script to load your data instead of Airbnb data
3. Write a skill file for the most common analysis you do
4. Run the full pipeline and produce a stakeholder-ready output

This is the closest this workshop gets to "real work." The goal is to end with something you could actually use.

---

## 🔑 Final Key Takeaways

1. **Instructions + skills + agents stack together** — each layer adds specificity without slowing you down
2. **Agent mode is for building; Chat mode is for asking** — use the right one for the task
3. **Describe the goal, not the steps** — the best Copilot prompts say what you want the output to be, not how to produce it
4. **Review everything** — Copilot is fast and usually right, but you are the analyst. The numbers need to be correct.
5. **The real value is the workflow** — not any single prompt, but the combination of instructions + skills + agent that means you never have to explain the same thing twice

---

## Where to Go Next

| Topic | Resource |
|---|---|
| Full Copilot CLI course | [github/copilot-cli-for-beginners](https://github.com/github/copilot-cli-for-beginners) |
| Community skills and agents | [github/awesome-copilot](https://github.com/github/awesome-copilot) |
| Official documentation | [docs.github.com/copilot](https://docs.github.com/copilot) |
| MCP servers (connect to external APIs) | [Chapter 06 of the CLI course](https://github.com/github/copilot-cli-for-beginners/tree/main/06-mcp-servers) |

---

**[← Back to Chapter 05](../05-custom-instructions-agents/README.md)** | **[Back to Workshop Home →](../README.md)**
