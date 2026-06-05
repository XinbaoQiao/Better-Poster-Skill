#!/usr/bin/env python3
"""Select an institution-aware poster palette from affiliation text.

The script is intentionally conservative: it only resolves institutions present
in the configured CSRankings list, then applies explicit palette mappings when
available. Unknown institutions fall back to a strong blue/orange palette.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_RANKING_PATH = Path("data/csrankings_all_world_2016_2026_may2026_top100_institutions.json")
DEFAULT_PALETTE_PATH = Path("data/institution_palettes.json")


def rgb_to_hex(rgb: list[int]) -> str:
    return "#" + "".join(f"{max(0, min(255, int(channel))):02x}" for channel in rgb[:3])


def color_name(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "", text.lower())
    return slug or "institution"


def load_ranking(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for index, item in enumerate(data.get("institutions", []), start=1):
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        rank = int(item.get("csrankings_rank") or index)
        aliases = [str(alias).strip() for alias in item.get("aliases", []) if str(alias).strip()]
        rows.append({"name": name, "rank": rank, "aliases": aliases})
    return rows


def collect_text(args: argparse.Namespace) -> str:
    chunks = list(args.text or [])
    for institution in args.institution or []:
        chunks.append(institution)
    for source in args.source or []:
        path = Path(source)
        if path.is_dir():
            for pattern in ("*.tex", "*.md", "*.txt", "*.html", "*.bbl"):
                for file in path.rglob(pattern):
                    chunks.append(file.read_text(encoding="utf-8", errors="ignore"))
        elif path.exists():
            chunks.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(chunks)


def non_overlapping_name_hits(text: str, ranking: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lowered = text.lower()
    candidates: list[dict[str, Any]] = []
    for item in ranking:
        names = [item["name"], *item["aliases"]]
        for candidate in names:
            candidate_low = candidate.lower()
            if not candidate_low:
                continue
            for match in re.finditer(r"\b" + re.escape(candidate_low) + r"\b", lowered):
                candidates.append(
                    {
                        "item": item,
                        "start": match.start(),
                        "end": match.end(),
                        "length": match.end() - match.start(),
                    }
                )

    candidates.sort(key=lambda hit: (-hit["length"], hit["item"]["rank"], hit["start"]))
    selected_hits: list[dict[str, Any]] = []
    occupied: list[tuple[int, int]] = []
    seen: set[str] = set()
    for hit in candidates:
        name = hit["item"]["name"]
        if name in seen:
            continue
        if any(hit["start"] < end and start < hit["end"] for start, end in occupied):
            continue
        selected_hits.append(hit)
        occupied.append((hit["start"], hit["end"]))
        seen.add(name)
    return [hit["item"] for hit in selected_hits]


def find_institutions(text: str, ranking: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    selected = sorted(non_overlapping_name_hits(text, ranking), key=lambda row: row["rank"])
    if limit <= 0:
        return selected
    return selected[:limit]


def palette_for(name: str, palettes: dict[str, Any]) -> dict[str, Any]:
    institutions = palettes.get("institutions", {})
    if name in institutions:
        return institutions[name]
    for inst_name, palette in institutions.items():
        aliases = [str(alias).lower() for alias in palette.get("aliases", [])]
        if name.lower() in aliases or inst_name.lower() == name.lower():
            return palette
    return palettes.get("default", {"primary": [0, 82, 155], "secondary": [239, 124, 0]})


def select_palette(selected: list[dict[str, Any]], palettes: dict[str, Any]) -> dict[str, Any]:
    default = palettes.get("default", {"primary": [0, 82, 155], "secondary": [239, 124, 0]})
    if not selected:
        primary = default["primary"]
        secondary = default["secondary"]
    elif len(selected) == 1:
        one = palette_for(selected[0]["name"], palettes)
        primary = one.get("primary", default["primary"])
        secondary = one.get("secondary", primary)
    else:
        first = palette_for(selected[0]["name"], palettes)
        second = palette_for(selected[1]["name"], palettes)
        primary = first.get("primary", default["primary"])
        secondary = second.get("secondary", second.get("primary", default["secondary"]))
    return {
        "institutions": [{"name": item["name"], "rank": item["rank"]} for item in selected],
        "primary": primary,
        "secondary": secondary,
        "primary_hex": rgb_to_hex(primary),
        "secondary_hex": rgb_to_hex(secondary),
    }


def latex_lines(selection: dict[str, Any]) -> str:
    primary = selection["primary"]
    secondary = selection["secondary"]
    return "\n".join(
        [
            f"\\definecolor{{institutionprimary}}{{RGB}}{{{primary[0]},{primary[1]},{primary[2]}}}",
            f"\\definecolor{{institutionsecondary}}{{RGB}}{{{secondary[0]},{secondary[1]},{secondary[2]}}}",
            "\\institutionpalette{institutionprimary}{institutionsecondary}",
            "\\renewcommand{\\maincolumnbackgroundcolor}{institutionprimary}",
        ]
    )


def css_lines(selection: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"--institution-primary:{selection['primary_hex']};",
            f"--institution-secondary:{selection['secondary_hex']};",
            "--main:var(--institution-primary);",
            "--accent:var(--institution-primary);",
            "--title:var(--institution-primary);",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Select a poster color palette from institution text.")
    parser.add_argument("--institution", action="append", help="Institution or affiliation text. Can repeat.")
    parser.add_argument("--text", action="append", help="Free-form text to scan. Can repeat.")
    parser.add_argument("--source", action="append", help="Source file or directory to scan. Can repeat.")
    parser.add_argument("--ranking", type=Path, default=DEFAULT_RANKING_PATH)
    parser.add_argument("--palettes", type=Path, default=DEFAULT_PALETTE_PATH)
    parser.add_argument("--max-institutions", type=int, default=0, help="Maximum matched institutions to return; 0 means all.")
    parser.add_argument("--format", choices=("json", "latex", "css", "all"), default="all")
    args = parser.parse_args()

    ranking = load_ranking(args.ranking)
    palettes = json.loads(args.palettes.read_text(encoding="utf-8"))
    text = collect_text(args)
    selected = find_institutions(text, ranking, args.max_institutions)
    selection = select_palette(selected, palettes)

    if args.format == "json":
        print(json.dumps(selection, ensure_ascii=False, indent=2))
    elif args.format == "latex":
        print(latex_lines(selection))
    elif args.format == "css":
        print(css_lines(selection))
    else:
        print("Institutions:")
        for item in selection["institutions"]:
            print(f"- rank {item['rank']}: {item['name']}")
        print("\nLaTeX:")
        print(latex_lines(selection))
        print("\nCSS:")
        print(css_lines(selection))
        print("\nJSON:")
        print(json.dumps(selection, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
