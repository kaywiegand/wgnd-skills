#!/usr/bin/env python3
"""
Generate reveal.js HTML presentations from storyline JSON files.

Input:  public/json/storyline-*.json
Output: public/{overview,storyview,techview,socialview}.html

Generates Reveal.js-based HTML slides with CSS styling from template.
"""

import json
import re
import shutil
from pathlib import Path
from typing import Dict, List, Any

# Design-Templates leben neben diesem Script im Skill (nicht im Projekt) — projektübergreifend
# ein gemeinsames Design, siehe skills/project-case/build-pipeline.md.
SKILL_TEMPLATES = Path(__file__).parent.parent / "templates"


# Sentiment → CSS modifier maps (see public/css/slides.css)
_METRIC_SENTIMENT = {"positive": "good", "negative": "bad", "warning": "warn"}
_FACT_SENTIMENT = {"positive": "green", "negative": "red", "warning": "amber"}
_IMG_EXT_RE = re.compile(r"\.(png|jpe?g|svg|gif|webp|html)$", re.IGNORECASE)


def _img_src(source: str) -> str:
    """Normalize a chart source to an img/ path, appending .png when no extension.

    Relativ ohne '../' — die Views liegen in public/ neben public/img/ (wie css/).
    Funktioniert lokal (file://) und deployt (public/ als Site-Root)."""
    source = source.strip()
    if not _IMG_EXT_RE.search(source):
        source = f"{source}.png"
    return f"img/{source}"


def load_json(path: Path) -> Dict[str, Any]:
    """Load JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_slides_template(path: Path) -> str:
    """Load reveal.js template HTML."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def render_head(chapter_label: str | None, title: str, subtitle: str) -> str:
    """Kicker + h2 + subline, gemeinsam in .slide-head gewrappt.

    .slide-head reserviert per CSS die feste 170px-Kopfzone (Styleguide v2 §2) —
    Subline sitzt dadurch immer direkt unter dem Titel, unabhängig davon, wie
    lang/kurz der Titel ist. Ohne diesen Wrapper hing die Subline-Position am
    h2-min-height und driftete Richtung Content-Zone ab, statt am Titel zu kleben.
    """
    html = '<div class="slide-head">'
    if chapter_label:
        html += f'<span class="slide-kicker">{chapter_label}</span>'
    if title:
        html += f'<h2>{title}</h2>'
    if subtitle:
        html += f'<p class="subline">{subtitle}</p>'
    html += '</div>'
    return html


def render_content_item(item: Dict[str, Any]) -> str:
    """Render a single content item to styleguide-conformant HTML.

    Class vocabulary is the single source of truth in skills/project-case/templates/slides.css
    (copied into public/css/slides.css on every run) and shown in templates/styleguide.html.
    """
    item_type = item.get("type", "")

    if item_type == "figures":
        # KPI cards in a row → .metric-row > .metric
        html = '<div class="metric-row">'
        for fig in item.get("items", []):
            mod = _METRIC_SENTIMENT.get(fig.get("sentiment", ""), "")
            cls = f"metric {mod}".strip()
            html += f'<div class="{cls}">'
            html += f'<div class="val">{fig.get("value", "")}</div>'
            html += f'<div class="lbl">{fig.get("label", "")}</div>'
            html += '</div>'
        html += '</div>'
        return html

    elif item_type == "view_teaser":
        # Title-Slide-Teaser für die aktuelle View — automatisch aus hub.view_cards[view]
        # (siehe generate_json_from_slides.py), nicht von Hand gepflegt. Nur das Label als
        # Mini-Überschrift (kein Badge/Tag-Text — Kay-Feedback 2026-07-13: "die brauchen
        # wir nicht"), Description als Fließtext darunter.
        html = '<div class="view-teaser">'
        html += f'<div class="view-teaser-heading">{item.get("label", "")}</div>'
        html += f'<p class="view-teaser-desc">{item.get("description", "")}</p>'
        html += '</div>'
        return html

    elif item_type == "figures_with_context":
        # Fact box + explanatory text → .kv-list > .kv-row
        html = '<div class="kv-list">'
        for fig in item.get("items", []):
            mod = _FACT_SENTIMENT.get(fig.get("sentiment", ""), "")
            cls = f"kv-fact {mod}".strip()
            html += '<div class="kv-row">'
            html += f'<div class="{cls}"><div class="fv">{fig.get("value", "")}</div>'
            html += f'<div class="fl">{fig.get("label", "")}</div></div>'
            html += f'<div class="kv-text">{fig.get("context", "")}</div>'
            html += '</div>'
        html += '</div>'
        return html

    elif item_type == "contrasts":
        # Myth-busting: assumption (✗) → finding (✓), marks via CSS ::before.
        # Optionales `topic` pro Item gibt den Labels einen Kurztitel ("Annahme: Stadtzentrum"
        # statt nur "Annahme") — rückwärtskompatibel, ohne `topic` bleibt es beim generischen Label.
        html = '<div class="myth-rows">'
        for c in item.get("items", []):
            topic = c.get("topic", "")
            assume_label = f"Annahme: {topic}" if topic else "Annahme"
            finding_label = f"Befund: {topic}" if topic else "Befund"
            html += '<div class="myth-row-pair">'
            html += f'<div class="myth-assume"><span class="myth-label">{assume_label}</span><div class="myth-text">{c.get("assumption", "")}</div></div>'
            html += '<div class="myth-arrow">→</div>'
            html += f'<div class="myth-finding"><span class="myth-label">{finding_label}</span><div class="myth-text">{c.get("finding", "")}</div></div>'
            html += '</div>'
        html += '</div>'
        return html

    elif item_type == "statement":
        if item.get("layout") == "lead_copy":
            # E17 auch kombinierbar mit anderen Content-Typen auf derselben Slide (nicht nur im
            # reinen "alle Items sind statement"-Sonderfall in render_slide). Optionales
            # align: left (Kay-Feedback 2026-07-14) statt der zentrierten Standarddarstellung.
            align_cls = " text-lead-copy-left" if item.get("align") == "left" else ""
            html = f'<div class="text-lead-copy{align_cls}">'
            html += f'<p class="lead">{item.get("text", "")}</p>'
            html += f'<p class="copy">{item.get("copy", "")}</p>'
            html += '</div>'
            return html
        return f'<blockquote class="statement">{item.get("text", "")}</blockquote>'

    elif item_type == "steps":
        # Numbered process steps → .steps > .step (.sn badge/.sl/p), 3/4/5-spaltig
        items = item.get("items", [])
        html = f'<div class="steps" style="grid-template-columns: repeat({len(items)}, 1fr)">'
        for step in items:
            html += '<div class="step">'
            html += f'<div class="sn">{step.get("step", "")}</div>'
            html += f'<span class="sl">{step.get("label", "")}</span>'
            detail = step.get("detail", "")
            if detail:
                html += f'<p>{detail}</p>'
            html += '</div>'
        html += '</div>'
        return html

    elif item_type == "sequence":
        # Chain of reasoning → E8 Timeline: .timeline > .tl-item (.tl-num/h4/p), Verbindungslinie per CSS
        # sentiment steuert die Farbe des letzten/hervorgehobenen Schritts: "positive" → grün (climax,
        # bisheriges Standardverhalten), "negative"/"warning" → rot/amber. Ohne explizites sentiment
        # bekommt das letzte Element weiterhin automatisch "climax" (rückwärtskompatibel).
        items = item.get("items", [])
        html = '<div class="timeline">'
        for i, step in enumerate(items):
            sentiment = step.get("sentiment")
            if sentiment == "positive":
                cls = " climax"
            elif sentiment in ("negative", "warning"):
                cls = f" {sentiment}"
            elif i == len(items) - 1:
                cls = " climax"
            else:
                cls = ""
            html += f'<div class="tl-item{cls}">'
            html += f'<div class="tl-num">{i + 1}</div>'
            html += f'<div><h4>{step.get("label", "")}</h4><p>{step.get("text", "")}</p></div>'
            html += '</div>'
        html += '</div>'
        return html

    elif item_type == "rings":
        # E4 Rings — Donut-Ringe, nur für echte Anteile, spaltenweise verteilt
        items = item.get("items", [])
        html = f'<div class="rings" style="grid-template-columns: repeat({len(items)}, 1fr);">'
        for ring in items:
            pct = ring.get("percent", 0)
            html += '<div class="ring-wrap">'
            html += f'<div class="ring" style="background: conic-gradient(var(--accent) {pct}%, var(--card) 0);">'
            html += f'<div class="ring-inner">{ring.get("value", "")}</div></div>'
            html += f'<div class="l">{ring.get("label", "")}</div>'
            html += '</div>'
        html += '</div>'
        return html

    elif item_type == "ring_value":
        # E5 Ring + Value — Ring und Zahlen gleichwertig nebeneinander
        items = item.get("items", [])
        html = f'<div class="combo" style="grid-template-columns: repeat({len(items)}, 1fr);">'
        for entry in items:
            if entry.get("kind") == "ring":
                pct = entry.get("percent", 0)
                html += '<div class="ring-wrap">'
                html += f'<div class="ring" style="background: conic-gradient(var(--accent) {pct}%, var(--card) 0);">'
                html += f'<div class="ring-inner">{entry.get("value", "")}</div></div>'
                html += f'<div class="l">{entry.get("label", "")}</div>'
                html += '</div>'
            else:
                html += f'<div class="value-peer"><div class="v">{entry.get("value", "")}</div>'
                html += f'<div class="l">{entry.get("label", "")}</div></div>'
        html += '</div>'
        return html

    elif item_type == "box_grid":
        # E6 Box-Grid — neutrale Boxen (Linksrand) + hervorgehobene (voller Akzentrand).
        # Items können plain strings oder {text, highlight} sein (wie process_arrows).
        html = '<div class="box-grid">'
        for box in item.get("items", []):
            is_dict = isinstance(box, dict)
            text = box.get("text", "") if is_dict else box
            highlight = bool(box.get("highlight")) if is_dict else False
            cls = "box-item highlight" if highlight else "box-item"
            html += f'<div class="{cls}">{text}</div>'
        html += '</div>'
        return html

    elif item_type == "h_timeline":
        # E9 Horizontale Timeline — Meilenstein-Punkte auf einer Linie
        items = item.get("items", [])
        html = '<div class="h-timeline"><div class="ht-line-row">'
        for _ in items:
            html += '<div class="ht-dot-wrap"><div class="ht-dot"></div></div>'
        html += '</div><div class="ht-labels">'
        for entry in items:
            html += f'<div class="ht-label"><h4>{entry.get("label", "")}</h4><p>{entry.get("text", "")}</p></div>'
        html += '</div></div>'
        return html

    elif item_type == "funnel":
        # E10 Funnel — echte Verengung/Filterung in Stufen, Breite linear gestaffelt
        items = item.get("items", [])
        n = len(items)
        html = '<div class="funnel">'
        for i, step in enumerate(items):
            text = step.get("text", "") if isinstance(step, dict) else step
            width = step.get("width_pct") if isinstance(step, dict) else None
            if width is None:
                width = 100 if n <= 1 else round(100 - i * (54 / (n - 1)))
            html += f'<div class="fu-step" style="width: {width}%;">{text}</div>'
        html += '</div>'
        return html

    elif item_type == "process_arrows":
        # E11 Process Arrows — kompakt, ohne Erklärtext je Schritt. Items als dict mit
        # current:true heben den jeweils aktuellen Schritt hervor (z.B. wenn dieselbe
        # Pfeilkette auf mehreren Folgeslides wiederkehrt, je Slide anderer Schritt aktiv).
        html = '<div class="arrows">'
        for step in item.get("items", []):
            is_dict = isinstance(step, dict)
            text = step.get("text", "") if is_dict else step
            current = bool(step.get("current")) if is_dict else False
            cls = "arrow-chip current" if current else "arrow-chip"
            html += f'<div class="{cls}">{text}</div>'
        html += '</div>'
        return html

    elif item_type == "value_row":
        # E12 Value-Row — große Zahlen, spaltenweise, optional Zitat als Fließtext darunter
        items = item.get("items", [])
        html = f'<div class="value-row" style="grid-template-columns: repeat({len(items)}, 1fr);">'
        for val in items:
            html += '<div class="value-item">'
            html += f'<div class="v">{val.get("value", "")}</div>'
            html += f'<div class="l">{val.get("label", "")}</div>'
            detail = val.get("detail", "")
            if detail:
                html += f'<div class="d">{detail}</div>'
            html += '</div>'
        html += '</div>'
        quote = item.get("quote", "")
        if quote:
            html += f'<div class="extra-text" style="text-align: center;"><p class="quote">{quote}</p></div>'
        return html

    elif item_type == "fact_grid":
        # E13 Fact-Grid — dichtes Zahlen-Raster für Detail-/Anhang-Slides
        html = '<div class="fact-grid">'
        for fact in item.get("items", []):
            html += f'<div class="fact-cell"><div class="v">{fact.get("value", "")}</div>'
            html += f'<div class="l">{fact.get("label", "")}</div></div>'
        html += '</div>'
        return html

    elif item_type == "sections":
        # sections: label + points. layout steuert die Darstellung (per Slide wählbar):
        #   "columns" → N Spalten nebeneinander (optional numbered: 1/2/3 vor dem Label)
        #   "text"    → Prosa-Variante (Label + Punkte als Fließtext, zweispaltiger Flow)
        #   (default) → bisheriges 2-Spalten-Raster (Rückwärtskompatibilität)
        # Optionales `heading` (Gruppen-Überschrift über der ganzen Sections-Reihe, nicht pro
        # Karte) wrappt das Ergebnis in .sections-block, damit die 3em-Abstandskonvention
        # (siehe .text-lead-copy + .sections-block) greifen kann.
        items = item.get("items", [])
        layout = item.get("layout", "")
        numbered = item.get("numbered", False)
        heading = item.get("heading", "")

        if layout == "text":
            html = '<div class="sec-text">'
            for sec in items:
                html += '<div class="sec-text-block">'
                html += f'<span class="sec-text-label">{sec.get("label", "")}</span> '
                html += " ".join(sec.get("points", []))
                html += '</div>'
            html += '</div>'
        else:
            if layout == "columns":
                grid_style = f' style="grid-template-columns: repeat({len(items)}, 1fr)"'
            else:
                grid_style = ""
            html = f'<div class="pf-grid"{grid_style}>'
            for i, sec in enumerate(items, 1):
                num = f'<span class="pf-num">{i}</span>' if numbered else ""
                # Optionales highlight: true (Kay-Feedback 2026-07-14) hebt eine einzelne Card
                # mit sanftem Akzent-Hintergrund hervor, z.B. neue/wichtige Features.
                card_cls = "pf-card highlight" if sec.get("highlight") else "pf-card"
                html += f'<div class="{card_cls}"><div class="pf-title">{num}{sec.get("label", "")}</div><ul>'
                for point in sec.get("points", []):
                    html += f'<li>{point}</li>'
                html += '</ul></div>'
            html += '</div>'

        if heading:
            html = f'<div class="sections-block"><h4 class="content-heading">{heading}</h4>{html}</div>'
        return html

    elif item_type == "text_columns":
        # E14 Copy, 2-spaltig mit Headline — als eigenständiger Content-Typ (statt nur als
        # Spezialfall, wenn ALLE Content-Items der Slide "statement" sind) kombinierbar mit
        # anderen Blöcken auf derselben Slide (z.B. sections-Cards oben, Erklärtext darunter).
        html = '<div class="text-cols-head">'
        for col in item.get("items", []):
            html += f'<div><h4>{col.get("heading", "")}</h4><p>{col.get("text", "")}</p></div>'
        html += '</div>'
        return html

    elif item_type == "tools":
        # Feature/tool cards → .pf-grid, one column per tool (e.g. 3 → three columns)
        tools = item.get("items", [])
        html = f'<div class="pf-grid" style="grid-template-columns: repeat({len(tools)}, 1fr)">'
        for tool in tools:
            html += f'<div class="pf-card"><div class="pf-title">{tool.get("label", "")}</div><ul>'
            for line in str(tool.get("description", "")).split("\n"):
                if line.strip():
                    html += f'<li>{line.strip()}</li>'
            html += '</ul></div>'
        html += '</div>'
        return html

    elif item_type == "recommendations":
        # Recommendation cards → .reco-grid > .reco (.rn/strong/ul)
        html = '<div class="reco-grid">'
        for rec in item.get("items", []):
            html += '<div class="reco">'
            html += f'<div class="rn">{rec.get("category", "")}</div>'
            html += f'<strong>{rec.get("title", "")}</strong><ul>'
            for point in rec.get("points", []):
                html += f'<li>{point}</li>'
            html += '</ul></div>'
        html += '</div>'
        return html

    elif item_type == "scenarios":
        # Prediction scenarios → .kv-list (seconds fact + conditions/interpretation)
        html = '<div class="kv-list">'
        for sc in item.get("items", []):
            mod = _FACT_SENTIMENT.get(sc.get("sentiment", ""), "")
            cls = f"kv-fact {mod}".strip()
            secs = sc.get("prediction_seconds", "")
            html += '<div class="kv-row">'
            html += f'<div class="{cls}"><div class="fv">{secs} s</div>'
            html += '<div class="fl">Prognose</div></div>'
            # Titel (conditions) und Copy (interpretation) untereinander statt inline mit
            # "—" verkettet (Kay-Feedback 2026-07-14) — .kv-text-stack bricht bewusst aus dem
            # flex/align-items:center des äusseren .kv-text aus, damit die zwei Zeilen stapeln.
            text = f'<div class="kv-text-stack"><div class="kv-title">{sc.get("conditions", "")}</div>'
            interp = sc.get("interpretation")
            if interp:
                text += f'<div class="kv-copy">{interp}</div>'
            text += '</div>'
            html += f'<div class="kv-text">{text}</div>'
            html += '</div>'
        html += '</div>'
        return html

    elif item_type == "comparison_table":
        columns = item.get("columns", [])
        rows = item.get("rows", [])
        html = '<table><thead><tr>'
        for col in columns:
            html += f'<th>{col}</th>'
        html += '</tr></thead><tbody>'
        for row in rows:
            cls = ' class="hl-green"' if row.get("highlight") else ''
            html += f'<tr{cls}>'
            for cell in row.get("cells", []):
                html += f'<td>{cell}</td>'
            html += '</tr>'
        html += '</tbody></table>'
        return html

    elif item_type == "chart_refs":
        # One full-size image per slide → .chart-single (slides are split so each
        # chart_refs carries a single item; loop kept for safety)
        html = ""
        for chart in item.get("items", []):
            src = _img_src(chart.get("source", ""))
            label = chart.get("label", "")
            caption = chart.get("caption", "")
            html += '<div class="chart-single">'
            html += f'<a class="chart-tile" href="{src}" target="_blank"><img src="{src}" alt="{label}"></a>'
            if caption:
                html += f'<div class="caption">{caption}</div>'
            html += '</div>'
        return html

    elif item_type == "links":
        # Link grid → .links-grid > a.quick-link
        html = '<div class="links-grid">'
        primary = item.get("primary", "")
        if primary:
            html += f'<a class="quick-link" href="{primary}" target="_blank">GitHub-Repo</a>'
        for link in item.get("items", []):
            html += f'<a class="quick-link" href="{link.get("href", "")}">{link.get("label", "")}</a>'
        html += '</div>'
        return html

    elif item_type == "agenda":
        items = item.get("items", [])
        html = '<div class="agenda">'
        if item.get("grouped"):
            for group in items:
                html += f'<div class="agenda-item"><span class="label">{group.get("section", "")}</span></div>'
        else:
            for i, entry in enumerate(items):
                html += f'<div class="agenda-item"><span class="num">{i + 1}</span><span class="label">{entry}</span></div>'
        html += '</div>'
        return html

    else:
        # Fallback for unknown types
        return f'<p><em>Unknown content type: {item_type}</em></p>'


_SENTIMENT_KPI_CLASS = {"positive": "green", "negative": "red", "warning": "amber"}


def render_title_slide_content(content: List[Any]) -> str:
    """Render content items for a title slide using .kpi-row .kpi structure."""
    html = ""
    for item in content:
        if item.get("type") == "figures":
            html += '<div class="kpi-row">'
            for fig in item.get("items", []):
                sentiment = fig.get("sentiment", "neutral")
                css = _SENTIMENT_KPI_CLASS.get(sentiment, "")
                cls = f'kpi {css}' if css else 'kpi'
                html += f'<div class="{cls}">'
                html += f'<div class="v">{fig.get("value", "")}</div>'
                html += f'<div class="l">{fig.get("label", "")}</div>'
                html += '</div>'
            html += '</div>'
        else:
            html += render_content_item(item)
    return html


def render_closing_links(
    github: str,
    extra_links: List[Dict[str, str]] | None = None,
    primary_link: Dict[str, str] | None = None,
    stacked: bool = False,
) -> str:
    """Render the link row for the end-slide: Zur Übersicht + GitHub + projekt-spezifische Extras.

    extra_links kommen aus slides.yaml hub.quick_links (via meta.closing_links) — kein Hardcoding
    pro Projekt mehr. "Zur Übersicht" bleibt _self (interne Hub-Navigation), alles andere ist
    standardmässig _blank (externe/andere Seiten — sonst verliert man beim Klick den Reveal.js-
    Zustand der Präsentation), pro Link über `target` überschreibbar.
    primary_link (optional, z.B. Dashboard) rendert als eigener Link vor der Reihe, GLEICHER Stil
    wie alle anderen (Kay-Feedback 2026-07-14: nur Position ändert sich, nicht Größe/Look — die
    Hervorhebung kommt aus der Platzierung im Layout, nicht aus einer eigenen CSS-Klasse).
    stacked=True rendert die Reihe als Spalte (für zweispaltige Closing-Layouts, siehe
    render_slide role=="closing", layout: split).
    """
    links = [("Zur Übersicht", "index.html", "_self")]
    if github:
        links.append(("GitHub-Repo", f"https://github.com/{github}", "_blank"))
    for lk in (extra_links or []):
        links.append((lk.get("label", ""), lk.get("href", ""), lk.get("target", "_blank")))
    if primary_link:
        links.insert(0, (primary_link.get("label", ""), primary_link.get("href", ""),
                         primary_link.get("target", "_blank")))
    cls = "closing-links closing-links-col" if stacked else "closing-links"
    html = f'<div class="{cls}">'
    for label, href, target in links:
        html += f'<a href="{href}" class="c-link" target="{target}">{label}</a>'
    html += '</div>'
    return html


def render_slide(
    slide: Dict[str, Any],
    chapter_idx: int = 0,
    chapter_label: str | None = None,
    chapter_tick_label: str | None = None,
    github: str = "",
    is_last_chapter: bool = False,
    closing_links: List[Dict[str, str]] | None = None,
    is_chapter_start: bool = False,
) -> str:
    """Render a single slide as HTML."""
    role = slide.get("role", "standard")
    title = slide.get("title", "")
    subtitle = slide.get("subtitle", "")
    content = slide.get("content", [])
    # Optionales Slide-Feld `kicker` überschreibt den sonst automatisch gezeigten
    # Kapitel-Namen nur für diese eine Slide (z.B. Agenda-Slide im Kapitel "Einstieg",
    # die "Agenda" statt "Einstieg" als Kicker zeigen soll).
    effective_label = slide.get("kicker") or chapter_label

    data_ch = f' data-chapter="{chapter_idx}"'
    # data-chapter-label steuert NUR die Nav-Tick-Beschriftung (Fortschrittsleiste), nicht den
    # sichtbaren Kicker auf der Slide selbst (der lebt in render_head/effective_label).
    # Kay-Prinzip (2026-07-14): Titel und Ende haben FIXE Nav-Label, unabhängig vom Kapitel, in
    # dem ihre Slide-ID technisch steckt (z.B. steckt die Titel-Slide im Kapitel "Einstieg", zeigt
    # aber trotzdem "Titel"). Alle anderen Slides gehören zu einem Kapitel — dessen NAME erscheint
    # in der Nav nur an der ersten regulären (nicht title/closing/abbinder) Slide dieses Kapitels
    # (is_chapter_start, siehe render_chapter).
    if role == "title" and not is_last_chapter:
        nav_tick_label = "Titel"
    elif role in ("closing", "abbinder") or (role == "title" and is_last_chapter):
        nav_tick_label = "Ende"
    elif slide.get("kicker"):
        # Slide-eigener Kicker-Override (z.B. Agenda im Kapitel "Einstieg") bekommt automatisch
        # einen eigenen Nav-Tick, unabhängig davon ob diese Slide is_chapter_start ist — sie soll
        # nicht stillschweigend im Kapitel-Tick untergehen (Kay-Feedback 2026-07-14).
        nav_tick_label = slide.get("kicker")
    elif is_chapter_start and chapter_tick_label:
        nav_tick_label = chapter_tick_label
    else:
        nav_tick_label = None
    data_lbl = f' data-chapter-label="{nav_tick_label}"' if nav_tick_label else ""

    if role == "title" and slide.get("layout") == "L6":
        # L6-Experiment v2 (Kay-Feedback 2026-07-13: Titel/Subline zurück in die
        # normale Kopfzone, wie jede andere Slide — nur KPI-Row/Teaser/Start
        # bleiben zweispaltig in der Content-Zone).
        html = f'<section class="title-slide title-split" data-background="#3E4A5C"{data_ch}{data_lbl}>'
        if isinstance(subtitle, list):
            sub_text = "<br>".join(s for s in subtitle if s)
        else:
            sub_text = subtitle or ""
        html += render_head(None, title, sub_text)
        html += '<div class="content-zone"><div class="title-split-cols">'
        html += '<div class="title-split-left">'
        for item in content:
            if item.get("type") == "view_teaser":
                html += render_content_item(item)
        html += '<div class="closing-links title-cta"><span class="c-link" onclick="Reveal.next()">Start</span></div>'
        html += '</div>'
        html += '<div class="title-split-right">'
        for item in content:
            if item.get("type") == "figures":
                html += render_title_slide_content([item])
        html += '</div>'
        html += '</div></div>'
        html += '</section>'
    elif role == "title":
        # Gleiche Kopfzone/Content-Zone-Struktur wie jede andere Slide (Kay: "quasi ganz
        # gleich, nur farblich invertiert") — kein Sonderlayout mehr für Title-Slides.
        html = f'<section class="title-slide" data-background="#3E4A5C"{data_ch}{data_lbl}>'
        if isinstance(subtitle, list):
            sub_text = "<br>".join(s for s in subtitle if s)
        else:
            sub_text = subtitle or ""
        html += render_head(None, title, sub_text)
        html += '<div class="content-zone">'
        html += render_title_slide_content(content)
        # Link-Reihe nur auf der End-Slide (title-repeat). Opening-Titel trägt KEIN github mehr
        # — der GitHub-Link lebt auf dem Closing (CTA).
        if is_last_chapter:
            html += render_closing_links(github, closing_links, slide.get("closing_primary_link"))
        else:
            # Opening-Titel: Start-CTA — exakt derselbe Baustein wie Closing (.closing-links > .c-link)
            html += '<div class="closing-links title-cta"><span class="c-link" onclick="Reveal.next()">Start</span></div>'
        html += '</div>'
        html += '</section>'
    elif role == "closing":
        # Closing / CTA — dunkel, sonst gleiche Kopfzone/Content-Zone-Struktur wie überall.
        # subtitle kann eine Liste sein (title_from_hub, siehe generate_json_from_slides.py) —
        # gleiche <br>-Verkettung wie beim Opening-Titel.
        html = f'<section class="closing" data-background="#3E4A5C"{data_ch}{data_lbl}>'
        if isinstance(subtitle, list):
            sub_text = "<br>".join(s for s in subtitle if s)
        else:
            sub_text = subtitle or ""
        html += render_head(None, title, sub_text)
        # Optionales Slide-Feld `closing_extra_links` überschreibt die sonst aus
        # meta.closing_links (hub.quick_links oder linkedin, siehe generate_json_from_slides.py)
        # kommende Link-Liste NUR für diese eine Slide — für exakte Kontrolle ohne den
        # projektübergreifend geteilten linkedin/quick_links-Mechanismus anzufassen.
        slide_links = slide.get("closing_extra_links")
        links_to_use = slide_links if slide_links is not None else closing_links
        primary_link = slide.get("closing_primary_link")
        if slide.get("layout") == "split" and primary_link:
            # Zweispaltig (Kay-Feedback 2026-07-14): Text + hervorgehobener Primary-Link links
            # (2/3 Breite), die übrigen Links gestapelt rechts (1/3) — Primary-Link im selben
            # .c-link-Stil wie alle anderen, nur die Platzierung macht ihn prominent.
            html += '<div class="content-zone"><div class="closing-split">'
            html += '<div class="closing-split-left">'
            for item in content:
                html += render_content_item(item)
            p_target = primary_link.get("target", "_blank")
            html += (f'<div class="closing-links"><a href="{primary_link.get("href", "")}" class="c-link" '
                     f'target="{p_target}">{primary_link.get("label", "")}</a></div>')
            html += '</div>'
            html += '<div class="closing-split-right">'
            html += render_closing_links(github, links_to_use, stacked=True)
            html += '</div>'
            html += '</div></div>'
        else:
            html += '<div class="content-zone">'
            for item in content:
                html += render_content_item(item)
            html += render_closing_links(github, links_to_use, primary_link)
            html += '</div>'
        html += '</section>'
    elif len(content) == 1 and content[0].get("type") == "agenda" and slide.get("layout") == "L1":
        # Agenda-Variante L1 — Kopfzone mit Kicker/Titel/Subline wie jede Standard-Slide,
        # Liste vertikal UND horizontal zentriert in der Content-Zone (Kay-Entscheidung
        # 2026-07-13, nach Vergleich mit der L6-Variante).
        agenda = content[0]
        html = f'<section{data_ch}{data_lbl}>'
        html += render_head(effective_label, title, subtitle)
        html += '<div class="content-zone"><div class="agenda-list agenda-list-center">'
        for i, entry in enumerate(agenda.get("items", [])):
            if agenda.get("grouped"):
                html += f'<div class="ag-item"><span class="ag-num">{i + 1}</span><span class="ag-label">{entry.get("section", "")}</span></div>'
                for sub in entry.get("slides", []):
                    html += f'<div class="ag-sub">{sub}</div>'
            else:
                html += f'<div class="ag-item"><span class="ag-num">{i + 1}</span><span class="ag-label">{entry}</span></div>'
        html += '</div></div></section>'
    elif len(content) == 1 and content[0].get("type") == "agenda":
        # Table-of-contents slide → two columns: title block left, chapter list right.
        # layout: L6 (Versuch, zur Auswahl) ergänzt Kicker+Subline im Kopfblock — Default
        # bleibt bewusst ohne Kicker/Subline (Kay), nur der Titel.
        agenda = content[0]
        html = f'<section{data_ch}{data_lbl}>'
        html += '<div class="agenda-cols">'
        html += '<div class="agenda-head">'
        if slide.get("layout") == "L6" and effective_label:
            html += f'<span class="slide-kicker">{effective_label}</span>'
        if title:
            html += f'<h2>{title}</h2>'
        if slide.get("layout") == "L6" and subtitle:
            html += f'<p class="subline">{subtitle}</p>'
        html += '</div>'
        html += '<div class="agenda-list">'
        for i, entry in enumerate(agenda.get("items", [])):
            if agenda.get("grouped"):
                html += f'<div class="ag-item"><span class="ag-num">{i + 1}</span><span class="ag-label">{entry.get("section", "")}</span></div>'
                for sub in entry.get("slides", []):
                    html += f'<div class="ag-sub">{sub}</div>'
            else:
                html += f'<div class="ag-item"><span class="ag-num">{i + 1}</span><span class="ag-label">{entry}</span></div>'
        html += '</div></div></section>'
    elif [c.get("type") for c in content] == ["statement", "scenarios"]:
        # Title row on top, then two columns: text left, KPI/scenario boxes right
        html = f'<section{data_ch}{data_lbl}>'
        html += render_head(effective_label, title, subtitle)
        html += '<div class="content-zone"><div class="cols">'
        html += f'<div class="w45">{render_content_item(content[0])}</div>'
        html += f'<div class="w55">{render_content_item(content[1])}</div>'
        html += '</div></div></section>'
    elif content and all(c.get("type") == "statement" for c in content) and slide.get("layout") != "callout":
        # Reine Text-Slides: 1 Aussage → zentrierte Lead (medium), 2–5 → zweispaltig light (randlos)
        # layout: callout fällt bewusst durch in die generische else-Branch unten (jede
        # Aussage einzeln als gestapeltes, zentriertes blockquote.statement — L1, volle Breite).
        html = f'<section{data_ch}{data_lbl}>'
        html += render_head(effective_label, title, subtitle)
        html += '<div class="content-zone">'
        if len(content) == 1 and content[0].get("layout") == "lead_copy":
            # E17: große These oben, erklärender Absatz darunter, zentriert als ein Block
            html += '<div class="text-lead-copy">'
            html += f'<p class="lead">{content[0].get("text", "")}</p>'
            html += f'<p class="copy">{content[0].get("copy", "")}</p>'
            html += '</div>'
        elif len(content) == 1:
            # E15: ein Gedanke, zentriert, max. 3 Zeilen
            html += f'<div class="statement-lead">{content[0].get("text", "")}</div>'
        elif any(c.get("heading") for c in content):
            # E14: Copy 2-spaltig mit Headline je Spalte, Gap 72px
            html += '<div class="text-cols-head">'
            for c in content:
                html += f'<div><h4>{c.get("heading", "")}</h4><p>{c.get("text", "")}</p></div>'
            html += '</div>'
        elif content[0].get("layout") == "stack":
            # E16: normaler Fließtext, Absätze untereinander
            html += '<div class="text-stack">'
            for c in content:
                html += f'<p>{c.get("text", "")}</p>'
            html += '</div>'
        else:
            # Default (bestehend): 2-5 Aussagen zweispaltig light, randlos
            html += '<div class="statement-cols">'
            for c in content:
                html += f'<p class="statement-col">{c.get("text", "")}</p>'
            html += '</div>'
        html += '</div>'
        html += '</section>'
    elif (content and content[0].get("type") == "chart_refs"
          and content[0].get("layout") == "image_right"):
        # Kopfzone bleibt STANDARD (fix 170px, volle Breite) — nur die Content-Zone splittet
        # sich in Beschreibung/Statement links + Bild rechts (Kay-Feedback 2026-07-14:
        # "Titelzone bleibt unangetastet, es geht um die Content-Zone").
        chart = content[0].get("items", [{}])[0]
        src = _img_src(chart.get("source", ""))
        html = f'<section{data_ch}{data_lbl}>'
        html += render_head(effective_label, title, subtitle)
        html += '<div class="content-zone"><div class="chart-cols">'
        html += '<div class="chart-cols-head">'
        if chart.get("caption"):
            html += f'<p class="chart-cols-caption">{chart.get("caption")}</p>'
        for extra_item in content[1:]:
            html += render_content_item(extra_item)
        html += '</div>'
        html += f'<div class="chart-cols-img"><a href="{src}" target="_blank"><img src="{src}" alt="{chart.get("label", "")}"></a></div>'
        html += '</div></div></section>'
    elif (content and content[0].get("type") == "chart_refs"
          and content[0].get("layout") == "image_left"):
        # Bild 2/3 links (so gross wie möglich, keine max-width/height-Deckelung), Text 1/3
        # rechts — Kopfzone bleibt STANDARD, gleiches Prinzip wie image_right oben, nur
        # Bild/Text-Reihenfolge und -Gewichtung gespiegelt (2:1 statt 40:60).
        chart = content[0].get("items", [{}])[0]
        src = _img_src(chart.get("source", ""))
        html = f'<section{data_ch}{data_lbl}>'
        html += render_head(effective_label, title, subtitle)
        html += '<div class="content-zone"><div class="chart-cols chart-cols-reverse">'
        html += f'<div class="chart-cols-img chart-cols-img-large"><a href="{src}" target="_blank"><img src="{src}" alt="{chart.get("label", "")}"></a></div>'
        html += '<div class="chart-cols-head">'
        if chart.get("caption"):
            html += f'<p class="chart-cols-caption">{chart.get("caption")}</p>'
        for extra_item in content[1:]:
            html += render_content_item(extra_item)
        html += '</div>'
        html += '</div></div></section>'
    else:
        html = f'<section{data_ch}{data_lbl}>'
        html += render_head(effective_label, title, subtitle)
        # Elemente schrumpfen auf ihren Inhalt und zentrieren sich als Gruppe vertikal
        # in der Inhaltszone (Styleguide v2 Prinzip 3) — .content-zone übernimmt das per CSS.
        html += '<div class="content-zone">'
        for item in content:
            html += render_content_item(item)
        html += '</div>'
        html += '</section>'

    return html


def render_chapter(chapter: Dict[str, Any], chapter_idx: int = 0, github: str = "", is_last: bool = False,
                   closing_links: List[Dict[str, str]] | None = None) -> str:
    """Render a chapter as flat reveal.js sections (1D, no nesting)."""
    nav_label = chapter.get("nav_label", "")
    # nav_tick_label: kürzere Variante nur für den Nav-Tick, fällt auf nav_label zurück wenn nicht
    # gesetzt (siehe generate_json_from_slides.py, Feld nav_tick_by_view).
    nav_tick_label = chapter.get("nav_tick_label", nav_label)
    slides = chapter.get("slides", [])

    # Kapitel-Start für die Nav ist die erste REGULÄRE Slide (kein title/closing/abbinder) —
    # Titel/Ende bekommen ihr fixes Nav-Label unabhängig davon direkt in render_slide (siehe dort).
    # Ohne diese Ausnahme würde z.B. im Kapitel "Einstieg" die Titel-Slide (immer erste Slide dort)
    # fälschlich als Kapitel-Start markiert, statt "Die These" (Kay-Feedback 2026-07-14).
    first_standard_idx = next(
        (j for j, s in enumerate(slides) if s.get("role") not in ("title", "closing", "abbinder")),
        None,
    )

    html = f'<!-- Chapter: {nav_label} -->\n'
    for j, slide in enumerate(slides):
        html += render_slide(slide, chapter_idx=chapter_idx, chapter_label=nav_label,
                             chapter_tick_label=nav_tick_label, github=github,
                             is_last_chapter=is_last, closing_links=closing_links,
                             is_chapter_start=(j == first_standard_idx))
    return html


def build_html(json_data: Dict[str, Any], template: str, css_version: str = "1") -> str:
    """Build complete HTML presentation from JSON."""
    meta = json_data.get("meta", {})
    chapters = json_data.get("chapters", [])

    github = meta.get("github", "")
    closing_links = meta.get("closing_links", [])
    total = len(chapters)
    # Render all chapters (flat, 1D — no chapter nesting)
    slides_html = ""
    for i, chapter in enumerate(chapters):
        slides_html += render_chapter(chapter, chapter_idx=i, github=github,
                                      is_last=(i == total - 1), closing_links=closing_links)

    # Replace placeholder in template
    html = template.replace("<!-- SLIDES_PLACEHOLDER -->", slides_html)

    # Update meta information in HTML
    html = html.replace("{{ PROJECT_TITLE }}", meta.get("project", "Project"))
    html = html.replace("{{ PRESENTATION_TITLE }}", meta.get("presentation_title", ""))
    html = html.replace("{{ AUDIENCE }}", meta.get("audience", ""))
    html = html.replace("{{ DURATION }}", str(meta.get("duration_minutes", "")))
    html = html.replace("{{ AUTHOR }}", meta.get("author", ""))
    html = html.replace("{{ GITHUB }}", meta.get("github", ""))
    html = html.replace("{{ CSS_VERSION }}", css_version)

    return html


def save_html(path: Path, content: str) -> None:
    """Save HTML to file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Wrote: {path}")


def main():
    """Main execution."""
    base_path = Path.cwd()  # invoked from the project root, matches skill calling convention
    json_dir = base_path / "public" / "json"
    output_dir = base_path / "public"
    template_path = SKILL_TEMPLATES / "slides-template.html"

    print("Loading template...")
    if template_path.exists():
        template = load_slides_template(template_path)
        print(f"✅ Loaded template: {template_path}")
    else:
        print(f"⚠️  Template not found: {template_path}")
        print("Using fallback template (basic reveal.js)")
        template = get_fallback_template()

    # slides.css ist projektübergreifend einheitlich und lebt kanonisch im Skill —
    # bei jedem Lauf frisch in dieses Projekt kopieren, nie im Projekt von Hand pflegen.
    canonical_css = SKILL_TEMPLATES / "slides.css"
    css_path = output_dir / "css" / "slides.css"
    if canonical_css.exists():
        css_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(canonical_css, css_path)
        print(f"✅ Kopiert: {canonical_css} → {css_path}")
    else:
        print(f"⚠️  Kanonische slides.css nicht gefunden: {canonical_css}")

    # Cache-buster for the linked stylesheet: changes whenever slides.css changes
    css_version = str(int(css_path.stat().st_mtime)) if css_path.exists() else "1"

    # Views are whatever storyline JSONs exist for this project — not hardcoded,
    # so the same script works across projects with different view compositions.
    views = sorted(p.stem.removeprefix("storyline-") for p in json_dir.glob("storyline-*.json"))

    for view in views:
        json_path = json_dir / f"storyline-{view}.json"
        html_path = output_dir / f"{view}.html"

        print(f"\n📊 Generating {view}...")

        if not json_path.exists():
            print(f"  ⚠️  JSON file not found: {json_path}, skipping")
            continue

        # Load JSON
        json_data = load_json(json_path)
        print(f"  → Loaded JSON: {json_path}")

        # Build HTML
        html_content = build_html(json_data, template, css_version)
        print(f"  → Built HTML presentation")

        # Save
        save_html(html_path, html_content)

    print("\n" + "="*60)
    print("✅ HTML generation complete!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Open generated HTML files in browser")
    print("  2. Compare with html-backup/ visually")
    print("  3. Run: python scripts/convert_json_to_md.py")


def get_fallback_template() -> str:
    """Return a minimal reveal.js template."""
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ PROJECT_TITLE }} — {{ PRESENTATION_TITLE }}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/theme/black.min.css">
    <style>
        .reveal h1, .reveal h2, .reveal h3 { text-transform: none; }
        .figures { display: flex; gap: 1em; flex-wrap: wrap; }
        .figure { text-align: center; }
        .figure.positive { color: #27ae60; }
        .figure.negative { color: #e74c3c; }
        .figure.warning { color: #f39c12; }
        .value { font-size: 2em; font-weight: bold; }
        .label { font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="reveal">
        <div class="slides">
            <!-- SLIDES_PLACEHOLDER -->
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/reveal.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/4.5.0/plugin/notes/notes.min.js"></script>
    <script>
        Reveal.initialize({
            hash: true,
            center: true,
            transition: 'slide',
            plugins: [RevealNotes]
        });
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
