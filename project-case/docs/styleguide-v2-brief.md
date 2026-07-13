# Auftrag: Slide-System aus STYLEGUIDE.html in den echten Generator übernehmen

## Kontext

Ich habe mit Claude (claude.ai) ein neues Design-System für meine Reveal.js-Präsentationen entworfen — ein 12-Spalten-Raster, 7 benannte Layouts (L1–L7) und 17 benannte Elemente (E1–E17), alles visuell durchgespielt und abgenommen. Das Ergebnis liegt als eigenständige Referenzdatei vor: **`STYLEGUIDE.html`** (im Anhang). Sie ist NUR eine visuelle Demo mit eigenem, vereinfachtem CSS — sie ersetzt NICHT meine echte `slides.css`, sondern ist die Vorlage, aus der du die echten Klassen ableitest.

Zusätzlich liegen vor:
- `slides.css` — die echte, aktuell produktive Theme-Datei (Kommentar oben: "TO CHANGE THEME: edit only the :root variables")
- `overview.html`, `techview.html`, `storyview.html` — die drei echten Reveal-Decks, die die Klassen aus `slides.css` nutzen
- `generate_html_from_json.py` — der Generator, der aus JSON-Input die Slide-HTML baut
- ggf. Beispiel-JSON-Dateien eines Projekts

## Wichtig: Klassennamen reichen sich NICHT 1:1 durch

`STYLEGUIDE.html` nutzt eigene Demo-Klassennamen (`.pf-card`, `.kpi`, `.box-item`, `.rings`, `.timeline`, `.h-timeline`, `.funnel`, `.arrows`, `.value-row`, `.fact-grid15` usw.). Einige davon entsprechen bereits real existierenden Klassen in `slides.css` (z. B. E1 KPI-Reihe ≈ `.kpi-row`/`.kpi`, E7 Steps ≈ `.steps`/`.step`). Andere sind komplett neu und existieren in der echten `slides.css` noch nicht (Rings, Box-Grid mit Akzent-Rand, Timeline mit Verbindungslinie, horizontale Timeline, Funnel, Process-Arrows, Value-Row, Fact-Grid, die reinen Text-Layouts E14–E17).

**Deine erste Aufgabe:** Gleiche die Klassenlisten ab (echte `slides.css` vs. `STYLEGUIDE.html`) und entscheide pro Element, ob es (a) eine bestehende Klasse erweitert, (b) umbenannt werden muss, damit es zur bestehenden Namenskonvention passt, oder (c) komplett neu ist.

## Das Raster (gilt für alle Layouts/Elemente)

- Canvas 1024×720px (unverändert, aus der bestehenden Reveal-Konfiguration)
- Rand 56px oben/seitlich, 40px unten
- Kopfzone fix 170px — Eyebrow/Titel/Subline sitzen immer hier, unabhängig vom Inhalt darunter
- 12 Spalten, Gutter 20–32px je nach Layout
- Feine Trennlinie zwischen Kopfzone und Inhaltszone (liegt auf der Kopfzone selbst, beginnt exakt am linken Textrand)
- Elemente schrumpfen standardmäßig auf ihren Inhalt und zentrieren sich als Gruppe vertikal in der Inhaltszone — Ausnahme: E1 KPI-Reihe darf volle Höhe nutzen
- Eine Akzentfarbe aktiv pro Slide

Alle Werte, Farben, Abstände und Typografie-Regeln stehen in `STYLEGUIDE.html` Sektion 1–5 (Prinzipien, Raster, Typografie, Abstände, Farbe) — dort steht auch das Farb-Prinzip: nur zwei Variablen (`--card`, `--card-border`) bestimmen die ganze Palette (Beige/Blau/Grün austauschbar ohne neues CSS).

## Layouts (L1–L7) — Aufteilung der Inhaltszone

| Name | Aufteilung | Verwendung |
|---|---|---|
| L1 Volle Fläche | span 12 | Diagramme, Einzeltabellen, ein Element ohne Unterteilung |
| L2 Zweispaltig | 6+6, Gap 32px | Vergleich, zwei parallele Argumente |
| L3 Dreispaltig | 4+4+4, Gap 28px | Karten-Trios |
| L4 Vierspaltig | 3+3+3+3, Gap 24px | Standard für KPI-Reihe |
| L5 Fünfspaltig | Flex-Sonderfall (12 nicht durch 5 teilbar) | 5-Schritt-Prozesse |
| L6 Schmal+Breit | 4+8, Gap 24px | Grafik/Steps links, Copy oder Diagramm rechts über volle Höhe |
| L7 Breit+Schmal | 8+4, Gap 24px | Hauptinhalt links, Zusatzinfo/Zahl rechts |

## Elemente (E1–E17) — Bausteine für die Inhaltszone

| Name | Beschreibung | Layout |
|---|---|---|
| E1 KPI-Reihe | volle Höhe, max. 4 Werte | L4 |
| E2 Karten, gleiche Höhe | schrumpft auf Inhalt, zentriert als Gruppe | L2/L3 |
| E3 Karten, natürliche Höhe | wächst individuell, oben bündig | L3 |
| E4 Rings | Donut-Ringe, nur für echte Anteile, spaltenweise verteilt (2/3/4-spaltig) | L1/L3 |
| E5 Ring + Value | Ring und Zahlen gleichwertig nebeneinander, spaltenweise verteilt | L1 |
| E6 Box-Grid | 3 neutrale Boxen (Linksrand) + 1 hervorgehoben (voller Akzentrand) | L1/L6 |
| E7 Steps | Prozessschritte, linksbündig, dünne Trennlinie vor jedem Schritt, spaltenweise (3/4/5) | L3/L4/L5 |
| E8 Timeline | vertikal, mit Verbindungslinie (läuft oben/unten leicht über die Punkte hinaus), kompakte Variante ideal für L6 links | L1/L6 |
| E9 Horizontale Timeline | Meilenstein-Punkte auf einer Linie, für Roadmap/Phasen | L1 |
| E10 Funnel | echte Verengung/Filterung in Stufen | L1 |
| E11 Process Arrows | kompakt, ohne Erklärtext je Schritt | L1/L4 |
| E12 Value-Row | große Zahlen, spaltenweise verteilt, optional Zitat als Fließtext darunter (keine Box) | L1 |
| E13 Fact-Grid | dichtes Zahlen-Raster für Detail-/Anhang-Slides | L1 |
| E14 Copy, 2-spaltig mit Headline | reiner Fließtext, kein Diagramm, Gap 72px | L1 |
| E15 Statement, prominent | ein großer, zentrierter Gedanke, max. 3 Zeilen | L1 |
| E16 Copy, zwei Absätze | normaler Fließtext untereinander, 2–4 Zeilen je Absatz | L1 |
| E17 Statement + Copy gemischt | große These oben, erklärender Absatz darunter, zentriert als ein Block | L1 |

Jedes Element (außer E1) verträgt zusätzlich: Subline in der Kopfzone (Kontext davor) und/oder 1–3 Absätze Zusatztext danach (40px Abstand, untereinander oder mehrspaltig).

## Was ich von dir brauche

1. **Abgleich** der Klassennamen zwischen `STYLEGUIDE.html` und der echten `slides.css` (siehe oben) — Ergebnis kurz zusammenfassen, bevor du loslegst.
2. **`slides.css` erweitern**: neue Komponentenklassen für alle Elemente ergänzen, die noch fehlen, in der bestehenden Namenskonvention und unter Nutzung der bestehenden `:root`-Variablen (Farbe, Radius etc. aus `STYLEGUIDE.html` übernehmen, aber an die echten Variablennamen anpassen).
3. **`generate_html_from_json.py` erweitern**: neue Content-Typen für die Layouts und Elemente registrieren, damit sie aus JSON heraus erzeugt werden können.
4. **Testlauf**: mindestens 2–3 Slides in `overview.html` (oder einer Kopie) probeweise auf die neuen Layouts/Elemente umstellen, regenerieren, im Browser prüfen.
5. **`styleguide.html`** (die echte, produktive Referenzdatei) aktualisieren, damit sie die neuen Bausteine zeigt statt Lorem-Ipsum-Platzhaltern.

Frag nach, wenn die Feldstruktur im JSON für ein neues Element unklar ist, statt zu raten — insbesondere bei Fünfspaltig (Sonderfall) und der Ring+Value-Kombination, da die genaue Datenstruktur (wie viele Werte, welche Reihenfolge) Auswirkungen auf die Spaltenverteilung hat.
