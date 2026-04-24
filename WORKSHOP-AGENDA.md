# Workshop Agenda — Data Analysis with GitHub Copilot (20 minutes)

> **For participants and facilitators.** This page is the shortest path through the workshop. Follow the steps below in order. Everything else in the chapter folders is available as self-study material after the session.

---

## Before the session — do this in advance (5–10 min)

Complete [Chapter 00 — Quick Start](./00-quick-start/README.md) before the session starts:

1. Install VS Code
2. Install the **GitHub Copilot** and **Jupyter** extensions
3. Sign in to GitHub and verify your Copilot access
4. Clone/download this repository and open it in VS Code
5. Open `samples/air-bnb-workshop.ipynb`
6. Run the first cell (installs packages) and the second cell (loads data)
7. Open Copilot Chat (`Cmd+Option+I` on Mac / `Ctrl+Alt+I` on Windows) and send any message to confirm it responds

If any of those steps fail, raise it at the start of the session — don't wait.

---

## Session (20 minutes)

### ① Chat basics — 5 minutes

**What:** Ask Copilot questions. Give it context. Use `#file` to point it at your notebook.

**Open the Copilot Chat panel** (`Cmd+Option+I` / `Ctrl+Alt+I`). Try these prompts in order:

```
I'm working with an Airbnb listings dataset with columns: city, room_type, price,
number_of_reviews, availability_365, neighbourhood. Explain what each column likely
represents and which ones would be most useful for understanding listing popularity.
```

Then drag the notebook file `samples/air-bnb-workshop.ipynb` into the Chat panel (or type `#air-bnb-workshop`) and ask:

```
#air-bnb-workshop.ipynb — look at the data loading section. What would happen if the
download for one city fails?
```

Then select any code cell in the notebook → right-click → **Copilot: Explain**. Read the explanation.

> **Skill learned:** You can give Copilot context about a file by dragging it in or using `#filename`. You don't have to paste code manually.

---

### ② Inline completions — 3 minutes

**What:** Copilot suggests code as you type. Tab to accept, Escape to reject.

Open a **new notebook cell** and type this comment — then pause:

```python
# Count the number of listings per city, ordered by count descending
```

Copilot should suggest code. Press **Tab** to accept.

Try another cell:

```python
# Create a bar chart showing average number_of_reviews by room_type
```

Pause again. If you see a grey suggestion, Tab accepts. **Alt+]** (Mac: **Option+]**) cycles to the next suggestion. **Escape** rejects.

> **Skill learned:** Comments are prompts. The more specific your comment, the better the suggestion.

---

### ③ SQL with DuckDB — 5 minutes

**What:** Run SQL directly on your pandas DataFrame. No database server. No connection string.

In the Chat panel, paste this prompt:

```
Write a DuckDB query to count the number of listings per city, ordered from largest
to smallest. The DataFrame is called df.
```

Copy the result into a new notebook cell and run it.

Then ask:

```
Write a DuckDB query that shows, for each city: total listings, percentage of listings
that are 'Entire home/apt', and the median number_of_reviews. Order by total listings.
```

Run it. Then paste the output back into Chat and ask:

```
I ran this DuckDB query and got this result: [paste your output here].
What does this tell us? Are there any patterns worth calling out for a business audience?
```

> **Skill learned:** Describe the question in plain English. Copilot writes the SQL. You run it and ask for the interpretation.

---

### ④ Charts from plain English — 4 minutes

**What:** Describe a chart, get the code, iterate in plain English.

In the Chat panel:

```
Create a horizontal bar chart showing the average number_of_reviews for each room_type
across all cities. Colour the bars. Add a title and axis labels. Use seaborn.
```

Copy the code into a notebook cell and run it. Then ask Copilot to improve it:

```
Make the x-axis label easier to read, add a subtitle saying 'Based on Airbnb data —
2,000 listings per city', and make the bars slightly thinner.
```

After running the improved chart, ask:

```
Based on this bar chart, write a two-sentence interpretation I could include in a
management report. Audience is a business stakeholder who doesn't read code.
```

> **Skill learned:** Describe what you want, not how to draw it. Iterate in plain English. Ask for the interpretation too — not just the chart.

---

### ⑤ Custom instructions — 3 minutes

**What:** Teach Copilot your project's conventions once. It applies them automatically.

In the Chat panel:

```
#copilot-instructions.md — read this file and summarise in 3 bullets what Copilot
should know about this project.
```

Notice that the file already tells Copilot to use DuckDB syntax, to query `df` directly, and to follow the charting conventions. That's why Copilot wrote `duckdb.query(...)` in step ③ without you asking.

Then open `.github/copilot-instructions.md` in VS Code and look at it. You can edit this file for your own team — add your SQL dialect, your table names, your output style. Every Copilot session in this folder will pick it up.

> **Skill learned:** `.github/copilot-instructions.md` is the file that gives Copilot persistent project context. Commit it to your repo and the whole team gets consistent Copilot behaviour.

---

## After the session — self-study

The full chapters are available for self-paced learning:

| Chapter | Topic | What's covered |
|:---:|---|---|
| [01](./01-understanding-data/README.md) | Understanding your data | More Chat techniques, Agent mode, data quality prompts |
| [02](./02-cleaning-preparing/README.md) | Cleaning & preparing | Derived columns, outlier detection, Agent mode file editing |
| [03](./03-explore-visualise/README.md) | Explore & visualise | Interactive Plotly charts, correlation heatmaps, chart interpretation |
| [04](./04-sql-with-duckdb/README.md) | SQL with DuckDB | Window functions, CTEs, advanced SQL challenges |
| [05](./05-custom-instructions-agents/README.md) | Custom instructions | How to write your own `copilot-instructions.md`, Agent mode in depth |
| [06](./06-putting-it-together/README.md) | End-to-end pipeline | Build a reusable city report script with Copilot |

---

## Quick reference — prompting patterns

These patterns work across all five skills above. Copy and adapt them.

**Give context:**
```
I'm working with a pandas DataFrame called df that contains Airbnb listings.
The columns are: city, room_type, price, number_of_reviews, availability_365.
[Your question here]
```

**Ask for plain English:**
```
Explain this as if I've never written Python. What does each line do?
```

**Ask for step-by-step help:**
```
Walk me through this step by step. After each step, pause and ask if I understand
before moving on.
```

**Avoid vague prompts:**
- ❌ "Analyse the data"
- ✅ "Find the top 5 neighbourhoods by average number_of_reviews in London, using only listings with more than 10 reviews"

**Ask Copilot to improve its own output:**
```
That's a good start. Now make it: [more specific change]. Keep everything else the same.
```

**Attach context from the notebook:**
- Drag a file into the Chat panel, or type `#filename` to reference it
- Select code → right-click → **Copilot: Explain** for instant explanation of any cell

---

## Sky environment notes

| Feature | Status |
|---|---|
| Copilot Chat in VS Code | ✅ Available |
| Inline completions (Tab) | ✅ Available |
| Inline editing (`Cmd+I` on selected code) | ✅ Available |
| Right-click → Copilot: Explain / Fix | ✅ Available |
| `#file` context in Chat | ✅ Available |
| Agent mode in VS Code Chat | ✅ Available |
| `.github/copilot-instructions.md` | ✅ Available |
| GitHub Copilot CLI (`gh copilot`) | ❌ Not available — currently in public preview, blocked by Sky GitHub Enterprise policy |
| MCP servers | ❌ Not available in our environment |

Any reference to the Copilot CLI or MCP in the chapter READMEs can be ignored for this workshop.
