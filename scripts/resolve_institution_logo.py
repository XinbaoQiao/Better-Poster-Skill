#!/usr/bin/env python3
"""Resolve and cache an institution logo for Better Poster templates.

The resolver can infer an institution from paper text / LaTeX source, match it
against the public CSRankings institutions list, then fetch a logo-like image via
Wikipedia/Wikidata/Commons and save it as assets/institutions/current-logo.png.

The script deliberately downloads logos on demand instead of vendoring many
third-party logo files into this repository.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile


CS_RANKINGS_INSTITUTIONS_URL = (
    "https://raw.githubusercontent.com/emeryberger/CSrankings/gh-pages/institutions.csv"
)

USER_AGENT = "Better-Poster-Skill/1.0 (+https://github.com/XinbaoQiao/Better-Poster-Skill)"

# CSRankings is query-dependent, so there is no single canonical all-time top 100.
# This seed list covers common high-visibility CSRankings institutions and is used
# only when --cache-top100 is requested or when network access to institutions.csv
# is unavailable.
COMMON_TOP_CS_INSTITUTIONS = [
    "Carnegie Mellon University", "Massachusetts Institute of Technology", "Stanford University",
    "University of California - Berkeley", "University of Illinois at Urbana-Champaign", "Cornell University",
    "University of Washington", "Georgia Institute of Technology", "Princeton University",
    "University of Texas at Austin", "University of Michigan", "University of California - San Diego",
    "Columbia University", "Harvard University", "University of California - Los Angeles",
    "University of Maryland - College Park", "University of Wisconsin - Madison", "Purdue University",
    "University of Pennsylvania", "New York University", "Duke University", "Brown University",
    "Rice University", "University of Southern California", "University of Chicago", "Yale University",
    "Northwestern University", "Johns Hopkins University", "University of Massachusetts Amherst",
    "University of North Carolina at Chapel Hill", "University of Virginia", "Pennsylvania State University",
    "Ohio State University", "University of Minnesota", "University of California - Irvine",
    "University of California - Santa Barbara", "University of California - Davis", "University of Colorado Boulder",
    "University of Utah", "Arizona State University", "Texas A&M University", "Rutgers University",
    "Stony Brook University", "Northeastern University", "Boston University", "University of Rochester",
    "University of Toronto", "University of British Columbia", "University of Waterloo", "McGill University",
    "University of Montreal", "ETH Zurich", "EPFL", "University of Oxford", "University of Cambridge",
    "Imperial College London", "University of Edinburgh", "University College London", "King's College London",
    "Technical University of Munich", "Max Planck Society", "Saarland University", "INRIA",
    "Tsinghua University", "Peking University", "Shanghai Jiao Tong University", "Zhejiang University",
    "Nanjing University", "Fudan University", "Chinese University of Hong Kong", "HKUST",
    "University of Hong Kong", "City University of Hong Kong", "National University of Singapore",
    "Nanyang Technological University", "KAIST", "Seoul National University", "POSTECH",
    "Korea University", "Yonsei University", "University of Tokyo", "Kyoto University",
    "Osaka University", "Institute of Science Tokyo", "National Taiwan University", "Technion",
    "Hebrew University of Jerusalem", "Tel Aviv University", "Weizmann Institute", "Australian National University",
    "University of Melbourne", "University of Sydney", "University of New South Wales", "Monash University",
    "Aalto University", "KTH Royal Institute of Technology", "KU Leuven", "University of Amsterdam",
    "Delft University of Technology", "University of Copenhagen", "Aarhus University", "University of Helsinki",
]

ALIASES = {
    "MIT": "Massachusetts Institute of Technology",
    "CMU": "Carnegie Mellon University",
    "UC Berkeley": "University of California - Berkeley",
    "Berkeley": "University of California - Berkeley",
    "UIUC": "University of Illinois at Urbana-Champaign",
    "UW": "University of Washington",
    "UT Austin": "University of Texas at Austin",
    "UCLA": "University of California - Los Angeles",
    "UCSD": "University of California - San Diego",
    "UMD": "University of Maryland - College Park",
    "NUS": "National University of Singapore",
    "NTU": "Nanyang Technological University",
    "CUHK": "Chinese University of Hong Kong",
    "HKUST": "HKUST",
    "ETH": "ETH Zurich",
    "TUM": "Technical University of Munich",
    "Tokyo Tech": "Institute of Science Tokyo",
}


@dataclass
class Institution:
    name: str
    region: str = ""
    country: str = ""
    homepage: str = ""


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug or "institution"


def request_json(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def request_bytes(url: str, timeout: int = 30) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read(), response.headers.get("Content-Type", "")


def load_csrankings_institutions(local_csv: Path | None = None) -> list[Institution]:
    if local_csv and local_csv.exists():
        text = local_csv.read_text(encoding="utf-8", errors="ignore")
    else:
        req = urllib.request.Request(CS_RANKINGS_INSTITUTIONS_URL, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as response:
            text = response.read().decode("utf-8")
    rows = csv.DictReader(text.splitlines())
    institutions: list[Institution] = []
    for row in rows:
        name = (row.get("institution") or "").strip()
        if name:
            institutions.append(
                Institution(
                    name=name,
                    region=(row.get("region") or "").strip(),
                    country=(row.get("countryabbrv") or "").strip(),
                    homepage=(row.get("homepage") or "").strip(),
                )
            )
    return institutions


def collect_source_text(paths: list[Path]) -> str:
    chunks: list[str] = []
    for path in paths:
        if path.is_dir():
            files = list(path.rglob("*.tex")) + list(path.rglob("*.md")) + list(path.rglob("*.txt")) + list(path.rglob("*.html"))
        else:
            files = [path]
        for file in files:
            try:
                chunks.append(file.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                continue
    return "\n".join(chunks)


def infer_institution(text: str, institutions: list[Institution]) -> str | None:
    low = text.lower()
    for alias, canonical in sorted(ALIASES.items(), key=lambda item: -len(item[0])):
        if re.search(r"\b" + re.escape(alias.lower()) + r"\b", low):
            return canonical
    ranked = sorted(institutions, key=lambda item: -len(item.name))
    for inst in ranked:
        name = inst.name.lower()
        if len(name) >= 5 and name in low:
            return inst.name
    return None


def wikipedia_thumbnail_url(title: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "format": "json",
            "redirects": "1",
            "titles": title,
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
        {
            "action": "wbsearchentities",
            "format": "json",
            "language": "en",
            "limit": "4",
            "search": name,
        }
    )
    search = request_json(f"https://www.wikidata.org/w/api.php?{search_params}")
    for hit in search.get("search", []):
        qid = hit.get("id")
        if not qid:
            continue
        entity_params = urllib.parse.urlencode(
            {
                "action": "wbgetentities",
                "format": "json",
                "ids": qid,
                "props": "claims",
            }
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


def find_logo_url(name: str) -> str | None:
    queries = [name, f"{name} logo", f"{name} seal"]
    for query in queries:
        try:
            url = wikipedia_thumbnail_url(query)
            if url:
                return url
        except Exception:
            continue
    try:
        return wikidata_logo_url(name)
    except Exception:
        return None


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
                raise RuntimeError(
                    "Downloaded logo is not PNG and Pillow could not convert it. Install Pillow or use a PNG logo."
                )
    finally:
        tmp_path.unlink(missing_ok=True)


def resolve_one(name: str, out_dir: Path, filename: str = "current-logo.png") -> Path:
    canonical = ALIASES.get(name, name)
    logo_url = find_logo_url(canonical)
    if not logo_url:
        raise RuntimeError(f"Could not find a logo URL for institution: {canonical}")
    data, content_type = request_bytes(logo_url)
    out_path = out_dir / filename
    write_png(data, content_type, out_path)
    metadata = {
        "institution": canonical,
        "logo_url": logo_url,
        "content_type": content_type,
        "generated_at_unix": int(time.time()),
        "note": "Review logo licensing/trademark restrictions before public redistribution.",
    }
    (out_dir / f"{Path(filename).stem}.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return out_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--institution", help="Institution name to resolve. Overrides source inference.")
    parser.add_argument("--source", action="append", default=[], help="Text/LaTeX/HTML file or directory used for institution inference.")
    parser.add_argument("--out-dir", default="assets/institutions", help="Logo cache output directory.")
    parser.add_argument("--institutions-csv", help="Optional local CSRankings institutions.csv path.")
    parser.add_argument("--cache-top100", action="store_true", help="Also cache common high-visibility CSRankings institutions under cache/.")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of seed institutions to cache with --cache-top100.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out_dir)
    csv_path = Path(args.institutions_csv) if args.institutions_csv else None

    try:
        institutions = load_csrankings_institutions(csv_path)
    except Exception as exc:
        print(f"Warning: could not load CSRankings institutions list: {exc}", file=sys.stderr)
        institutions = [Institution(name=name) for name in COMMON_TOP_CS_INSTITUTIONS]

    name = args.institution
    if not name and args.source:
        source_text = collect_source_text([Path(path) for path in args.source])
        name = infer_institution(source_text, institutions)
    if not name:
        print("Error: no institution provided or inferred. Use --institution or --source.", file=sys.stderr)
        return 2

    try:
        current = resolve_one(name, out_dir, "current-logo.png")
        print(f"Current institution logo: {current}")
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.cache_top100:
        cache_dir = out_dir / "cache"
        for seed in COMMON_TOP_CS_INSTITUTIONS[: max(0, args.limit)]:
            try:
                cached = resolve_one(seed, cache_dir, f"{slugify(seed)}.png")
                print(f"Cached: {seed} -> {cached}")
            except Exception as exc:
                print(f"Warning: failed to cache {seed}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
