# Communication Concept for Portfolio Projects

**Blueprint for presenting data science projects to diverse audiences.**

Based on the Zürich Tram Flow project (2026). Generalized for all portfolio projects.

---

## 1. Zielgruppen (Audience Segmentation)

Every project reaches different people with different goals. Each person should find a clear entry point.

| # | Zielgruppe | Frage | Span | Tech-Level | Primary Channel |
|:--|:-----------|:------|:-----|:-----------|:----------------|
| A | Data Peers / Kollegen | What is your workflow? How did you solve that? | 5–15 min | high | Notebooks + StoryView |
| B | HR / Recruiter | Does this person fit? Convince me in 30s. | 30–60 sec | low | Hub (index.html) + README |
| C | Tech Lead / Hiring Manager | Can they think rigorously? What's the code quality? | 5–15 min | high | TechView + Notebooks + GitHub |
| D | Potenzielle Kunden | Is this relevant for us? Can we talk? | 3–5 min | medium | Hub (index.html) + Dashboard + Overview |
| E | Non-Data People | What's possible with data? | 2–3 min | none | Hub (index.html) + Dashboard |
| F | Community (LinkedIn, Blog) | What can I learn / share? | 1–2 min | medium | Hub (index.html) + LinkedIn post |
| G | Second Brain (Obsidian) | Can I import this? Machine readable? | N/A | N/A | Obsidian MD + PDFs |
| H | AI Tools (NotebookLM, GPT) | Can you analyze / summarize this? | N/A | N/A | PDF exports + JSON metadata |

**Key insight:** B scans, C prüft, D entscheidet, E trägt weiter, F rekrutiert (the flywheel).

---

## 2. Artefakte (Artifact Catalog)

### Core Artefakte (alle Projekte)

Landing Page und Artifact Hub sind **eine** Datei, kein Artefakt-Paar: `index.html` übernimmt
beide Rollen zugleich (Social-Media-Einstieg *und* Navigation). Ein eigenständiges "Full Report"-
Artefakt gibt es nicht mehr — dessen Rolle (Narrative + alle Findings) übernimmt die StoryView-
Präsentation. Statt einer generischen "Presentation" gibt es drei benannte, aus `slides.yaml`
generierte Views mit je eigenem Zweck — siehe `build-pipeline.md` für den Mechanismus.

| Artefakt | Zweck | Format | Audience | Effort |
|:---------|:------|:-------|:---------|:--------|
| **README** | Einstieg ins Projekt | Markdown | A, B, C, F | low |
| **Hub** (`index.html`) | Landing + Navigation kombiniert — Einstiegspunkt für fast alle Zielgruppen | HTML (generiert aus `slides.yaml`s `hub`-Block) | A, B, C, D, E, F | low (generiert) |
| **Dashboard / Demo** | Interaktive Exploration | Streamlit/Web | B, D, E | medium–high |
| **Overview** (Presentation) | Business-focused Story, kurz | HTML Slides / Reveal.js (generiert aus `slides.yaml`) | B, D | medium |
| **StoryView** (Presentation) | Komplette Narrative + alle Findings — ersetzt "Full Report" | HTML Slides / Reveal.js (generiert aus `slides.yaml`) | A, C, F | medium |
| **TechView** (Presentation) | Technischer Deep-Dive | HTML Slides / Reveal.js (generiert aus `slides.yaml`) | A, C | medium |
| **Notebooks** | Code + Iterationen | Jupyter | A, C, F | high (created, not for export) |

### Optional Artefakte (zielgruppen-spezifisch)

| Artefakt | Für Zielgruppe | Format | Effort |
|:---------|:-----------------|:-------|:--------|
| **PDF Exports** | G (Obsidian), H (AI Tools) | PDF | low–medium |
| **Obsidian Frontmatter** | G (Second Brain) | YAML + MD | low |
| **Project Metadata JSON** | H (AI Tools) | JSON | low |
| **Blog Post / LinkedIn** | F (Community) | Markdown | medium |

---

## 3. Artefakt × Zielgruppe Matrix

**✓✓** = primär · **✓** = unterstützend · **–** = nicht geeignet

| Artefakt | A | B | C | D | E | F | G | H |
|:---------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| README | ✓ | ✓✓ | ✓✓ | ✓ | – | ✓ | ✓ | ✓ |
| Hub (`index.html`) | ✓ | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓✓ | – | – |
| Dashboard | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | – | – |
| Overview | – | ✓✓ | ✓ | ✓✓ | ✓ | ✓ | – | – |
| StoryView | ✓✓ | – | ✓✓ | ✓ | – | ✓✓ | ✓ | ✓ |
| TechView | ✓✓ | – | ✓✓ | – | – | ✓ | ✓ | ✓ |
| Notebooks | ✓✓ | – | ✓✓ | – | – | ✓✓ | ✓ | ✓ |
| PDFs | ✓ | – | ✓ | – | – | – | ✓✓ | ✓✓ |

---

## 4. Lesepfade (User Journeys)

Everyone's path is different. Don't force a single narrative.

```
B · HR/Recruiter
  LinkedIn/Instagram → Hub / index.html (30s) → Dashboard (wow) → [optional] Overview

C · Tech Lead
  README → TechView + StoryView → Notebooks (deep dive)

D · Potenzielle Kunden
  LinkedIn/Email → Hub / index.html → Dashboard → Overview (pitch) → Gespräch

E · Non-Data People
  Instagram/Hub / index.html → Dashboard (spielerisch) → [optional] Overview

A · Data Peer
  README → Notebooks (code + context) → StoryView (findings)

F · Community
  LinkedIn Post → Hub / index.html → Dashboard → README → Notebooks

G · Obsidian
  export_artifacts.py → docs/exports/zh-tram-flow.md → Obsidian

H · AI Tools
  export_artifacts.py → docs/exports/*.pdf + project_summary.json → NotebookLM/GPT
```

**Roter Faden:** Hub (`index.html`) ist für fast alle der Einstiegspunkt (außer Tech Lead + Community, die direkt ins Repo gehen).

---

## 5. Design-Grundsätze

### Hub (`index.html`)

- **Zielgruppe:** B (HR), E (Non-Data), Breite Audience
- **Tonalität:** Professional aber zugänglich. Keine akademische Jargon.
- **Länge:** Erster Eindruck 30s, vollständige Navigation 3–5 min
- **Design:** Swiss / Clean. Whitespace. Grad-Hero. Keine CTA-Overkill.
- **Differentiator:** Das eine Ding, das man sich merkt (z.B. "Delays are predictable, not random")

### Dashboard

- **Zielgruppe:** Alle (aber speziell B, D, E)
- **Tonalität:** Spielerisch + erkenntnisreich. "Wow-Momente."
- **Tiefe:** Progressive Disclosure. Start einfach, optionale Tiefe.
- **Bsp. Struktur:**
  - Seite 1: Überblick (Hero + KPIs + Übersichtskarte)
  - Seite 2: Analyse (3–4 Key Findings mit interaktiven Charts)
  - Seite 3: Demo (Live-Vorhersage / Kernfeature ausprobieren)
  - Seite 4: Kontakt (Links, Next Steps)

### StoryView

- **Zielgruppe:** A (Peers), C (Tech Lead), F (Community)
- **Tonalität:** Narrativ + datengestützt. "Story with Evidence."
- **Struktur:** Problem → Analyse → Befund → Modell → Empfehlungen
- **Länge:** 45+ Minuten zu lesen
- **Charts:** Alle Charts erklären. Keine "selbstverständlichen" Visualisierungen.

### Notebooks

- **Zielgruppe:** A (Peers), C (Tech Lead), G/H (Export)
- **Tonalität:** Technisch + transparent. Code + Text + Output.
- **Struktur:** Etablierte (sequentiell nach Phase)
  - 00: Intro + Setup
  - 01–02: Data Exploration & Preparation
  - 03: Analysis (nach Themen) → 6+ Notebooks
  - 04: Insights & Synthesis
  - 05: Feature Engineering
  - 06: Modeling & Evaluation (sequentiell)

---

## 6. Deployment-Strategie

### Wo liegt was

| Artefakt | Platform | URL | Maintenance |
|:---------|:---------|:----|:------------|
| Hub + Overview + StoryView + TechView | GitHub Pages | `https://<user>.github.io/<project>/` | Auto (push to main) |
| Dashboard | Streamlit Cloud | `https://<project>.streamlit.app` | Auto (push to main) |
| Notebooks | GitHub | `/<repo>/tree/main/notebooks/` | Manual (notebook edits) |
| PDFs + Obsidian + JSON | GitHub | `docs/exports/` | On-demand (export_artifacts.py) |

### Reproduzierbarkeit

**Requirement:** Jedes Artefakt muss reproduzierbar sein.

- **Notebooks:** Kommando `make notebooks` (oder jupyter lab)
- **Dashboard:** `make precompute && make dashboard`
- **Overview/StoryView/TechView:** `make portfolio` (generiert aus `public/md/slides.yaml`, siehe `build-pipeline.md`)
- **Exports:** `python scripts/export_artifacts.py`

---

## 7. Checkliste: Projekt Portfolio-Ready Machen

Für jedes neue Projekt:

### Phase 1 — Fundament (Notebooks + README)
- [ ] CLAUDE.md: Projekt-Setup dokumentiert
- [ ] PROCESS_LOG.md: Verlauf dokumentiert
- [ ] ROADMAP.md: Ziele + Phasen definiert
- [ ] README.md: Überblick für externe Leser
- [ ] Notebooks: 6+ sequentiell + sauberer Code
- [ ] 1 Key Visual: Aufmachen der README

### Phase 2 — Kommunikation (Artefakte)
- [ ] Hub (`public/index.html`, generiert aus `slides.yaml`s `hub`-Block)
- [ ] Dashboard (optional, aber empfohlen)
- [ ] Overview (Business-Präsentation, aus `slides.yaml`)
- [ ] StoryView (komplette Narrative, aus `slides.yaml`)
- [ ] TechView (technischer Deep-Dive, aus `slides.yaml`)

### Phase 3 — Export & Maschinenlesbarkeit (Optional, aber für Portfolio wichtig)
- [ ] `scripts/export_artifacts.py`: Alle Artefakte als PDF + Obsidian MD
- [ ] `docs/exports/`: README + Obsidian + JSON
- [ ] DEPLOYMENT.md: Anleitung für Public Deployment

### Phase 4 — Dokumentation & Blueprint
- [ ] Dieses Concept Document (für alle Projekte gleich)
- [ ] communication-concept.md ins Projekt (adaptiert)
- [ ] Skill integration: /project-review + /project-case Updated

---

## 8. Best Practices

### Fehler, die passieren

❌ **Ein Artefakt für alle Zielgruppen**
→ Hub ist nicht StoryView. HR will nicht 45 Minuten lesen.
→ Lösung: Mehrere Artefakte, klare Lesepfade.

❌ **Zu viel Text ohne Bilder**
→ Dashboard/StoryView werden nicht angeklickt.
→ Lösung: Jeder Absatz hat einen Chart / Datenpoint.

❌ **Keine Projekt-Einleitung in jedem Artefakt**
→ Jemand kann über Google auf jedes Artefakt stoßen.
→ Lösung: Jede Seite hat "Was ist das?" (2–3 Sätze).

❌ **Modernes aber lesergenerisch Design**
→ Alle Projekte sehen gleich aus.
→ Lösung: Ein Ding, das man sich merkt (→ Designberatung).

### Was funktioniert

✓ **Hub + Dashboard als Tandem**
→ Hub lockt, Dashboard hält und bewegt.
→ Kombination ist unschlagbar für B (HR) + E (Non-Data).

✓ **Narrative Views (StoryView + Overview)**
→ "Befund vor Modell" statt "Modell ist cool."
→ Menschen folgen Beweisketten, nicht Algorithmen.

✓ **Notebooks als Source of Truth**
→ Alle anderen Artefakte verlinken / zitieren Notebooks.
→ Keine Duplikationen, keine veralteten Zahlen.

✓ **Progressive Disclosure in Dashboards**
→ Seite 1: für Everyone (Hero + Overview)
→ Seite 3: für Enthusiasten (Deep Dive + Demo)

---

## 9. Sprachen

**Regel:** Inhalt = Projektsprache, Struktur/Code = Englisch

| Element | Sprache |
|:--------|:--------|
| README | Englisch (GitHub Standard) |
| Hub (`index.html`) | Projektsprache (Deutsch für DACH) |
| Dashboard | Projektsprache (Deutsch für DACH) |
| Overview / StoryView / TechView | Projektsprache |
| Notebooks | Englisch (Code) + Projektsprache (Markdown) |
| Code Comments | Englisch |
| Variable Names | Englisch |

---

## 10. Tools & Stack (empfohlen)

### Artefakt-Erstellung

| Artefakt | Tool | Why |
|:---------|:-----|:----|
| Hub (`index.html`) | HTML, generiert aus `slides.yaml`s `hub`-Block | Fast, Static, GitHub Pages |
| Dashboard | Streamlit | Python-native, 1-Klick Deploy |
| Overview / StoryView / TechView | Reveal.js, generiert aus `slides.yaml` | Ein Slide-Registry, drei Views ohne Copy-Paste-Drift |
| Notebooks | Jupyter | Standard in DS-Community |

### Export & Machine Readability

| Zielgruppe | Tool |
|:-----------|:-----|
| PDFs | `nbconvert` (Notebooks) + `weasyprint` (HTML) |
| Obsidian | Custom YAML Frontmatter + Markdown |
| AI Tools (NotebookLM etc.) | PDF + JSON metadata |

---

## 11. Messgrößen

Wie weiß man ob es funktioniert?

| Metrik | Zielgruppe | Erfolgskriterium |
|:-------|:-----------|:-----------------|
| Hub Bounce Rate | B, E | < 50% (first impression works) |
| Dashboard Time Spent | D, E | > 3 min (they explore) |
| GitHub Stars | A, C, F | > 10 (technical credibility) |
| LinkedIn Reach | B, F | > 500 impressions (visibility) |
| Inquiries / Gespräche | D | ≥ 1 (business validation) |

---

## 12. Versioning & Maintenance

### Updates

- **Hub:** Update bei jedem neuen Release
- **Dashboard:** Auto (Streamlit Cloud) oder manuell (Plotly)
- **Overview/StoryView/TechView:** Nach neuen Findings (`slides.yaml` editieren + `make portfolio`)
- **Notebooks:** Fortlaufend (ist Livingdocument)
- **communication-concept.md:** Nur wenn neue Erkenntnisse (jährlich prüfen)

### Archivieren

Wenn ein Projekt "done" ist (keine neuen Insights mehr):
1. Tag als `portfolio-ready` in PROJECTS.md
2. README → Past Tense ("showed", "achieved")
3. Dashboard kann am Laufen bleiben (Showcase)
4. Repo archivieren auf GitHub (falls nicht mehr aktiv)

---

**Basis-Version:** 2026-06-02
**Anwendbar auf:** Alle zukünftigen Portfolio-Projekte
**Nächste Review:** 2026-12-02
