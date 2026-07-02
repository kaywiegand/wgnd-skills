---
description: Neues Projekt im Workspace initialisieren. Legt Ordner, Standard-MD-Files und git-Repo an, trägt das Projekt in PROJECTS.md ein. Aufruf: /project-init [name] [typ]
---

Du initialisierst ein neues Projekt im aktuellen Workspace.

**Pfad-Konvention (gilt für die ganze Skill):**
- `WORKSPACE_ROOT` = das Wurzelverzeichnis des Workspace, in dem diese Skill läuft (enthält `CLAUDE.md`, `docs/`, `skills/`). Ermittle es aus dem aktuellen Arbeitskontext — nicht hart annehmen.
- `SCAFFOLDING_ROOT` = `{WORKSPACE_ROOT}/wgnd-scaffolding`, sofern dort vorhanden. Existiert der Pfad nicht, frage nach dem korrekten Ort statt zu raten.

**Aufruf:** `/project-init [name] [typ]`
- `name` — Repo-Name (kebab-case, z.B. `kaywiegand-website`)
- `typ` — optional: `web` · `data` · `tool` · `general` (Default: `general`)

Lies `$ARGUMENTS`. Wenn kein Name vorhanden: frage nach Name und Typ bevor du anfängst.

---

## Schritt 1 — Input klären

Parse `$ARGUMENTS`:
- Erstes Wort = Projektname
- Zweites Wort = Typ (optional, Default: `general`)

Wenn kein Name: frage kurz nach:
```
Projektname (kebab-case)?
Typ? web / data / tool / general (Enter = general)
Kurze Beschreibung (1 Satz, für PROJECTS.md)?
```

Wenn Name vorhanden aber keine Beschreibung: kurz nachfragen.

**Wenn Typ = `data`:** zusätzlich fragen: "DAN (Data Analytics) oder DSC (Data Science)?" — Default `DAN` falls unklar.

Setze intern:
- `PROJECT_NAME` = der angegebene Name
- `PROJECT_TYPE` = der angegebene Typ (oder `general`)
- `PROJECT_PATH` = `{WORKSPACE_ROOT}/[PROJECT_NAME]`
- `TODAY` = heutiges Datum (YYYY-MM-DD)

---

## Schritt 2 — Prüfen ob Ordner bereits existiert

```bash
ls {WORKSPACE_ROOT}/[PROJECT_NAME]
```

Wenn Ordner existiert: stoppe und frage Kay ob er überschreiben will. Nie blind überschreiben.

---

## Schritt 3 — Weg wählen

**Wenn `PROJECT_TYPE` = `data`:** Dieses Projekt ist Data Analytics/Data Science — `wgnd-scaffolding` deckt das vollständig und passender ab als die generischen Templates hier (Notebooks, `src/`-Struktur, Data-Ordner, BACKLOG.md, Git-Init — alles bereits im Generator). Führe aus:

```bash
python3 {SCAFFOLDING_ROOT}/generator.py --slug [PROJECT_NAME] --type [DAN|DSC] --path {WORKSPACE_ROOT} --name "[Lesbarer Name]"
```

Der Generator übernimmt Ordner, alle Docs, `.gitignore`, Notebooks/`src/`, sowie `git init` + Erstcommit selbstständig. **Weiter direkt mit Schritt 7** — Schritt 4–6 und 8 entfallen für diesen Pfad.

**Sonst (`web` · `tool` · `general`):** weiter mit Schritt 4 — dieser Pfad bleibt unverändert und vollständig, wie er ist.

---

## Schritt 4 — Ordner + git anlegen

*(nur web/tool/general — beim Data-Pfad macht das der Generator)*

```bash
mkdir {WORKSPACE_ROOT}/[PROJECT_NAME]
cd {WORKSPACE_ROOT}/[PROJECT_NAME]
git init
```

---

## Schritt 5 — MD-Files schreiben

*(nur web/tool/general)*

Schreibe alle fünf Files nacheinander mit dem Write-Tool.

### CLAUDE.md

```md
# CLAUDE.md — [PROJECT_NAME]

> Projektspezifische Anweisungen für Claude Code.
> Ergänzt die globale CLAUDE.md aus dem Workspace-Root.

---

## Projekt

| Feld | Inhalt |
| :--- | :--- |
| Slug | `[PROJECT_NAME]` |
| Typ | [PROJECT_TYPE] |
| Stack | — |
| Status | 🟢 aktiv |

---

## Session-Einstieg

1. PROCESS_LOG.md lesen — aktueller Stand und letzte Session
2. ROADMAP.md lesen — offene Phasen
3. Globale CLAUDE.md aus dem Workspace-Root gilt weiterhin
```

### README.md

```md
# [PROJECT_NAME]

> [BESCHREIBUNG]

---

## Überblick

[Was ist dieses Projekt? Für wen? Warum?]

## Stack

[Tech-Stack eintragen sobald bekannt]

## Setup

[Setup-Anweisungen eintragen sobald bekannt]
```

### ROADMAP.md

```md
# ROADMAP — [PROJECT_NAME]

> Ausgangslage → Phasen → Ziel

---

## Ausgangslage

[Was ist der Startpunkt? Was existiert bereits?]

---

## Phasen

- [ ] Phase 1 — Setup & Struktur
- [ ] Phase 2 — [nächste Phase]

---

## Ziel

[Was ist der fertige Zustand? Was soll dieses Projekt leisten?]
```

### BACKLOG.md

```md
# BACKLOG.md — [PROJECT_NAME]

Projektspezifische offene Tasks und Todos.
Nie mitten in einer Session den Kontext wechseln — hier notieren, gesammelt abarbeiten.

Prio: `1` = hoch · `2` = mittel · `3` = niedrig

---

| # | Beschreibung | Prio | Entdeckt in |
| :--- | :--- | :--- | :--- |
```

### PROCESS_LOG.md

```md
# PROCESS_LOG.md — [PROJECT_NAME]

Verlauf + Entscheidungen. Pointer auf Files — kein Inhalt kopieren.
Metriken, Findings, Outputs gehören in Notebooks/Code — nicht hier.

---

## [TODAY] — Projekt-Setup

- Projekt initialisiert via `/project-init`
- MD-Files angelegt: CLAUDE.md · README.md · ROADMAP.md · BACKLOG.md · PROCESS_LOG.md
- Nächster Schritt: Stack und Ziel in CLAUDE.md + ROADMAP.md konkretisieren
```

---

## Schritt 6 — .gitignore anlegen

*(nur web/tool/general)*

Schreibe eine minimale `.gitignore`:

```
.DS_Store
*.env
.env.*
node_modules/
```

---

## Schritt 7 — PROJECTS.md aktualisieren

*(beide Pfade — Data-Projekte kommen hier wieder rein)*

```bash
[ -f "{WORKSPACE_ROOT}/docs/PROJECTS.md" ] && echo "vorhanden" || echo "fehlt — Schritt überspringen"
```

Existiert die Datei nicht (z.B. auf einem anderen Rechner ohne diese Konvention): Schritt überspringen, nicht anlegen, nicht fehlschlagen.

Existiert sie: Lies `{WORKSPACE_ROOT}/docs/PROJECTS.md` und füge unter `## Aktiv` eine neue Zeile ein:

```
| `[PROJECT_NAME]` | [PROJECT_TYPE] | 1 — Setup | 🟢 aktiv | — | → PROCESS_LOG |
```

---

## Schritt 8 — Initialer Commit

*(nur web/tool/general — beim Data-Pfad hat der Generator das schon erledigt)*

```bash
cd {WORKSPACE_ROOT}/[PROJECT_NAME]
git add .
git commit -m "chore: init project scaffold"
```

---

## Schritt 9 — Abschluss-Report

Gib eine knappe Zusammenfassung:

```
✅ Projekt [PROJECT_NAME] initialisiert

Pfad:    {WORKSPACE_ROOT}/[PROJECT_NAME]
Typ:     [PROJECT_TYPE]
Weg:     [wgnd-scaffolding (Data) | generische Templates (web/tool/general)]
Git:     initialisiert + erster Commit

Nächste Schritte:
→ Stack in CLAUDE.md eintragen
→ Phasen in ROADMAP.md konkretisieren
→ Mit der Arbeit starten
```

---

## Regeln

- Nie einen bestehenden Ordner überschreiben — immer nachfragen
- Keine Dateien löschen ohne Erlaubnis
- Bei Unsicherheit über Name oder Typ: erst fragen, dann anlegen
- PROJECTS.md nur ergänzen, nie bestehende Einträge ändern — und nur wenn die Datei existiert
