---
description: Vollständiger Projekt-Audit vor Portfolio-Aufbereitung. Scannt Struktur, MD-Kohärenz, README, Notebooks, Git-Hygiene. Gibt priorisierte Verbesserungsvorschläge.
---

Du führst einen vollständigen Projekt-Review durch.
Das Projekt ist das aktuelle Working-Directory.

**Pfad-Konvention:** `WORKSPACE_ROOT` = das Wurzelverzeichnis des Workspace, in dem diese Skill läuft (enthält `CLAUDE.md`, `docs/`, `skills/`). Aus dem aktuellen Arbeitskontext ermitteln, nicht hart annehmen.

**Aufruf:** `/project-review`

**Wichtig:** Nur lesen, nichts verändern. Dieser Review ist ein Audit — kein Implement-Schritt.

---

## Schritt 1 — Kontext aufbauen

Lies (falls vorhanden):
- `CLAUDE.md` — Projekt-Identität, Typ, Stack
- `ROADMAP.md` — Phasen, aktueller Stand
- `PROCESS_LOG.md` — letzten 20–30 Zeilen
- `BACKLOG.md` — offene Tasks

Lies global:
- `{WORKSPACE_ROOT}/docs/CONVENTIONS.md` — aktuelle Notebook-Konventionen

---

## Schritt 2 — Strukturprüfung (binär ✅/❌)

Prüfe ob folgende Dateien/Ordner existieren:

**Pflicht-Files:**
```
CLAUDE.md
PROCESS_LOG.md
README.md
ROADMAP.md
BACKLOG.md
pyproject.toml  (oder requirements.txt)
.gitignore
```

**Notebook-Struktur:**
```
notebooks/00_introduction.ipynb    ← Einstieg für externe Leser
notebooks/01_*.ipynb               ← min. 1 Exploration-Notebook
public/                            ← Ordner existiert
public/img/                    ← mind. 3 PNG-Dateien
```

**Report-Pflicht (✅/❌ — kein Optional):**
```
public/index.html                 ← Pflicht — primäres externes Leseartefakt
```
Prüfe zusätzlich:
- Dateigröße > 50 KB (`ls -lh public/index.html`) — zu klein = Inhalt fehlt
- Enthält mind. 1 `<img`-Tag — Visualisierungen eingebettet?
- Enthält Fließtext (mind. 3 `<p>`-Tags) — Befunde narrativ erklärt?

**Optional aber wichtig (⚠️ wenn fehlt):**
```
public/presentation.html           ← Präsentation
public/md/portfolio.md                 ← Portfolio-Summary (Interface-File für /project-case story)
src/[paket]/                       ← Python-Paket
tests/                             ← Test-Ordner
```

---

## Schritt 3 — README-Qualität

Referenz-Template: `portfolio-readme-template.md` (im selben Ordner wie diese Datei)

Lies `README.md`. Prüfe nach den drei Leseebenen (Zielgruppen-Definitionen → `../project-case/communication-concept.md`):

**Scan-Ebene (HR Recruiter — 30 Sek):**
| Section | Pflicht | Prüfung |
|---|---|---|
| Projekttitel + 1-Satz-Pitch | ✅ | Spezifisch (nicht generisch) — Thema + Scope klar |
| Key Visual | ✅ | Mind. 1 eingebettetes PNG nahe Anfang — relativer Pfad korrekt? |
| TL;DR / Key Results | ✅ | Mind. 3 konkrete Findings MIT Zahlen |

**Dive-Ebene (Hiring Manager / Data Scientist — 5–10 Min):**
| Section | Pflicht | Prüfung |
|---|---|---|
| Problem Statement | ✅ | Was? Warum relevant? Leitfrage? — kein generischer Satz |
| Dataset | ✅ | Quelle, Größe, Zeitraum, Lizenz |
| Approach / Methodology | ✅ | Zum Projekttyp (DSC/DAN/DEV/SKL) passend — falsche Sections entfernt? |
| Results | ✅ | Findings-Tabelle mit Zahlen — DSC: Modell-Tabelle mit Baseline |
| Tech Stack | ✅ | Konkrete Tools, keine Buzzword-Listen |
| Setup / Installation | ✅ | Reproduzierbar — `uv sync` oder `pip install -e .` |

**Deep-Dive-Ebene (Tech Lead — 30+ Min):**
| Section | Pflicht | Prüfung |
|---|---|---|
| Projektstruktur | ⚠️ | Ordnerbaum vorhanden und aktuell |
| Notebooks-Tabelle | ✅ | Alle Notebooks verlinkt in Lesereihenfolge |
| Reports-Links | ✅ | Link auf `public/index.html` + `public/presentation.html` |
| Autor / Kontakt | ⚠️ | Name + LinkedIn + GitHub |

**Fehler-Muster die aktiv gesucht werden:**
- ❌ Metriken oder Zahlen im README die nicht aus Notebooks stammen können
- ❌ Generische Sätze ("This project analyzes data to gain insights...")
- ❌ Key Visual fehlt oder ist broken link (falscher Pfad)
- ❌ Setup-Anleitung mit falschem Paketnamen oder falschem Pfad
- ❌ Approach-Sections für falschen Projekttyp (z.B. ML-Sections in einem DAN-Projekt)
- ❌ Keine Links auf Report-Artefakte

---

## README Best Practices — Referenz (zh-tram-flow, Jun 2026)

Erarbeitet im Review-Prozess. Gilt als Qualitäts-Referenz für alle zukünftigen Portfolio-Projekte.

### Struktur (Reihenfolge)

```
# Titel + 1-Satz-Subline
Badges (Python · Stack · Type · Status)

## TL;DR          ← Results first — Zahlen, kein Fließtext
## Where to start ← Tabelle: Lesertyp → Direktlink
## Table of Contents
## Project Overview  ← Motivation (warum dieses Thema?) + Data Cycle Tabelle
## Problem Statement ← Leitfragen + KPI-Tabelle (Ist vs. Ziel vs. Gap)
## Dataset           ← Final Dataset first, dann Quellen-Liste, dann Known Issues
## Approach
   ### Data Engineering
   ### Data Analysis   ← Dimensionen-Tabelle mit Notebook-Links
   ### Data Science    ← Modell-Progressionstabelle
   ### Data Storytelling ← Artefakte mit konkretem Mehrwert pro Zeile
## Results           ← Modell-Ergebnis + Recommendations (nicht Findings wiederholen)
## Notebooks         ← Volle Dateinamen als Link-Text, nicht Kurzformen
## Tech Stack
## Reports & Artifacts
## Setup             ← 3 Zeilen + Link zu docs/SETUP.md
## Author
```

### Konkrete Regeln

**Badges:**
- `Status` Badge immer dabei: `Phase X complete` / `In Progress` / `Complete`
- Type Badge: keine internen Kürzel (DAN/DSC/DANSC) — lesbar: `Analysis + Prediction`

**TL;DR:**
- Target Variable in Alltagssprache erklären — kein `regression`, kein `classification`
- OTP / KPIs beim ersten Auftreten ausschreiben
- 4–5 Bullets, jeder mit konkreter Zahl

**Where to start:**
- Tabelle mit 3–4 Lesertypen und Direktlinks (Notebook + Live-Artefakt)
- Vor dem ToC platzieren — erste Interaktion für jeden Lesertyp

**Project Overview:**
- Motivation beibehalten — warum dieses Projekt, warum dieses Thema
- Data Cycle als Tabelle: Phase · Scope · Where (mit Direktlink)

**Dataset:**
- Final Dataset zuerst (Tabelle: Rows · Columns · Period · Granularity · Network)
- Dann Quellen als Liste mit konkreten Zahlen (Dateigröße, Einträge, etc.)
- Known Issues explizit benennen — Transparenz > Perfektion
- Link zu `docs/DATA_DICTIONARY.md`

**Approach:**
- Jede Section mit `→ [Einstiegs-Notebook]` verlinken
- Analysis: Dimensionen-Tabelle mit Notebook-Links (volle Dateinamen)
- Data Storytelling: pro Artefakt beschreiben was es *zeigt*, nicht was es *ist*

**Results:**
- Keine Findings-Tabelle wenn Approach sie schon hat — Redundanz vermeiden
- Recommendations als eigene Tabelle mit Evidenz-Spalte
- Top Features nennen

**Notebooks:**
- Volle Dateinamen als Link-Text: `03_analysis_4-spatial` — nicht `Spatial` oder `03-4`

**Setup:**
- Max. 3–4 Zeilen in README, Rest in `docs/SETUP.md`
- `--extra`-Flags erklären wenn nicht selbsterklärend

**Was nicht in die README gehört:**
- ROADMAP — intern, auf Deutsch, zu granular
- BACKLOG — nie öffentlich
- Vollständige Deployment-Anleitung → `docs/SETUP.md`
- Lizenz-Zeile wenn mehrere Quellen mit unterschiedlichen Bedingungen
- Internes Tooling ohne Kontext (wgnd-scaffolding Referenzen → nur im Footer)

### Ausgelagerte Files (Standard)

| File | Inhalt |
|:-----|:-------|
| `docs/DATA_DICTIONARY.md` | Alle Spalten mit Typ + Beschreibung + Known Issues |
| `docs/SETUP.md` | Vollständiges Setup · Deployment · Retraining · Production Notes |
| `docs/PROJECT_STRUCTURE.md` | Ordner-Tree mit Erklärungen (optional) |

---

## Schritt 3.5 — Kommunikations-Artefakte (optional, aber flagged)

**Prüfe ob folgende öffentliche Artefakte vorhanden sind** (optional, aber wenn fehlt: ⚠️)

Referenz: `../project-case/communication-concept.md` — definiert 8 Zielgruppen + Artefakt-Rollen

| Artefakt | Path | Zielgruppe | Prüfung |
|:---------|:-----|:-----------|:--------|
| Artifact Hub / Index | `public/index.html` | Alle (inkl. B HR, E Non-Data, F Community) | existiert? |
| Dashboard / App | `apps/dashboard/` + `apps/dashboard/app.py` | B, D, E (visuell) | existiert? |
| Obsidian Export | `docs/exports/*.md` | G (Second Brain) | existiert? |
| PDF Exports | `docs/exports/*.pdf` | G (Obsidian), H (AI Tools) | existiert? |
| JSON Metadata | `docs/exports/project_summary.json` | H (AI Tools) | existiert? |

**Output-Zeile für Scorecard (beispiel):**
```
📋 Communication: Hub ❌ | Dashboard ✅ | Exports ⚠️ | Obsidian ❌
```

**Wichtig:**
- ✅ Nicht blockierend — optional artifacts sind Teil der Portfolio-Aufbereitung (Schicht 2)
- Für **detailliertes Zielgruppen-Alignment Audit**: siehe `/project-case audit-communication`

---

## Schritt 3.6 — Fact-Check der öffentlichen Artefakte in public/

**Ziel:** Sicherstellen, dass alle Zahlen und Daten in den öffentlichen Artefakten (`public/`) korrekt sind und nicht veraltet.

**Schritt 1 — Datei-Inventar:**
Liste alle HTML-, JSON- und Markdown-Dateien in `public/` auf (ausgenommen `public/img/`, `public/json/`, `public/pdf/`, `public/md/`):
```bash
find public -maxdepth 1 -type f \( -name "*.html" -o -name "*.json" -o -name "*.md" \)
```

**Schritt 2 — Zahlen-Extraktion pro Datei:**
Für jede Datei: Grep nach Zahlen-Patterns (MAE, Baseline, OTP %, Millionen Zeilen, Feature-Counts, etc.):
```bash
grep -oE "[0-9]+\.?[0-9]*(s|s\.|%|M|Mio|Zeilen|Features|Slides)" file.html
```

**Schritt 3 — Validierung gegen Single Source of Truth:**

Für jede gefundene Zahl:
1. Suche die **Original-Quelle** (Notebook Cell Output, PROCESS_LOG, ROADMAP)
2. Vergleich: Stimmt die Zahl überein? Format korrekt? (z.B. "18.6s" nicht "18.6 Sekunden")
3. Prüfe: Ist die Datei aktueller als die Quelle?

**Kritische Metriken (immer validieren):**
- MAE / RMSE / Baseline-Werte
- OTP % und Ziel
- Feature-Counts (34, 36, etc.)
- Datensatz-Größen (94.4M, 41M, 29M Zeilen)
- Slide-Zähler und Navigation-Struktur

**Schritt 4 — Alterscheck:**
```bash
git log --oneline -- public/*.html | head -10
```
Sind diese Dateien älter als 2 Sessions? Wenn ja: ⚠️ "Artefakte möglicherweise veraltet"

**Schritt 5 — Output:**
```
📋 Public Artifact Fact-Check:
✅ MAE 18.6s (valide, von Notebook 06_eval, letzter Update vor 2 Tagen)
⚠️  Slide-Zähler 14 (Slides auf 9 reduziert, aber index.html zeigt noch 14 — Update nötig)
❌ OTP-Ziel 95% (in storyview.html als 95% korrekt, aber overview zeigt "95% bis 2028", widersprüchlich)

Kritische Lücken:
- [Liste was nicht validiert werden konnte]
```

---

## Schritt 3.7 — Cross-Artefakt-Konsistenzcheck (public/)

**Ziel:** Sicherstellen dass Kernbotschaften, Bezeichnungen und Formulierungen in allen
Präsentations-Artefakten identisch sind. Verhindert Drift zwischen JSON, HTML und MD.

**Gilt nur wenn `public/json/` mit Storyline-JSONs existiert.**

---

### A — Kapitelbezeichnungen

Prüfe ob `nav_label` in den JSONs mit den Slide-Titeln in den HTMLs übereinstimmt:

```bash
grep -h "nav_label" public/json/storyline-*.json
grep -h "<h2>" public/overview.html public/techview.html public/storyview.html public/socialview.html
```

**Prüfe speziell:**
- Einstiegs-Kapitel: heisst es überall `Ausgangssituation`? (nicht "Die Frage", "Ausgangslage", "Ausgangsfrage")
- Sind Kapitelbezeichnungen zwischen JSON (`nav_label`) und HTML (`<h2>`) deckungsgleich?

---

### B — Kernbefunde

Prüfe ob die drei Kernbefunde in allen Views identisch formuliert sind:

```bash
grep -rh "Kernbefund\|Kaskadeneffekt\|keinen Puffer\|Peripherie" \
  public/socialview.html public/json/storyline-socialview.json public/md/socialview.md
```

**Erwartete Kernbefunde (Stand Jun 2026):**
1. `Kaskadeneffekt: Verspätungen breiten sich aus`
2. `Das System hat keinen Puffer eingebaut`
3. `Verspätungen entstehen systematisch an der Peripherie — nicht im Zentrum`

Prüfe: Stimmen Titel und Kurztext in HTML, JSON und MD überein?

---

### C — Projektlogik / Ausgangssituation

Prüfe ob die Zwei-Schritt-Logik überall korrekt formuliert ist:

```bash
grep -rh "Entstehungsmuster\|Einflussfaktoren\|Temporal.*Räumlich" \
  public/index.html public/overview.html public/techview.html \
  public/storyview.html public/socialview.html public/json/storyline-*.json
```

**Erwartete Formulierung Schritt 1:**
`Analyse der Entstehungsmuster und Einflussfaktoren`
`Temporal · Räumlich · Netzwerk · Meteorologie · Events · Zieldefinition`

Abweichungen (z.B. "Verspätungen verstehen", "Wo entstehen sie?") → ❌ melden.

---

### D — Zahlen-Konsistenz zwischen JSON und HTML

Für die 5 Kern-KPIs prüfen ob JSON und HTML übereinstimmen:

| KPI | Sollwert (deutsch) |
|:----|:---------|
| OTP netzweit | `87 %` |
| VBZ-Ziel | `95 %` |
| MAE LightGBM v2 | `18,56 s` |
| vs. Baseline | `−63 %` |
| Halt-Ereignisse | `94,4 M` |
| Kaskadenkorrelation | `r ≥ 0,85` |
| Findings | `66` |

```bash
grep -rh "87 %\|95 %\|18,56\|63 %\|94,4\|0,85" \
  public/json/storyline-*.json public/overview.html public/techview.html \
  public/storyview.html public/socialview.html public/index.html
```

Abweichende Werte → ❌ mit Datei und Zeile melden.

---

### E — Deutsches Zahlenformat (Sprachkonvention)

Gilt für alle deutschen Artefakte in `public/` (HTML, JSON, MD).
README.md ist Englisch — dort gelten englische Konventionen (Punkt, kein Leerzeichen).

**Regeln:**
- Dezimaltrennzeichen: Komma statt Punkt → `18,56` nicht `18.56`
- Leerzeichen zwischen Zahl und Einheit → `87 %` · `18,56 s` · `94,4 M` · `r ≥ 0,85`
- Prozentpunkte als `%` schreiben, nicht als `pp` → `−8 %` nicht `−8pp`

```bash
# Suche nach englischen Dezimalzahlen mit Einheit (außer CSS-Kontext)
python3 -c "
import re, os
base = 'public'
css_vals = {'0.12','0.15','0.18','0.25','0.2'}
for root,dirs,files in os.walk(base):
    dirs[:] = [d for d in dirs if d != 'img']
    for fn in files:
        if not fn.endswith(('.html','.json','.md')): continue
        content = re.sub(r'<style>.*?</style>', '', open(os.path.join(root,fn)).read(), flags=re.DOTALL)
        for i,line in enumerate(content.split('\n'),1):
            if any(c in line for c in ['font-size','transition:','rgba(']): continue
            for m in re.finditer(r'(?<![,\d])(\d+\.\d+)(s|%)(?!\w)', line):
                if m.group(1) not in css_vals:
                    print(f'{fn}:{i}: [{m.group()}]')
            if re.search(r'\d\s*pp\b', line):
                print(f'{fn}:{i}: [pp gefunden]')
"
```

Treffer → ❌ melden.

---

### Output Schritt 3.7

```
📋 Cross-Artefakt-Konsistenz:
✅ Kapitelbezeichnungen — alle Views: "Ausgangssituation"
✅ Kernbefunde — JSON / HTML / MD konsistent
⚠️ Schritt-1-Formulierung — storyview.html Zeile 134: "Verspätungen verstehen" (veraltet)
❌ KPI-Abweichung — socialview.html: "~19s" statt "18.6s"

Drift-Risiko: GERING / MITTEL / HOCH
```

Drift-Risiko MITTEL oder HOCH → im Top-5 Verbesserungen aufführen.

---

## Schritt 4 — MD-Kohärenz

Prüfe Konsistenz zwischen den MD-Files:

**ROADMAP vs. PROCESS_LOG:**
- Sind abgeschlossene Phasen in ROADMAP als ✅ markiert?
- Gibt es PROCESS_LOG-Einträge ohne ROADMAP-Referenz?
- Gibt es ROADMAP-Phasen die laut PROCESS_LOG schon fertig sind, aber nicht markiert?

**BACKLOG vs. PROCESS_LOG:**
- Gibt es Items im BACKLOG die laut PROCESS_LOG schon erledigt sind?
- Gibt es Entscheidungen im PROCESS_LOG die nicht im BACKLOG als "erledigt" stehen?

**CLAUDE.md vs. Realität:**
- Stimmt der beschriebene Tech-Stack mit dem tatsächlichen Code (pyproject.toml) überein?
- Ist der Projekttyp (DSC/DAN/DEV/SKL) korrekt definiert?

---

## Schritt 5 — Notebook-Qualität

Lies für jedes Notebook die ersten 60 Zeilen (JSON-Format):

**Prüfe:**
- ✅ Nummerierung korrekt (00_, 01_, 02_, ...) und keine Lücken
- ✅ Erste Markdown-Cell enthält Titel + Beschreibung (Zweck · Input · Output)
- ⚠️ Notebook-Name stimmt mit Inhalt überein (kein "Untitled-3")

**Outputs in Git — Design-Entscheidung beachten:**
Notebook-Outputs werden in vielen Projekten bewusst NICHT committed (saubere Diffs,
Reproducibility). Prüfe `.gitignore` oder `pyproject.toml` auf `nbstripout`-Konfiguration.
- Wenn Outputs committed → prüfen ob mind. 1 Output-Cell Inhalt hat ✅
- Wenn keine Outputs in Git → ✅ kein Befund — `index.html` ist dann das externe Leseartefakt

**CONVENTIONS-Check:**
Grep in Notebooks nach:
- `show_df(` oder `an.table_` — Tabellen-Ausgaben zu Plots vorhanden?
- `# TODO` oder `# FIXME` — offene Punkte die zu BACKLOG gehören?

---

## Schritt 6 — Git-Hygiene

Führe folgende Befehle aus (read-only):

```bash
git status --short
git log --oneline -10
git diff --stat HEAD
```

**Prüfe:**
- Gibt es uncommitted changes? → ⚠️
- Stimmen die letzten Commit-Messages mit dem PROCESS_LOG überein?
- Gibt es `docs:` Commits nach Code-Commits? (Post-Commit-Protokoll)
- Gibt es große Binary-Files im Git (data/, *.pkl, *.h5)? → ❌

---

## Schritt 7 — Globale Workspace-Regeln

Prüfe gegen `{WORKSPACE_ROOT}/CLAUDE.md`:

- Sind alle MD-Files UPPERCASE?
- Enthält PROCESS_LOG nur Pointer (keine Zahlen/Metriken kopiert)?
- Ist CLAUDE.md des Projekts aktuell (passt zu aktuellem Stand)?

---

## Output-Format

```
# Project Review — [Projektname]
Datum: [heute]
Projekttyp: [DSC / DAN / DEV / SKL]

## Scorecard

| Bereich | Status | Schwerwiegendster Befund |
| :--- | :---: | :--- |
| Struktur & Files | ✅/⚠️/❌ | ... |
| README-Qualität | ✅/⚠️/❌ | ... |
| Kommunikations-Artefakte | ✅/⚠️/❌ | ... |
| Public Artifact Fact-Check | ✅/⚠️/❌ | ... |
| Cross-Artefakt-Konsistenz | ✅/⚠️/❌ | ... |
| MD-Kohärenz | ✅/⚠️/❌ | ... |
| Notebook-Qualität | ✅/⚠️/❌ | ... |
| Git-Hygiene | ✅/⚠️/❌ | ... |
| Workspace-Regeln | ✅/⚠️/❌ | ... |

## Detaillierte Befunde

### Struktur & Files
[Auflistung was fehlt / was OK ist]

### README
[Konkrete Sections die fehlen oder schwach sind + Verbesserungsvorschläge]

### Kommunikations-Artefakte (public/)
[Hub (index.html), Dashboard, PDF-Exports vorhanden? Links funktionieren?]

### Public Artifact Fact-Check
[Zahlen-Validierung gegen Notebooks · Alterscheck · Widersprüche erkannt?]

### Cross-Artefakt-Konsistenz
[Kapitelbezeichnungen · Kernbefunde · Schritt-1-Formulierung · KPI-Drift zwischen JSON/HTML/MD · Deutsches Zahlenformat]

### MD-Kohärenz
[Konkrete Widersprüche oder Lücken]

### Notebooks
[Ausgeführt? Nummerierung? CONVENTIONS-Verstöße?]

### Git
[Uncommitted Changes? Commit-Historie sauber?]

## Top 5 Verbesserungen (priorisiert)

1. [Wichtigste Lücke] — Warum: ...  Aufwand: [gering/mittel/hoch]
2. ...
3. ...
4. ...
5. ...

## Bereit für /project-case: JA / NEIN / BEDINGT
Begründung: ...
Nächster Schritt: ...
```

---

## Allgemeine Regeln

- **Nur lesen** — kein Edit, kein Write, kein Bash der Dateien verändert
- **Proaktiv Verbesserungen vorschlagen** — nicht nur Fehler benennen
- **Keine Zahlen erfinden** — nur was wirklich in den Files steht
- **Workspace-Regeln haben Vorrang** — CLAUDE.md im Workspace-Root ist die Referenz
- Bei Unklarheit über Projektinhalt: im Output explizit als "unklar" markieren, nicht raten
