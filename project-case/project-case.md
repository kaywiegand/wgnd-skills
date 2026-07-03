---
description: Builds the portfolio case study for the current project. Extracts story, drafts slide content in dialog, generates index.html hub and presentation views. Modes: check | story | slides | report | full | audit-communication
---

Du baust den **Portfolio Case Study** für das **aktuelle Projekt**.
Das Projekt ist das aktuelle Working-Directory von Claude Code.

**Pfad-Konvention:** `SKILL_ROOT` = der Ordner dieser Datei selbst (`.../wgnd-skills/project-case/`). Beim Lesen dieser Skill-Datei bereits bekannt — keine Herleitung nötig, kein Workspace-Bezug erforderlich.

**Skill-eigene Ressourcen (alle im selben Ordner wie diese Datei):**
```
Case-Standards:       case-standards.md
Checklist-Template:   portfolio-check-template.md
Preparation-Workflow: preparation-workflow.md
Communication-Concept: communication-concept.md
Summary-Template:     portfolio-summary-template.md
Build-Pipeline (Details): build-pipeline.md

Design-Templates (projektübergreifend einheitliches Design):
Slides-Template:  templates/slides-template.html
Slides-CSS:       templates/slides.css
Index-Template:   templates/index-template.html
Styleguide:       templates/styleguide.html
```

**Aufruf:** `/project-case [mode]`
**Modi:** `check` · `story` · `slides` · `report` · `full` · `audit-communication`
(`json` war früher ein eigener Modus, ist aber nirgends mehr definiert — entfernt 2026-07-01;
das mechanische JSON-Bauen passiert innerhalb von `report`/`make portfolio`.)

Lies den Modus aus `$ARGUMENTS`. Wenn kein Argument: frage "Welcher Modus?".

---

## ⚙️ Portfolio Pipeline — Mechanisiert (ab 2026-06-19, Scripts global seit 2026-07-01)

Die generischen Pipeline-Scripts liegen **im Skill**, nicht im Projekt — projektübergreifend
wiederverwendbar, da sie ausschließlich relativ zum aktuellen Arbeitsverzeichnis (`Path.cwd()`)
arbeiten:
```
{SKILL_ROOT}/scripts/
    ├─ archive_portfolio_artifacts.py
    ├─ generate_json_from_slides.py
    ├─ generate_html_from_json.py
    ├─ generate_index_from_portfolio.py
    ├─ convert_json_to_md.py
    └─ print_slide_matrix.py
```
Immer aus dem **Projekt-Root** heraus aufrufen (`uv run python <Skill-Pfad>/<script>.py`) —
die Scripts lesen/schreiben unter dem aktuellen Arbeitsverzeichnis, genau wie zuvor bei
projektlokalen Scripts.

**Architektur (sicher: archiviert vor Überschreiben):**
```
                    archive_portfolio_artifacts.py
                    → public/archive/vN/  (Snapshot des alten Stands, kein Promoten nötig)
                                   ↓
public/md/slides.yaml  (Single Source of Truth für Slide-Struktur + -Inhalt)
        ├─ generate_json_from_slides.py    → public/json/storyline-{view}.json (1 pro View)
        ├─ generate_html_from_json.py      → public/{view}.html
        ├─ generate_index_from_portfolio.py → public/index.html   (Hub, aus slides.yaml["hub"] + Skill-Template)
        ├─ convert_json_to_md.py           → public/md/{view}.md
        └─ print_slide_matrix.py           → public/md/slides-matrix.md (Audit: Slide × View)
```
`public/md/portfolio.md` bleibt daneben bestehen — Fakten/Findings/These, Referenz beim
Schreiben von `slides.yaml`, sowie Input für `generate_index_from_portfolio.py` (Hub-Metadaten:
Name, Zeitraum, Dashboard-Link). Details + Migrationsgeschichte: `build-pipeline.md`.

**Wichtig — wo lebt was (übersteht Regenerierung):**
- **Slide-Inhalt** (Titel, Text, welche Slide in welcher View) → `public/md/slides.yaml` (im Projekt)
- **Fakten/Findings/Recommendations** → `public/md/portfolio.md` (im Projekt)
- **Slide-Design** → `{SKILL_ROOT}/templates/{slides-template.html,slides.css}` (global, für alle Portfolios identisch) — `public/css/slides.css` im Projekt ist nur die Build-Kopie, NIE von Hand editieren
- **Hub-Layout** → `{SKILL_ROOT}/templates/index-template.html` (global — reines Layout, kein Projekt-Content mehr)
- **Mechanik** (JSON/HTML/MD generieren) → `{SKILL_ROOT}/scripts/*.py` (global)
- NIE die generierten `public/*.html` direkt editieren — wird überschrieben.
- Jeder Lauf **archiviert** zuerst nach `public/archive/vN/` → stabile Namen bleiben,
  Historie bleibt erhalten, Vergleich gegen Archiv möglich.

**⚠️ Der Hub gehört zur Slide-Autorenarbeit dazu — nicht danach vergessen:** `public/index.html`
wird aus dem `hub`-Block in `slides.yaml` gebaut (Hero-KPIs per Zeiger auf eine Slide-ID, 3
View-Karten mit Titel/Beschreibung/Zielgruppe/Dauer). Bei jeder Content-Änderung an `slides.yaml` —
egal ob heute manuell oder künftig über einen `/project-case slides`-Modus — mitdenken:
ändert sich eine Kernzahl, eine View-Beschreibung oder eine Zielgruppe, die auch auf dem Hub
auftaucht? Dann `hub.headline_kpis_from` / `hub.view_cards` in `slides.yaml` konsistent halten.
Details + Schema: `build-pipeline.md`, Abschnitt „generate_index_from_portfolio.py".

**Ein-Befehl (empfohlen):** `make portfolio`
→ archive → json → html → index → md → matrix (kompletter sicherer Lauf)

**Modi:**
- `story` — portfolio.md aktualisieren (Input: Notebooks + MD-Files)
- `slides` — slides.yaml im Dialog erstellen/weiterentwickeln (Kapitel-Feedback + Tabellen-Review)
- `report` — **archiviert zuerst**, dann JSONs + HTMLs (alle Views) + index + MDs + Matrix, rein mechanisch
- `full` — check → story → slides → report (mit Bestätigungen dazwischen)

---

## Mode: check

**Ziel:** Vollständiger Qualitäts-Audit. Nichts verändern — nur lesen und bewerten.

**Schritt 1 — Kontext lesen:**
Lies (falls vorhanden): `CLAUDE.md` · `PROCESS_LOG.md` · `ROADMAP.md`
Lies: `case-standards.md` (im selben Ordner wie diese Datei) — besonders "Maschinenprüfbare Kriterien"

**Schritt 2 — Datei-Existenz prüfen (binary ✅/❌):**

Zuerst: Web-Root bestimmen — Projekte nutzen `public/` als Web-Root:
```bash
[ -d "public" ] && echo "web_root=public" || echo "❌ public/ not found"
```

```
README.md · ROADMAP.md · PROCESS_LOG.md · BACKLOG.md · pyproject.toml
notebooks/00_introduction.ipynb
public/*.html             (mind. 1 Datei > 50 KB)
public/img/*.png          (mind. 3 Dateien)
src/[paket]/__init__.py
tests/
.gitignore
public/md/portfolio.md    ← Interface-File für Story/Slides
```

Hinweis: `public/` ist der Standard-Web-Root für alle Projekte (GitHub Pages und lokal).

**Schritt 3 — README-Qualität prüfen:**
Lies README.md. Prüfe nach Best-Practice-Struktur (Referenz: zh-tram-flow Jun 2026 / project-review Skill):

Pflicht-Sections (✅/❌):
- `TL;DR` — Zahlen vorhanden, Target erklärt, KPIs ausgeschrieben?
- `Where to start` — Tabelle mit Lesertypen + Direktlinks?
- `Project Overview` — Motivation + Data Cycle Tabelle mit Links?
- `Problem Statement` — Leitfragen + KPI-Tabelle (Ist / Ziel / Gap)?
- `Dataset` — Final Dataset first · Quellen-Liste · Known Issues · Link DATA_DICTIONARY?
- `Approach` — Sections mit Notebook-Links · Dimensionen-Tabelle · Modell-Tabelle?
- `Results` — Recommendations vorhanden (nicht nur Findings)?
- `Notebooks` — volle Dateinamen als Link-Text?
- `Setup` — max. 4 Zeilen + Link zu SETUP.md?
- `Status Badge` — aktueller Projektstatus im Badge?

Fehler-Muster (aktiv prüfen):
- ❌ Key Visual als PNG im README (zu groß, Ladezeit) — besser in public/index.html
- ❌ Findings-Tabelle doppelt (Approach + Results)
- ❌ Interne Kürzel im Type-Badge (DAN/DSC/DANSC)
- ❌ ROADMAP oder BACKLOG verlinkt — nie öffentlich
- ❌ Notebook-Links mit Kurzformen (`03-4`) statt vollen Dateinamen
- ❌ Lizenz-Zeile bei gemischten Datenquellen ohne differenzierte Angabe

**Schritt 4 — ML-Pflicht (nur wenn notebooks/06_* oder data/models/ existiert):**
Grep nach Keywords in prediction- und evaluation-Notebooks:
- "baseline" oder "MAE" → Baseline-Dokumentation
- "leakage" → Leakage-Check
- "error analysis" oder "Fehleranalyse" → Error Analysis
- "limitation" oder "Limitierung" → Known Limitations

**Schritt 5 — Notebook-Ausführung prüfen:**
Lies je Notebook die ersten 50 Zeilen (JSON). Prüfe: Hat mind. 1 output-Cell Inhalt?
Alle leeren Notebooks → ⚠️

**Schritt 5b — Notebook-Header-Format prüfen:**
Für jedes Notebook in `notebooks/` prüfe die erste Markdown-Zelle (cell 0).

Pflicht-Format:
```
# Title (English)
**UPPERCASE SUBTITLE**

---
```

Checks (✅/⚠️/❌):
- `#`-Titel auf Englisch (kein Deutsch)?
- Subtitle vorhanden und in `**UPPERCASE**`?
- `---` Trennlinie nach Subtitle?
- Zweite Zelle ist `## Inhalt` ToC? (besonders wichtig bei Notebooks > 5 Sections)
- Alle `##`- bis `####`-Header in eigenen Zellen, nicht zusammen mit Inhalt?

Schnell-Check via Bash:
```bash
python3 -c "
import json
from pathlib import Path
for p in sorted(Path('notebooks').glob('*.ipynb')):
    nb = json.load(open(p))
    c0 = ''.join(nb['cells'][0]['source'])
    ok = c0.startswith('# ') and '**' in c0 and '---' in c0
    toc = len(nb['cells']) > 1 and '## Inhalt' in ''.join(nb['cells'][1]['source'])
    flag = '✅' if ok else '❌'
    toc_flag = '📋' if toc else '  '
    print(f'{flag} {toc_flag} {p.name}')
"
```

**Schritt 6 — portfolio.md prüfen:**
Suche:
- `public/md/portfolio.md`

```bash
[ -f "public/md/portfolio.md" ] && echo "✅ public/md/portfolio.md" || \
echo "❌ portfolio.md nicht gefunden — Story-Phase noch nicht ausgeführt"
```

Wenn gefunden → kurz prüfen ob Kernthese, Findings und Modell-Ergebnisse befüllt sind.

**Schritt 7 — Public Index & Linking prüfen:**
Prüfe ob `public/index.html` existiert und alle relevanten Artefakte verlinkt sind:

Wenn `public/index.html` existiert:
- ✅ Überprüfe ob folgende Dateien verlinkt sind (via `href=` oder `<a>` Tags):
  - `overview.html` oder `presentation.html` (Präsentationen)
  - `public/index.html` (Report)
  - `apps/dashboard/` oder Link zu Live-App
  - Notebooks (GitHub-Links oder lokale `notebooks/` Links)
  - Social Media One-Pager (falls vorhanden: `index.html`)

- ✅ Prüfe Linkgültigkeit:
  ```bash
  grep -o 'href="[^"]*"' public/index.html | cut -d'"' -f2 | while read link; do
    [ -f "public/$link" ] && echo "✅ $link" || echo "❌ Missing: $link"
  done
  ```

Wenn `public/index.html` NICHT existiert:
- ⚠️ Flag: "Kein Public Index vorhanden — Navigation-Hub fehlt"

Output-Befund:
```
📍 Public Navigation (index.html):
✅ index.html existiert
✅ overview.html verlinkt
✅ public/index.html verlinkt
⚠️  Streamlit-Link ist extern (zh-tram-flow.streamlit.app)
❌ index.html verlinkt (lokale Version, aber im index nicht genannt)
```

---

**Output-Format:**
```
# Portfolio Check — [Projektname]
Datum: [heute]

## 1. Story & Relevanz       [✅/⚠️/❌]
## 2. Struktur & Files       [✅/⚠️/❌]
## 3. Kohärenz               [✅/⚠️/❌]
## 4. Analyse-Qualität       [✅/⚠️/❌]
## 5. ML-Qualität            [✅/⚠️/❌ / n.a.]
## 6. Code & Architektur     [✅/⚠️/❌]
## 7. Artefakte              [✅/⚠️/❌]
## 8. Public Navigation      [✅/⚠️/❌]
## 9. Reproduzierbarkeit     [✅/⚠️/❌]

## Top 3 Gaps
1. ...
2. ...
3. ...

## Bereit für Story-Phase: JA / NEIN
Begründung: ...
```

---

## Mode: story

**Ziel:** Storyline aus Projekt-Material extrahieren und `public/md/portfolio.md` schreiben.
Das ist die Fakten-Referenz für Findings/Recommendations/These — genutzt beim Schreiben von
`public/md/slides.yaml` (der eigentlichen Slide-Struktur, siehe Pipeline-Sektion oben), nicht
mehr automatisch von den nachfolgenden Modi geparst.

**Schritt 1 — Kontext aufbauen:**
Lies: `CLAUDE.md` · `PROCESS_LOG.md` · `ROADMAP.md`

**Schritt 2 — Findings aus Notebooks lesen:**
Suche Notebooks mit "insights", "analysis", "evaluation" im Namen.
Lies jeweils nur die **Markdown-Cells** (type == "markdown") — keine Code-Outputs.
Extrahiere: Findings, Metriken, Zahlen, Schlussfolgerungen.

**Schritt 3 — Figures inventarisieren:**
Liste alle Dateien in `public/img/` auf.
Ordne sie thematisch zu (Temporal, Geo, Meteo, Events, Model, etc.).

**Schritt 4 — Template lesen:**
Lies: `portfolio-summary-template.md` (im selben Ordner wie diese Datei)

**Schritt 5 — Portfolio Summary schreiben:**
Fülle das Template mit den extrahierten Informationen.
Schreibe nach: `public/md/portfolio.md`

**Wichtig:**
- Nur Zahlen verwenden die tatsächlich in Notebooks oder PROCESS_LOG stehen
- Kernthese: eine klare These-Aussage, nicht generisch
- Findings: konkret mit Zahlen — kein "XY ist wichtig"
- Model Results: alle Modelle mit MAE/Metrik-Werten
- Recommendations: direkt aus Analyse-Findings ableitbar

**Output:**
`public/md/portfolio.md` schreiben + Zusammenfassung was befüllt wurde.
Frage Kay: "Story-Phase abgeschlossen. Bitte einmal durchlesen — passt die Kernthese?"

---

## Mode: report

**Ziel:** Alle HTML-Artefakte mechanisch aus `public/md/slides.yaml` regenerieren —
**zerstörungsfrei** (alter Stand wird zuvor archiviert).

**Ablauf (nichts von Hand schreiben — die Scripts machen es):**
```bash
SKILL_SCRIPTS={SKILL_ROOT}/scripts
uv run python $SKILL_SCRIPTS/archive_portfolio_artifacts.py    # Snapshot → public/archive/vN/
uv run python $SKILL_SCRIPTS/generate_json_from_slides.py      # → public/json/storyline-*.json
uv run python $SKILL_SCRIPTS/generate_html_from_json.py        # → public/{view}.html
uv run python $SKILL_SCRIPTS/generate_index_from_portfolio.py  # → public/index.html (Hub)
uv run python $SKILL_SCRIPTS/convert_json_to_md.py             # → public/md/{view}.md
uv run python $SKILL_SCRIPTS/print_slide_matrix.py             # → public/md/slides-matrix.md (Audit)
```
oder kurz: `make portfolio` (Makefile im Projekt kapselt die Skill-Pfade bereits)

**Wichtig:**
- `public/index.html` wird aus `{SKILL_ROOT}/templates/index-template.html` generiert
  (Layout, global) + `slides.yaml`s `hub`-Block (Inhalt, im Projekt) + `portfolio.md`
  (Name, Zeitraum, URLs).
- Slide-**Inhalt** steckt in `public/md/slides.yaml` (im Projekt) — dort ändern, nicht in den
  generierten JSONs/HTMLs.
- Slide-**Design** steckt in `{SKILL_ROOT}/templates/{slides-template.html,slides.css}`
  (global, für alle Portfolios identisch) — `public/css/slides.css` im Projekt ist nur die
  Build-Kopie.
- Generierte `public/*.html` NIE direkt editieren — beim nächsten Lauf weg (aber im Archiv).

---

## Mode: slides

**Ziel:** `public/md/slides.yaml` im Dialog mit Kay erstellen oder weiterentwickeln — die
Urteilsarbeit, die keine Automatik leisten kann (welches Finding wird welche Slide, in
welchem Kapitel, für welche Views). Das Gegenstück zu `story`: `story` verdichtet Notebooks
zu Fakten (`portfolio.md`), `slides` verdichtet Fakten zu Präsentation (`slides.yaml`).

Für die reine Mechanik danach (JSON/HTML aus einer fertigen `slides.yaml` bauen) siehe
Mode `report` — das ist unverändert ein einziger `make portfolio`-Lauf, keine Dialog-Phase.

**Schritt 0 — Bestehenden Stand prüfen (immer zuerst, nie überschreiben ohne zu fragen):**
```bash
[ -f "public/md/slides.yaml" ] && echo "EXISTIERT" || echo "NEU"
```

Wenn **NEU** → weiter mit Schritt 1.

Wenn **EXISTIERT** → Kay fragen, in dieser Reihenfolge:
1. "Es gibt bereits eine `slides.yaml`. Soll ich vorher ein Backup anlegen? (ja/nein)"
   - Ja → `cp public/md/slides.yaml public/md/slides.yaml.bak-$(date +%Y%m%d-%H%M)`
2. "Komplett neu aufbauen, oder an der bestehenden Datei weiterarbeiten (nur Ergänzungen/Änderungen)?"
   - **Neu aufbauen** → bestehenden Inhalt nicht als Vorlage nutzen, weiter mit Schritt 1 wie bei NEU
   - **Weiterarbeiten** → bestehende `chapters`/`view_composition` als Ausgangspunkt lesen, im
     Dialog klären was sich ändert (neue Findings, geänderte Zahlen, neue Views), nur die
     betroffenen Kapitel neu durchgehen — nicht die ganze Datei neu schreiben

Es gibt **kein** `locked`-Feld mehr (frühere Idee, verworfen) — dieser Dialog am Anfang ersetzt
es: die Entscheidung "anfassen oder nicht" liegt bei Kay, pro Lauf, nicht pro Slide fest codiert.

**Schritt 1 — Kontext lesen:**
- `public/md/portfolio.md` (Fakten, Findings, These, Recommendations)
- Notebooks, wo `portfolio.md` nicht genug Detail für eine gute Slide hergibt
- `public/img/` für verfügbare Charts (`chart_refs`)

**Schritt 2 — StoryView zuerst aufbauen (die vollständigste Version):**
StoryView ist die längste, vollständigste Erzählung — kompletter Data Cycle (Data Engineering →
Exploration → Erkenntnis → Machine Learning → Empfehlungen → Projektrahmen → Weitere
Potenziale/Ausblick). Alles andere leitet sich in Schritt 3 daraus ab — deshalb zuerst.

Gehe **Kapitel für Kapitel** vor, nicht alles auf einmal:
1. Ein Kapitel vorschlagen: welche Slides, mit welchem Titel/Inhalt, Bezug auf konkrete
   Finding-IDs aus `portfolio.md`
2. Kay bestätigen lassen ("passt Kapitel X so?") bevor es weitergeht zum nächsten
3. Erst nach Bestätigung aller Kapitel weiter zu Schritt 3

Das ist die **Feedback-Schleife** — nie mehr als ein Kapitel auf einmal vorschlagen, sonst
prüft niemand mehr wirklich nach.

**Schritt 3 — Overview + TechView durch Wiederverwendung ableiten, nicht neu schreiben:**
Für jede StoryView-Slide aus Schritt 2 prüfen: passt sie unverändert auch für Overview
und/oder TechView?
- **Ja** → `views`-Liste der Slide einfach um die weitere(n) View(s) erweitern. Das ist der
  Normalfall — die meisten Slides sollten hier landen.
- **Nein, aber ähnlich** → eine zusätzliche, view-spezifische Slide anlegen (Ausnahme, nicht Regel)
- **Nein, komplett irrelevant für diese View** → Slide bleibt nur bei StoryView, Kapitel taucht
  in `view_composition` der anderen View gar nicht auf

Ziel: am Ende so wenige separate Varianten wie möglich. Wenn für ein Kapitel mehr als eine
view-spezifische Zusatz-Slide nötig scheint, das explizit mit Kay absprechen statt einfach
zu duplizieren.

**Schritt 4 — Tabellen-Review vor dem Schreiben (Texte abnehmen lassen):**
Bevor `slides.yaml` geschrieben/überschrieben wird, den geplanten Stand als Tabelle zeigen —
gleiches Format wie `print_slide_matrix.py`, aber vorab am Entwurf, nicht erst danach als Audit:

| id | Kapitel | Inhalt | StoryView | TechView | Overview |
|:---|:---|:---|:---:|:---:|:---:|
| ... | ... | ... | ✅/– | ✅/– | ✅/– |

Kay bestätigt (oder korrigiert) diese Tabelle explizit. Erst danach `slides.yaml` schreiben.

**Schritt 5 — Schreiben + nächster Schritt:**
`public/md/slides.yaml` schreiben (neu oder aktualisiert). Dann vorschlagen:
`make portfolio` ausführen, um JSON/HTML/Matrix zu regenerieren und das Ergebnis zu prüfen
(→ Mode `report`, rein mechanisch, keine weitere Rückfrage nötig).

**Nicht Teil dieses Modus:** `.pptx`-Export — auf expliziten Wunsch von Kay zusätzlich via
`anthropic-skills:pptx`, nachdem `slides.yaml` steht.

---

## Mode: full

**Ziel:** Vollständige Pipeline in Sequenz. Nur ausführen wenn check grünes Licht gibt.

**Ablauf:**
1. Führe `check` aus
2. Wenn "Bereit für Story-Phase: NEIN" → stoppe und zeige Top 3 Gaps
3. Führe `story` aus → warte auf Kay's Bestätigung der Kernthese
4. Führe `slides` aus → Dialog-Modus mit Kapitel-Feedback-Schleife + Tabellen-Review
   (siehe Mode `slides` oben) — **kein automatischer Durchlauf**, `full` wartet hier auf Kay
5. Führe `report` aus (= `make portfolio`: archive → json → html → index → md → matrix)
6. Erstelle git commit:
   `docs: portfolio prep — index.html + Views regeneriert`
7. Aktualisiere PROCESS_LOG.md:
   Session-Eintrag: "Portfolio-Aufbereitung: slides.yaml + index + Views regeneriert (alter Stand in public/archive/)"

---

## Mode: audit-communication

**Ziel:** Validiere dass Artefakte alle 8 Zielgruppen (A–H) erreichen. Basiert auf `communication-concept.md`

**Schritt 1 — Kontext prüfen:**
Lies:
- `communication-concept.md` (im selben Ordner wie diese Datei) — Abschnitt 3 (Zielgruppen-Matrix) + Abschnitt 7 (Checkliste)
- `PROCESS_LOG.md` — welche Artefakte wurden gebaut?
- `README.md` — 3-tier Struktur für Zielgruppe B vorhanden?

**Schritt 2 — Zielgruppen-Audit Matrix:**

Für jede Zielgruppe (A–H) prüfen ob die **Pflicht-Artefakte** vorhanden und verlinkt sind:

| # | Zielgruppe | Pflicht-Artefakte | Vorhanden | Status |
|:--|:-----------|:-----------------|:----------|:-------|
| A | Data Peers | README + Notebooks + Full Report | ✓? | ✅/❌ |
| B | HR/Recruiter | Hub + README (3-tier) | ✓? | ✅/❌ |
| C | Tech Lead | Full Report + Notebooks + GitHub | ✓? | ✅/❌ |
| D | Kunden | Hub + Dashboard + Presentation | ✓? | ✅/❌ |
| E | Non-Data | Hub + Dashboard | ✓? | ✅/❌ |
| F | Community | Hub + README + Notebooks + GitHub | ✓? | ✅/❌ |
| G | Obsidian | PDFs + Obsidian MD + Frontmatter | ✓? | ✅/❌ |
| H | AI Tools | PDFs + JSON metadata | ✓? | ✅/❌ |

**Schritt 3 — Pro Zielgruppe detailliert:**

**A (Data Peer):**
- README vorhanden? (English, technisch, Problem + Ergebnis)
- Notebooks zugänglich? (alle 00_–06_ vorhanden + verlinkt?)
- Full Report (`public/index.html`) vorhanden?
- Status: "Peer-ready?" JA / NEIN / PARTIAL

**B (HR/Recruiter):**
- Hub (`public/index.html`) vorhanden?
- README hat 3 Leseebenen (Scan 30s / Dive 5min / DeepDive 30min)?
- README: Projekttitel + Key Visuals + KPIs + Key Results präsent?
- Status: "HR-ready?" JA / NEIN / PARTIAL

**C (Tech Lead):**
- Full Report vorhanden + ist > 100 KB + enthält Code-Snippets?
- Notebooks vorhanden + sind numeriert (00_–06_)?
- GitHub Link im README?
- Status: "Tech-Lead-ready?" JA / NEIN / PARTIAL

**D (Kunden):**
- Hub vorhanden + ist Deutsch + hat Business-Frames?
- Dashboard vorhanden + ist aufgerufen worden?
- Presentation vorhanden + hat 22+ Slides?
- Status: "Customer-ready?" JA / NEIN / PARTIAL

**E (Non-Data):**
- Hub vorhanden + einfache Sprache (keine Jargon)?
- Dashboard vorhanden + visuell-spielerisch (nicht Code-heavy)?
- Status: "Non-Data-ready?" JA / NEIN / PARTIAL

**F (Community):**
- README vorhanden + auf GitHub öffentlich?
- Notebooks vorhanden + exportierbar?
- Hub shareable (Deutsch, Kontext-gut)?
- Status: "Community-ready?" JA / NEIN / PARTIAL

**G (Obsidian):**
- PDFs exportiert (`docs/exports/*.pdf`)?
- Obsidian MD mit Frontmatter vorhanden (`docs/exports/zh-tram-flow.md`)?
- Frontmatter enthält: project, slug, type, status, findings, model_mae?
- Status: "Obsidian-ready?" JA / NEIN / PARTIAL

**H (AI Tools):**
- PDFs exportiert (`docs/exports/*.pdf`)?
- JSON Metadata vorhanden (`docs/exports/project_summary.json`)?
- JSON enthält: project, type, findings, stack, model, artifacts?
- Status: "AI-Tool-ready?" JA / NEIN / PARTIAL

**Schritt 4 — Scorecard erstellen:**

```
# Audit: Communication-Readiness — [Projektname]
Datum: [heute]

## Audience Coverage

| Zielgruppe | Artefakte | Status | Lücke |
|:-----------|:----------|:-------|:------|
| A (Peer) | README + Notebooks + Report | ✅/⚠️/❌ | – |
| B (HR) | Hub + README 3-tier | ✅/⚠️/❌ | – |
| C (Tech) | Report + Notebooks + GitHub | ✅/⚠️/❌ | – |
| D (Kunden) | Hub + Dashboard + Slides | ✅/⚠️/❌ | – |
| E (Non-Data) | Hub + Dashboard | ✅/⚠️/❌ | – |
| F (Community) | Hub + README + Notebooks | ✅/⚠️/❌ | – |
| G (Obsidian) | PDFs + MD + Frontmatter | ✅/⚠️/❌ | – |
| H (AI Tools) | PDFs + JSON + Metadata | ✅/⚠️/❌ | – |

**Summary:** X von 8 Zielgruppen vollständig abgedeckt
```

**Schritt 5 — Top 3 Fehlende Artefakte:**

Liste auf:
1. [Missing Artifact] — Zielgruppe X braucht das — Aufwand: gering/mittel/hoch
2. ...
3. ...

**Schritt 6 — Optional: Nächste Schritte:**

```
Nächste Actions:
- [ ] Hub bauen (`public/index.html`)
- [ ] Dashboard aufsetzen (`apps/dashboard/app.py`)
- [ ] PDFs exportieren (`scripts/export_artifacts.py`)
- [ ] Obsidian Frontmatter erstellen
- [ ] Deployment: GitHub Pages + Streamlit Cloud
- [ ] LinkedIn-Artikel schreiben (Zielgruppe F)
```

---

## Allgemeine Regeln (alle Modi)

- **Keine Zahlen erfinden.** Nur was in PROCESS_LOG, ROADMAP oder Notebooks steht.
- **Vor NotebookEdit immer fragen** ob Kay gespeichert hat und bereit ist.
- **Keine Dateien löschen** ohne explizite Erlaubnis.
- **Jeder Plot braucht eine Tabelle** als Zahlenbasis (Memory: Plot immer mit Tabelle).
- **English im Code** — Labels, Variablen, Kommentare auf Englisch.
- Bei Unsicherheit über Projektinhalt: erst fragen, dann schreiben.

## Notebook-Standard (gilt für alle Modi)

Jedes Notebook folgt diesem einheitlichen Format:

**Titelzelle (cell 0):**
```
# Title (English)
**UPPERCASE SUBTITLE**

---
```

**ToC-Zelle (cell 1, bei Notebooks mit > 4 Sections):**
```markdown
## Inhalt

- [Section Name](#anchor)
- [Section Name](#anchor)
  - [Subsection](#anchor)
```

**Header-Konvention:**
- Alle `#`- bis `####`-Überschriften immer in **eigener Markdown-Zelle** — nie zusammen mit Inhalt
- Alle Überschriften auf **Englisch**
- `#` nur für den Notebook-Titel (einmalig, cell 0)
- `##` für Haupt-Sections, `###` für Subsections, `####` für Detail-Ebene

Wenn beim `check` Abweichungen gefunden werden: als ⚠️ in Kategorie "7. Artefakte" aufführen und im Top-3-Gaps nennen falls > 3 Notebooks betroffen.
