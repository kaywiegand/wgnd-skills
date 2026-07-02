# Portfolio Workflow
### Schritt-für-Schritt: Projekt portfolio-ready machen

Von "cleanup nötig" zu "portfolio-ready" in 5 Phasen.
Immer in dieser Reihenfolge — keine Phase überspringen.

---

## Phase 1 — Audit

**Ziel:** Aktuellen Zustand erfassen, bevor irgendetwas geändert wird.

```
1. Checklist kopieren:
   portfolio-check-template.md → [projekt]/PORTFOLIO_CHECK.md

2. Checklist abarbeiten (nur lesen, nichts ändern)
   Jeden offenen Punkt in Kategorie einordnen:
   A = fehlt komplett
   B = vorhanden, aber unvollständig oder veraltet
   C = vorhanden, braucht nur kleine Anpassung

3. Gesamtbild festhalten:
   — Wie viele A / B / C?
   — Wieviel Aufwand ist das realistisch?
   — Neu aufsetzen (scaffolding) oder in-place bereinigen?
```

**Entscheidungsregel:**
→ Struktur stark abweichend oder viele A-Punkte → neu aufsetzen mit wgnd-scaffolding
→ Struktur grob stimmt, vor allem B/C → in-place bereinigen

---

## Phase 2 — Triage

**Ziel:** Reihenfolge festlegen. Nicht alles gleichzeitig angehen.

Feste Priorisierung — immer in dieser Reihenfolge:

| Schritt | Dimension | Warum zuerst |
| :--- | :--- | :--- |
| 1 | Story | Wenn die Story nicht klar ist, bringt der Rest nichts |
| 2 | Struktur | Scaffolding-Basis schaffen bevor Inhalt eingefüllt wird |
| 3 | Kohärenz | Erst wenn Struktur steht, synchronisieren |
| 4 | Artefakte | Erst wenn Notebooks sauber sind, exportieren |
| 5 | Reproduzierbarkeit | Letzter Schliff — Umgebung aufräumen |

---

## Phase 3 — Prep

**Ziel:** Alle Punkte aus Triage abarbeiten.

### 3a · Story
- README: Headline-Ergebnis formulieren (eine Zahl, ein Befund)
- README: Stack, Status-Badge, Key-Visual ergänzen
- `00_introduction.ipynb`: Projektziel, Phasen, wichtigste Ergebnisse einbauen
- Elevator Pitch in 3 Sätzen ausformulieren

### 3b · Struktur
- wgnd-scaffolding für fehlende Ordner und Files verwenden
- Notebooks nach Phase umbenennen wenn nötig (`00_`, `01_`, `02_`, ...)
- `ROADMAP.md` anlegen / aktualisieren
- `PROCESS_LOG.md` anlegen / aktualisieren

### 3c · Kohärenz
- Phasen-Namen gegen `docs/CONVENTIONS.md` prüfen und angleichen
- README und Introduction-Notebook synchronisieren
- ROADMAP: abgeschlossene Phasen markieren (`✅`)
- Alle Notebooks in Introduction referenzieren

### 3d · Artefakte
- Notebooks vollständig und sauber ausführen (von oben nach unten)
- HTML-Report exportieren: `jupyter nbconvert --to html`
- Key-Visual als PNG exportieren und in README einbinden
- Modell speichern (falls ML-Projekt): `models/[name].[format]`

### 3e · Reproduzierbarkeit
- `pyproject.toml` prüfen: alle Dependencies vorhanden?
- Absolute Pfade durch `PATHS`-Konfiguration ersetzen
- Debug-Zellen und auskommentierte Blöcke entfernen
- `.gitignore` prüfen: `data/raw/` ausgeschlossen?

---

## Phase 4 — QA

**Ziel:** Zweiter Checklist-Lauf. Alle Punkte müssen grün sein.

```
1. PORTFOLIO_CHECK.md erneut vollständig durchgehen
2. GitHub-Ansicht prüfen (wie sieht das Repo von außen aus?):
   — README lesbar und Key-Visual sichtbar?
   — Status klar erkennbar?
   — Beschreibung und Topics gesetzt?
3. README laut vorlesen — klingt es klar ohne Projekt-Kontext?
4. Optional: jemanden ohne Projekt-Kontext fragen:
   "Was macht dieses Projekt in einem Satz?"
```

---

## Phase 5 — Publish

**Ziel:** Projekt als portfolio-ready markieren und verlinken.

```
1. README Status updaten: "✅ Portfolio-ready"
2. docs/PROJECTS.md updaten: Status auf "✅ portfolio-ready"
3. PORTFOLIO_CHECK.md committen (bleibt im Repo als Nachweis)
4. GitHub Repository:
   — Description setzen (= Elevator Pitch aus README)
   — Topics setzen (z.B. data-science, python, portfolio)
5. Optional: LinkedIn / Portfolio-Seite aktualisieren
```

---

## Zeitschätzung

| Projekttyp | Aufwand |
| :--- | :--- |
| Gute Basis, vor allem Docs fehlen | 2–4h |
| Struktur vorhanden, viel Inhalt fehlt | 4–8h |
| Fast leer (z.B. Titanic-Skeleton) | Neu aufbauen oder aus Portfolio streichen |

---

*Standard → `case-standards.md`*
*Checklist → `portfolio-check-template.md`*
