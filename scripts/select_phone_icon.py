#!/usr/bin/env python3
"""Select one scan-row QR/scan icon for Better Poster templates."""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path


SCAN_ICON_MANIFEST = "scan-icon-manifest.txt"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_manifest_stems(icons_dir: Path) -> list[str] | None:
    manifest = icons_dir / SCAN_ICON_MANIFEST
    if not manifest.exists():
        return None
    stems = []
    for raw in manifest.read_text(encoding="utf-8").splitlines():
        stem = raw.split("#", 1)[0].strip()
        if not stem:
            continue
        if (icons_dir / f"{stem}.svg").exists() and (icons_dir / f"{stem}.png").exists():
            stems.append(stem)
    return stems


def discover_icon_stems(icons_dir: Path) -> list[str]:
    manifest_stems = read_manifest_stems(icons_dir)
    if manifest_stems is not None:
        return manifest_stems

    stems = []
    for svg in sorted(icons_dir.glob("*-white.svg")):
        png = svg.with_suffix(".png")
        if png.exists():
            stems.append(svg.stem)
    return stems


def choose_icon(stems: list[str], seed: str | None) -> str:
    if not stems:
        raise ValueError("No paired QR/scan SVG and PNG icons were found.")
    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    return rng.choice(stems)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--icons-dir", default="assets/scan-icons", help="Directory containing paired QR/scan SVG and PNG icons.")
    parser.add_argument("--prefix", default="../assets/scan-icons", help="Path prefix to print for template files.")
    parser.add_argument("--format", choices=("both", "latex", "html", "name"), default="both", help="Output format.")
    parser.add_argument("--seed", help="Optional seed for reproducible selection.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    icons_dir = Path(args.icons_dir)
    if not icons_dir.is_absolute():
        icons_dir = repo_root() / icons_dir

    try:
        stem = choose_icon(discover_icon_stems(icons_dir), args.seed)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    prefix = args.prefix.rstrip("/")
    latex_path = f"{prefix}/{stem}.png"
    html_path = f"{prefix}/{stem}.svg"

    if args.format == "latex":
        print(latex_path)
    elif args.format == "html":
        print(html_path)
    elif args.format == "name":
        print(stem)
    else:
        print(f"latex={latex_path}")
        print(f"html={html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
