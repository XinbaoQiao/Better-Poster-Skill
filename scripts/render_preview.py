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
DEFAULT_HTML_TIMEOUT_SECONDS = 45

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


def run(
    cmd: list[str],
    cwd: Path,
    env: dict[str, str],
    timeout: int | None = None,
) -> subprocess.CompletedProcess[str]:
    print("$ " + " ".join(cmd))
    try:
        return subprocess.run(
            cmd,
            cwd=str(cwd),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout or ""
        if isinstance(output, bytes):
            output = output.decode("utf-8", errors="ignore")
        raise RuntimeError(f"command timed out after {timeout}s: {' '.join(cmd)}\n{output}") from exc


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


def footer_ink_pixel(rgb: tuple[int, int, int]) -> bool:
    r, g, b = rgb
    if r > 242 and g > 242 and b > 242:
        return False
    if max(rgb) - min(rgb) < 12 and r > 155:
        return False
    return r < 235 or g < 235 or b < 235


def footer_logo_bbox(image: object, x0: int, x1: int, y0: int) -> tuple[int, int, int, int] | None:
    crop = image.crop((x0, y0, x1, image.height))
    width, height = crop.size
    pixels = crop.load()
    mask = bytearray(width * height)

    for y in range(height):
        row = y * width
        for x in range(width):
            if footer_ink_pixel(pixels[x, y]):
                mask[row + x] = 1

    seen = bytearray(width * height)
    components: list[tuple[int, int, int, int, int]] = []
    min_area = max(32, int(width * height * 0.00035))

    for index, value in enumerate(mask):
        if not value or seen[index]:
            continue
        stack = [index]
        seen[index] = 1
        area = 0
        min_x = width
        min_y = height
        max_x = 0
        max_y = 0
        while stack:
            item = stack.pop()
            y, x = divmod(item, width)
            area += 1
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < width and 0 <= ny < height:
                    neighbor = ny * width + nx
                    if mask[neighbor] and not seen[neighbor]:
                        seen[neighbor] = 1
                        stack.append(neighbor)
        if area >= min_area:
            components.append((area, min_x + x0, min_y + y0, max_x + x0, max_y + y0))

    if not components:
        return None

    max_area = max(component[0] for component in components)
    keep = [component for component in components if component[0] >= max(min_area, int(max_area * 0.08))]
    return (
        min(component[1] for component in keep),
        min(component[2] for component in keep),
        max(component[3] for component in keep),
        max(component[4] for component in keep),
    )


def audit_footer_logo_alignment(preview: Path) -> list[str]:
    try:
        from PIL import Image  # type: ignore
    except Exception as exc:
        return [f"footer logo visual audit skipped because Pillow is unavailable: {exc}"]

    image = Image.open(preview).convert("RGB")
    if image.width > 2400:
        scale = 2400 / image.width
        image = image.resize((2400, max(1, int(image.height * scale))))

    width, height = image.size
    footer_y = int(height * 0.80)
    left_bbox = footer_logo_bbox(image, 0, int(width * 0.245), footer_y)
    right_bbox = footer_logo_bbox(image, int(width * 0.795), width, footer_y)
    warnings: list[str] = []
    edge_margin = max(6, int(height * 0.006))

    for label, bbox in (("left", left_bbox), ("right", right_bbox)):
        if bbox is None:
            continue
        bottom_margin = height - bbox[3] - 1
        if bottom_margin < edge_margin:
            warnings.append(
                f"{label} footer logo is too close to the page bottom "
                f"(margin {bottom_margin}px; expected at least {edge_margin}px)."
            )

    if left_bbox and right_bbox:
        left_center = (left_bbox[1] + left_bbox[3]) / 2
        right_center = (right_bbox[1] + right_bbox[3]) / 2
        tolerance = max(4, int(height * 0.005))
        difference = abs(left_center - right_center)
        if difference > tolerance:
            warnings.append(
                "left institution logos and right conference logo are not center-aligned "
                f"(visible center difference {difference:.1f}px; tolerance {tolerance}px)."
            )

    return warnings


def report_visual_audit(preview: Path) -> list[str]:
    warnings = audit_footer_logo_alignment(preview)
    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    return warnings


def copy_file(source: Path, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / source.name
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)
    return target


def browser_screenshot_commands(browser: str, screenshot: Path, window_size: str, file_url: str) -> list[list[str]]:
    name = Path(browser).name.lower()
    if "firefox" in name:
        return [
            [
                browser,
                "--headless",
                f"--window-size={window_size}",
                "--screenshot",
                str(screenshot),
                file_url,
            ]
        ]
    return [
        [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--window-size={window_size}",
            f"--screenshot={screenshot}",
            file_url,
        ],
        [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--window-size={window_size}",
            f"--screenshot={screenshot}",
            file_url,
        ],
    ]


def render_html_browser_screenshot(
    html_path: Path,
    out_dir: Path,
    env: dict[str, str],
    timeout: int,
    window_size: str,
) -> Path | None:
    browsers = [
        shutil.which(name)
        for name in (
            "chromium",
            "chromium-browser",
            "google-chrome",
            "google-chrome-stable",
            "firefox",
        )
    ]
    screenshot = out_dir / f"{html_path.stem}.browser.png"
    file_url = html_path.resolve().as_uri()

    for browser in [path for path in browsers if path]:
        for cmd in browser_screenshot_commands(browser, screenshot, window_size, file_url):
            try:
                if screenshot.exists():
                    screenshot.unlink()
                result = run(cmd, html_path.parent, env, timeout=timeout)
            except RuntimeError as exc:
                print(f"Warning: browser screenshot failed: {exc}", file=sys.stderr)
                continue
            print(result.stdout[-2000:])
            if result.returncode == 0 and screenshot.exists() and screenshot.stat().st_size > 0:
                return screenshot
            print(f"Warning: browser screenshot command failed with exit {result.returncode}", file=sys.stderr)

    print(
        "Warning: no HTML render preview was produced; install WeasyPrint or a headless browser.",
        file=sys.stderr,
    )
    return None


def render_html(
    html_path: Path,
    out_dir: Path,
    dpi: int,
    env: dict[str, str],
    html_timeout: int,
    html_window_size: str,
) -> tuple[Path, Path | None, Path | None]:
    warn_placeholders(html_path)
    copied_html = copy_file(html_path, out_dir)
    pdf_path = out_dir / f"{html_path.stem}.pdf"

    try:
        from weasyprint import HTML  # type: ignore
    except Exception:
        print("Warning: WeasyPrint is not installed; trying a headless browser screenshot.", file=sys.stderr)
        preview = render_html_browser_screenshot(html_path, out_dir, env, html_timeout, html_window_size)
        return copied_html, None, preview

    try:
        HTML(filename=str(html_path), base_url=str(html_path.parent)).write_pdf(str(pdf_path))
    except Exception as exc:
        print(f"Warning: WeasyPrint failed ({exc}); trying a headless browser screenshot.", file=sys.stderr)
        preview = render_html_browser_screenshot(html_path, out_dir, env, html_timeout, html_window_size)
        return copied_html, None, preview

    try:
        preview = render_pdf(pdf_path, out_dir, dpi, env)
    except Exception as exc:
        print(f"Warning: PDF-to-PNG preview failed ({exc}); trying a headless browser screenshot.", file=sys.stderr)
        preview = render_html_browser_screenshot(html_path, out_dir, env, html_timeout, html_window_size)
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
    parser.add_argument(
        "--html-timeout",
        type=int,
        default=DEFAULT_HTML_TIMEOUT_SECONDS,
        help="Seconds before a headless browser HTML preview attempt is stopped.",
    )
    parser.add_argument(
        "--html-window-size",
        default="2200,1200",
        help="Browser screenshot viewport as WIDTH,HEIGHT.",
    )
    parser.add_argument("--skip-visual-audit", action="store_true", help="Do not run footer logo visual checks on PNG previews.")
    parser.add_argument("--strict-visual-audit", action="store_true", help="Exit nonzero when footer logo visual checks warn.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    env = clean_env()

    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        return 2

    visual_warnings: list[str] = []
    with tempfile.TemporaryDirectory(prefix="better-poster-") as tmp:
        try:
            source_root = prepare_input(input_path, Path(tmp), args.root)
            if source_root.suffix.lower() in HTML_SUFFIXES:
                if args.no_render:
                    copied_html = copy_file(source_root, out_dir)
                    print(f"HTML: {copied_html}")
                else:
                    html_out, pdf_out, preview = render_html(
                        source_root,
                        out_dir,
                        args.dpi,
                        env,
                        args.html_timeout,
                        args.html_window_size,
                    )
                    print(f"HTML: {html_out}")
                    if pdf_out:
                        print(f"PDF: {pdf_out}")
                    if preview:
                        print(f"Preview: {preview}")
                        if not args.skip_visual_audit:
                            visual_warnings.extend(report_visual_audit(preview))
            else:
                pdf_path = compile_latex(source_root, args.engine, args.passes, env)
                copied_pdf = copy_file(pdf_path, out_dir)
                print(f"PDF: {copied_pdf}")
                if not args.no_render:
                    preview = render_pdf(pdf_path, out_dir, args.dpi, env)
                    print(f"Preview: {preview}")
                    if not args.skip_visual_audit:
                        visual_warnings.extend(report_visual_audit(preview))
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
    if args.strict_visual_audit and visual_warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
