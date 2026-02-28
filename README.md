<p align="center">
  <h1>🚀 Casely — QA Test Case Generator</h1>
</p>

<p align="center">
  <img src="/assets/logo.png" alt="Casely Banner" width="200">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/QA-Automation-green.svg" alt="QA">
</p>

---

### **From messy PDF requirements → 47 TestRail-ready Excel files in 8 minutes. No manual writing.**

Casely is an intelligent QA assistant that automates the entire test case lifecycle—from parsing chaotic documentation to generating perfectly formatted test cases that match **your** specific team style.

---

## 🎯 The Problem (40 hours → 8 minutes)

Manual QA engineers often spend up to **40% of their time** performing repetitive writing tasks:

* ❌ **Fragmented Docs:** Requirements scattered across 10+ PDF/DOCX files.  
* ❌ **Inconsistency:** Every team/project uses different Excel columns.  
* ❌ **Time Sink:** Writing 50 test cases manually takes 2–3 business days.  
* ❌ **Import Errors:** TestRail/Qase imports fail due to column mismatches.  
* ❌ **Blind Spots:** Lack of a structured test plan leads to missed edge cases.

**The Result:** QA becomes a bottleneck, releases are delayed, and bugs leak into production.

---

## ✅ The Casely Solution

Casely acts as your **Virtual QA Lead**, transforming raw requirements into structured test suites using a smart pipeline:

1. **`/parse`** ➔ Converts PDF/DOCX/XLSX into clean Markdown using **Docling**.  
2. **`/style`** ➔ Analyzes your existing files to extract **YOUR** specific column structure.  
3. **`/plan`** ➔ Generates a high-level test plan (e.g., "47 tests across 6 modules").  
4. **`/generate`** ➔ Creates atomic `.md` test cases based on the plan.  
5. **`/export`** ➔ Converts everything into **TestRail-ready** Excel files.

---

## 🎬 8-Minute Demo Workflow

Transform chaotic documentation into a structured test suite in four simple stages.

### 🛠️ Step 1: Initialize & Feed

Set up your workspace and provide the "DNA" of your project.

* **Command:** `/init my-project`  
* **Action:** Drop your `requirements.pdf` and an `example.xlsx` into the `/input` folder.

---

### 🧠 Step 2: Intelligence Engine

* **`/parse`** — **High-Fidelity Parsing:** Uses Docling to extract text and tables from PDFs.  
* **`/style`** — **Style Extraction:** Clones your unique Excel naming conventions and columns.  
* **`/plan`** — **Strategic Mapping:** "Detected 6 modules. Recommended: 47 test cases."

---

### ⚡ Step 3: Production Line

* **Command:** `/generate functional AccountTransfer`  
* **Result:** Casely creates 10+ atomic `.md` files.  
* **Why Markdown?** Easy to review, edit, and version control before export.

---

### 📦 Step 4: Final Delivery

* **Command:** `/export`  
* **Output:** Batch-converts all Markdown files into **TestRail-ready Excel files**.

> [!TIP]  
> **The Payoff:** Open `exports/functional_TC001_happy_path.xlsx`. It’s a 1:1 match to your team's template, ready for immediate import.

---

## 🌟 Why Teams Love Casely

| Feature | **Casely** | Manual Writing | Traditional Tools |
| :--- | :---: | :---: | :---: |
| **Parse ANY format** | ✅ **Yes** | ❌ | ❌ |
| **Matches YOUR style** | ✅ **1:1 Mapping** | ❌ | ❌ |
| **Smart test plan** | ✅ **AI-Driven** | ❌ | ❌ |
| **Atomic export** | ✅ **1 Test = 1 File** | ❌ | ⚠️ Bulk only |
| **TestRail Ready** | ✅ **Out of the box** | ❌ | ⚠️ Manual fix |

---

## ⚡ Quick Start

> **Prerequisites:** Python 3.10+ and [uv](https://github.com/astral-sh/uv) (for 10x faster setup).

### Add the skill (Skills CLI)

| CLI | Command |
| --- | --- |
| **bunx** | `bunx skills add JohnWayneeee/casely-qa-skill` |
| **npx** | `npx skills@latest add JohnWayneeee/casely-qa-skill` |
| **npm** | `npm install -g skills-cli` then `skills add JohnWayneeee/casely-qa-skill` |

### Run from source (clone + scripts)

Dependencies and environment are defined in the **repository root** `pyproject.toml`. Run setup once from the repo root so the skill's scripts (`/parse`, `/export`) have access to `docling` and `openpyxl`.

```bash
# 1. Clone & Enter
git clone https://github.com/JohnWayneeee/casely-qa-skill.git
cd casely-qa-skill

# 2. Install dependencies (from repo root — required for scripts to work)
uv sync

# 3. Use in your AI IDE / Skills environment
# Commands: /init → /parse → /style → /plan → /generate → /export
```

---

## 📋 Full Command Reference

| Command | Action | Deep Dive |
| --- | --- | --- |
| `/init` | **Setup** | Scaffolds project structure and local dependencies. |
| `/parse` | **Extract** | High-fidelity OCR parsing for PDF/DOCX tables. |
| `/style` | **Adapt** | Clones your team's unique Excel column structure. |
| `/plan` | **Map** | Generates an ISTQB-aligned coverage strategy. |
| `/generate` | **Build** | Writes atomic `.md` cases (Functional/Negative/Edge). |
| `/export` | **Convert** | Batch-delivers final, import-ready Excel files. |

---

## 🔧 Under the Hood

* **Docling Engine:** Advanced OCR and table extraction for complex PDFs.  
* **Atomic Design:** Each test case is a single source of truth (1 MD = 1 Excel).  
* **Style Guide System:** No more hardcoded columns; Casely learns from you.  
* **Language Agnostic:** Seamlessly works with **English** and **Russian** requirements.

---

## 🎉 Get Started Now

**🐛 Issues:** [Report a bug](https://github.com/JohnWayneeee/casely-qa-skill/issues)

**⭐ Support:** Star this repo if Casely saved you a work week!

---

<p align="center">
<i>Made with ❤️ for QA engineers who hate repetitive tasks. <b>Casely — Your Test Case Factory.</b></i>
</p>
