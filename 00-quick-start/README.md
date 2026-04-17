![Data Analysis with GitHub Copilot — Sky Workshop](../images/Picture%201.png)

# Chapter 00 — Quick Start 🚀

Welcome! This chapter gets you set up and ready to go. By the end you'll have VS Code open, Copilot connected, and the workshop notebook running. The real demos start in Chapter 01.

## 🎯 Learning Objectives

By the end of this chapter you'll have:

- VS Code installed with the GitHub Copilot and Jupyter extensions
- Signed in to GitHub Copilot
- The workshop notebook open and running
- Verified that Copilot Chat is working

> ⏱️ **Estimated time:** ~15 minutes

---

## Step 1 — Install VS Code

If you don't have VS Code already, download it from [code.visualstudio.com](https://code.visualstudio.com/) and follow the installer.

---

## Step 2 — Install the Required Extensions

Open VS Code, click the **Extensions** icon in the left sidebar (or press `Cmd+Shift+X` / `Ctrl+Shift+X`), and install these three:

| Extension | What it does |
|---|---|
| **GitHub Copilot** | The core Copilot extension — chat, inline suggestions, agent mode |
| **GitHub Copilot Chat** | Usually bundled with the above — enables the Chat panel |
| **Jupyter** | Lets you open and run `.ipynb` notebook files |

> 💡 Search for "GitHub Copilot" in the Extensions panel — both extensions will appear together.

---

## Step 3 — Sign In to GitHub

After installing, VS Code will prompt you to sign in. Click **Sign in to GitHub** and follow the browser flow:

1. A browser window opens at GitHub
2. Authorise VS Code to access your account
3. Return to VS Code — you're signed in

**Verify your Copilot access**: At [github.com/settings/copilot](https://github.com/settings/copilot) you should see one of:

- **Copilot Individual** — personal subscription
- **Copilot Business** — through your organisation
- **Copilot Enterprise** — through your enterprise

If you see "You don't have access to GitHub Copilot", speak to your workshop organiser.

---

## Step 4 — Open the Workshop

Clone or download this repository, then open it in VS Code:

```bash
# If you have git installed:
git clone <workshop-repo-url>
cd sky-copilot-workshop
code .
```

Or use **File → Open Folder** in VS Code and navigate to the `sky-copilot-workshop` folder.

---

## Step 5 — Open the Workshop Notebook

In the VS Code file explorer (left sidebar), open:

```
samples/air-bnb-workshop.ipynb
```

VS Code will open the Jupyter notebook. You may be prompted to select a Python kernel — choose your Python 3.10+ installation.

> 💡 **First time with Jupyter in VS Code?** The notebook is made up of cells. Click a code cell, then press `Shift+Enter` to run it. The output appears directly below.

Run the first two cells (install packages and import libraries) to confirm everything is working.

---

## Step 6 — Verify Copilot Chat Works

Open the Copilot Chat panel:

- **Mac:** `Cmd+Option+I`
- **Windows/Linux:** `Ctrl+Alt+I`

The Chat panel opens on the right side of VS Code. Try this prompt:

> 💬 *"I'm going to be analysing Airbnb listing data in a Jupyter notebook. What kinds of questions can you help me answer about this data?"*

**Expected response:** Copilot lists the kinds of analysis it can help with — price analysis, neighbourhood comparisons, availability patterns, visualisations, SQL queries, and so on.

If you see a response, you're ready. Move on to Chapter 01!

---

## ✅ You're Ready!

That's the setup complete. In Chapter 01 you'll load the dataset and start exploring it — with Copilot's help at every step.

**[Continue to Chapter 01: Understanding Your Data →](../01-understanding-data/README.md)**

---

## Optional — Install the Copilot CLI

The Copilot CLI brings AI assistance to your terminal. It's entirely optional for this workshop, but useful if you're comfortable with the command line.

### Install

```bash
# macOS/Linux with Homebrew:
brew install copilot-cli

# All platforms with npm (requires Node.js):
npm install -g @github/copilot

# macOS/Linux with install script:
curl -fsSL https://gh.io/copilot-install | bash

# Windows with WinGet:
winget install GitHub.Copilot
```

### Sign in

```bash
copilot
> /login
```

Follow the device code flow (same as VS Code — browser opens, enter the code, authorise).

### Verify

```bash
copilot
> Say hello and tell me what you can help with
> /exit
```

---

## Troubleshooting

### "GitHub Copilot extension not activating"

1. Make sure you're signed in: click the account icon at the bottom-left of VS Code
2. Check your subscription at [github.com/settings/copilot](https://github.com/settings/copilot)
3. Reload VS Code: `Cmd+Shift+P` → "Developer: Reload Window"

### "No kernel found" in the notebook

1. Make sure Python 3.10+ is installed: run `python3 --version` in the terminal
2. In VS Code, press `Cmd+Shift+P` → "Python: Select Interpreter" and pick your Python install
3. Run the first cell — it installs all required packages automatically

### "Copilot Chat panel not appearing"

Press `Cmd+Option+I` (Mac) or `Ctrl+Alt+I` (Windows). If it still doesn't appear, make sure the **GitHub Copilot Chat** extension is installed and enabled.

---

## 🔑 Key Takeaways

1. **Two interfaces, same AI** — VS Code Chat UI and the Copilot CLI both talk to the same model. Use whichever feels most natural.
2. **One-time sign-in** — your login persists across sessions
3. **The notebook is the sample project** — `samples/air-bnb-workshop.ipynb` is what you'll work with throughout the entire workshop

---

**[Continue to Chapter 01: Understanding Your Data →](../01-understanding-data/README.md)**
