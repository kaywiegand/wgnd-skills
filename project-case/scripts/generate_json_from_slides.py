#!/usr/bin/env python3
"""
Generate storyline JSON files from the slide registry.

Input:  public/md/slides.yaml       (single source of truth for slide structure/content)
Output: public/json/storyline-{view}.json — one file per view in view_composition

Purely mechanical: filters chapters/slides by view membership and orders them per
view_composition. No parsing, no content decisions — those are made once, by hand,
in slides.yaml.

Run: uv run python scripts/generate_json_from_slides.py
"""

import json
from pathlib import Path

import yaml

BASE = Path.cwd()  # invoked from the project root, matches skill calling convention
SLIDES_PATH = BASE / "public" / "md" / "slides.yaml"
JSON_OUTPUT_DIR = BASE / "public" / "json"


def load_registry(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"❌ {path} nicht gefunden.")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_view_json(registry: dict, view: str, chapter_ids: list[str]) -> dict:
    chapters_by_id = {ch["id"]: ch for ch in registry["chapters"]}
    hub = registry.get("hub", {})
    meta = dict(registry.get("view_meta", {}).get(view, {}))
    chapters_out = []

    for idx, chapter_id in enumerate(chapter_ids):
        if chapter_id not in chapters_by_id:
            raise SystemExit(f"❌ view_composition['{view}'] referenziert unbekanntes Kapitel: {chapter_id}")
        chapter = chapters_by_id[chapter_id]

        slides_for_view = [s for s in chapter["slides"] if view in s["views"]]
        if not slides_for_view:
            continue  # Kapitel existiert, hat aber keine Slides für diese View

        nav_label = chapter.get("nav_label_by_view", {}).get(view, chapter["nav_label"])
        # nav_tick_label: optionale KÜRZERE Variante nur für den Nav-Tick unten (Platzmangel in
        # der Leiste bei langen Kapitelnamen) — der sichtbare Kicker auf der Slide und das
        # Inhaltsverzeichnis nutzen weiterhin nav_label (voller Name). Fällt auf nav_label
        # zurück, wenn kein nav_tick_by_view gesetzt ist (Kay-Entscheidung 2026-07-14: nur für
        # "Exploration / EDA" genutzt, kein generelles Kürzungssystem).
        nav_tick_label = chapter.get("nav_tick_by_view", {}).get(view, nav_label)

        rendered_slides = []
        for slide in slides_for_view:
            rendered = {k: v for k, v in slide.items() if k not in ("id", "views")}
            # Opening-Titel (erstes Kapitel, role:title): Titel/Subline und der
            # View-Teaser kommen automatisch aus dem hub-Block statt pro View von Hand
            # gepflegt zu werden — sonst driftet der Wortlaut zwischen Hub und
            # Titel-Slide auseinander (Kay-Feedback 2026-07-12: "immer ähnlicher aber
            # anderer Text wirkt verwirrend"). Betrifft NUR die Opening-Titel-Slide
            # (erstes Kapitel), nicht die Ende-Titel-Wiederholung.
            if idx == 0 and rendered.get("role") == "title" and hub:
                rendered["title"] = meta.get("project", rendered.get("title", ""))
                period = meta.get("period", "")
                subtitle_line2 = f'{hub.get("subtitle", "")} | {period}' if period else hub.get("subtitle", "")
                rendered["subtitle"] = [hub.get("tagline", ""), subtitle_line2]
                view_card = hub.get("view_cards", {}).get(view)
                if view_card:
                    content = list(rendered.get("content", []))
                    content.append({
                        "type": "view_teaser",
                        "label": view_card.get("label", ""),
                        "description": view_card.get("description", ""),
                    })
                    rendered["content"] = content
            # Closing mit title_from_hub: true (Opt-in, siehe slides.yaml) — NUR Titel/
            # Subline kommen wie beim Opening aus dem hub-Block (identischer Wortlaut,
            # kein Drift). Der Content-Text bleibt eigenständig von Hand gepflegt — anders
            # als der Opening-Titel hat der Closing eigene Absätze (Kay-Feedback
            # 2026-07-13: Subline = wie Title-Slide, Content-Text = eigener Wortlaut).
            if rendered.get("role") == "closing" and rendered.get("title_from_hub") and hub:
                rendered["title"] = meta.get("project", rendered.get("title", ""))
                period = meta.get("period", "")
                subtitle_line2 = f'{hub.get("subtitle", "")} | {period}' if period else hub.get("subtitle", "")
                rendered["subtitle"] = [hub.get("tagline", ""), subtitle_line2]
            rendered_slides.append(rendered)

        chapters_out.append({"nav_label": nav_label, "nav_tick_label": nav_tick_label, "slides": rendered_slides})

    # Closing-Links (kein Hardcoding im Renderer): LinkedIn wenn gesetzt, sonst hub.quick_links.
    # Übersicht + GitHub werden im Renderer davor gesetzt.
    linkedin = meta.get("linkedin", "")
    if linkedin:
        meta["closing_links"] = [{"label": "LinkedIn-Profil", "href": linkedin}]
    else:
        meta["closing_links"] = registry.get("hub", {}).get("quick_links", [])
    return {"meta": meta, "chapters": chapters_out}


def save_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Wrote: {path}")


def main() -> None:
    registry = load_registry(SLIDES_PATH)
    print(f"📖 Read {SLIDES_PATH} ({len(registry['chapters'])} chapters)")

    JSON_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    view_composition = registry.get("view_composition", {})
    if not view_composition:
        raise SystemExit("❌ 'view_composition' fehlt in slides.yaml.")

    for view, chapter_ids in view_composition.items():
        print(f"\n📝 Processing {view}...")
        json_data = build_view_json(registry, view, chapter_ids)
        n_slides = sum(len(ch["slides"]) for ch in json_data["chapters"])
        print(f"  → {len(json_data['chapters'])} Kapitel, {n_slides} Slides")
        save_json(JSON_OUTPUT_DIR / f"storyline-{view}.json", json_data)

    print("\n" + "=" * 60)
    print("✅ JSON generation complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. python scripts/generate_html_from_json.py")
    print("  2. python scripts/print_slide_matrix.py  (Konsistenz-Check)")


if __name__ == "__main__":
    main()
