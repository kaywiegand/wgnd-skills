# Portfolio Summary — [PROJEKTNAME]
<!-- Interface-Datei: Wird von /project-case story befüllt.
     Einzige Zahlenquelle für /project-case report und /project-case slides.
     KEINE Inhalte aus Notebooks kopieren — nur kuratierte Kernaussagen.
-->

---

## Project

```
name:       [Projektname, z.B. "Zürich Tram Flow"]
slug:       [z.B. zh-tram-flow]
type:       [DANSC | DAN | DA | DSC]
stage:      [Phase X — kurze Beschreibung des aktuellen Stands]
target:     [Zielvariable, z.B. "arrival_delay (Sekunden)"]
stack:      [z.B. Python · Polars · LightGBM · Plotly · Jupyter]
period:     [Zeitraum der Daten, z.B. "2023–2025"]
rows:       [Anzahl Datenpunkte, z.B. "~85M (lf_clean)"]
notebooks:  [Anzahl]
findings:   [Anzahl]
dashboard:  [URL falls deployed, z.B. https://zh-tram-flow.streamlit.app — sonst weglassen]
```

---

## Storyline

```
thesis:     [Die eine These in einem Satz — konkret, nicht generisch]
hook:       [Der überraschendste oder relevanteste Befund]
proof:      [Wie wird die These bewiesen? z.B. "4-Schritt-Beweiskette"]
so_what:    [Was folgt daraus? z.B. "Vorhersagbar heisst steuerbar"]
```

---

## Problem

```
kpi_name:   [Name des Haupt-KPIs, z.B. "OTP"]
kpi_ist:    [Ist-Wert, z.B. "87%"]
kpi_soll:   [Ziel-Wert, z.B. "95%"]
kpi_gap:    [Abweichung, z.B. "-8pp"]
problem_statement: |
  [2–3 Sätze: Was ist das Problem, wie gross ist es, warum ist es relevant?]
```

---

## Key Findings
<!-- Max 6 Findings — jeweils mit konkreter Zahl und Quelle-Notebook -->

### F1 — [Kurztitel, z.B. "Temporal: Peak 21h"]
```
finding:   [Befund in einem Satz mit Zahl]
number:    [Die eine Zahl, z.B. "+11.7s vs. Mittel"]
source:    [Notebook-Name]
```

### F2 — [Kurztitel]
```
finding:   
number:    
source:    
```

### F3 — [Kurztitel]
```
finding:   
number:    
source:    
```

### F4 — [Kurztitel]
```
finding:   
number:    
source:    
```

### F5 — [Kurztitel]
```
finding:   
number:    
source:    
```

### F6 — [Kurztitel]  <!-- optional -->
```
finding:   
number:    
source:    
```

---

## Model Results
<!-- Nur befüllen wenn ML-Projekt (Typ DANSC oder DSC) -->

```
algorithm:      [z.B. LightGBM]
target:         [z.B. arrival_delay]
metric:         [z.B. MAE (Mean Absolute Error)]
split_strategy: [z.B. temporal — 2025 als Test-Jahr]
train_rows:     [z.B. 41.2M]
val_rows:       [z.B. 14.3M]
test_rows:      [z.B. 29.9M]
```

### Baseline Benchmark

| Model | Logic | Metric |
|---|---|---|
| Grand Mean | Always predict ⌀ | [z.B. 50.6s] |
| [weitere Baselines] | | |
| **[Best Baseline]** | **[Logik]** | **[Wert] ← Ziel** |

### Model Progression

| Model | Features | Test Metric | vs. Baseline | Data Requirement |
|---|---|---|---|---|
| [Best Baseline] | — | [Wert] | — | Historical mean |
| [Modell v1] | [N] | [Wert] | [Delta] | [z.B. Schedule · Weather · Events] |
| [Modell v2] | [N] | [Wert] | [Delta] | [z.B. + Live signal] |

```
best_model:     [Name des besten Modells]
best_metric:    [Wert]
key_insight:    [Das wichtigste Feature oder Erkenntnis aus Feature Importance]
mbe:            [Mean Bias Error — Tendenz zu über/unterschätzen]
```

---

## Figures
<!-- Alle relevanten Exports in public/img/ — für Report und Slides -->

```yaml
geo:
  - figures/geo-delay.png         # [kurze Beschreibung]

temporal:
  - figures/tempo-day-hours.png   # [kurze Beschreibung]
  - figures/tempo-week-days.png   # [kurze Beschreibung]

network:
  - figures/network.png           # [kurze Beschreibung]

meteo:
  - figures/meteo-types.png       # [kurze Beschreibung]

events:
  - figures/events-timeline.png   # [kurze Beschreibung]

model:
  - figures/feature-importance.png # [kurze Beschreibung, wenn vorhanden]

interactive:
  - figures/plotly_chart_1.html   # [kurze Beschreibung]
```

---

## Recommendations

```
r1:
  title:  [Handlungsfeld 1 — kurzer Titel]
  detail: [1–2 Sätze: Was, warum, Hebel aus Daten]

r2:
  title:  [Handlungsfeld 2]
  detail: 

r3:
  title:  [Handlungsfeld 3]
  detail: 

r4:
  title:  [Handlungsfeld 4, optional]
  detail: 
```

---

## Status

```
generated_by:   /project-case story
generated_at:   [Datum]
summary_version: 1
portfolio_check: [✅ passed | ⚠️ partial | ❌ pending]
report_html:    [✅ generated | ❌ pending]
slides_html:    [✅ generated | ❌ pending]
dashboard:      [✅ live — URL | ❌ not deployed — aus DEPLOYMENT.md lesen]
```
