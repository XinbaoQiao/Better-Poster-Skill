#!/usr/bin/env python3
"""Cache institution badge images from the configured top-100 institution list.

Each badge combines a downloaded institution mark with the institution name, so
poster templates can show both school symbol and school text in one image.
Generated badges are review-required assets because university marks are often
copyrighted or trademarked.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import sys
import urllib.request
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROXY_ENV_KEYS = (
    "http_proxy",
    "https_proxy",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "all_proxy",
    "ALL_PROXY",
)
USER_AGENT = "Better-Poster-Skill/1.0"
DEFAULT_TOP100_PATH = Path("data/csrankings_top100_institutions.json")
DEFAULT_OUT_DIR = Path("assets/institutions")


@dataclass(frozen=True)
class Institution:
    name: str
    aliases: tuple[str, ...]
    domains: tuple[str, ...]


def clean_proxy_env() -> None:
    for key in PROXY_ENV_KEYS:
        os.environ.pop(key, None)


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-") or "institution"


def load_institutions(path: Path) -> list[Institution]:
    data = json.loads(path.read_text(encoding="utf-8"))
    items: list[Institution] = []
    for raw in data.get("institutions", []):
        name = str(raw.get("name", "")).strip()
        if not name:
            continue
        aliases = tuple(str(x).strip() for x in raw.get("aliases", []) if str(x).strip())
        domains = tuple(str(x).strip() for x in raw.get("domains", []) if str(x).strip())
        items.append(Institution(name=name, aliases=aliases, domains=domains))
    return items


def match_institution(query: str, institutions: list[Institution]) -> Institution | None:
    q = query.strip().lower()
    for inst in institutions:
        names = (inst.name, *inst.aliases)
        if any(name.lower() == q for name in names):
            return inst
    for inst in institutions:
        names = (inst.name, *inst.aliases)
        if any(name.lower() in q for name in names):
            return inst
    return None


def logo_urls(inst: Institution) -> list[str]:
    urls: list[str] = []
    for domain in inst.domains:
        urls.extend(
            [
                f"https://logo.clearbit.com/{domain}",
                f"https://www.google.com/s2/favicons?domain={domain}&sz=512",
                f"https://icons.duckduckgo.com/ip3/{domain}.ico",
                f"https://{domain}/favicon.ico",
            ]
        )
    return urls


def fetch_image(url: str, timeout: float) -> Image.Image | None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            data = response.read(2_500_000)
    except Exception:
        return None
    try:
        image = Image.open(BytesIO(data)).convert("RGBA")
        if min(image.size) < 24:
            return None
        return image
    except Exception:
        return None


def trim_logo(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    bbox = alpha.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    return rgba


def fit_logo(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    image = trim_logo(image)
    image.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (255, 255, 255, 0))
    x = (size[0] - image.width) // 2
    y = (size[1] - image.height) // 2
    canvas.alpha_composite(image, (x, y))
    return canvas


def font(path: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        width = draw.textbbox((0, 0), trial, font=font_obj)[2]
        if width <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:3]


def make_badge(inst: Institution, logo: Image.Image, out_path: Path) -> None:
    width, height = 980, 360
    badge = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(badge)
    border = (209, 213, 219, 255)
    ink = (17, 24, 39, 255)
    muted = (75, 85, 99, 255)
    accent = (0, 62, 116, 255)
    draw.rounded_rectangle([8, 8, width - 8, height - 8], radius=34, fill=(255, 255, 255, 255), outline=border, width=4)
    draw.rounded_rectangle([34, 44, 278, 316], radius=24, fill=(247, 249, 252, 255), outline=border, width=2)
    badge.alpha_composite(fit_logo(logo, (206, 206)), (56, 80))

    bold = font("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 47)
    regular = font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    small = font("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    x = 318
    y = 54
    for line in wrap_text(draw, inst.name, bold, 620):
        draw.text((x, y), line, fill=ink, font=bold)
        y += 54
    aliases = " / ".join(inst.aliases[:2]) if inst.aliases else (inst.domains[0] if inst.domains else "")
    if aliases:
        draw.text((x, y + 8), aliases, fill=accent, font=regular)
    domain = inst.domains[0] if inst.domains else ""
    if domain:
        draw.text((x, height - 68), domain, fill=muted, font=small)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    badge.save(out_path)


def cache_one(inst: Institution, out_dir: Path, timeout: float, force: bool = False) -> dict[str, str]:
    slug = slugify(inst.name)
    raw_path = out_dir / "cache" / f"{slug}.png"
    badge_path = out_dir / "badges" / f"{slug}.png"
    if badge_path.exists() and raw_path.exists() and not force:
        return {"institution": inst.name, "status": "cached", "badge": str(badge_path), "raw": str(raw_path)}

    logo = None
    source = ""
    if raw_path.exists() and not force:
        try:
            logo = Image.open(raw_path).convert("RGBA")
            source = "cache"
        except Exception:
            logo = None
    if logo is None:
        for url in logo_urls(inst):
            logo = fetch_image(url, timeout)
            if logo is not None:
                source = url
                raw_path.parent.mkdir(parents=True, exist_ok=True)
                logo.save(raw_path)
                break
    if logo is None:
        return {"institution": inst.name, "status": "failed"}

    make_badge(inst, logo, badge_path)
    return {"institution": inst.name, "status": "ok", "badge": str(badge_path), "raw": str(raw_path), "source": source}


def write_manifest(out_dir: Path, results: list[dict[str, str]]) -> None:
    manifest = {
        "note": "Generated badges combine downloaded institution marks with institution names. Review copyright/trademark terms before redistribution.",
        "results": results,
    }
    path = out_dir / "badges" / "manifest.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--top100", default=str(DEFAULT_TOP100_PATH))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--institution", action="append", default=[], help="Specific institution name/alias. Repeatable.")
    parser.add_argument("--all", action="store_true", help="Cache badges for all configured institutions.")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--timeout", type=float, default=6.0)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--activate", help="Copy the matched institution badge to current-logo.png.")
    return parser.parse_args()


def main() -> int:
    clean_proxy_env()
    args = parse_args()
    institutions = load_institutions(Path(args.top100))
    out_dir = Path(args.out_dir)

    selected: list[Institution] = []
    if args.all:
        selected.extend(institutions[: max(0, args.limit)])
    for query in args.institution:
        match = match_institution(query, institutions)
        if match and match not in selected:
            selected.append(match)
        elif not match:
            print(f"Warning: no configured institution matched: {query}", file=sys.stderr)
    if not selected:
        print("No institutions selected. Use --all or --institution.", file=sys.stderr)
        return 2

    results: list[dict[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = [executor.submit(cache_one, inst, out_dir, args.timeout, args.force) for inst in selected]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(f"{result.get('status')}: {result.get('institution')} {result.get('badge', '')}")

    results.sort(key=lambda item: item.get("institution", ""))
    write_manifest(out_dir, results)

    if args.activate:
        match = match_institution(args.activate, institutions)
        if not match:
            print(f"Error: cannot activate unknown institution: {args.activate}", file=sys.stderr)
            return 1
        badge = out_dir / "badges" / f"{slugify(match.name)}.png"
        if not badge.exists():
            activated = cache_one(match, out_dir, args.timeout, args.force)
            if activated.get("status") not in {"ok", "cached"}:
                print(f"Error: cannot activate badge for {match.name}", file=sys.stderr)
                return 1
        shutil.copy2(badge, out_dir / "current-logo.png")
        (out_dir / "current-institution.txt").write_text(match.name + "\n", encoding="utf-8")
        print(f"activated: {match.name} -> {out_dir / 'current-logo.png'}")

    ok_count = sum(1 for result in results if result.get("status") in {"ok", "cached"})
    print(f"cached badges: {ok_count}/{len(results)}")
    return 0 if ok_count else 1


if __name__ == "__main__":
    raise SystemExit(main())
