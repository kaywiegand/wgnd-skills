# Communication Concept for Portfolio Projects

**Blueprint for presenting data science projects to diverse audiences.**

Based on the Zürich Tram Flow project (2026). Generalized for all portfolio projects.

---

## 1. Zielgruppen (Audience Segmentation)

Every project reaches different people with different goals. Each person should find a clear entry point.

| # | Zielgruppe | Frage | Span | Tech-Level | Primary Channel |
|:--|:-----------|:------|:-----|:-----------|:----------------|
| A | Data Peers / Kollegen | What is your workflow? How did you solve that? | 5–15 min | high | Notebooks + Full Report |
| B | HR / Recruiter | Does this person fit? Convince me in 30s. | 30–60 sec | low | Landing Page + README |
| C | Tech Lead / Hiring Manager | Can they think rigorously? What's the code quality? | 5–15 min | high | Full Report + Notebooks + GitHub |
| D | Potenzielle Kunden | Is this relevant for us? Can we talk? | 3–5 min | medium | Landing Page + Dashboard + Presentation |
| E | Non-Data People | What's possible with data? | 2–3 min | none | Landing Page + Dashboard |
| F | Community (LinkedIn, Blog) | What can I learn / share? | 1–2 min | medium | Landing Page + LinkedIn post |
| G | Second Brain (Obsidian) | Can I import this? Machine readable? | N/A | N/A | Obsidian MD + PDFs |
| H | AI Tools (NotebookLM, GPT) | Can you analyze / summarize this? | N/A | N/A | PDF exports + JSON metadata |

**Key insight:** B scans, C prüft, D entscheidet, E trägt weiter, F rekrutiert (the flywheel).

---

## 2. Artefakte (Artifact Catalog)

### Core Artefakte (alle Projekte)

| Artefakt | Zweck | Format | Audience | Effort |
|:---------|:------|:-------|:---------|:--------|
| **README** | Einstieg ins Projekt | Markdown | A, B, C, F | low |
| **Landing Page** | Social-Media Köder | HTML (static) | B, D, E, F | medium |
| **Artifact Hub / Index** | Navigation Übersicht | HTML (static) | A, B, C, D, E, F | low |
| **Dashboard / Demo** | Interaktive Exploration | Streamlit/Web | B, D, E | medium–high |
| **Full Report** | Narrative + alle Findings | HTML | A, C, D, F | high |
| **Presentation** | Business-focused Story | HTML Slides | B, C, D | medium |
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
| Landing Page | ✓ | ✓✓ | ✓ | ✓✓ | ✓✓ | ✓✓ | – | – |
| Index / Hub | ✓ | ✓✓ | ✓ | ✓ | ✓ | ✓ | – | – |
| Dashboard | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | ✓✓ | – | – |
| Full Report | ✓✓ | – | ✓✓ | ✓ | – | ✓✓ | ✓ | ✓ |
| Presentation | ✓ | ✓✓ | ✓ | ✓✓ | ✓ | ✓ | – | – |
| Notebooks | ✓✓ | – | ✓✓ | – | – | ✓✓ | ✓ | ✓ |
| PDFs | ✓ | – | ✓ | – | – | – | ✓✓ | ✓✓ |

---

## 4. Lesepfade (User Journeys)

Everyone's path is different. Don't force a single narrative.

```
B · HR/Recruiter
  LinkedIn/Instagram → Landing Page (30s) → Dashboard (wow) → [optional] Presentation

C · Tech Lead
  README → Full Report → Notebooks (deep dive)

D · Potenzielle Kunden
  LinkedIn/Email → Landing Page → Dashboard → Presentation (pitch) → Gespräch

E · Non-Data People
  Instagram/Landing Page → Dashboard (spielerisch) → [optional] Presentation

A · Data Peer
  README → Notebooks (code + context) → Full Report (findings)

F · Community
  LinkedIn Post → Landing Page → Dashboard → README → Notebooks

G · Obsidian
  export_artifacts.py → docs/exports/zh-tram-flow.md → Obsidian

H · AI Tools
  export_artifacts.py → docs/exports/*.pdf + project_summary.json → NotebookLM/GPT
```

**Roter Faden:** Landing Page ist für fast alle der Einstiegspunkt (außer Tech Lead + Community, die direkt ins Repo gehen).

---

## 5. Design-Grundsätze

### Landing Page & Hub

- **Zielgruppe:** B (HR), E (Non-Data), Breite Audience
- **Tonalität:** Professional aber zugänglich. Keine akademische Jargon.
- **Länge:** Landing 30s, Hub 3–5 min
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

### Full Report

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
| Landing + Hub + Report + Presentation | GitHub Pages | `https://<user>.github.io/<project>/` | Auto (push to main) |
| Dashboard | Streamlit Cloud | `https://<project>.streamlit.app` | Auto (push to main) |
| Notebooks | GitHub | `/<repo>/tree/main/notebooks/` | Manual (notebook edits) |
| PDFs + Obsidian + JSON | GitHub | `docs/exports/` | On-demand (export_artifacts.py) |

### Reproduzierbarkeit

**Requirement:** Jedes Artefakt muss reproduzierbar sein.

- **Notebooks:** Kommando `make notebooks` (oder jupyter lab)
- **Dashboard:** `make precompute && make dashboard`
- **Reports/Presentation:** Aus Notebooks oder Source-Markdown
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
- [ ] Landing Page (`public/landingpage.html`)
- [ ] Index/Hub (`public/index.html`)
- [ ] Dashboard (optional, aber empfohlen)
- [ ] Full Report (aus Notebooks oder custom)
- [ ] Presentation (22–30 Slides)

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
→ Landing Page ist nicht Full Report. HR will nicht 2h lesen.
→ Lösung: Mehrere Artefakte, klare Lesepfade.

❌ **Zu viel Text ohne Bilder**
→ Dashboard/Report werden nicht angeklickt.
→ Lösung: Jeder Absatz hat einen Chart / Datenpoint.

❌ **Keine Projekt-Einleitung in jedem Artefakt**
→ Jemand kann über Google auf jedes Artefakt stoßen.
→ Lösung: Jede Seite hat "Was ist das?" (2–3 Sätze).

❌ **Modernes aber lesergenerisch Design**
→ Alle Projekte sehen gleich aus.
→ Lösung: Ein Ding, das man sich merkt (→ Designberatung).

### Was funktioniert

✓ **Landing Page + Dashboard als Tandem**
→ Landing lockt, Dashboard hält und bewegt.
→ Kombination ist unschlagbar für B (HR) + E (Non-Data).

✓ **Narrative Reports (Full + Presentation)**
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
| Landing Page | Projektsprache (Deutsch für DACH) |
| Dashboard | Projektsprache (Deutsch für DACH) |
| Report | Projektsprache |
| Presentation | Projektsprache |
| Notebooks | Englisch (Code) + Projektsprache (Markdown) |
| Code Comments | Englisch |
| Variable Names | Englisch |

---

## 10. Tools & Stack (empfohlen)

### Artefakt-Erstellung

| Artefakt | Tool | Why |
|:---------|:-----|:----|
| Landing Page | HTML + CSS | Fast, Static, GitHub Pages |
| Dashboard | Streamlit | Python-native, 1-Klick Deploy |
| Report | HTML + Plotly | Narrativ möglich, interaktive Charts |
| Presentation | HTML Slides (Reveal.js oder custom) | Moderner als PowerPoint |
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
| Landing Page Bounce Rate | B, E | < 50% (first impression works) |
| Dashboard Time Spent | D, E | > 3 min (they explore) |
| GitHub Stars | A, C, F | > 10 (technical credibility) |
| LinkedIn Reach | B, F | > 500 impressions (visibility) |
| Inquiries / Gespräche | D | ≥ 1 (business validation) |

---

## 12. Versioning & Maintenance

### Updates

- **Landing Page / Hub:** Update bei jedem neuen Release
- **Dashboard:** Auto (Streamlit Cloud) oder manuell (Plotly)
- **Reports:** Nach neuen Findings (vierteljährlich?)
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
