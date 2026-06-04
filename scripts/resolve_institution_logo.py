#!/usr/bin/env python3
"""Resolve and cache a CSRankings top-100 institution logo for poster templates.

Workflow:
1. Infer or accept an institution name.
2. Match only against data/csrankings_top100_institutions.json.
3. Check assets/institutions/cache/<institution-slug>.png.
4. If cached, copy it to assets/institutions/current-logo.png.
5. If not cached and --download is enabled, try network logo sources, cache the result,
   then copy it to current-logo.png.
6. If no top-100 institution is identified or no logo can be resolved, remove current-logo
   so the poster institution-brand area remains blank.

Logo files are generated artifacts because university marks are commonly protected by
copyright/trademark terms. Review each logo before redistribution.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile

USER_AGENT = "Better-Poster-Skill/1.0 (+https://github.com/XinbaoQiao/Better-Poster-Skill)"
DEFAULT_TOP100_PATH = Path("data/csrankings_top100_institutions.json")
DEFAULT_OUT_DIR = Path("assets/institutions")


@dataclass(frozen=True)
class Institution:
    name: str
    aliases: tuple[str, ...]
    domains: tuple[str, ...]


def slugify(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-") or "institution"


def request_json(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def request_bytes(url: str, timeout: int = 30) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read(), response.headers.get("Content-Type", "")


def load_top100(path: Path) -> list[Institution]:
    data = json.loads(path.read_text(encoding="utf-8"))
    institutions = []
    for item in data.get("institutions", []):
        name = str(item.get("name", "")).strip()
        if not name:
            continue
        aliases = tuple(str(alias).strip() for alias in item.get("aliases", []) if str(alias).strip())
        domains = tuple(str(domain).strip() for domain in item.get("domains", []) if str(domain).strip())
        institutions.append(Institution(name=name, aliases=aliases, domains=domains))
    if not institutions:
        raise ValueError(f"No institutions found in {path}")
    return institutions


def collect_source_text(paths: list[Path]) -> str:
    chunks: list[str] = []
    for path in paths:
        if path.is_dir():
            files = []
            for suffix in ("*.tex", "*.md", "*.txt", "*.html", "*.bbl"):
                files.extend(path.rglob(suffix))
        else:
            files = [path]
        for file in files:
            try:
                chunks.append(file.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                continue
    return "\n".join(chunks)


def match_institution(name_or_text: str, institutions: list[Institution]) -> Institution | None:
    low = name_or_text.lower()
    candidates: list[tuple[int, Institution]] = []
    for inst in institutions:
        names = (inst.name, *inst.aliases)
        for candidate in names:
            cand_low = candidate.lower()
            if not cand_low:
                continue
            if cand_low == low.strip():
                return inst
            if re.search(r"\b" + re.escape(cand_low) + r"\b", low):
                candidates.append((len(cand_low), inst))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1]


def wikipedia_thumbnail_url(query: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "redirects": "1",
            "titles": query,
            "prop": "pageimages",
            "piprop": "thumbnail|original",
            "pithumbsize": "1200",
        }
    )
    data = request_json(f"https://en.wikipedia.org/w/api.php?{params}")
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        thumb = page.get("thumbnail", {}).get("source")
        if thumb:
            return thumb
        original = page.get("original", {}).get("source")
        if original:
            return original
    return None


def commons_thumb_for_file(filename: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "titles": f"File:{filename}",
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": "1200",
        }
    )
    data = request_json(f"https://commons.wikimedia.org/w/api.php?{params}")
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if infos:
            return infos[0].get("thumburl") or infos[0].get("url")
    return None


def wikidata_logo_url(name: str) -> str | None:
    search_params = urllib.parse.urlencode(
        {"action": "wbsearchentities", "format": "json", "language": "en", "limit": "4", "search": name}
    )
    search = request_json(f"https://www.wikidata.org/w/api.php?{search_params}")
    for hit in search.get("search", []):
        qid = hit.get("id")
        if not qid:
            continue
        entity_params = urllib.parse.urlencode(
            {"action": "wbgetentities", "format": "json", "ids": qid, "props": "claims"}
        )
        entity = request_json(f"https://www.wikidata.org/w/api.php?{entity_params}")
        claims = entity.get("entities", {}).get(qid, {}).get("claims", {})
        for prop in ("P154", "P94", "P18"):
            for claim in claims.get(prop, []):
                value = claim.get("mainsnak", {}).get("datavalue", {}).get("value")
                if isinstance(value, str):
                    thumb = commons_thumb_for_file(value)
                    if thumb:
                        return thumb
    return None


def candidate_logo_urls(inst: Institution) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []

    # Stable structured sources first.
    try:
        url = wikidata_logo_url(inst.name)
        if url:
            candidates.append(("wikidata_commons", url))
    except Exception:
        pass
    for query in (inst.name, f"{inst.name} logo", f"{inst.name} seal"):
        try:
            url = wikipedia_thumbnail_url(query)
            if url:
                candidates.append(("wikipedia_pageimages", url))
        except Exception:
            pass

    # Fast domain-based fallbacks. They are useful for speed but must still be reviewed.
    for domain in inst.domains:
        candidates.append(("clearbit_logo", f"https://logo.clearbit.com/{domain}"))
        candidates.append(("google_s2_favicon", f"https://www.google.com/s2/favicons?domain={domain}&sz=256"))
        candidates.append(("duckduckgo_ip3", f"https://icons.duckduckgo.com/ip3/{domain}.ico"))
    return candidates


def write_png(data: bytes, content_type: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    try:
        try:
            from PIL import Image  # type: ignore

            with Image.open(tmp_path) as image:
                image.convert("RGBA").save(out_path)
        except Exception:
            if "png" in content_type.lower():
                out_path.write_bytes(data)
            else:
                raise RuntimeError("Downloaded logo is not PNG and Pillow could not convert it.")
    finally:
        tmp_path.unlink(missing_ok=True)


def clear_current(out_dir: Path) -> None:
    for name in ("current-logo.png", "current-logo.json", "current-institution.txt"):
        try:
            (out_dir / name).unlink()
        except FileNotFoundError:
            pass


def activate_cached_logo(inst: Institution, cache_path: Path, out_dir: Path, source: str = "cache") -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    current = out_dir / "current-logo.png"
    shutil.copy2(cache_path, current)
    metadata = {
        "institution": inst.name,
        "cache_path": str(cache_path),
        "source": source,
        "generated_at_unix": int(time.time()),
        "note": "Review logo copyright/trademark requirements before public redistribution.",
    }
    (out_dir / "current-logo.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (out_dir / "current-institution.txt").write_text(inst.name + "\n", encoding="utf-8")
    return current


def resolve_logo(inst: Institution, out_dir: Path, download: bool) -> Path | None:
    cache_dir = out_dir / "cache"
    slug = slugify(inst.name)
    cache_path = cache_dir / f"{slug}.png"
    if cache_path.exists():
        return activate_cached_logo(inst, cache_path, out_dir, source="cache")
    if not download:
        clear_current(out_dir)
        return None

    for source_name, url in candidate_logo_urls(inst):
        try:
            data, content_type = request_bytes(url)
            if not data:
                continue
            write_png(data, content_type, cache_path)
            return activate_cached_logo(inst, cache_path, out_dir, source=source_name)
        except Exception as exc:
            print(f"Warning: {source_name} failed for {inst.name}: {exc}", file=sys.stderr)
            continue
    clear_current(out_dir)
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--institution", help="Institution name. Must match the configured CSRankings top-100 list.")
    parser.add_argument("--source", action="append", default=[], help="Text/LaTeX/HTML file or directory used for institution inference.")
    parser.add_argument("--top100", default=str(DEFAULT_TOP100_PATH), help="Path to csrankings_top100_institutions.json.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Logo cache output directory.")
    parser.add_argument("--download", action="store_true", help="Download logo on cache miss. Without this, cache miss leaves the logo area blank.")
    parser.add_argument("--cache-top100", action="store_true", help="Download/cache all configured top-100 institutions. Use with care.")
    parser.add_argument("--limit", type=int, default=100, help="Maximum institutions for --cache-top100.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    top100_path = Path(args.top100)
    out_dir = Path(args.out_dir)
    institutions = load_top100(top100_path)

    if args.cache_top100:
        failures = 0
        for inst in institutions[: max(0, args.limit)]:
            result = resolve_logo(inst, out_dir, download=True)
            if result:
                print(f"Cached: {inst.name} -> {result}")
            else:
                failures += 1
                print(f"Warning: no logo cached for {inst.name}", file=sys.stderr)
        return 0 if failures == 0 else 1

    query = args.institution or ""
    if not query and args.source:
        query = collect_source_text([Path(path) for path in args.source])
    if not query:
        clear_current(out_dir)
        print("No institution provided or inferred; institution area will remain blank.")
        return 0

    inst = match_institution(query, institutions)
    if not inst:
        clear_current(out_dir)
        print("No configured CSRankings top-100 institution matched; institution area will remain blank.")
        return 0

    result = resolve_logo(inst, out_dir, download=args.download)
    if result:
        print(f"Current institution logo: {result}")
        print(f"Institution: {inst.name}")
    else:
        print(f"Matched {inst.name}, but no cached logo was available; institution area will remain blank.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
