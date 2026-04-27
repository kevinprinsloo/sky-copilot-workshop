![Data Analysis with GitHub Copilot - Sky Workshop](./images/Picture%201.png)

# 📊 Data Analysis with GitHub Copilot - Sky Workshop

> **Learn how GitHub Copilot can help you do more advanced analytical work without needing deep software engineering skills.**

This hands-on workshop is designed for **finance and analytics teams** who work with data every day. You'll work with a real dataset throughout all chapters, using Copilot to explore, clean, analyse, and explain data - all from VS Code.

---

## ⚡ 20-Minute Workshop Path

**Start here if you're in the live session.** The full agenda with copy-paste prompts is in:

> **[WORKSHOP-AGENDA.md](./WORKSHOP-AGENDA.md) - the 20-minute session guide**

The chapter folders below contain the full reference material for self-study after the session.

---

## 🚦 Sky environment - what's available

This workshop uses **GitHub Copilot in VS Code only**. Some features described in GitHub Copilot documentation are not yet available in our GitHub Enterprise environment:

| Feature | Available at Sky |
|---|---|
| Copilot Chat in VS Code | ✅ |
| Inline completions (Tab to accept) | ✅ |
| Inline editing (`Cmd+I` on selected code) | ✅ |
| Right-click → Copilot: Explain / Fix | ✅ |
| `#file` context in Chat | ✅ |
| Agent mode in VS Code Chat | ✅ |
| `.github/copilot-instructions.md` | ✅ |
| GitHub Copilot CLI (`gh copilot`) | ❌ Currently in public preview - blocked by Sky GitHub Enterprise policy |
| MCP servers | ❌ Not available in our environment |

> Any "Copilot CLI" sections in the chapter READMEs are marked optional and can be skipped entirely.

---

## 🔄 Automating with Copilot - what's possible today

Beyond one-off chat prompts, Copilot supports several mechanisms for **teaching it your team's conventions and automating repetitive work**. Understanding these is key to getting long-term value from Copilot in an analytics workflow.

| Approach | What it does | How to use it | Available at Sky |
|---|---|---|---|
| **`.github/copilot-instructions.md`** | Project-wide context that Copilot reads automatically in every chat session. Set your SQL dialect, data schema, charting conventions, and coding standards once - Copilot applies them without you repeating yourself. | Create the file and commit it to your repo. The whole team benefits immediately. | ✅ Yes |
| **`AGENTS.md`** | A broader project context file in the repo root. Describes the data, tools, and conventions for any AI assistant. Copilot in VS Code does not read it automatically - reference it with `#AGENTS.md` in Chat. | Create in the repo root. Reference manually when needed. | ✅ Yes (manual reference) |
| **Skill files (`.github/skills/*/SKILL.md`)** | Task-specific instruction documents. Think of them as "recipe cards" for recurring tasks - e.g., running a pipeline, writing a DuckDB query, adding a chart. Reference them in Chat and Copilot follows the instructions. | Create under `.github/skills/<task-name>/SKILL.md`. Reference with `#` in Chat. | ✅ Yes (manual reference) |
| **Custom agents (`.github/agents/*.agent.md`)** | Specialised personas with defined tool access and behaviour. For example, an "Analyst" agent that always uses DuckDB and follows your charting conventions. | Create `.agent.md` files. Select the agent from the Chat dropdown. | ✅ Requires VS Code 1.106+ |
| **Copilot CLI (`gh copilot`)** | Shell-level Copilot access - ask questions and generate commands from the terminal. Would enable pipeline automation from the command line. | `gh copilot suggest` / `gh copilot explain` | ❌ Public preview - blocked by policy |
| **MCP servers** | Connect Copilot to external tools (databases, APIs, services) via the Model Context Protocol. Would enable live data queries from Chat. | Configure in VS Code settings or `.agent.md` files. | ❌ Not available |

### Practical example - the analysis pipeline skill

This repo includes a skill file at [`.github/skills/analysis-pipeline/SKILL.md`](./.github/skills/analysis-pipeline/SKILL.md) and a reference Python script at [`samples/airbnb_analysis_pipeline.py`](./samples/airbnb_analysis_pipeline.py). In a future Copilot session, an analyst can reference the skill and ask Copilot to run, modify, or extend the pipeline:

```
#.github/skills/analysis-pipeline/SKILL.md - Run the analysis pipeline
for London and Paris only, and add a correlation heatmap to the charts.
```

The accompanying guide at [`samples/PIPELINE-README.md`](./samples/PIPELINE-README.md) walks through building this pipeline from scratch using Copilot's Plan and Agent modes - a step-by-step exercise designed for analysts who are new to Python.

---

## 🎯 What You'll Learn

| Chapter | Theme | What You'll Do |
|:-------:|-------|----------------|
| 00 | 🚀 [Quick Start](./00-quick-start/README.md) | Set up VS Code, install Copilot, open the workshop |
| 01 | 🔍 [Understanding Your Data](./01-understanding-data/README.md) | Load a dataset and explore it with Copilot's help |
| 02 | 🧹 [Cleaning & Preparing](./02-cleaning-preparing/README.md) | Spot and fix data quality issues faster |
| 03 | 📊 [Explore & Visualise](./03-explore-visualise/README.md) | Generate charts from plain-English descriptions |
| 04 | 🗄️ [SQL with DuckDB](./04-sql-with-duckdb/README.md) | Run SQL directly on your data - no database needed |
| 05 | 🤖 [Custom Instructions](./05-custom-instructions-agents/README.md) | Teach Copilot your tools, data, and team standards |
| 06 | 🎯 [Putting It All Together](./06-putting-it-together/README.md) | Build a reusable analysis pipeline end-to-end |

---

## 📖 How This Workshop Works

Each chapter follows the same pattern:

1. **Real-World Analogy** - understand the concept through a familiar comparison
2. **Core Concepts** - the essential knowledge, kept brief
3. **Hands-On Demos** - prompts to try immediately, with expected outputs
4. **Your Turn** - a challenge to try yourself
5. **What's Next** - preview of the next chapter

**All prompts are ready to copy.** Every Copilot prompt in this workshop can be pasted directly into the Chat panel.

---

## 🗂️ The Dataset

Throughout this workshop we use real **Airbnb listings data** from [Inside Airbnb](http://insideairbnb.com/) - 2,000 listings per city across New York, London, Paris, Amsterdam, and Barcelona.

This is the kind of tabular data you'd recognise from your own work: rows and columns, missing values, price outliers, categorical fields like room type and neighbourhood. The analysis tasks - summarising, cleaning, segmenting, visualising - map directly to things analytics and finance teams do every day.

The data lives in `samples/air-bnb-workshop.ipynb`. You'll load and work with it throughout the workshop.

---

## ✅ Prerequisites

| Requirement | Details |
|---|---|
| **GitHub account** with Copilot access | [Check your access](https://github.com/settings/copilot) |
| **VS Code** installed | [Download](https://code.visualstudio.com/) |
| **GitHub Copilot extension** in VS Code | Install from the Extensions panel |
| **Python 3.10+** | [Download](https://www.python.org/downloads/) |
| **Jupyter extension** in VS Code | Install from the Extensions panel |

> 💡 **No terminal experience needed.** All core exercises use the VS Code Chat panel.

---

## 🧭 How to Use GitHub Copilot - Modes & Features

GitHub Copilot in VS Code offers several distinct ways to interact. Each is suited to different tasks. This section explains what they are, when to use them, and how to switch between them.

### Chat Modes

The Copilot Chat panel (`Cmd+Option+I` / `Ctrl+Alt+I`) has a **mode dropdown** at the top. Click it to switch between modes.

#### Ask Mode

| | |
|---|---|
| **What it does** | A read-only conversational mode. Copilot answers questions, explains code, and suggests approaches - but does **not** modify any files. |
| **When to use it** | When you want to understand something before changing it. Great for exploring unfamiliar code, asking "what does this do?", or getting a second opinion on an approach. |
| **How to activate** | Select **Ask** from the mode dropdown at the top of the Chat panel. |

**Example prompts:**

```
What does the groupby().agg() chain do in this cell?
```

```
#air-bnb-workshop.ipynb - explain the data cleaning steps and why they matter.
```

#### Edit Mode

| | |
|---|---|
| **What it does** | Copilot suggests edits directly to files you have open. It shows proposed changes as diffs that you can accept or reject - one file at a time. |
| **When to use it** | When you have a specific, focused change in mind - fixing a bug, refactoring a function, or updating a single file. |
| **How to activate** | Select **Edit** from the mode dropdown. You can also select code in the editor, press `Cmd+I` (Mac) / `Ctrl+I` (Windows), and type your instruction for an inline edit. |

**Example prompts:**

```
Rename the 'price' column to 'listing_price' everywhere in this notebook.
```

```
Add error handling to the data download function.
```

#### Agent Mode

| | |
|---|---|
| **What it does** | The most autonomous mode. Copilot can read and write files, run terminal commands, install packages, and iterate on errors - all within a single conversation. It plans a sequence of steps and executes them. |
| **When to use it** | When the task spans multiple files or requires running code. Building a new script, setting up a project, or debugging across several files. This is your go-to for "just do it" tasks. |
| **How to activate** | Select **Agent** from the mode dropdown. Agent mode is the default in newer versions of VS Code. |

**Example prompts:**

```
Create a Python script that loads the Airbnb data, calculates summary statistics
per city, and saves the results to a CSV file.
```

```
The chart in cell 5 is throwing a KeyError. Debug it, fix the code, and re-run.
```

> **Tip:** Agent mode works best when you give it a clear goal. It will figure out the steps. If it goes off track, you can course-correct mid-conversation.

#### Plan Mode (via Agent Mode)

| | |
|---|---|
| **What it does** | Before executing, Copilot outlines a step-by-step plan of what it intends to do. You review and approve the plan before any changes are made. Think of it as Agent mode with a safety net. |
| **When to use it** | When the task is large or unfamiliar and you want to review the approach before Copilot starts editing. Useful for multi-file refactors, new features, or anything where you want to stay in control. |
| **How to activate** | In Agent mode, ask Copilot to plan first - e.g. "Plan how you would…". You can also hold `Cmd+Shift+Enter` (Mac) / `Ctrl+Shift+Enter` (Windows) when sending a message to request a plan before execution. |

**Example prompts:**

```
Plan how you would build a reusable analysis pipeline that processes each city
separately and produces a summary report with charts.
```

```
Before making changes, outline the steps to refactor the notebook into a clean
Python module.
```

### Inline Features (No Chat Panel Required)

These features work directly in the editor - no need to open the Chat panel.

#### Ghost Text (Inline Completions)

As you type - or after writing a comment - Copilot suggests code in grey "ghost text". This is the fastest way to write code with Copilot.

| Action | Shortcut |
|---|---|
| Accept suggestion | **Tab** |
| Reject suggestion | **Escape** |
| Next suggestion | **Alt+]** (Mac: **Option+]**) |
| Previous suggestion | **Alt+[** (Mac: **Option+[**) |
| Trigger suggestion manually | **Alt+\\** (Mac: **Option+\\**) |

> **Tip:** Write a descriptive comment first. The more specific the comment, the better the completion. For example, `# Calculate median price per city, excluding outliers above the 99th percentile` gives much better results than `# get prices`.

#### Inline Chat (`Cmd+I` / `Ctrl+I`)

Select code in the editor and press `Cmd+I` (Mac) / `Ctrl+I` (Windows) to open an inline prompt. Type your instruction and Copilot will edit the selected code in place, showing a diff you can accept or dismiss.

**Good for:** quick fixes, renaming, reformatting, adding error handling, or converting between styles - without leaving the editor.

#### Right-Click Context Menu

Select any code, right-click, and choose from the **Copilot** submenu:

| Option | What it does |
|---|---|
| **Copilot: Explain** | Provides a plain-English explanation of the selected code |
| **Copilot: Fix** | Suggests a fix if the selected code contains an error |
| **Copilot: Generate Docs** | Adds a docstring or comment block to the selected function |
| **Copilot: Generate Tests** | Creates test cases for the selected code |

### Quick Comparison - Which Mode Should I Use?

| Situation | Recommended Mode |
|---|---|
| "What does this code do?" | **Ask** |
| "Fix this one function" | **Edit** or **Inline Chat** (`Cmd+I`) |
| "Build me a script that does X" | **Agent** |
| "Plan a refactor, then do it" | **Agent** (with plan first) |
| "Write the next line of code" | **Ghost Text** (just keep typing) |
| "Explain this error" | **Ask** or right-click → **Copilot: Explain** |

---

## 📋 Quick Reference - VS Code Chat UI

| Action | How |
|---|---|
| Open Chat panel | `Cmd+Option+I` (Mac) / `Ctrl+Alt+I` (Windows) |
| Reference a file | Type `#` then the filename, or drag the file into chat |
| Switch to Agent mode | Click the dropdown at the top of Chat → **Agent** |
| Explain selected code | Select code → right-click → **Copilot: Explain** |
| Edit selected code | Select code → `Cmd+I` (Mac) / `Ctrl+I` (Windows) |
| Inline suggestion | Start typing or write a comment - Copilot autocompletes; **Tab** to accept, **Escape** to reject, **Alt+]** to cycle |

---

## 🙋 Getting Help

- **Something not working?** Check the troubleshooting section at the end of each chapter
- **Copilot subscription issues?** Visit [github.com/settings/copilot](https://github.com/settings/copilot)
- **Official docs:** [GitHub Copilot documentation](https://docs.github.com/copilot)
