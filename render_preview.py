#!/usr/bin/env python3
"""Compile a LaTeX poster and render a PNG preview.

Inputs may be a .tex file, a directory containing LaTeX sources, or a .zip archive.
The script avoids network access and only uses local tools.
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


def clean_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in PROXY_ENV_KEYS:
        env.pop(key, None)
    return env


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


def safe_extract_zip(zip_path: Path, dest: Path) -> None:
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            target = dest / member.filename
            resolved = target.resolve()
            if not str(resolved).startswith(str(dest.resolve()) + os.sep):
                raise ValueError(f"Unsafe zip path: {member.filename}")
        archive.extractall(dest)


def find_tex_root(source_dir: Path, preferred: str | None) -> Path:
    if preferred:
        root = source_dir / preferred
        if not root.exists():
            raise FileNotFoundError(f"Requested root tex file not found: {root}")
        return root

    candidates: list[tuple[int, Path]] = []
    for tex in source_dir.rglob("*.tex"):
        try:
            text = tex.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        score = 0
        if "\\documentclass" in text:
            score += 4
        if "\\begin{document}" in text:
            score += 4
        if "\\title" in text:
            score += 1
        if "\\author" in text:
            score += 1
        if "\\bibliography" in text or "\\addbibresource" in text:
            score += 1
        if score:
            candidates.append((score, tex))

    if not candidates:
        raise FileNotFoundError("No plausible LaTeX root file found.")
    candidates.sort(key=lambda item: (-item[0], len(str(item[1]))))
    return candidates[0][1]


def prepare_input(input_path: Path, temp_root: Path, root: str | None) -> Path:
    if input_path.suffix.lower() == ".zip":
        source_dir = temp_root / "source"
        source_dir.mkdir(parents=True, exist_ok=True)
        safe_extract_zip(input_path, source_dir)
        return find_tex_root(source_dir, root)

    if input_path.is_dir():
        return find_tex_root(input_path, root)

    if input_path.suffix.lower() == ".tex":
        return input_path

    raise ValueError("Input must be a .tex file, a directory, or a .zip archive.")


def compile_latex(tex_root: Path, engine: str, passes: int, env: dict[str, str]) -> Path:
    cwd = tex_root.parent
    tex_name = tex_root.name
    pdf_path = tex_root.with_suffix(".pdf")

    latexmk = shutil.which("latexmk")
    if latexmk and engine == "pdflatex":
        cmd = [
            latexmk,
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            tex_name,
        ]
        result = run(cmd, cwd, env)
        print(result.stdout[-6000:])
        if result.returncode != 0:
            raise RuntimeError(f"latexmk failed. Inspect log near: {tex_root.with_suffix('.log')}")
    else:
        executable = shutil.which(engine)
        if not executable:
            raise RuntimeError(f"LaTeX engine not found: {engine}")
        for _ in range(max(1, passes)):
            cmd = [
                executable,
                "-interaction=nonstopmode",
                "-halt-on-error",
                tex_name,
            ]
            result = run(cmd, cwd, env)
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

    cmd = [
        pdftoppm,
        "-png",
        "-singlefile",
        "-r",
        str(dpi),
        str(pdf_path),
        str(stem),
    ]
    result = run(cmd, pdf_path.parent, env)
    print(result.stdout[-2000:])
    if result.returncode != 0:
        raise RuntimeError("pdftoppm failed.")

    preview = stem.with_suffix(".png")
    if not preview.exists():
        raise FileNotFoundError(f"Expected preview was not created: {preview}")
    return preview


def copy_pdf(pdf_path: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / pdf_path.name
    if pdf_path.resolve() != target.resolve():
        shutil.copy2(pdf_path, target)
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="A .tex file, project directory, or .zip archive.")
    parser.add_argument("--root", help="Root .tex file path relative to extracted zip or directory.")
    parser.add_argument("--out-dir", default="build", help="Directory for PDF and PNG outputs.")
    parser.add_argument("--engine", default="pdflatex", help="LaTeX engine, default: pdflatex.")
    parser.add_argument("--passes", type=int, default=2, help="Manual engine passes when latexmk is unavailable.")
    parser.add_argument("--dpi", type=int, default=160, help="PNG preview DPI.")
    parser.add_argument("--no-render", action="store_true", help="Compile only; do not render PNG.")
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
        temp_root = Path(tmp)
        try:
            tex_root = prepare_input(input_path, temp_root, args.root)
            pdf_path = compile_latex(tex_root, args.engine, args.passes, env)
            copied_pdf = copy_pdf(pdf_path, out_dir)
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
