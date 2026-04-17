![Data Analysis with GitHub Copilot — Sky Workshop](./images/Picture%201.png)

# 📊 Data Analysis with GitHub Copilot — Sky Workshop

> **Learn how GitHub Copilot can help you do more advanced analytical work without needing deep software engineering skills.**

This hands-on workshop is designed for **finance and analytics teams** who work with data every day. You'll work with a real dataset throughout all chapters, using Copilot to explore, clean, analyse, and explain data — all from VS Code.

---

## 🎯 What You'll Learn

| Chapter | Theme | What You'll Do |
|:-------:|-------|----------------|
| 00 | 🚀 [Quick Start](./00-quick-start/README.md) | Set up VS Code, install Copilot, open the workshop |
| 01 | 🔍 [Understanding Your Data](./01-understanding-data/README.md) | Load a dataset and explore it with Copilot's help |
| 02 | 🧹 [Cleaning & Preparing](./02-cleaning-preparing/README.md) | Spot and fix data quality issues faster |
| 03 | 📊 [Explore & Visualise](./03-explore-visualise/README.md) | Generate charts from plain-English descriptions |
| 04 | 🗄️ [SQL with DuckDB](./04-sql-with-duckdb/README.md) | Run SQL directly on your data — no database needed |
| 05 | 🤖 [Custom Instructions & Agents](./05-custom-instructions-agents/README.md) | Teach Copilot your tools, data, and team standards |
| 06 | 🎯 [Putting It All Together](./06-putting-it-together/README.md) | Build a reusable analysis pipeline end-to-end |

---

## 📖 How This Workshop Works

Each chapter follows the same pattern:

1. **Real-World Analogy** — understand the concept through a familiar comparison
2. **Core Concepts** — the essential knowledge, kept brief
3. **Hands-On Demos** — prompts to try immediately, with expected outputs
4. **Your Turn** — a challenge to try yourself
5. **What's Next** — preview of the next chapter

**All prompts are ready to copy.** Every Copilot prompt in this workshop can be pasted directly into the Chat panel.

---

## 🤖 Two Ways to Use Copilot

Every exercise in this workshop can be done in two ways. You'll see both options throughout:

| | VS Code Chat UI | Copilot CLI |
|---|---|---|
| **How to open** | `Cmd+Option+I` / `Ctrl+Alt+I` | `copilot` in terminal |
| **Best for** | Most participants — visual, approachable | Power users comfortable with the terminal |
| **References files with** | `#file` or drag-and-drop | `@path/to/file` |
| **Planning** | Agent mode → describe the task | `/plan` command |
| **Great for** | Chat, explain, generate, edit | Automation, batch tasks, scripting |

> 💡 **Not sure which to use?** Start with the VS Code Chat UI. It's more visual, easier to navigate, and works the same way. The CLI gives you more power once you're comfortable.

---

## 🗂️ The Dataset

Throughout this workshop we use real **Airbnb listings data** from [Inside Airbnb](http://insideairbnb.com/) — 2,000 listings per city across New York, London, Paris, Amsterdam, and Barcelona.

This is the kind of tabular data you'd recognise from your own work: rows and columns, missing values, price outliers, categorical fields like room type and neighbourhood. The analysis tasks — summarising, cleaning, segmenting, visualising — map directly to things analytics and finance teams do every day.

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

> 💡 **No terminal experience needed.** All core exercises use the VS Code Chat panel. The Copilot CLI is covered as an optional extension for those who want it.

---

## 🤖 Understanding the GitHub Copilot Family

GitHub Copilot has grown into a family of tools. Here's where each one lives — and which ones we use in this workshop:

| Product | Where It Runs | Used in This Workshop? |
|---|---|---|
| **GitHub Copilot in VS Code** | VS Code sidebar & inline | ✅ Primary tool |
| **GitHub Copilot CLI** | Terminal | ✅ Optional extension |
| **Copilot on GitHub.com** | github.com | Referenced |
| **GitHub Copilot cloud agent** | GitHub issues/PRs | Referenced |

---

## 📋 Quick Reference

### VS Code Chat UI

| Action | How |
|---|---|
| Open Chat panel | `Cmd+Option+I` (Mac) / `Ctrl+Alt+I` (Windows) |
| Reference a file | Type `#` then the filename, or drag the file into chat |
| Switch to Agent mode | Click the dropdown at the top of Chat → **Agent** |
| Explain selected code | Select code → right-click → **Copilot: Explain** |
| Inline suggestion | Start typing — Copilot autocompletes |

### Copilot CLI (optional)

| Action | Command |
|---|---|
| Start interactive session | `copilot` |
| One-shot question | `copilot -p "your question"` |
| Plan a task | `/plan describe the task` |
| List skills | `/skills list` |
| List agents | `/agent` |
| Exit | `/exit` |

---

## 🙋 Getting Help

- **Something not working?** Check the troubleshooting section at the end of each chapter
- **Copilot subscription issues?** Visit [github.com/settings/copilot](https://github.com/settings/copilot)
- **Official docs:** [GitHub Copilot documentation](https://docs.github.com/copilot)
