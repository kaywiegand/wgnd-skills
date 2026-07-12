#!/usr/bin/env python3
"""
Generate public/index.html (Portfolio-Hub) from portfolio.md + slides.yaml + index-template.html.

Input:   public/md/portfolio.md   (Project-Block: name, slug, period, dashboard)
         public/md/slides.yaml    (hub: headline_kpis_from, view_order, view_cards)
         skills/project-case/templates/index-template.html  (Layout, {{...}}-Platzhalter — im Skill, nicht im Projekt)
Output:  public/index.html

Dynamische Werte aus portfolio.md + slides.yaml; Layout/Design aus dem Template.
Die Hero-KPIs und View-Karten werden aus slides.yaml gerendert statt im Template
hartcodiert zu sein — sonst driftet der Hub-Inhalt unbemerkt von den Slides weg
(gefunden 2026-07-01: identische KPIs standen doppelt in Template und slides.yaml).

Run:     python scripts/generate_index_from_portfolio.py
"""

import re
import sys
from pathlib import Path

import yaml

BASE          = Path.cwd()  # invoked from the project root, matches skill calling convention
MD_PATH       = BASE / "public" / "md" / "portfolio.md"
SLIDES_PATH   = BASE / "public" / "md" / "slides.yaml"
# Layout lebt im Skill (projektübergreifend einheitlicher Hub), nicht im Projekt.
TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "index-template.html"
OUT_PATH      = BASE / "public" / "index.html"

GITHUB_USER   = "kaywiegand"   # Workspace-Owner (stabil)

_SENTIMENT_CLASS = {"positive": "positive", "negative": "negative", "warning": "warning"}


def parse_project(md_text: str) -> dict:
    """Read the fenced code block under '## Project' into a dict."""
    m = re.search(r"## Project\s*```(.*?)```", md_text, re.DOTALL)
    if not m:
        raise SystemExit("❌ '## Project'-Block in portfolio.md nicht gefunden.")
    result = {}
    for line in m.group(1).strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip()
    return result


def find_slide(registry: dict, slide_id: str) -> dict:
    for chapter in registry["chapters"]:
        for slide in chapter["slides"]:
            if slide["id"] == slide_id:
                return slide
    raise SystemExit(f"❌ hub.headline_kpis_from='{slide_id}' — keine Slide mit dieser ID gefunden.")


def render_headline_kpis(registry: dict) -> str:
    hub = registry["hub"]
    slide = find_slide(registry, hub["headline_kpis_from"])
    figures = next(c for c in slide["content"] if c["type"] == "figures")["items"]

    html = ""
    for fig in figures:
        cls = "kpi " + _SENTIMENT_CLASS.get(fig.get("sentiment", ""), "")
        html += f'      <div class="{cls.strip()}">\n'
        html += f'        <div class="v">{fig["value"]}</div>\n'
        html += f'        <div class="l">{fig["label"]}</div>\n'
        html += '      </div>\n'
    return html


def render_view_cards(registry: dict) -> str:
    hub = registry["hub"]
    view_meta = registry.get("view_meta", {})

    html = ""
    for view in hub["view_order"]:
        card = hub["view_cards"][view]
        duration = view_meta.get(view, {}).get("duration_minutes", "")
        html += f'      <a href="{view}.html" class="view-card {view}">\n'
        html += f'        <div class="view-label">{card["kicker"]}</div>\n'
        html += f'        <h3>{card["label"]}</h3>\n'
        html += f'        <p class="view-desc">{card["description"]}</p>\n'
        html += '        <div class="view-meta">\n'
        html += f'          <span class="view-time">⏱️ {duration} Min</span>\n'
        html += f'          <span class="view-badge {card["badge_class"]}">{card["badge"]}</span>\n'
        html += '        </div>\n'
        html += '      </a>\n'
    return html


def render_about(hub: dict) -> str:
    """Render die 'Das Projekt'-Absätze aus hub.about (Liste von {label, text}) als
    2-spaltiges Grid — fette Zwischenüberschrift ohne Doppelpunkt, Zeilenumbruch, Text."""
    html = '    <div class="about-grid">\n'
    for para in hub.get("about", []):
        label = para.get("label", "")
        text = para.get("text", "")
        strong = f"<strong>{label}</strong><br>" if label else ""
        html += f'      <div class="about-item">{strong}{text}</div>\n'
    html += '    </div>\n'
    return html


def render_quick_links(hub: dict, repo_url: str) -> str:
    """GitHub-Repo immer zuerst, danach projektspezifische hub.quick_links ({href, label})."""
    links = [{"href": repo_url, "label": hub.get("repo_link_label", "GitHub-Repo")}]
    links += hub.get("quick_links", [])
    html = ""
    for link in links:
        html += f'        <a href="{link["href"]}" class="quick-link" target="_blank">{link["label"]}</a>\n'
    return html


def main() -> None:
    if not MD_PATH.exists():
        raise SystemExit(f"❌ {MD_PATH} nicht gefunden.")
    if not SLIDES_PATH.exists():
        raise SystemExit(f"❌ {SLIDES_PATH} nicht gefunden.")
    if not TEMPLATE_PATH.exists():
        raise SystemExit(f"❌ {TEMPLATE_PATH} nicht gefunden.")

    project = parse_project(MD_PATH.read_text(encoding="utf-8"))
    registry = yaml.safe_load(SLIDES_PATH.read_text(encoding="utf-8"))

    name   = project.get("name", "Portfolio Project")
    slug   = project.get("slug", "")
    period = project.get("period", "")
    dash   = project.get("dashboard", "").strip()

    repo_url = f"https://github.com/{GITHUB_USER}/{slug}" if slug else f"https://github.com/{GITHUB_USER}"
    user_url = f"https://github.com/{GITHUB_USER}"

    hub = registry.get("hub", {})

    replacements = {
        "{{PROJECT_NAME}}":    name,
        "{{PERIOD}}":          period,
        "{{TAGLINE}}":         hub.get("tagline", ""),
        "{{SUBTITLE}}":        hub.get("subtitle", ""),
        "{{FOOTER_TAGLINE}}":  hub.get("footer_tagline", hub.get("tagline", "")),
        "{{ABOUT}}":           render_about(hub),
        "{{QUICK_LINKS}}":     render_quick_links(hub, repo_url),
        "{{GITHUB_REPO_URL}}": repo_url,
        "{{GITHUB_USER_URL}}": user_url,
        "{{DASHBOARD_URL}}":   dash or repo_url,   # Fallback: Repo, falls kein Dashboard
        "{{HEADLINE_KPIS}}":   render_headline_kpis(registry),
        "{{VIEW_CARDS}}":      render_view_cards(registry),
    }

    html = TEMPLATE_PATH.read_text(encoding="utf-8")
    for key, val in replacements.items():
        html = html.replace(key, val)

    leftover = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if leftover:
        print(f"⚠️  Unersetzte Platzhalter: {sorted(set(leftover))}", file=sys.stderr)

    OUT_PATH.write_text(html, encoding="utf-8")
    print(f"✅ Wrote: {OUT_PATH}")
    print(f"   name={name} · period={period} · dashboard={dash or '(Fallback: Repo)'}")


if __name__ == "__main__":
    main()
