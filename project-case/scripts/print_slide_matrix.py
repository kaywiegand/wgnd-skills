#!/usr/bin/env python3
"""
Print/write the slide-registry audit matrix: id | chapter | content | per-view membership.

Input:  public/md/slides.yaml
Output: public/md/slides-matrix.md + console table

Reads the registry directly (not the generated JSONs) — the registry is the source of
truth, so this is the mechanism that lets Kay verify at a glance which slide is shown
in which view, without opening 3 HTML files and comparing by hand.

Run: uv run python scripts/print_slide_matrix.py
"""

import re
from pathlib import Path

import yaml

BASE = Path.cwd()
SLIDES_PATH = BASE / "public" / "md" / "slides.yaml"
PORTFOLIO_PATH = BASE / "public" / "md" / "portfolio.md"
OUT_PATH = BASE / "public" / "md" / "slides-matrix.md"

VIEWS = ["storyview", "techview", "overview"]

_CONTENT_LABELS = {
    "figures": "KPIs",
    "figures_with_context": "KPIs+Kontext",
    "steps": "Schritte",
    "chart_refs": "Chart",
    "contrasts": "Annahme/Befund",
    "sequence": "Beweiskette",
    "statement": "Statement",
    "comparison_table": "Vergleichstabelle",
    "scenarios": "Szenarien",
    "recommendations": "Empfehlungen",
    "sections": "Abschnitte",
    "tools": "Tool-Karten",
    "agenda": "Agenda",
    "links": "Links",
}


def content_summary(content: list) -> str:
    parts = []
    for item in content:
        label = _CONTENT_LABELS.get(item.get("type", "?"), item.get("type", "?"))
        parts.append(label)
    return " + ".join(parts) if parts else "—"


def load_registry(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"❌ {path} nicht gefunden.")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_project_name(path: Path) -> str:
    """Read 'name' from the '## Project'-Block in portfolio.md (same pattern as
    generate_index_from_portfolio.py) so the matrix title matches the actual project."""
    if not path.exists():
        return "Portfolio Project"
    m = re.search(r"## Project\s*```(.*?)```", path.read_text(encoding="utf-8"), re.DOTALL)
    if not m:
        return "Portfolio Project"
    for line in m.group(1).strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            if key.strip() == "name":
                return val.strip()
    return "Portfolio Project"


def chapter_label_for_row(chapter: dict, views_present: set) -> str:
    """Show the actual per-view nav_label — flags it when views disagree on the chapter name,
    which is exactly the kind of drift this matrix exists to catch."""
    overrides = chapter.get("nav_label_by_view", {})
    labels = {v: overrides.get(v, chapter["nav_label"]) for v in views_present}
    distinct = set(labels.values())
    if len(distinct) == 1:
        return distinct.pop()
    return " / ".join(f"{label} ({view})" for view, label in sorted(labels.items()))


def build_rows(registry: dict) -> list[dict]:
    rows = []
    for chapter in registry["chapters"]:
        for slide in chapter["slides"]:
            views_present = set(slide["views"])
            rows.append(
                {
                    "id": slide["id"],
                    "chapter": chapter_label_for_row(chapter, views_present),
                    "content": content_summary(slide.get("content", [])),
                    "views": views_present,
                }
            )
    return rows


def render_markdown(rows: list[dict], project_name: str) -> str:
    lines = [
        f"# Slide-Matrix — {project_name}",
        "",
        "Automatisch generiert aus `public/md/slides.yaml` via `scripts/print_slide_matrix.py`. "
        "Nicht von Hand editieren — bei jeder Registry-Änderung neu ausführen.",
        "",
        "| id | Kapitel | Inhalt | StoryView | TechView | Overview |",
        "|:---|:---|:---|:---:|:---:|:---:|",
    ]
    for row in rows:
        marks = ["✅" if v in row["views"] else "" for v in VIEWS]
        lines.append(
            f"| `{row['id']}` | {row['chapter']} | {row['content']} | {marks[0]} | {marks[1]} | {marks[2]} |"
        )

    n_shared = sum(1 for r in rows if len(r["views"]) > 1)
    lines += [
        "",
        f"**{len(rows)} Slide-Einträge total · {n_shared} davon in mehr als 1 View wiederverwendet.**",
    ]
    return "\n".join(lines)


def main() -> None:
    registry = load_registry(SLIDES_PATH)
    rows = build_rows(registry)
    project_name = load_project_name(PORTFOLIO_PATH)
    markdown = render_markdown(rows, project_name)

    print(markdown)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(markdown + "\n")
    print(f"\n✅ Wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
