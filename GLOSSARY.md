![Data Analysis with GitHub Copilot — Sky Workshop](./images/Picture%201.png)

# Glossary

Quick reference for terms used throughout this workshop. You don't need to memorise these — refer back as needed.

---

## A

### Agent mode
A mode in the GitHub Copilot Chat panel (VS Code) where Copilot takes actions — reading and editing files, creating new files, running code — rather than just answering questions. Switch to it via the dropdown at the top of the Chat panel. Always review its proposed changes before accepting.

### AGENTS.md
A markdown file in the project root that gives AI tools context about the project: what the data contains, which tools to use, coding conventions, and so on. GitHub Copilot in VS Code does not read this file automatically — it is used as a reference document you can share with Copilot via `#AGENTS.md` in Chat. (Some other AI tools, including Cursor and the GitHub Copilot CLI, do read it automatically.)

---

## C

### Chat mode
The default mode in the GitHub Copilot Chat panel. Copilot answers your questions and suggests code, but does not make changes to files itself. You copy the suggestion and paste it where you need it.

### Context
The information Copilot has available when generating a response — your message, any files you've referenced with `#`, the custom instructions file, and the current file you're editing. More context generally means better responses.

### copilot-instructions.md
The file at `.github/copilot-instructions.md` that GitHub Copilot reads automatically in VS Code. Use it to set project-wide conventions: SQL dialect, schema, coding standards, tone. Committed to git so the whole team gets the same behaviour.

### CTE (Common Table Expression)
A SQL construct that lets you define a named temporary result set within a query using `WITH`. CTEs make complex queries more readable by breaking them into named steps. DuckDB supports them fully. Example: `WITH city_avg AS (SELECT city, AVG(price) FROM df GROUP BY city) SELECT * FROM city_avg WHERE avg > 100`.

---

## D

### DataFrame
A table-like data structure in Python (from the pandas library), with rows and columns. Similar to a spreadsheet or a SQL result set. In this workshop the main DataFrame is called `df`.

### DuckDB
An in-process SQL database engine that can query pandas DataFrames directly — no database server, no connection string. You write a SQL query, DuckDB reads from the live Python variable, and returns a new DataFrame. Syntax: `duckdb.query("SELECT ... FROM df").df()`.

---

## F

### `#file` (in Chat)
A way to give Copilot access to a specific file's content within a Chat message. Type `#` followed by the filename, or drag the file into the Chat panel. Copilot can then answer questions based on the actual content.

---

## I

### Inline suggestion
Code that Copilot suggests as you type in the editor — shown in grey. Press **Tab** to accept, **Escape** to reject, **Alt+]** (Windows) or **Option+]** (Mac) to cycle through alternatives.

### Inline edit
A targeted edit mode triggered by selecting code and pressing `Cmd+I` (Mac) / `Ctrl+I` (Windows). Copilot applies a change to just the selected code. Different from Chat (which explains and suggests) and Agent mode (which acts across files).

---

## J

### Jupyter Notebook
A file format (`.ipynb`) that mixes code cells, text, and outputs in a single document. Common in data analysis. In VS Code, install the Jupyter extension to open and run notebooks.

---

## K

### Kernel
The Python process that runs the code in a Jupyter notebook. When VS Code asks you to "select a kernel", choose your Python 3.10+ installation. The kernel needs to be running for cells to execute.

---

## P

### pandas
The main Python library for working with tabular data. Provides the DataFrame structure. In this workshop, pandas is used to load data and do basic cleaning. SQL queries are done with DuckDB.

### Prompt
What you type into the Copilot Chat panel. A good prompt gives context (what data you're working with, what the column names are), describes what you want clearly, and specifies the format if it matters.

---

## S

### seaborn
A Python plotting library built on top of matplotlib. Good for statistical charts — bar charts, box plots, KDE plots, heatmaps. In this workshop we use it for static charts, and plotly for interactive ones.

### SKILL.md
A structured markdown document that describes a task-specific set of instructions. In this project, `.github/skills/duckdb-query/SKILL.md` contains DuckDB conventions. In VS Code, this file is not read automatically — reference it manually with `#.github/skills/duckdb-query/SKILL.md` in Chat. (In the GitHub Copilot CLI, SKILL.md files do load automatically when your prompt matches — but the CLI is not available at Sky.)

---

## T

### Token
A unit of text that AI models process — roughly 4 characters or 0.75 words. Large files, long conversations, and many `#file` references all use tokens. If Copilot seems to be ignoring earlier context, the conversation may be near its token limit. Start a new Chat session.

### Type hints
Python annotations that describe what types a function expects and returns. Example: `def get_summary(city: str) -> dict:`. They don't affect how the code runs, but make it easier to read and let tools flag mistakes. The `AGENTS.md` in this project asks Copilot to always add type hints.

---

## W

### Window function
A SQL function that calculates a value across a set of rows related to the current row, without collapsing the result into a group. Useful for ranking, running totals, and comparisons within a group. Example: `RANK() OVER (PARTITION BY city ORDER BY price DESC)`. DuckDB supports window functions fully.
