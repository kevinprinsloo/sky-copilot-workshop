![Data Analysis with GitHub Copilot — Sky Workshop](../images/Picture%201.png)

# Chapter 01 — Understanding Your Data 🔍

> **Watch Copilot explain a dataset, identify data quality problems, and tell you which columns actually matter — in seconds.**

The first step in any analysis is understanding what you're working with: how many rows, what columns mean, where the gaps are. Copilot can short-circuit this step dramatically. Instead of reading documentation or manually profiling each column, you describe the data and ask.

> ⚠️ **Prerequisites:** Complete [Chapter 00](../00-quick-start/README.md) first. Have `samples/air-bnb-workshop.ipynb` open in VS Code.

> ❌ **Sky environment note:** This chapter includes optional "Copilot CLI" examples. **Ignore those sections** — the CLI is not available in our GitHub Enterprise environment. All core exercises use VS Code Chat only.

## 🎯 Learning Objectives

By the end of this chapter you'll be able to:

- Use Copilot Chat to understand the structure of an unfamiliar dataset
- Ask Copilot to explain what columns mean and which are most useful
- Spot data quality problems with Copilot's help
- Use the `@` / `#file` syntax to give Copilot context about specific files

> ⏱️ **Estimated time:** ~30 minutes (10 min reading + 20 min hands-on)

---

## 🧩 Real-World Analogy: The New Starter

Think about joining a new team and being handed a spreadsheet with 20 columns and 50,000 rows. Nobody's around to explain it. Normally you'd spend an hour reading column headers, checking data types, and trying to work out what "availability_365" means.

With Copilot, you describe what you've got and ask. It's like having a knowledgeable colleague available immediately who can read the data, explain the structure, and flag the things worth investigating first.

---

## See It In Action

### Demo 1: Explain what the dataset contains

Open Copilot Chat (`Cmd+Option+I` / `Ctrl+Alt+I`) and try this:

**💬 VS Code Chat UI:**

> *"I'm working with an Airbnb listings dataset that has these columns: id, name, host_id, neighbourhood, room_type, price, minimum_nights, number_of_reviews, reviews_per_month, availability_365, city. Explain what each column likely represents and which ones would be most useful for understanding what drives listing prices."*

**What happens:** Copilot gives you a column-by-column breakdown in plain English — including which are likely most correlated with price, and which are probably less useful. A junior analyst would take 20 minutes to write the same thing.

---

**🖥️ Copilot CLI (optional):**

```bash
copilot
> I'm working with an Airbnb listings dataset. Columns are: id, name, host_id, neighbourhood, room_type, price, minimum_nights, number_of_reviews, reviews_per_month, availability_365, city. Explain what each column represents and which are most useful for price analysis.
```

---

### Demo 2: Explain a specific output

Run the dataset overview cell in the notebook (cell under **Section 3 — Dataset Overview**). Then paste the output into Chat:

**💬 VS Code Chat UI:**

> *"This is the output from `df.describe()` on our Airbnb dataset: [paste the output]. Explain what stands out to you. Are there any values that look suspicious or worth investigating?"*

**What happens:** Copilot reads the summary statistics and flags things like extreme outliers in `minimum_nights`, the high percentage of missing `price` values, or the wide range in `availability_365`. This is exactly the kind of first-look commentary you'd put in a data quality report.

---

### Demo 3: Explain missing data

Run the missing values cell (Section 4) and ask:

**💬 VS Code Chat UI:**

> *"The price column is missing for 72% of rows in our dataset. What are the most likely reasons for this in an Airbnb context, and how should we handle it for an analysis?"*

**The takeaway:** Rather than guessing, you get three or four plausible explanations (different data extract types, scraping limitations, city-level data differences) plus a recommended approach. This is the kind of question you'd normally ask a more senior colleague.

---

## The `#file` and `@` Syntax

You can give Copilot direct access to files, so it can answer questions based on the actual content rather than you having to paste things in.

**💬 VS Code Chat UI** — drag the notebook into the Chat panel, or type `#` followed by the filename:

> *"#air-bnb-workshop.ipynb — look at the data loading section. What would happen if the download for one city fails? How would the code behave?"*

**🖥️ Copilot CLI:**

```bash
copilot
> @samples/air-bnb-workshop.ipynb Look at the data loading section. What would happen if one city download fails?
```

**Key insight:** Both `#file` (VS Code) and `@file` (CLI) let Copilot read the actual file rather than working from your description. Use this whenever you want Copilot to reason about specific code or data.

---

## 🔄 Interactive vs Agent Mode

For the exercises above, you've been using **Chat mode** — Copilot answers your question but doesn't take action.

**Agent mode** can do more: it reads files, runs code, and edits notebooks. Try switching to Agent mode (dropdown at the top of the Chat panel → **Agent**) and ask:

> *"Open the notebook at samples/air-bnb-workshop.ipynb and summarise what the dataset overview section shows. Tell me the shape of the data, which columns have missing values, and what the most common room type is."*

**What's different:** In Agent mode, Copilot reads the notebook file directly and works through the question systematically, rather than waiting for you to paste output.

**🖥️ CLI equivalent:**
```bash
copilot
# Copilot CLI is always in interactive (agent-like) mode by default
> @samples/air-bnb-workshop.ipynb Summarise what the dataset overview section shows
```

---

## ▶️ Your Turn

### Exercise 1 — Column decoder

Run the notebook up to and including the overview cell, then ask Copilot:

> 💬 *"Looking at this Airbnb dataset, which column would be the best proxy for how popular a listing is, given that we don't have booking data? Explain your reasoning."*

There's no single right answer — the interesting part is Copilot's reasoning.

### Exercise 2 — Data quality report

Run the missing values cell, then ask Copilot to write a short data quality summary:

> 💬 *"Based on this missing values output, write a 3-bullet data quality summary I could include in a report. Audience is a finance manager who needs to decide whether to trust a price analysis based on this data."*

### Exercise 3 — Explain someone else's code

Select the data loading code block in the notebook, right-click, and choose **Copilot: Explain**. 

Then ask in Chat:

> 💬 *"Why does this code sample 2,000 rows per city rather than using all the data? What are the trade-offs?"*

---

## 📝 Assignment

The examples above focused on understanding the Airbnb dataset. Now apply the same skills to a different scenario:

Imagine you've just received a new CSV file from a colleague containing monthly sales data. You don't have any documentation.

1. Ask Copilot to write Python code that produces a "first look" summary of an unknown DataFrame — shape, column names, data types, missing value counts, and numeric summary stats — all in one output.
2. Ask Copilot to explain what each part of the code does, as if explaining to someone who has never written Python.
3. Ask Copilot what questions you should always ask when you first see a new dataset.

**Success criteria:** You have a reusable "first look" function you could apply to any new dataset, and you understand what it produces.

---

<details>
<summary>🔧 Troubleshooting</summary>

**"Copilot doesn't seem to know what columns I have"**
Either paste the column list directly into the prompt, or use `#filename` to reference the notebook. The more context you give, the better the response.

**"The response is too technical"**
Add to your prompt: *"Explain this for a finance analyst, not a developer. Use plain language."*

**"Copilot's answer seems generic"**
Be more specific. Instead of "explain this data", try "explain what the `availability_365` column means for a property owner who lists on Airbnb, and what a value of 30 vs 300 would tell us."

</details>

---

## 🔑 Key Takeaways

1. **Describe, don't paste** — for quick questions, describe what you're working with. For specific code questions, use `#file` or `@file`.
2. **Ask for reasoning** — Copilot's value isn't just the answer, it's the explanation. Ask "why?" and "what would you investigate first?"
3. **Agent mode goes further** — it can read files and chain multiple steps together without you manually copying outputs between cells

---

## ➡️ What's Next

In **[Chapter 02: Cleaning & Preparing Data](../02-cleaning-preparing/README.md)**, you'll learn:

- How to ask Copilot to fix data quality issues
- Generating new columns from plain-English descriptions
- Using Agent mode to make edits directly in the notebook

---

**[← Back to Quick Start](../00-quick-start/README.md)** | **[Continue to Chapter 02 →](../02-cleaning-preparing/README.md)**
