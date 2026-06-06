#!/usr/bin/env python3
"""Generate poster QR codes with site logos and a LaTeX include snippet.

The script uses local LaTeX `qrcode` as the QR encoder so it does not require a
Python QR package. It rasterizes SVG logos only at generation time, then uses
Pillow to paste a centered logo tile.

With `--icon auto`, recognizable paper URLs such as OpenReview, ICML, ICLR, and
NeurIPS are rendered with a centered site icon. OpenReview uses the project
asset under `assets/site-icons/openreview.png` by default; missing known-site
icons are treated as asset errors instead of silently producing bare QR codes.
"""

from __future__ import annotations

import argparse
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image


PROXY_ENV_KEYS = (
    "http_proxy",
    "https_proxy",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "all_proxy",
    "ALL_PROXY",
)

SITE_LOGO_CANDIDATES = {
    "openreview": ("openreview.png", "OpenReview.png", "review.png", "Review.png"),
    "icml": ("ICML-logo.svg", "ICML.svg", "icml.svg"),
    "iclr": ("iclr.svg", "ICLR.svg"),
    "neurips": ("NeurIPS.svg", "neurips.svg"),
}

SCAN_ICON_MANIFEST = "scan-icon-manifest.txt"


@dataclass(frozen=True)
class QRItem:
    label: str
    url: str
    icon_key: str | None


def clean_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in PROXY_ENV_KEYS:
        env.pop(key, None)
    return env


def run(cmd: list[str], cwd: Path, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def latex_escape(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text)


def qr_latex_arg(text: str) -> str:
    if any(ch in text for ch in "{}\n\r"):
        raise ValueError("URLs containing braces or newlines are not supported by the LaTeX QR backend.")
    return text


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return slug or "qr"


def detect_icon_key(url: str, label: str = "") -> str | None:
    parsed = urlparse(url)
    haystack = " ".join([parsed.netloc.lower(), parsed.path.lower(), label.lower()])
    if "openreview" in haystack:
        return "openreview"
    if "iclr" in haystack:
        return "iclr"
    if "neurips" in haystack or "nips.cc" in haystack:
        return "neurips"
    if "icml" in haystack or "mlr.press" in haystack:
        return "icml"
    return None


def default_label(url: str, icon_key: str | None) -> str:
    if icon_key == "openreview":
        return "OpenReview"
    if icon_key == "icml":
        return "ICML"
    if icon_key == "iclr":
        return "ICLR"
    if icon_key == "neurips":
        return "NeurIPS"
    host = urlparse(url).netloc.removeprefix("www.")
    return host or "Link"


def parse_item(raw: str, explicit_icon: str | None) -> QRItem:
    label = ""
    url = raw.strip()
    if "=" in raw and not raw.lstrip().startswith(("http://", "https://")):
        label, url = raw.split("=", 1)
        label = label.strip()
        url = url.strip()
    icon_key = explicit_icon if explicit_icon != "auto" else detect_icon_key(url, label)
    if icon_key and icon_key not in SITE_LOGO_CANDIDATES:
        icon_key = None
    return QRItem(label=label or default_label(url, icon_key), url=url, icon_key=icon_key)


def render_base_qr(url: str, out_png: Path, size_px: int, env: dict[str, str]) -> None:
    pdflatex = shutil.which("pdflatex")
    pdftoppm = shutil.which("pdftoppm")
    if not pdflatex:
        raise RuntimeError("pdflatex is required for QR generation.")
    if not pdftoppm:
        raise RuntimeError("pdftoppm is required to render QR PNGs.")

    with tempfile.TemporaryDirectory(prefix="better-poster-qr-") as tmp:
        work = Path(tmp)
        tex = work / "qr.tex"
        tex.write_text(
            "\n".join(
                [
                    r"\documentclass{article}",
                    r"\usepackage[paperwidth=2.4in,paperheight=2.4in,margin=0in]{geometry}",
                    r"\usepackage{qrcode}",
                    r"\pagestyle{empty}",
                    r"\begin{document}",
                    r"\noindent\centering\qrcode[height=2.4in,level=H]{"
                    + qr_latex_arg(url)
                    + "}",
                    r"\end{document}",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        for _ in range(2):
            result = run(
                [pdflatex, "-interaction=nonstopmode", "-halt-on-error", "qr.tex"],
                work,
                env,
            )
            if result.returncode != 0:
                raise RuntimeError("pdflatex failed while generating QR:\n" + result.stdout[-4000:])
        result = run(
            [pdftoppm, "-png", "-singlefile", "-r", "600", str(work / "qr.pdf"), str(work / "qr")],
            work,
            env,
        )
        if result.returncode != 0:
            raise RuntimeError("pdftoppm failed while rendering QR:\n" + result.stdout[-2000:])

        base = Image.open(work / "qr.png").convert("RGBA")
        cropped = crop_white(base)
        resized = cropped.resize((size_px, size_px), Image.Resampling.NEAREST)
        resized.save(out_png)


def crop_white(image: Image.Image) -> Image.Image:
    rgb = image.convert("RGB")
    pixels = rgb.load()
    width, height = rgb.size
    xs: list[int] = []
    ys: list[int] = []
    for y in range(height):
        for x in range(width):
            if pixels[x, y] != (255, 255, 255):
                xs.append(x)
                ys.append(y)
    if not xs:
        return image
    pad = max(8, min(width, height) // 40)
    left = max(0, min(xs) - pad)
    top = max(0, min(ys) - pad)
    right = min(width, max(xs) + pad)
    bottom = min(height, max(ys) + pad)
    return image.crop((left, top, right, bottom))


def load_logo_image(logo_path: Path, env: dict[str, str]) -> Image.Image:
    logo_path = logo_path.resolve()
    if logo_path.suffix.lower() == ".svg":
        convert = shutil.which("convert")
        if not convert:
            raise RuntimeError(f"ImageMagick convert is required to rasterize SVG logos: {logo_path}")
        with tempfile.TemporaryDirectory(prefix="better-poster-logo-") as tmp:
            out_png = Path(tmp) / "logo.png"
            result = run(
                [
                    convert,
                    "-background",
                    "none",
                    "-density",
                    "600",
                    str(logo_path),
                    "-trim",
                    "+repage",
                    "-resize",
                    "430x430",
                    "-gravity",
                    "center",
                    "-extent",
                    "512x512",
                    f"PNG32:{out_png}",
                ],
                logo_path.parent,
                env,
            )
            if result.returncode != 0:
                raise RuntimeError(f"Failed to rasterize SVG logo {logo_path}:\n{result.stdout[-2000:]}")
            return Image.open(out_png).convert("RGBA")
    return Image.open(logo_path).convert("RGBA")


def logo_candidate_paths(icon_key: str, logos_dir: Path, site_icons_dir: Path) -> list[Path]:
    candidates = [site_icons_dir / name for name in SITE_LOGO_CANDIDATES[icon_key]]
    candidates.extend(logos_dir / name for name in SITE_LOGO_CANDIDATES[icon_key])
    return candidates


def resolve_site_icon(item: QRItem, logos_dir: Path, site_icons_dir: Path, env: dict[str, str]) -> Image.Image | None:
    if not item.icon_key:
        return None
    candidates = logo_candidate_paths(item.icon_key, logos_dir, site_icons_dir)
    for logo_path in candidates:
        if logo_path.exists():
            return load_logo_image(logo_path, env)
    checked = ", ".join(str(path) for path in candidates)
    raise FileNotFoundError(f"Missing center icon asset for {item.icon_key}; checked: {checked}")


def paste_logo(qr_path: Path, logo_image: Image.Image, icon_scale: float) -> None:
    qr = Image.open(qr_path).convert("RGBA")
    icon = logo_image.convert("RGBA")
    qr_size = qr.size[0]
    tile_size = int(qr_size * icon_scale)
    padding = max(8, int(tile_size * 0.08))
    card_size = tile_size + 2 * padding

    icon = icon.resize((tile_size, tile_size), Image.Resampling.LANCZOS)
    card = Image.new("RGBA", (card_size, card_size), (255, 255, 255, 255))
    card.alpha_composite(icon, (padding, padding))
    x = (qr.size[0] - card_size) // 2
    y = (qr.size[1] - card_size) // 2
    qr.alpha_composite(card, (x, y))
    qr.save(qr_path)


def manifest_phone_icons(icons_dir: Path) -> list[Path] | None:
    manifest = icons_dir / SCAN_ICON_MANIFEST
    if not manifest.exists():
        return None
    icons = []
    for raw in manifest.read_text(encoding="utf-8").splitlines():
        stem = raw.split("#", 1)[0].strip()
        if not stem:
            continue
        png = icons_dir / f"{stem}.png"
        if png.is_file():
            icons.append(png)
    return icons


def discover_phone_icons(icons_dir: Path) -> list[Path]:
    manifest_icons = manifest_phone_icons(icons_dir)
    if manifest_icons is not None:
        return manifest_icons
    return sorted(path for path in icons_dir.glob("*-white.png") if path.is_file())


def resolve_phone_icon(phone_icon: str, icons_dir: Path, icon_prefix: str, seed: str | None) -> str:
    if phone_icon == "none":
        return ""
    if phone_icon != "auto":
        return phone_icon
    icons = discover_phone_icons(icons_dir)
    if not icons:
        return ""
    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    selected = rng.choice(icons)
    return f"{icon_prefix.rstrip('/')}/{selected.name}"


def write_snippet(items: list[tuple[QRItem, Path]], snippet_path: Path, tex_prefix: str, phone_icon: str) -> None:
    lines = [
        r"% Generated by scripts/generate_qr.py. Edit URLs and regenerate instead of editing manually.",
    ]
    for idx, (item, path) in enumerate(items):
        if idx:
            lines.append(r"\par\vspace{0.18in}")
        rel_path = f"{tex_prefix.rstrip('/')}/{path.name}"
        lines.extend(
            [
                rf"\qrcode{{{rel_path}}}{{{phone_icon}}}{{%",
                rf"{{\fontsize{{32}}{{37}}\selectfont\bfseries Scan}}",
                r"\par\vspace{0.04in}",
                rf"{{\fontsize{{22}}{{27}}\selectfont {latex_escape(item.label)}}}",
                r"}",
            ]
        )
    lines.extend([""])
    snippet_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", action="append", required=True, help="URL or Label=URL. Repeat for multiple QR codes.")
    parser.add_argument("--out-dir", default="figures/qr", help="Output directory for PNGs and qr-snippet.tex.")
    parser.add_argument("--logos-dir", default="assets/conference-logos", help="Directory containing venue logo assets such as ICML/ICLR/NeurIPS SVG logos.")
    parser.add_argument("--site-icons-dir", default="assets/site-icons", help="Directory containing URL-site center icons such as openreview.png.")
    parser.add_argument("--icon", default="auto", help="auto, none, or one of: openreview, icml, iclr, neurips.")
    parser.add_argument("--size", type=int, default=1200, help="Output QR image size in pixels.")
    parser.add_argument("--icon-scale", type=float, default=0.18, help="Center icon size as fraction of QR width.")
    parser.add_argument("--tex-prefix", default="figures/qr", help="Path prefix used inside generated LaTeX snippet.")
    parser.add_argument("--scan-icon", "--phone-icon", dest="phone_icon", default="auto", help="none, auto, or a LaTeX path to a PNG/PDF QR/scan icon.")
    parser.add_argument("--scan-icons-dir", "--phone-icons-dir", dest="phone_icons_dir", default="assets/scan-icons", help="Directory with QR/scan PNG icons used by --scan-icon auto.")
    parser.add_argument("--scan-icon-prefix", "--phone-icon-prefix", dest="phone_icon_prefix", default="../assets/scan-icons", help="Path prefix written into the LaTeX snippet for auto-selected QR/scan icons.")
    parser.add_argument("--scan-icon-seed", "--phone-icon-seed", dest="phone_icon_seed", help="Optional seed for reproducible QR/scan icon selection.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.icon not in {"auto", "none", *SITE_LOGO_CANDIDATES.keys()}:
        print(f"Unsupported --icon value: {args.icon}", file=sys.stderr)
        return 2

    env = clean_env()
    out_dir = Path(args.out_dir)
    logos_dir = Path(args.logos_dir)
    site_icons_dir = Path(args.site_icons_dir)
    phone_icon = resolve_phone_icon(
        args.phone_icon,
        Path(args.phone_icons_dir),
        args.phone_icon_prefix,
        args.phone_icon_seed,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    items: list[tuple[QRItem, Path]] = []

    try:
        for index, raw in enumerate(args.url, start=1):
            item = parse_item(raw, explicit_icon=None if args.icon == "none" else args.icon)
            filename = f"{index:02d}-{slugify(item.label)}.png"
            qr_path = out_dir / filename
            render_base_qr(item.url, qr_path, args.size, env)
            logo_image = resolve_site_icon(item, logos_dir, site_icons_dir, env)
            if logo_image:
                paste_logo(qr_path, logo_image, args.icon_scale)
            items.append((item, qr_path))
        write_snippet(items, out_dir / "qr-snippet.tex", args.tex_prefix, phone_icon)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    for _, path in items:
        print(path)
    print(out_dir / "qr-snippet.tex")
    if phone_icon:
        print(f"Scan icon: {phone_icon}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
