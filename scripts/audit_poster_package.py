#!/usr/bin/env python3
"""Audit and optionally repair a Better Poster output directory.

The audit is intentionally conservative: it checks portability, broken local
asset references, placeholder text, direct SVG usage in LaTeX, and stale build
artifacts. With --fix-portable it copies betterposter.cls next to poster .tex
files so a recipient can run pdflatex from the poster directory.
"""

from __future__ import annotations

import argparse
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CLASS = REPO_ROOT / "templates" / "betterposter.cls"

PLACEHOLDER_PATTERNS = (
    "Main finding goes here",
    "A claim-first title states exactly what changed",
    "Paper title or short research object",
    "Research Title",
    "author@example.com",
    "contact@example.edu",
    "Replace with",
)

MACHINE_PATH_PATTERNS = tuple(f"/{name}/" for name in ("data", "home"))

BUILD_SUFFIXES = {
    ".aux",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".synctex.gz",
    ".toc",
}

ASSET_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".svg",
    ".webp",
    ".gif",
}


@dataclass
class AuditResult:
    warnings: list[str]
    fixed: list[str]
    removed: list[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def source_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.iterdir()
        if path.is_file() and path.suffix.lower() in {".tex", ".html", ".htm"}
    )


def is_betterposter_tex(path: Path) -> bool:
    text = read_text(path)
    return "\\documentclass" in text and "{betterposter}" in text


def asset_refs_from_text(text: str) -> set[str]:
    refs: set[str] = set()
    quoted_patterns = [
        r'src=["\']([^"\']+)["\']',
        r'href=["\']([^"\']+)["\']',
    ]
    braced_patterns = [
        r'\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}',
        r'\\(?:postergraphic|posterlabeledgraphic|posterimagetextrow)\s*(?:\[[^\]]*\])?\{([^{}]+)\}',
        r'\{((?:figures|assets|\.\./)[^{}]+\.(?:png|jpg|jpeg|pdf|svg|webp|gif))\}',
    ]
    for pattern in quoted_patterns + braced_patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            ref = match.group(1).strip()
            if ref.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            if any(ref.lower().endswith(suffix) for suffix in ASSET_SUFFIXES):
                refs.add(ref)
    return refs


def resolve_ref(root: Path, source: Path, ref: str) -> Path:
    ref_path = Path(ref)
    if ref_path.is_absolute():
        return ref_path
    return (source.parent / ref_path).resolve()


def referenced_assets(root: Path, sources: list[Path]) -> set[Path]:
    refs: set[Path] = set()
    for source in sources:
        for ref in asset_refs_from_text(read_text(source)):
            refs.add(resolve_ref(root, source, ref))
    return refs


def audit_placeholders(sources: list[Path], result: AuditResult) -> None:
    for source in sources:
        text = read_text(source)
        for pattern in PLACEHOLDER_PATTERNS:
            if pattern in text:
                result.warnings.append(f"{source}: placeholder-like text remains: {pattern}")
        for pattern in MACHINE_PATH_PATTERNS:
            if pattern in text:
                result.warnings.append(f"{source}: machine-specific absolute path remains: {pattern}")


def audit_assets(root: Path, sources: list[Path], result: AuditResult) -> set[Path]:
    refs = referenced_assets(root, sources)
    for path in sorted(refs):
        if not path.exists():
            result.warnings.append(f"missing referenced asset: {path}")
    return refs


def audit_latex_portability(root: Path, sources: list[Path], fix: bool, result: AuditResult) -> None:
    if not any(source.suffix.lower() == ".tex" and is_betterposter_tex(source) for source in sources):
        return
    target = root / "betterposter.cls"
    if target.exists():
        return
    if fix:
        shutil.copy2(DEFAULT_CLASS, target)
        result.fixed.append(f"copied {DEFAULT_CLASS.relative_to(REPO_ROOT)} -> {target.relative_to(root)}")
    else:
        result.warnings.append("betterposter.cls is not packaged next to the LaTeX source; use --fix-portable")


def audit_direct_svg_in_latex(sources: list[Path], result: AuditResult) -> None:
    for source in sources:
        if source.suffix.lower() != ".tex":
            continue
        text = read_text(source)
        for ref in asset_refs_from_text(text):
            if ref.lower().endswith(".svg"):
                result.warnings.append(
                    f"{source}: LaTeX references SVG directly ({ref}); convert with scripts/prepare_poster_logo.py"
                )


def clean_artifacts(root: Path, refs: set[Path], result: AuditResult, dry_run: bool) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() in BUILD_SUFFIXES or path.name.endswith(".synctex.gz"):
            if dry_run:
                result.removed.append(f"would remove build artifact {path.relative_to(root)}")
            else:
                path.unlink()
                result.removed.append(f"removed build artifact {path.relative_to(root)}")
            continue
        if "figures" in path.relative_to(root).parts and path.suffix.lower() in ASSET_SUFFIXES:
            if path.resolve() not in refs:
                if dry_run:
                    result.removed.append(f"would remove unreferenced asset {path.relative_to(root)}")
                else:
                    path.unlink()
                    result.removed.append(f"removed unreferenced asset {path.relative_to(root)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("poster_dir", type=Path)
    parser.add_argument("--fix-portable", action="store_true", help="Copy betterposter.cls into the poster directory.")
    parser.add_argument("--clean", action="store_true", help="Remove TeX build files and unreferenced figure assets.")
    parser.add_argument("--dry-run", action="store_true", help="Report cleanup actions without deleting files.")
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when warnings remain.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.poster_dir.resolve()
    result = AuditResult(warnings=[], fixed=[], removed=[])

    if not root.is_dir():
        print(f"poster directory not found: {root}")
        return 2

    sources = source_files(root)
    if not sources:
        print(f"no poster .tex/.html sources found in {root}")
        return 2

    audit_placeholders(sources, result)
    refs = audit_assets(root, sources, result)
    audit_latex_portability(root, sources, args.fix_portable, result)
    audit_direct_svg_in_latex(sources, result)
    if args.clean:
        clean_artifacts(root, refs, result, args.dry_run)

    for item in result.fixed:
        print(f"fixed: {item}")
    for item in result.removed:
        print(f"clean: {item}")
    for item in result.warnings:
        print(f"warning: {item}")
    if not result.warnings:
        print("audit-ok")

    return 1 if args.strict and result.warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
