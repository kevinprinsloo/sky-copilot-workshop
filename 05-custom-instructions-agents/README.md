![Data Analysis with GitHub Copilot — Sky Workshop](../images/Picture%201.png)

# Chapter 05 — Custom Instructions & Agent Mode 🤖

> **What if Copilot already knew your tools, your data schema, and your team's conventions — before you even typed a word?**

So far, Copilot has been answering your questions one at a time. In this chapter, you'll learn how to give Copilot **persistent context** — project-level instructions it reads automatically — and how to use **Agent mode** in VS Code to let Copilot take multi-step actions across files.

By the end you'll understand exactly why Copilot knew to write DuckDB syntax in Chapter 04 without you asking — and how to set the same thing up for your own team.

> ⚠️ **Prerequisites:** Complete Chapters 01–04.

## 🎯 Learning Objectives

By the end of this chapter you'll be able to:

- Understand what `.github/copilot-instructions.md` does and how to edit it
- Give Copilot consistent context that applies across the whole team
- Use Agent mode in VS Code Chat to make changes across files
- Know when to use Chat mode vs Agent mode

> ⏱️ **Estimated time:** ~30 minutes (10 min reading + 20 min hands-on)

---

## 🧩 Real-World Analogy: Briefing a New Colleague

Imagine briefing a new hire before their first day. You tell them:

- "We use DuckDB for all SQL queries, not PostgreSQL"
- "The main dataset is called `df` and has these columns..."
- "When you write functions, add a docstring in plain English"

After that briefing, they don't need reminding every time. They just work to your standards automatically.

That's exactly what the custom instructions file does for Copilot.

---

## Layer 1 — Project Instructions (`.github/copilot-instructions.md`)

### What is it?

`.github/copilot-instructions.md` is a plain markdown file that GitHub Copilot reads automatically whenever you work in a VS Code project that contains it. It's committed to the repository, so every team member gets the same Copilot behaviour.

> **This is the only file Copilot reads automatically in VS Code.** Other files in this project (like the `SKILL.md` and `AGENTS.md` files) are useful reference documents, but they don't auto-load in VS Code — you reference them manually with `#filename` in Chat.

### Read the workshop instructions

In the Chat panel, try:

**💬 VS Code Chat UI:**

> *"#copilot-instructions.md — read this file and summarise in 3 bullets what Copilot should know about this project."*

### Why DuckDB worked in Chapter 04

Open `.github/copilot-instructions.md` in VS Code and look at the SQL section:

```markdown
## SQL queries — always use DuckDB

- Always write SQL using DuckDB syntax, not SQLite, PostgreSQL, or any other dialect.
- DuckDB can query pandas DataFrames directly by variable name — no loading step needed:
  duckdb.query("SELECT * FROM df WHERE city = 'London'").df()
```

That's why every SQL query Copilot suggested used `duckdb.query(...).df()` without you asking. The instructions file sets the default for the whole project.

### What else is in it?

The file in this project covers:
- **Project context** — what the data is, what the DataFrame is called
- **SQL rules** — always use DuckDB, always chain `.df()`
- **Data schema** — every column name and what it means
- **Python conventions** — which libraries to use, type hints, docstrings
- **Charting conventions** — figure sizes, titles, formatting

### Write your own instructions

To adapt this for your own team's project, edit the file or ask Copilot to help:

**💬 VS Code Chat UI — Agent mode:**

> *"Update .github/copilot-instructions.md to add a section about our team's SQL conventions: we use Snowflake SQL dialect, our main table is called `transactions`, and all monetary amounts should be formatted to 2 decimal places."*

Review what Agent mode proposes, then accept or adjust.

---

## Layer 2 — Agent Mode in VS Code

### What is it?

Agent mode is the built-in Copilot mode in VS Code where Copilot doesn't just answer questions — it takes actions. It can:
- Read and edit files
- Create new files
- Run terminal commands
- Chain multiple steps together

Switch to it by clicking the dropdown at the top of the Chat panel → **Agent**.

### Chat mode vs Agent mode

| | Chat mode | Agent mode |
|---|---|---|
| **What it does** | Answers questions, suggests code | Takes actions — reads, edits, creates files |
| **You paste the code** | Yes | No — it writes to the file directly |
| **Best for** | Getting suggestions, understanding concepts | Building something, making multi-file edits |
| **Review process** | Read the suggestion, copy what you need | Review each proposed change before accepting |

### Demo: Use Agent mode to add a notebook cell

Switch to Agent mode (dropdown → **Agent**) and try:

**💬 VS Code Chat UI — Agent mode:**

> *"In the notebook samples/air-bnb-workshop.ipynb, add a new cell after the existing data overview section. The cell should use DuckDB to produce a summary table: for each city, show the number of listings with valid prices, the number without, and the percentage with. Format the result clearly."*

**What happens:** Agent mode reads the notebook, identifies the right location, and proposes adding the cell. You review the change and accept it.

> 💡 **Always review before accepting.** Agent mode is usually right, but you're the analyst — you make the call on what goes into the notebook.

### Demo: Use Agent mode to create a file

**💬 VS Code Chat UI — Agent mode:**

> *"Create a new Python script at samples/quick_summary.py. The script should: import the same data as the notebook (use the same download URLs), use DuckDB to calculate median price and average reviews by city, and print the results as a formatted table. Add a docstring explaining what the script does."*

Agent mode will propose the file. Review it, then accept.

---

## Layer 3 — The `AGENTS.md` and `SKILL.md` files (reference documents)

This project also includes `AGENTS.md` (project root) and `.github/skills/duckdb-query/SKILL.md`. These are well-written reference documents that describe project conventions in a structured format.

**In VS Code**, these files do not auto-load — Copilot does not read them automatically. But you can use them manually:

- Drag them into Chat, or type `#AGENTS.md` to give Copilot their content as context
- They're useful as structured briefing documents you can reference any time

**Example:**

> *"#AGENTS.md — I'm going to write some analysis code. Apply the Python and SQL conventions from this file."*

> **Note on the wider GitHub ecosystem:** In the GitHub Copilot CLI (not available at Sky), `SKILL.md` files can trigger automatically when your prompt matches. On GitHub.com, `.agent.md` files define named coding agents. These features are not available in VS Code Copilot at Sky — but if access is granted in future, this project is already set up to use them.

---

## ▶️ Your Turn

### Exercise 1 — See the before/after

To see what Copilot does *without* instructions, open a new VS Code window, open a blank folder with no `.github/copilot-instructions.md`, and ask:

> 💬 *"Write a SQL query to count listings per city in a pandas DataFrame called df."*

You'll probably get generic SQL or pandas code. Back in the workshop folder, the same prompt produces DuckDB. Same model, different project context.

### Exercise 2 — Add your team's conventions

Edit `.github/copilot-instructions.md` and add a short section for a convention from your own work. For example:

- A SQL dialect your team uses
- A specific table or column naming pattern
- A formatting preference for reports

Then test it — ask Copilot a question that should trigger your new convention.

### Exercise 3 — Use Agent mode end-to-end

Switch to Agent mode, then complete this workflow in a single conversation:

1. Ask it to write a DuckDB query for top neighbourhoods by reviews and put it in a new notebook cell
2. Ask it to add a seaborn chart cell below that visualises the result
3. Ask it to write a two-sentence interpretation of the chart as a markdown cell

Notice how Agent mode maintains context across all three steps and works in the right locations in the file.

---

<details>
<summary>🔧 Troubleshooting</summary>

**"Copilot isn't following the instructions in copilot-instructions.md"**
Instruction files are loaded at session start. Close and re-open VS Code (or restart the Chat session) after adding or editing the file.

**"Agent mode isn't appearing in the dropdown"**
Make sure the GitHub Copilot Chat extension is up to date. In VS Code, go to Extensions → find GitHub Copilot Chat → check for updates.

**"Agent mode proposed a change I didn't want"**
Click **Discard** (not Accept). Agent mode always shows you what it's going to do before making changes. You're always in control.

**"The notebook didn't update when Agent mode said it would"**
Make sure the notebook is open in VS Code. Agent mode needs the file open and the kernel connected. Try running at least one cell first.

</details>

---

## 🔑 Key Takeaways

1. **`.github/copilot-instructions.md` = always-on context** — this is the file Copilot reads automatically in VS Code. Use it for project-wide rules: SQL dialect, schema, coding conventions.
2. **Commit it to git** — everyone on the team gets the same Copilot behaviour
3. **Agent mode is for building; Chat mode is for asking** — use Agent mode when you want Copilot to make changes; use Chat mode when you want to understand or get suggestions
4. **Always review Agent mode changes** — Copilot is fast and usually correct, but you're the analyst. The output needs to be right.
5. **The other files (`AGENTS.md`, `SKILL.md`) are reference documents** — useful for context via `#file`, but not auto-loaded in VS Code

---

## ➡️ What's Next

In **[Chapter 06: Putting It All Together](../06-putting-it-together/README.md)** you'll:

- Build a complete analysis pipeline using everything from this workshop
- Use Agent mode to scaffold a reusable Python script
- Practice the full workflow from data loading to stakeholder output

---

**[← Back to Chapter 04](../04-sql-with-duckdb/README.md)** | **[Continue to Chapter 06 →](../06-putting-it-together/README.md)**
