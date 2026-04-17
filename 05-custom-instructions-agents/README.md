![Data Analysis with GitHub Copilot — Sky Workshop](../images/Picture%201.png)

# Chapter 05 — Custom Instructions & Agents 🤖

> **What if you could hire a specialist — a data analyst who already knows your tools, your data schema, and your team's standards — and have them available in every Copilot session?**

So far, Copilot has been answering your questions one at a time. In this chapter, you'll learn how to give Copilot persistent context: project-level instructions it reads automatically, skills it applies without being asked, and specialist agents tailored to your workflow.

By the end you'll understand exactly why Copilot knew to write DuckDB syntax in Chapter 04 without you asking — and how to set the same thing up for your own team's data and tools.

> ⚠️ **Prerequisites:** Complete Chapters 01–04.

## 🎯 Learning Objectives

By the end of this chapter you'll be able to:

- Understand the three layers of Copilot context: instructions, skills, agents
- Read and modify the project instruction files for this workshop
- Create your own skill that auto-triggers for a specific task
- Use the data-analyst agent included in this workshop
- Know when to use instructions vs skills vs agents

> ⏱️ **Estimated time:** ~50 minutes (20 min reading + 30 min hands-on)

---

## 🧩 Real-World Analogy: Briefing a New Colleague

Imagine briefing a new hire before their first day. You tell them:

- "We use DuckDB for all SQL queries, not PostgreSQL"
- "The main dataset is called `df` and has these columns..."
- "When you write functions, add a docstring in plain English"

After that briefing, they don't need reminding every time. They just work to your standards automatically.

That's exactly what instruction files, skills, and agents do for Copilot.

| Tool | Analogy | When It Applies |
|---|---|---|
| **Instructions** (`AGENTS.md`, `copilot-instructions.md`) | The onboarding document | Every session, automatically |
| **Skills** (`SKILL.md`) | A specialist checklist | When your prompt matches the skill's description |
| **Agents** (`.agent.md`) | A named specialist colleague | When you explicitly call them |

---

## Layer 1 — Project Instructions

### What are they?

Instruction files are plain markdown documents that Copilot reads automatically whenever you open the project. They're committed to the repository, so every team member gets the same Copilot behaviour.

This workshop includes two:

| File | Scope | Purpose |
|---|---|---|
| `AGENTS.md` (project root) | Cross-platform standard | Works with Copilot and other AI tools |
| `.github/copilot-instructions.md` | GitHub Copilot specific | More detailed, project-specific rules |

### Read the workshop instructions

**💬 VS Code Chat UI:**

> *"#AGENTS.md — read this file and summarise in 3 bullets what Copilot should know about this project."*

**🖥️ Copilot CLI:**
```bash
copilot
> @AGENTS.md Read this and summarise what Copilot should know about this project in 3 bullets.
```

### Why DuckDB worked in Chapter 04

Look at `AGENTS.md` — the SQL section says:

```markdown
## SQL — always use DuckDB
- Always write SQL using DuckDB syntax
- DataFrames are queried directly by variable name
- Always chain `.df()` at the end
```

That's why every SQL query Copilot suggested used `duckdb.query(...).df()` — without you asking. The instruction file sets the default.

### Exercise: See the before/after

To see what Copilot does *without* instructions, open a new VS Code window, open a blank folder (no `AGENTS.md`), and ask:

> 💬 *"Write a SQL query to count listings per city in a pandas DataFrame called df."*

You'll probably get generic SQL or pandas code. Back in the workshop folder, the same prompt produces DuckDB. Same model, different project context.

### Generate instructions with `/init`

If you're setting up a new project, the Copilot CLI can generate instruction files automatically:

```bash
# In your project folder:
copilot
> /init
```

Copilot scans your codebase and generates a starter `AGENTS.md`. You then edit it to add your team's specifics.

---

## Layer 2 — Skills

### What are they?

Skills are task-specific instructions stored in a `SKILL.md` file. Copilot loads them **automatically** when your prompt matches the skill's description. No slash command, no `/agent` — just ask naturally.

This workshop includes a DuckDB skill at `.github/skills/duckdb-query/SKILL.md`.

### Read the DuckDB skill

**💬 VS Code Chat UI:**

> *"#.github/skills/duckdb-query/SKILL.md — read this skill file and explain what it does and when Copilot will automatically use it."*

### Skill vs instruction file: what's the difference?

| Instruction file | Skill |
|---|---|
| Always active | Active only when prompt matches |
| General project context | Specific task instructions |
| "Always use DuckDB" | "When writing a DuckDB query, follow these exact steps and format" |
| Like team rules | Like a specialist checklist |

### Create your own skill

Skills live in `.github/skills/<skill-name>/SKILL.md`. Here's the format:

```markdown
---
name: your-skill-name
description: What the skill does — include trigger words that match how you'd naturally ask for it
---

# Skill title

Instructions for how Copilot should behave when this skill is active.
```

**Exercise: Create a data-summary skill**

**💬 VS Code Chat UI — Agent mode:**

> *"Create a new skill file at .github/skills/data-summary/SKILL.md. The skill should trigger when I ask for a summary of the dataset or analysis findings. It should instruct Copilot to: always write summaries in bullet points, always include the city name when referring to a city, always round numbers to one decimal place, and write as if for a senior finance manager."*

Accept the file Agent mode creates. Then test it:

> 💬 *"Give me a summary of what we've found about the Airbnb dataset so far."*

**🖥️ CLI approach:**
```bash
mkdir -p .github/skills/data-summary

cat > .github/skills/data-summary/SKILL.md << 'EOF'
---
name: data-summary
description: Use when summarising dataset findings, writing analysis summaries, or producing reports for non-technical stakeholders
---

# Data Summary Writer

When writing summaries of analysis findings:

- Use bullet points, not paragraphs
- Always name the city when referring to a city-level finding
- Round all numbers to one decimal place
- Write for a senior finance manager — no jargon, just clear insight
- End with one "so what?" — what should the reader do with this information?
EOF

copilot
> /skills reload
> Give me a summary of what we know about the Airbnb dataset
```

### Manage skills

**🖥️ CLI:**
```bash
copilot
> /skills list          # See all available skills
> /skills info duckdb-query   # Details about a specific skill
> /skills reload        # Reload after editing a SKILL.md
```

**💬 VS Code Chat UI:**
Skills load automatically — there's no manual management in the UI. To see what skills are loaded, ask:

> 💬 *"What skills do you have available? List them."*

---

## Layer 3 — Agents

### What are they?

Agents are named specialists you call on explicitly. Unlike skills (which auto-trigger), you invoke an agent deliberately. The agent brings a specific persona, expertise, and set of standards.

This workshop includes a **data-analyst agent** at `.github/agents/data-analyst.agent.md`.

### The specialist vs generic difference

This is the same pattern as the original Copilot CLI course — worth seeing firsthand.

**Without the agent:**

> 💬 *"Write a function that takes a city name and returns a summary of the Airbnb listings for that city."*

You'll get a working function — probably with no type hints, no docstring, and aimed at a developer audience.

**With the data-analyst agent:**

**💬 VS Code Chat UI:**

Switch the dropdown at the top of Chat from **Ask** → **Agent**, then select **data-analyst** from the agent list.

> *"Write a function that takes a city name and returns a summary of the Airbnb listings for that city."*

**What's different:** The function now includes type hints, a docstring written in plain English for a non-developer, and the output is formatted as a clean dictionary rather than raw values. The agent applies those standards automatically.

**🖥️ CLI:**
```bash
copilot --agent data-analyst
> Write a function that takes a city name and returns a summary of the Airbnb listings for that city.
```

### Read the data-analyst agent

**💬 VS Code Chat UI:**

> *"#.github/agents/data-analyst.agent.md — read this agent file. What are the three most important things it instructs Copilot to do?"*

### Create your own agent

```markdown
---
name: your-agent-name
description: What this agent is for — used to find the agent in the list
tools: ["read", "edit", "search"]
---

# Agent Name

You are a [role] specialising in [domain].

## Your approach
[How the agent should behave]

## Standards
[Specific rules to follow]
```

**Exercise: Create a "report-writer" agent**

**💬 VS Code Chat UI — Agent mode:**

> *"Create an agent file at .github/agents/report-writer.agent.md. This agent is a business report writer who specialises in translating data analysis into clear, concise management reports. It should: write in plain English, use bullet points for key findings, include a 'so what?' recommendation, avoid technical jargon, and structure every response with: Summary, Key Findings, and Recommendation sections."*

Then switch to the report-writer agent and try:

> *"Based on our Airbnb analysis, write a short report on pricing differences between cities. Keep it to half a page."*

---

## How They Work Together

Skills and agents combine naturally:

| Scenario | What to use |
|---|---|
| Every SQL query should use DuckDB | Instruction file (`AGENTS.md`) |
| When writing a SQL query, follow these exact formatting steps | Skill (`duckdb-query`) |
| I want a specialist who always gives business-ready output | Agent (`data-analyst`) |
| I want a specialist who also always follows the SQL skill | Agent + skill together — they stack |

```bash
# CLI: agent + skill work together automatically
copilot --agent data-analyst
> Write a SQL query to find the top 5 cities by average listing price
# data-analyst agent applies its tone standards
# duckdb-query skill applies DuckDB syntax rules
# Both active at the same time
```

---

## ▶️ Your Turn

### Exercise 1 — Compare with and without instructions

1. Ask in this project: *"Write a function to calculate the median price per room type."*
2. Note what Copilot produces — type hints, docstring, which library it uses
3. Open a blank VS Code folder with no `AGENTS.md` and ask the same question
4. Compare the two outputs

### Exercise 2 — Write a skill for your team

Think about a task your team does repeatedly — a report format, a data quality check, a standard output structure. Write a `SKILL.md` for it.

Minimum requirements:
- A `name` and `description` that include natural trigger words
- At least 5 specific instructions
- A clear output format section

Test it with a natural prompt — don't use the skill name, just describe what you want.

### Exercise 3 — Use the data-analyst agent end-to-end

Switch to the data-analyst agent, then complete this workflow in a single conversation:

1. Ask it to write a DuckDB query for top neighbourhoods by reviews
2. Ask it to explain the output in plain English
3. Ask it to write a 3-bullet summary suitable for a management slide

Notice how the agent maintains a consistent tone across all three steps.

---

## 📝 Assignment

Build a mini instruction setup for a hypothetical analytics project at your own team:

1. Write an `AGENTS.md` for a project you work on (or could work on). Include: project context, the database/SQL dialect you use, key table/column names, output style preferences.
2. Create one skill file for a task you repeat regularly.
3. Test both by asking Copilot the same question with and without the files.
4. Write two sentences explaining what you'd change in the current workshop's `AGENTS.md` to better reflect your team's workflow.

---

<details>
<summary>🔧 Troubleshooting</summary>

**"Copilot isn't following the instructions"**
Instruction files are loaded at session start. Close and re-open VS Code (or restart the CLI) after adding a new file.

**"My skill isn't auto-triggering"**
The `description` field is the trigger mechanism — it needs to include words that match how you naturally ask. Add more synonyms: "SQL queries, data aggregation, GROUP BY, summarising data" is better than just "SQL".

**"Agent not showing in the dropdown"**
Agent files must have `.agent.md` extension and be in `.github/agents/`. The `description` field in frontmatter is required.

**"CLI: agent not found"**
```bash
copilot
> /agent   # Lists all available agents
```
Check the file is in `.github/agents/` with `.agent.md` extension.

</details>

---

## 🔑 Key Takeaways

1. **Instructions = always-on context** — `AGENTS.md` and `copilot-instructions.md` are read every session. Use them for project-wide rules.
2. **Skills = auto-triggered checklists** — `SKILL.md` files load when your prompt matches. The description field is what triggers them.
3. **Agents = named specialists** — `.agent.md` files give Copilot a specific persona and standards for a domain.
4. **They stack** — instructions + skill + agent all apply together. Each layer adds specificity.
5. **Share via git** — commit these files and the whole team gets the same Copilot behaviour.

---

## ➡️ What's Next

In **[Chapter 06: Putting It All Together](../06-putting-it-together/README.md)** you'll:

- Build a complete analysis pipeline using everything from this workshop
- Use Agent mode to scaffold a reusable Python script
- Create a skills-first workflow your team could actually adopt

---

**[← Back to Chapter 04](../04-sql-with-duckdb/README.md)** | **[Continue to Chapter 06 →](../06-putting-it-together/README.md)**
