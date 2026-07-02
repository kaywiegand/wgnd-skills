# Case Standards
### Was jedes Portfolio-Case braucht

Mindeststandard für ein portfolio-fähiges Projekt — die objektive Meßlatte,
unabhängig von Zielgruppe/Kanal (dafür: `communication-concept.md`).
Referenzprojekt: `zh-tram-flow` — aktueller Gold Standard.

Checklist → `portfolio-check-template.md`
Workflow  → `preparation-workflow.md`

---

## Die acht Qualitätsdimensionen

| # | Dimension | Kernfrage |
| :--- | :--- | :--- |
| 1 | **Story & Relevanz** | Problem, Ansatz, Ergebnis in 3 Sätzen klar? |
| 2 | **Struktur & Files** | Entspricht das Layout dem Standard? |
| 3 | **Kohärenz** | Erzählen README, Introduction und ROADMAP dieselbe Geschichte? |
| 4 | **Analyse-Qualität** | Findings strukturiert, beantwortet, mit Business-Impact? |
| 5 | **ML-Qualität** | Baseline, Modellwahl, Leakage, Error Analysis? *(nur ML-Projekte)* |
| 6 | **Code & Architektur** | src/ verwendbar, Tests sinnvoll, kein dead code? |
| 7 | **Artefakte & Präsentation** | Reports exportiert, Key-Visual sichtbar, Notebooks ausgeführt? |
| 8 | **Reproduzierbarkeit** | Clone → install → run funktioniert für Dritte? |

---

## Pflicht-Artefakte (Datei-Existenz, binär prüfbar)

| Artefakt | Beschreibung |
| :--- | :--- |
| `README.md` | Elevator Pitch + Key-Visual + Stack + Status + Setup |
| `ROADMAP.md` | Phasen mit aktuellem Status |
| `PROCESS_LOG.md` | Projektverlauf + Entscheidungen chronologisch |
| `BACKLOG.md` | Offene Tasks |
| `pyproject.toml` | Reproduzierbare Umgebung |
| `00_introduction.ipynb` | Geführter Einstieg — ausgeführt, kein leerer Output |
| `public/*.html` | Mindestens ein exportierter HTML-Report (>50 KB) |
| `public/img/*.png` | Mindestens 3 exportierte PNGs |
| `src/[paket]/__init__.py` | Importierbares Package mit realen Funktionen |
| `tests/` | Testordner vorhanden |
| `.gitignore` | Vorhanden |

---

## Maschinenprüfbare Kriterien (für Skill)

### README-Sections (Keyword-Check)
```
## Problem / ## Das Problem / ## Problemstellung
## Ergebnis / ## Was die Daten zeigen / ## Results
## Tech Stack / ## Stack
## Setup / ## Schnellstart / ## Installation
## Motivation / ## Portfolio / ## Warum
```

### ML-Pflicht (nur wenn notebooks/06_* oder models/ existiert)
```
Baseline: keyword "baseline" oder "MAE" in prediction-Notebooks
Leakage: keyword "leakage" oder "Leakage" in preparation/feature-Notebooks
Error Analysis: keyword "error" oder "Fehler" in evaluation-Notebooks
Limitierungen: keyword "Limitierung" oder "limitation" oder "Known" in README oder evaluation
```

### Artefakte (Datei + nicht-leer)
```
public/ hat ≥ 1 .html-Datei (>50 KB)
public/img/ hat ≥ 3 .png-Dateien
data/raw/ ist NICHT in Git (via .gitignore-Check)
models/ hat ≥ 1 Modelldatei (wenn ML-Projekt)
```

### Code-Qualität (Heuristiken)
```
Keine absoluten Pfade: kein "/Users/" oder "C:\\" im src/-Code
Keine Debug-Zellen: kein "test123", "tmp", "DELETE" in Notebooks
src/ hat > 1 .py-Datei mit > 10 Zeilen (nicht nur Scaffold)
```
