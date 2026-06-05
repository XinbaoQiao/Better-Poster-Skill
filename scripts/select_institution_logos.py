#!/usr/bin/env python3
"""Select cached institution logo assets from affiliation text in source order."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

DEFAULT_RANKING_PATH = Path("data/csrankings_all_world_2016_2026_may2026_top100_institutions.json")
DEFAULT_LOGO_DIR = Path("assets/institutions/badgets/csrankings_all_world_2016_2026_may2026_top100")


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")


def load_ranking(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for index, item in enumerate(data.get("institutions", []), start=1):
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        rows.append(
            {
                "name": name,
                "rank": int(item.get("csrankings_rank") or index),
                "aliases": [str(alias).strip() for alias in item.get("aliases", []) if str(alias).strip()],
            }
        )
    return rows


def collect_text(args: argparse.Namespace) -> str:
    chunks = list(args.text or [])
    chunks.extend(args.institution or [])
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
        for candidate in [item["name"], *item["aliases"]]:
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
    selected_hits.sort(key=lambda hit: hit["start"])
    return [hit["item"] for hit in selected_hits]


def find_matches(text: str, ranking: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    selected = non_overlapping_name_hits(text, ranking)
    if limit <= 0:
        return selected
    return selected[:limit]


def logo_for_institution(item: dict[str, Any], logo_dir: Path) -> Path | None:
    slugs = [slugify(item["name"]), *(slugify(alias) for alias in item.get("aliases", []))]
    matches = []
    paths = logo_dir.iterdir() if logo_dir.exists() else []
    for path in paths:
        if not path.is_file():
            continue
        stem = re.sub(r"^\d+-", "", path.stem.lower())
        if stem in slugs:
            matches.append(path)
    if not matches:
        return None
    preferred = {".png": 0, ".jpg": 1, ".jpeg": 1, ".webp": 2, ".svg": 3}
    matches.sort(key=lambda path: preferred.get(path.suffix.lower(), 9))
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--institution", action="append", help="Institution or affiliation text. Can repeat.")
    parser.add_argument("--text", action="append", help="Free-form text to scan. Can repeat.")
    parser.add_argument("--source", action="append", help="Source file or directory to scan. Can repeat.")
    parser.add_argument("--ranking", type=Path, default=DEFAULT_RANKING_PATH)
    parser.add_argument("--logo-dir", type=Path, default=DEFAULT_LOGO_DIR)
    parser.add_argument("--max-institutions", type=int, default=0, help="Maximum matched institutions to return; 0 means all.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    selected = find_matches(collect_text(args), load_ranking(args.ranking), args.max_institutions)
    rows = []
    for item in selected:
        logo = logo_for_institution(item, args.logo_dir)
        rows.append(
            {
                "name": item["name"],
                "rank": item["rank"],
                "logo": str(logo) if logo else None,
                "note": "Convert SVG/WebP to PNG before pdflatex if needed." if logo and logo.suffix.lower() in {".svg", ".webp"} else "",
            }
        )

    if args.format == "json":
        print(json.dumps({"institutions": rows}, indent=2, ensure_ascii=False))
    else:
        if not rows:
            print("No configured institution logos matched.")
        for index, row in enumerate(rows, start=1):
            logo = row["logo"] or "missing cached logo"
            print(f"{index}. rank {row['rank']}: {row['name']} -> {logo}")
            if row["note"]:
                print(f"   {row['note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
