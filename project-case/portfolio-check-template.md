# Portfolio Checklist
### Quality-Check pro Projekt

**Anleitung:** Als `PORTFOLIO_CHECK.md` ins Projekt-Repo kopieren, ausfüllen.
Alle ⚠️-Items müssen ✅ sein bevor das Projekt als portfolio-ready gilt.

Persona-Tags: `[HR]` Recruiter · `[HM]` Hiring Manager · `[DS]` Data Scientist · `[TL]` Tech Lead · `[DA]` Data Analyst

---

## Projekt: _______________
**Datum Check:** _______________
**Typ:** DS / DA / DEV / SKL *(zutreffendes behalten)*
**Status vor Check:** _______________

---

## Dimension 1 — Story & Relevanz

- [ ] ⚠️ Problem in max. 2 Sätzen klar formuliert `[HR · HM]`
- [ ] ⚠️ Headline-Ergebnis vorhanden — eine Zahl, ein Befund, ein konkreter Output `[HR · HM]`
- [ ] ⚠️ Elevator Pitch: Problem + Ansatz + Ergebnis in 3 Sätzen `[HR]`
- [ ] Projekt-Typ explizit sichtbar (EDA / ML / Dashboard) `[HR · HM]`
- [ ] Persönliche Motivation / Warum dieses Thema? `[HR · HM]`
- [ ] "Welche Skills demonstriert dieses Projekt" — explizit in README `[HM]`
- [ ] Business-Relevanz: Für wen ist das nützlich — konkret `[HM · DA]`
- [ ] Wichtige Entscheidungen begründet (nicht nur WAS, sondern WARUM) `[DS · TL]`

**Notizen:**

---

## Dimension 2 — Struktur & Files

- [ ] ⚠️ `README.md` vorhanden und vollständig ausgefüllt `[HR · HM]`
- [ ] ⚠️ `ROADMAP.md` vorhanden mit aktuellem Phasen-Status `[HM]`
- [ ] ⚠️ `PROCESS_LOG.md` vorhanden und aktuell `[TL]`
- [ ] ⚠️ `pyproject.toml` oder `requirements.txt` vorhanden `[TL]`
- [ ] `BACKLOG.md` vorhanden `[TL]`
- [ ] Notebooks klar nach Phase benannt (`00_`, `01_`, `02_`, ...) `[HM]`
- [ ] `public/` Ordner vorhanden und nicht leer `[HR · HM]`
- [ ] `src/` Package vorhanden *(wenn applicable)* `[TL]`
- [ ] `.gitignore` korrekt — `data/raw/` ausgeschlossen `[TL]`
- [ ] Verzeichnisstruktur entspricht wgnd-scaffolding Standard `[TL]`

**Notizen:**

---

## Dimension 3 — Kohärenz

- [ ] ⚠️ README und `00_introduction.ipynb` erzählen dieselbe Geschichte `[HM]`
- [ ] ROADMAP und PROCESS_LOG sind synchron `[TL]`
- [ ] Phasen-Namen stimmen mit `docs/CONVENTIONS.md` überein `[TL]`
- [ ] Alle Notebooks in `00_introduction.ipynb` referenziert `[HM]`
- [ ] Headline-Ergebnis konsistent: README · Introduction · Reports `[HR · HM]`

**Notizen:**

---

## Dimension 4 — Analyse-Qualität

- [ ] ⚠️ Zentrale Analyse-Fragen explizit gestellt UND beantwortet `[HM · DA]`
- [ ] ⚠️ Findings strukturiert dokumentiert (Tabelle, IDs oder Insights-Report) `[HM · DA]`
- [ ] Kontraintuitive oder überraschende Findings explizit hervorgehoben `[HM · DA]`
- [ ] Business-Impact der Findings artikuliert (nicht nur "X > Y") `[HM · DA]`
- [ ] Visualisierungen haben Kontext (Beschriftung, Einheit, Quelle) `[DA]`
- [ ] Mindestens ein Findings-Report in `public/` exportiert `[HR · HM]`
- [ ] Visualisierungen haben Datenbasis (Tabelle oder Zahlennachweise) `[DA · DS]`

**Notizen:**

---

## Dimension 5 — ML-Qualität *(nur wenn ML-Projekt)*

- [ ] ⚠️ Baseline explizit definiert und begründet (warum diese Baseline?) `[DS · HM]`
- [ ] ⚠️ Modellwahl begründet — warum dieses Modell, nicht Alternativen? `[DS]`
- [ ] ⚠️ Leakage-Risiko dokumentiert — wo war es, wie wurde es verhindert? `[DS]`
- [ ] ⚠️ Train/Val/Test-Split-Strategie begründet (besonders bei Zeitreihendaten) `[DS]`
- [ ] Evaluation-Metriken mit Begründung gewählt (warum MAE und nicht RMSE?) `[DS · HM]`
- [ ] Error Analysis vorhanden: segmentiert nach Zeit / Gruppe / Subpopulation `[DS]`
- [ ] Bekannte Limitierungen explizit dokumentiert `[DS · HM]`
- [ ] "Was würde v2 anders machen?" dokumentiert `[HM · TL]`
- [ ] Modell gespeichert in `models/` (reproduzierbares Artefakt) `[TL]`

**Notizen:**

---

## Dimension 6 — Code & Architektur

- [ ] ⚠️ Keine hardcodierten absoluten Pfade — nur via `PATHS`-Konfiguration `[TL]`
- [ ] `src/` hat reale, importierbare Funktionen (nicht nur Scaffold-Dummy) `[TL]`
- [ ] Tests existieren und sind meaningful (keine 0%-Coverage auf produktivem Code) `[TL]`
- [ ] Keine auskommentierten Debug-Blöcke in `src/` `[TL]`
- [ ] Keine `test123`- oder `tmp`-Zellen in Notebooks `[TL]`
- [ ] Trade-offs dokumentiert: was wurde bewusst nicht gemacht und warum `[TL · HM]`
- [ ] Commit-History lesbar: saubere Messages, keine Massen-Commits `[TL · HM]`

**Notizen:**

---

## Dimension 7 — Artefakte & Präsentation

- [ ] ⚠️ Key-Visual in README — sichtbar VOR dem ersten Scroll `[HR]`
- [ ] ⚠️ Key-Visual zeigt ein echtes Ergebnis (kein Dummy-Plot) `[HR · HM]`
- [ ] ⚠️ Mindestens ein HTML-Report in `public/` (>50 KB, ausgeführt) `[HM · DA]`
- [ ] `00_introduction.ipynb` vollständig ausgeführt — kein leerer Output `[HM]`
- [ ] Alle Kern-Notebooks ausgeführt `[TL]`
- [ ] GitHub Repository hat Description und Topics gesetzt `[HR]`
- [ ] Live-Demo oder interaktives Element vorhanden *(optional, aber differenzierend)* `[HR · HM]`

**Notizen:**

---

## Dimension 8 — Reproduzierbarkeit

- [ ] ⚠️ README enthält Setup-Anleitung: clone → install → run `[TL · HM]`
- [ ] `pyproject.toml` / `requirements.txt` vollständig und getestet `[TL]`
- [ ] `data/raw/` nicht in Git `[TL]`
- [ ] Datenzugang dokumentiert — wie kommt man an die Originaldaten? `[TL · HM]`
- [ ] Python-Version festgelegt (`.python-version` oder in `pyproject.toml`) `[TL]`

**Notizen:**

---

## Persona-Check A — HR Recruiter (30 Sekunden)

*Simulation: GitHub-Seite öffnen, 30 Sekunden lesen, Entscheidung.*

- [ ] ⚠️ Sofort erkennbar: Was ist das Projekt? `[HR]`
- [ ] ⚠️ Sofort erkennbar: Welches Ergebnis wurde erreicht? `[HR]`
- [ ] ⚠️ Ein visuelles Element ist das erste was ich sehe `[HR]`
- [ ] Tech Stack ist ohne Code-Kenntnisse lesbar (Badges oder einfache Liste) `[HR]`
- [ ] Status des Projekts klar (abgeschlossen / in Arbeit) `[HR]`

**Fazit HR:** ⬜ Würde ich an Hiring Manager weiterleiten?

---

## Persona-Check B — Hiring Manager (5–10 Minuten)

*Simulation: README vollständig lesen + kurz ins Notebook schauen.*

- [ ] ⚠️ Ich verstehe was diese Person technisch kann `[HM]`
- [ ] ⚠️ Scope und Komplexität sind einschätzbar `[HM]`
- [ ] Motivation und persönlicher Bezug sichtbar `[HM]`
- [ ] AI-Workflow-Nutzung erkennbar *(falls relevant für Stelle)* `[HM]`
- [ ] Ich kann einschätzen ob das Ergebnis realistisch und solide ist `[HM]`

**Fazit HM:** ⬜ Würde ich zum Interview einladen?

---

## Persona-Check C — Data Scientist Interview

*Simulation: Code + Notebooks auf methodische Sauberkeit prüfen.*

- [ ] ⚠️ Leakage-Prävention nachvollziehbar `[DS]`
- [ ] ⚠️ Baseline und Modell-Ergebnis in Relation gesetzt `[DS]`
- [ ] ⚠️ Ich kann die Modellwahl fachlich verteidigen `[DS]`
- [ ] Error Analysis zeigt wo das Modell versagt `[DS]`
- [ ] Limitierungen reflektiert — zeigt Selbstwahrnehmung `[DS]`

**Fazit DS:** ⬜ Wäre ich als DS-Interviewer zufrieden?

---

## Persona-Check D — Tech Lead / Code Review

*Simulation: src/ und Tests kurz reviewen.*

- [ ] ⚠️ Code ist ohne tiefe Erklärung verständlich `[TL]`
- [ ] Ich würde diesen Code in einer Codebase akzeptieren `[TL]`
- [ ] Trade-offs sind sichtbar und nachvollziehbar `[TL]`

**Fazit TL:** ⬜ Code-Qualität vertretbar?

---

## Persona-Check E — Data Analyst

*Simulation: Findings und Visualisierungen prüfen.*

- [ ] ⚠️ Findings sind valide und belegt `[DA]`
- [ ] Visualisierungen sind klar beschriftet und selbsterklärend `[DA]`
- [ ] Business-Impact ist ohne Statistik-Kenntnisse verständlich `[DA]`

**Fazit DA:** ⬜ Würde ich die Findings präsentieren?

---

## Ergebnis

| Dimension | Pflicht-Items | Status | Offene Punkte |
| :--- | :--- | :--- | :--- |
| 1 · Story & Relevanz | 3 | ⬜ offen | |
| 2 · Struktur & Files | 4 | ⬜ offen | |
| 3 · Kohärenz | 1 | ⬜ offen | |
| 4 · Analyse-Qualität | 2 | ⬜ offen | |
| 5 · ML-Qualität | 4 | ⬜ offen | |
| 6 · Code & Architektur | 1 | ⬜ offen | |
| 7 · Artefakte | 3 | ⬜ offen | |
| 8 · Reproduzierbarkeit | 2 | ⬜ offen | |
| A · HR Recruiter | 3 | ⬜ offen | |
| B · Hiring Manager | 2 | ⬜ offen | |
| C · Data Scientist | 3 | ⬜ offen | |
| D · Tech Lead | 2 | ⬜ offen | |
| E · Data Analyst | 2 | ⬜ offen | |

**Portfolio-ready:** ⬜ Nein / ✅ Ja
**Offene Pflicht-Items gesamt:** ___ / 30
**Nächste Schritte:**

---

*Standard → `case-standards.md`*
*Workflow → `preparation-workflow.md`*
