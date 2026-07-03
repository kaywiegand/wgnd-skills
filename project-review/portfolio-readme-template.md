# README Template — Portfolio Projects
<!-- 
VERWENDUNG:
  Dieses Template als README.md ins Projekt-Root kopieren und Platzhalter befüllen.
  Kommentare (<!-- ... -->) vor dem Veröffentlichen entfernen.
  Projekttyp wählen: DS (DE+DA+ML) · DA (DE+DA) · DEV (Tool/Package) · SKL (Skill/Command)

DREI LESEEBENEN (aus communication-concept.md, ../project-case/):
  Scan   (30 Sek) → Title + Key Visual + TL;DR            ← HR Recruiter
  Dive   (5–10 Min) → Problem + Dataset + Results + Setup  ← Hiring Manager / Data Scientist
  Deep Dive (30+ Min) → Notebooks + Code + Structure       ← Tech Lead
-->

---

# [Project Title] <!-- kurz, topic-beschreibend, keine Buzzwords -->

<!-- SCAN-EBENE START — das sieht jeder, der auf GitHub landet -->

**[One-sentence pitch: Was wurde analysiert/gebaut, was ist die Kernaussage, was ist der Scope?]**  
*Example: Analysis of 2.1M tram trips in Zürich (2020–2023) to quantify delay patterns by weather, events and infrastructure.*

<!-- Badge-Zeile — optional aber empfohlen. Badges von shields.io -->
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Polars](https://img.shields.io/badge/Polars-latest-orange)
<!-- weitere Badges: Status, License, Last Commit -->

---

## Key Visual

<!-- Das stärkste Chart des Projekts — direkt eingebettet. Kein Fließtext davor.
     Pfad relativ zum README. Muss eine tatsächlich existierende public/img/*.png sein. -->

![Key Visual](public/img/[key_visual_filename].png)
*[Kurze Bildunterschrift: Was zeigt der Chart? Welche Aussage steckt drin?]*

---

## TL;DR

<!-- Mind. 3 konkrete Findings MIT Zahlen. Keine generischen Aussagen.
     Diese Bullets sind das Wichtigste für HR-Recruiter (Scan-Ebene). -->

- **[Finding 1 mit Zahl]** — *Example: Rain increases average delay by 47% (2.3 → 3.4 min)*
- **[Finding 2 mit Zahl]** — *Example: Line 8 is responsible for 31% of all severe delays (>5 min)*
- **[Finding 3 mit Zahl]** — *Example: XGBoost predicts delay class with 78% F1 (vs. 61% baseline)*
<!-- Für DA: 3–5 Findings. Für DS: 2 Analysis-Findings + 1 ML-Finding minimum. -->

---
<!-- SCAN-EBENE ENDE -->

<!-- DIVE-EBENE START -->

## Problem Statement

<!-- 3–5 Sätze. Struktur: Was ist das Problem? Warum ist es relevant? Was war die Leitfrage?
     Kein generisches "This project analyzes data to gain insights." -->

[What is the operational/business problem?]  
[Why does it matter — who is affected, what is the scale?]  
[What is the core analytical question this project answers?]

## Dataset

<!-- Quelle + Größe + Zeitraum + bekannte Qualitätsprobleme. Keine Schönfärberei. -->

| Property | Value |
| :--- | :--- |
| Source | [Name, URL or institution] |
| Size | [Rows × Columns, e.g. 2.1M rows × 12 columns] |
| Time Period | [e.g. Jan 2020 – Dec 2023] |
| Granularity | [e.g. per trip, per day, per sensor reading] |
| License | [e.g. Open Government Data, CC BY 4.0] |
| Known Issues | [e.g. 3.2% missing values in delay column for 2021-Q3] |

## Approach

<!-- Kurze Beschreibung des methodischen Vorgehens. NACH PROJEKTTYP ANPASSEN (s. unten). -->

<!-- ── DS (DE + DA + ML / full cycle) ─────────────────────────────────────── -->
<!-- Uncomment when project type = DS

### Data Engineering
- Extracted [X sources] via [API / scraping / download]
- Cleaning: [key steps, e.g. deduplication, outlier handling]
- Master dataset: [final row count × column count] in `data/processed/`

### Data Analysis
- Analysed [N dimensions]: [list, e.g. temporal patterns, geo distribution, weather correlation, event impact]
- Key method: [e.g. seasonal decomposition, correlation analysis, clustering]

### Data Science / ML
- Target: [what is being predicted? classification or regression?]
- Baseline: [naive model + metric, e.g. ZeroR MAE = 1.87 min]
- Models tested: [e.g. Linear Regression, Random Forest, XGBoost]
- Best model: [name, metric, e.g. XGBoost — MAE 0.91 min, R² 0.74]
-->

<!-- ── DA (DE + DA, kein ML) ────────────────────────────────────────────────── -->
<!-- Uncomment when project type = DA

### Data Engineering
- Extracted [X sources] via [method]
- Cleaning: [key steps]
- Master dataset: [final shape]

### Data Analysis
- Analysed [N dimensions]: [list]
- Key methods: [e.g. time series aggregation, spatial analysis, statistical tests]
-->

<!-- ── DEV (Tool / Package) ───────────────────────────────────────────────────── -->
<!-- Uncomment when project type = DEV

### Architecture
- Package structure: [e.g. analytics/ · visualization/ · config]
- Key design decisions: [e.g. why Polars over Pandas, why dataclass config]

### Implementation
- Core modules: [list with 1-line description each]
- Dependencies: [key external libs]

### Usage Example
```python
from [package] import [module]
# one-liner showing the key use case
```
-->

<!-- ── SKL (Skill / Command) ───────────────────────────────────────────────── -->
<!-- Uncomment when project type = SKL

### Design
- Trigger condition: [what user intent / keywords activate this skill]
- Modes / variants: [if applicable]

### Implementation
- Command file: `~/.claude/commands/[skill-name].md`
- Dependencies: [other skills, MCP tools, or commands it calls]

### Example
```
/[skill-name] [args]
```
[Description of what happens when invoked]
-->

## Results

<!-- ── Für DA/DS: Findings-Tabelle ──────────────────────────────────────── -->
<!-- 
| Dimension | Key Finding | Evidence |
| :--- | :--- | :--- |
| [e.g. Temporal] | [Finding with number] | [chart / notebook reference] |
| [e.g. Weather] | [Finding with number] | [chart / notebook reference] |
| [e.g. Events] | [Finding with number] | [chart / notebook reference] |
-->

<!-- ── Für DS: Modell-Tabelle + dann Findings ────────────────────────────── -->
<!--
### Model Comparison

| Model | MAE | RMSE | R² | Notes |
| :--- | :---: | :---: | :---: | :--- |
| Baseline (ZeroR) | — | — | — | Predicts mean always |
| Linear Regression | X.XX | X.XX | X.XX | — |
| Random Forest | X.XX | X.XX | X.XX | n_estimators=200 |
| **XGBoost** | **X.XX** | **X.XX** | **X.XX** | **Best model** |

### Key Findings
[same table format as DA above]
-->

---
<!-- DIVE-EBENE ENDE -->

<!-- DEEP-DIVE-EBENE START -->

## Tech Stack

<!-- Konkrete Tools mit Version wo relevant. Keine Buzzword-Listen. -->

| Category | Tools |
| :--- | :--- |
| Language | Python 3.12 |
| Data | Polars, Pandas |
| Analysis | SciPy, statsmodels |
| Visualization | Matplotlib, Seaborn |
| ML *(DS only)* | scikit-learn, XGBoost |
| Packaging | uv, pyproject.toml |
| Notebooks | JupyterLab |
| Version Control | Git, GitHub |

## Project Structure

<!-- Ordner-Baum mit 1-Zeilen-Erklärungen. Nicht jeden File listen — nur was relevant ist. -->

```
[project-name]/
├── notebooks/
│   ├── 00_introduction.ipynb       ← Start here — guided project overview
│   ├── 01_exploration.ipynb        ← Initial data exploration
│   ├── 02_preparation.ipynb        ← Cleaning & master dataset
│   ├── 03_analysis_[topic].ipynb   ← [Analysis dimension 1]
│   ├── 04_insights.ipynb           ← Synthesised findings
│   └── 06_prediction.ipynb         ← ML model (DS only)
├── public/
│   ├── img/                       ← All exported charts (PNG)
│   ├── json/                      ← Storyline data per view
│   ├── md/                        ← Exported markdown docs
│   ├── index.html                 ← Portfolio hub (landing + navigation)
│   ├── overview.html              ← Business-focused story (slides)
│   ├── storyview.html             ← Full narrative + all findings (slides)
│   └── techview.html              ← Technical deep-dive (slides)
├── src/[package]/                  ← Importable Python package
│   ├── analytics/                  ← Analysis functions
│   ├── features/                   ← Feature engineering (DS)
│   ├── visualization/              ← Plot functions
│   ├── config.py                   ← PATHS, constants
│   └── settings.py                 ← Run-time settings
├── data/
│   ├── raw/                        ← Original data — never modified
│   ├── interim/                    ← After cleaning
│   └── processed/                  ← ML-ready features (DS)
├── pyproject.toml                  ← Dependencies
└── ROADMAP.md                      ← Project phases & status
```

## Setup

<!-- Muss reproduzierbar sein. Auf fremdem Rechner testen bevor ins README schreiben. -->

**Prerequisites:** Python 3.12+, [uv](https://docs.astral.sh/uv/) (recommended) or pip

```bash
# Clone
git clone https://github.com/kaywiegand/[project-name].git
cd [project-name]

# Install dependencies
uv sync
# or: pip install -e .

# Launch notebooks
uv run jupyter lab
```

<!-- Falls Rohdaten nicht im Repo (zu groß): Download-Anweisung hinzufügen -->
<!--
**Data:** Download raw data from [Source URL] and place in `data/raw/`.
```bash
# optional: automated download script
python scripts/download_data.py
```
-->

## Notebooks

<!-- Reihenfolge für externe Leser explizit angeben. -->

| # | Notebook | Description |
| :--- | :--- | :--- |
| 00 | [00_introduction.ipynb](notebooks/00_introduction.ipynb) | Start here — project overview and key results |
| 01 | [01_exploration.ipynb](notebooks/01_exploration.ipynb) | Raw data exploration and quality assessment |
| 02 | [02_preparation.ipynb](notebooks/02_preparation.ipynb) | Cleaning, transformation, master dataset |
| 03 | [03_analysis_[topic].ipynb](notebooks/03_analysis_[topic].ipynb) | [Analysis dimension] |
| 04 | [04_insights.ipynb](notebooks/04_insights.ipynb) | Synthesised findings across all dimensions |
| 06 | [06_prediction.ipynb](notebooks/06_prediction.ipynb) | *(DS only)* ML modelling and evaluation |

## Reports

<!-- Links zu den exportierten Reports. Müssen existieren und > 50 KB sein. -->

| Report | Description |
| :--- | :--- |
| [Hub](public/index.html) | Portfolio landing page + navigation to all views |
| [StoryView](public/storyview.html) | Full narrative + all findings (slides) |
| [Overview](public/overview.html) | Business-focused short story (slides) |
| [TechView](public/techview.html) | Technical deep-dive (slides) |

---

## Author

**Kay Alexander Wiegand**  
Senior Consultant · Data Scientist  
[LinkedIn](https://linkedin.com/in/kaywiegand) · [GitHub](https://github.com/kaywiegand)

<!-- DEEP-DIVE-EBENE ENDE -->

---

<!-- 
QUALITY CHECKLIST — vor dem Publish abhaken:

SCAN-EBENE:
[ ] Titel spezifisch — kein Buzzword-Titel
[ ] Key Visual eingebettet und korrekte Pfadangabe (relativ)
[ ] TL;DR hat mind. 3 Findings MIT konkreten Zahlen
[ ] Keine generischen Sätze ("This project analyzes data to gain insights")

DIVE-EBENE:
[ ] Problem Statement in 3–5 Sätzen — was, warum, Leitfrage
[ ] Dataset-Tabelle vollständig (Source, Size, Time Period, License, Known Issues)
[ ] Approach-Section zum Projekttyp passend (DS/DA/DEV/SKL) — falsche Sections entfernt
[ ] Results: Tabelle mit Findings + Zahlen
[ ] DS: Modell-Tabelle mit Baseline + Metriken

DEEP-DIVE-EBENE:
[ ] Tech Stack: echte Tools mit Versionen — keine Buzzword-Liste
[ ] Projektstruktur: Ordner-Baum vorhanden und aktuell
[ ] Setup: tatsächlich getestet — auf fremdem Rechner reproduzierbar
[ ] Notebooks-Tabelle: alle existierenden Notebooks verlinkt
[ ] Hub: index.html existiert, enthält Beschreibung + verlinkt die Views (storyview/overview/techview)

KONSISTENZ:
[ ] Zahlen im TL;DR stammen aus Notebooks — nicht erfunden
[ ] Key Visual existiert in public/img/
[ ] Setup-Paketname stimmt mit pyproject.toml überein
[ ] Alle Links sind erreichbar (nicht broken)
-->
