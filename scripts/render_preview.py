#!/usr/bin/env python3
"""Compile LaTeX posters and render LaTeX/HTML Better Poster previews.

Inputs may be a .tex file, an .html file, a directory containing poster sources,
or a .zip archive. The script avoids network access and only uses local tools.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


PROXY_ENV_KEYS = (
    "http_proxy",
    "https_proxy",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "all_proxy",
    "ALL_PROXY",
)

HTML_SUFFIXES = {".html", ".htm"}
DEFAULT_OUT_DIR = Path(tempfile.gettempdir()) / "better-poster-preview"

PLACEHOLDER_PATTERNS = (
    "Main finding goes here",
    "A claim-first title states exactly what changed",
    "Paper title or short research object",
    "author@example.com",
    "Replace with",
    "+12%",
    "3x",
)


def clean_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in PROXY_ENV_KEYS:
        env.pop(key, None)
    return env


def latex_search_env(cwd: Path, env: dict[str, str]) -> dict[str, str]:
    latex_env = env.copy()
    roots = [
        cwd,
        cwd / "templates",
        cwd.parent,
        cwd.parent / "templates",
        cwd.parent.parent,
        cwd.parent.parent / "templates",
    ]
    parts = [str(path) for path in roots if path.exists()]
    existing = latex_env.get("TEXINPUTS")
    if existing:
        parts.append(existing)
    parts.append("")  # preserve TeX default search path
    latex_env["TEXINPUTS"] = os.pathsep.join(parts)
    return latex_env


def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(cmd))
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def warn_placeholders(path: Path) -> None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return
    hits = [pattern for pattern in PLACEHOLDER_PATTERNS if pattern in text]
    if hits:
        print(f"Warning: unresolved placeholder-like text in {path}: {', '.join(hits)}")


def safe_extract_zip(zip_path: Path, dest: Path) -> None:
    root = dest.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            target = dest / member.filename
            resolved = target.resolve()
            if resolved != root and root not in resolved.parents:
                raise ValueError(f"Unsafe zip path: {member.filename}")
        archive.extractall(dest)


def score_tex_root(tex: Path) -> int:
    try:
        text = tex.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return 0
    score = 0
    if "\\documentclass" in text:
        score += 4
    if "\\begin{document}" in text:
        score += 4
    if "\\betterposter" in text:
        score += 4
    if "\\title" in text:
        score += 1
    if "\\author" in text:
        score += 1
    if "\\bibliography" in text or "\\addbibresource" in text:
        score += 1
    return score


def score_html_root(html: Path) -> int:
    try:
        text = html.read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return 0
    score = 0
    if "<html" in text:
        score += 3
    if "better poster" in text or "even better poster" in text:
        score += 3
    if "class=\"poster" in text or "class='poster" in text:
        score += 3
    if "@page" in text and "a0" in text:
        score += 2
    return score


def find_source_root(source_dir: Path, preferred: str | None) -> Path:
    if preferred:
        root = source_dir / preferred
        if not root.exists():
            raise FileNotFoundError(f"Requested root source file not found: {root}")
        return root

    candidates: list[tuple[int, Path]] = []
    for path in source_dir.rglob("*"):
        suffix = path.suffix.lower()
        if suffix == ".tex":
            score = score_tex_root(path)
        elif suffix in HTML_SUFFIXES:
            score = score_html_root(path)
        else:
            continue
        if score:
            candidates.append((score, path))

    if not candidates:
        raise FileNotFoundError("No plausible LaTeX or HTML poster root found.")
    candidates.sort(key=lambda item: (-item[0], len(str(item[1]))))
    return candidates[0][1]


def prepare_input(input_path: Path, temp_root: Path, root: str | None) -> Path:
    if input_path.suffix.lower() == ".zip":
        source_dir = temp_root / "source"
        source_dir.mkdir(parents=True, exist_ok=True)
        safe_extract_zip(input_path, source_dir)
        return find_source_root(source_dir, root)
    if input_path.is_dir():
        return find_source_root(input_path, root)
    if input_path.suffix.lower() == ".tex" or input_path.suffix.lower() in HTML_SUFFIXES:
        return input_path
    raise ValueError("Input must be a .tex file, .html file, directory, or .zip archive.")


def compile_latex(tex_root: Path, engine: str, passes: int, env: dict[str, str]) -> Path:
    cwd = tex_root.parent
    tex_name = tex_root.name
    pdf_path = tex_root.with_suffix(".pdf")
    warn_placeholders(tex_root)
    env = latex_search_env(cwd, env)

    latexmk = shutil.which("latexmk")
    if latexmk and engine == "pdflatex":
        result = run([latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex_name], cwd, env)
        print(result.stdout[-6000:])
        if result.returncode != 0:
            raise RuntimeError(f"latexmk failed. Inspect log near: {tex_root.with_suffix('.log')}")
    else:
        executable = shutil.which(engine)
        if not executable:
            raise RuntimeError(f"LaTeX engine not found: {engine}")
        for _ in range(max(1, passes)):
            result = run([executable, "-interaction=nonstopmode", "-halt-on-error", tex_name], cwd, env)
            print(result.stdout[-6000:])
            if result.returncode != 0:
                raise RuntimeError(f"{engine} failed. Inspect log near: {tex_root.with_suffix('.log')}")

    if not pdf_path.exists():
        raise FileNotFoundError(f"Expected PDF was not created: {pdf_path}")
    return pdf_path


def render_pdf(pdf_path: Path, out_dir: Path, dpi: int, env: dict[str, str]) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / pdf_path.stem
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        raise RuntimeError("pdftoppm not found. Install poppler-utils or keep the compiled PDF.")
    result = run([pdftoppm, "-png", "-singlefile", "-r", str(dpi), str(pdf_path), str(stem)], pdf_path.parent, env)
    print(result.stdout[-2000:])
    if result.returncode != 0:
        raise RuntimeError("pdftoppm failed.")
    preview = stem.with_suffix(".png")
    if not preview.exists():
        raise FileNotFoundError(f"Expected preview was not created: {preview}")
    return preview


def copy_file(source: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / source.name
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)
    return target


def render_html(html_path: Path, out_dir: Path, dpi: int, env: dict[str, str]) -> tuple[Path, Path | None, Path | None]:
    warn_placeholders(html_path)
    copied_html = copy_file(html_path, out_dir)
    pdf_path = out_dir / f"{html_path.stem}.pdf"

    try:
        from weasyprint import HTML  # type: ignore
    except Exception:
        print("Warning: WeasyPrint is not installed; HTML copied but not rendered.", file=sys.stderr)
        return copied_html, None, None

    HTML(filename=str(html_path), base_url=str(html_path.parent)).write_pdf(str(pdf_path))
    preview = render_pdf(pdf_path, out_dir, dpi, env)
    return copied_html, pdf_path, preview


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="A .tex/.html file, project directory, or .zip archive.")
    parser.add_argument("--root", help="Root source file path relative to extracted zip or directory.")
    parser.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT_DIR),
        help="Directory for PDF/HTML and PNG outputs. Defaults to the system temp directory.",
    )
    parser.add_argument("--engine", default="pdflatex", help="LaTeX engine, default: pdflatex.")
    parser.add_argument("--passes", type=int, default=2, help="Manual engine passes when latexmk is unavailable.")
    parser.add_argument("--dpi", type=int, default=160, help="PNG preview DPI.")
    parser.add_argument("--no-render", action="store_true", help="Compile/copy only; do not render PNG preview.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    env = clean_env()

    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory(prefix="better-poster-") as tmp:
        try:
            source_root = prepare_input(input_path, Path(tmp), args.root)
            if source_root.suffix.lower() in HTML_SUFFIXES:
                if args.no_render:
                    copied_html = copy_file(source_root, out_dir)
                    print(f"HTML: {copied_html}")
                else:
                    html_out, pdf_out, preview = render_html(source_root, out_dir, args.dpi, env)
                    print(f"HTML: {html_out}")
                    if pdf_out:
                        print(f"PDF: {pdf_out}")
                    if preview:
                        print(f"Preview: {preview}")
            else:
                pdf_path = compile_latex(source_root, args.engine, args.passes, env)
                copied_pdf = copy_file(pdf_path, out_dir)
                print(f"PDF: {copied_pdf}")
                if not args.no_render:
                    preview = render_pdf(pdf_path, out_dir, args.dpi, env)
                    print(f"Preview: {preview}")
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
