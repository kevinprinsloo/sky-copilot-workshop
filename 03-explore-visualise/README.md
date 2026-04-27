![Data Analysis with GitHub Copilot - Sky Workshop](../images/Picture%201.png)

# Chapter 03 - Explore & Visualise 📊

> **Describe the chart you want in plain English. Copilot writes the code.**

For analysts who aren't Python experts, charting code is often the biggest barrier. Syntax for colours, axes, legends, layouts - it takes experience to remember all of it. Copilot removes that barrier entirely. You describe what you want to see; it writes the code.

> ⚠️ **Prerequisites:** Complete [Chapter 02](../02-cleaning-preparing/README.md).

## 🎯 Learning Objectives

By the end of this chapter you'll be able to:

- Generate charts from plain-English descriptions
- Iterate on a chart by asking Copilot to improve it
- Create interactive Plotly charts without knowing Plotly syntax
- Ask Copilot to interpret a chart output in plain language

> ⏱️ **Estimated time:** ~40 minutes (10 min reading + 30 min hands-on)

---

## 🧩 Real-World Analogy: Briefing a Designer

When you brief a designer, you describe the output you want - not the tool settings to produce it. "I want a bar chart showing revenue by region, sorted largest to smallest, with the company colours" - the designer handles the rest.

That's exactly how this works. You describe the chart; Copilot handles the `figsize`, `palette`, `tight_layout`, and axis formatting.

---

## See It In Action

### Demo 1: Generate a chart from a description

In a new notebook cell, open Chat and paste:

**💬 VS Code Chat UI:**

> *"Create a horizontal bar chart showing the top 10 most common neighbourhoods across all cities combined. Colour the bars by count (darkest = highest count). Add a title and axis labels. Use seaborn."*

Run the generated code. Then ask Copilot to improve it:

> *"Make the labels on the y-axis easier to read - increase font size and truncate any neighbourhood names longer than 25 characters."*

**The takeaway:** You iterate in plain English. No Stack Overflow, no documentation hunting.

---

### Demo 2: Side-by-side comparison

**💬 VS Code Chat UI:**

> *"Create a figure with two side-by-side box plots. Left: price distribution by city (using price_capped, only rows where has_price is True). Right: number_of_reviews distribution by city. Use a muted colour palette and add a title to each subplot."*

---

### Demo 3: Interactive chart

**💬 VS Code Chat UI:**

> *"Create an interactive Plotly bar chart showing the percentage of each room_type per city. Stack the bars to 100%. Add a hover tooltip showing the exact count and percentage. Use the plotly_white template."*

---

### Demo 4: Explain a chart

After running a chart cell, ask:

**💬 VS Code Chat UI:**

> *"I've just generated a violin plot showing price distribution by city. The London distribution has a very long upper tail and a wide body, while Amsterdam's is narrower and more concentrated. What does this tell us about these two markets from a business perspective?"*

**The takeaway:** This is the "so what?" layer - translating a visual into insight. It's exactly the kind of commentary that goes in a management report.

---

## ▶️ Your Turn

### Exercise 1 - Availability patterns

> 💬 *"Create a KDE (kernel density) plot showing the distribution of availability_365 for each city on the same axes. Add a legend, title, and label the x-axis as 'Days available per year'. Which city appears to have the most restricted supply?"*

### Exercise 2 - Improve a chart

Take one of the charts from the notebook that already exists. Paste the code into Chat and ask:

> 💬 *"Improve this chart for a management presentation: make the font sizes larger, remove the top and right spines, add gridlines on the x-axis only, and make the title bold."*

### Exercise 3 - Correlation heatmap

> 💬 *"Create a correlation heatmap for the numeric columns in our dataset: price, number_of_reviews, reviews_per_month, availability_365, calculated_host_listings_count. Only show the lower triangle. Use a red-blue diverging colour scheme centred at zero."*

Then ask:

> 💬 *"Looking at this correlation matrix, explain in plain English what the strongest relationships are and what they might mean for understanding Airbnb pricing."*

---

## 📝 Assignment

Choose a question you'd genuinely want a chart to answer about this dataset - something a business stakeholder might ask. Then:

1. Write a Copilot prompt that describes the chart
2. Run it and review it
3. Ask Copilot to make at least two improvements based on your own judgement
4. Ask Copilot to write a two-sentence caption for the chart, suitable for a slide deck

**Success criteria:** A chart you'd be comfortable putting in a presentation, produced entirely through Copilot prompts.

---

## 🔑 Key Takeaways

1. **Describe, don't code** - tell Copilot what you want to see, not how to draw it
2. **Iterate** - ask for improvements in plain English. "Make the labels bigger", "use a different colour", "add gridlines"
3. **Ask for the interpretation** - the chart is the output; the insight is the point. Ask Copilot "what does this tell us?"
4. **Interactive charts are one prompt away** - Plotly interactivity from a single description

---

**[← Back to Chapter 02](../02-cleaning-preparing/README.md)** | **[Continue to Chapter 04 →](../04-sql-with-duckdb/README.md)**
