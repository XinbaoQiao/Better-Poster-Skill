#!/usr/bin/env python3
"""Prepare a LaTeX-safe poster logo and recolor white marks when needed.

SVG is not portable with pdflatex. This helper rasterizes SVG/raster input to a
PNG, trims simple backgrounds, and optionally tints high-luminance marks to the
poster theme color when they would be invisible on a light sidebar.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required: install the python3-pil or Pillow package.") from exc


RASTER_TIMEOUT_SECONDS = 45


def parse_hex_color(value: str) -> tuple[int, int, int]:
    text = value.strip().lstrip("#")
    if len(text) != 6:
        raise argparse.ArgumentTypeError(f"expected #RRGGBB color, got {value}")
    return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))


def luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = rgb
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def run(cmd: list[str]) -> None:
    try:
        result = subprocess.run(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            timeout=RASTER_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"command timed out: {' '.join(cmd)}") from exc
    if result.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{result.stdout}")


def raster_is_usable(path: Path) -> bool:
    try:
        with Image.open(path).convert("RGBA") as image:
            if image.width <= 1 or image.height <= 1:
                return False
            return image.getchannel("A").getbbox() is not None
    except Exception:
        return False


def unique_python_candidates() -> list[str]:
    candidates = [
        sys.executable,
        shutil.which("python3") or "",
        "/usr/bin/python3",
    ]
    seen: set[str] = set()
    unique: list[str] = []
    for candidate in candidates:
        if not candidate:
            continue
        path = shutil.which(candidate) if "/" not in candidate else candidate
        if not path or path in seen or not Path(path).exists():
            continue
        seen.add(path)
        unique.append(path)
    return unique


def rasterize_svg_with_python_gi(python: str, source: Path, out_path: Path, width: int) -> None:
    code = r"""
import sys
from pathlib import Path

import cairo
import gi

gi.require_version("Rsvg", "2.0")
from gi.repository import Rsvg

source = Path(sys.argv[1])
out_path = Path(sys.argv[2])
width = int(sys.argv[3])
handle = Rsvg.Handle.new_from_file(str(source))

try:
    ok, w0, h0 = handle.get_intrinsic_size_in_pixels()
except Exception:
    ok = False
if not ok or not w0 or not h0:
    dims = handle.get_dimensions()
    w0, h0 = dims.width, dims.height

height = max(1, round(width * h0 / w0))
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)
ctx.set_source_rgba(0, 0, 0, 0)
ctx.paint()

if hasattr(Rsvg, "Rectangle") and hasattr(handle, "render_document"):
    rect = Rsvg.Rectangle()
    rect.x = 0
    rect.y = 0
    rect.width = width
    rect.height = height
    handle.render_document(ctx, rect)
else:
    ctx.scale(width / w0, height / h0)
    handle.render_cairo(ctx)

out_path.parent.mkdir(parents=True, exist_ok=True)
surface.write_to_png(str(out_path))
"""
    run([python, "-c", code, str(source), str(out_path), str(width)])


def rasterize_svg(source: Path, out_path: Path, width: int) -> str:
    rsvg = shutil.which("rsvg-convert")
    if rsvg:
        run([rsvg, "-w", str(width), "-f", "png", "-o", str(out_path), str(source)])
        if raster_is_usable(out_path):
            return "rsvg-convert"

    cairosvg = shutil.which("cairosvg")
    if cairosvg:
        run([cairosvg, str(source), "-o", str(out_path), "--output-width", str(width)])
        if raster_is_usable(out_path):
            return "cairosvg"

    for python in unique_python_candidates():
        try:
            run([python, "-m", "cairosvg", str(source), "-o", str(out_path), "--output-width", str(width)])
            if raster_is_usable(out_path):
                return f"{Path(python).name}-cairosvg"
        except RuntimeError:
            pass
        try:
            rasterize_svg_with_python_gi(python, source, out_path, width)
            if raster_is_usable(out_path):
                return f"{Path(python).name}-gi-rsvg"
        except RuntimeError:
            pass

    magick = shutil.which("magick")
    if magick:
        run([magick, str(source), "-background", "none", "-resize", f"{width}x", str(out_path)])
        if raster_is_usable(out_path):
            return "imagemagick"
    convert = shutil.which("convert")
    if convert:
        run([convert, "-background", "none", str(source), "-resize", f"{width}x", str(out_path)])
        if raster_is_usable(out_path):
            return "imagemagick-convert"
    raise RuntimeError(
        "SVG input requires a usable renderer: rsvg-convert, CairoSVG, "
        "Python gi/librsvg+cairo, or ImageMagick with SVG support"
    )


def load_source(source: Path, width: int) -> tuple[Image.Image, str]:
    if source.suffix.lower() == ".svg":
        with tempfile.TemporaryDirectory(prefix="poster-logo-") as tmp:
            raster = Path(tmp) / "logo.png"
            renderer = rasterize_svg(source, raster, width)
            return Image.open(raster).convert("RGBA"), renderer
    image = Image.open(source).convert("RGBA")
    if image.width > width:
        ratio = width / image.width
        image = image.resize((width, max(1, int(image.height * ratio))), Image.Resampling.LANCZOS)
    return image, "pillow"


def content_mask(image: Image.Image, threshold: int) -> Image.Image:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    if alpha.getextrema()[0] < 250:
        return alpha.point(lambda value: 255 if value >= threshold else 0)

    pixels = rgba.load()
    width, height = rgba.size
    corners = [
        pixels[0, 0],
        pixels[width - 1, 0],
        pixels[0, height - 1],
        pixels[width - 1, height - 1],
    ]
    bg = tuple(sum(channel) // len(corners) for channel in zip(*corners))

    mask = Image.new("L", rgba.size, 0)
    mask_pixels = mask.load()
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a < threshold:
                continue
            delta = abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2])
            if delta > 42:
                mask_pixels[x, y] = 255
    return mask


def average_content_color(image: Image.Image, mask: Image.Image) -> tuple[int, int, int] | None:
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    mask_pixels = mask.load()
    totals = [0, 0, 0]
    count = 0
    for y in range(rgba.height):
        for x in range(rgba.width):
            if mask_pixels[x, y] == 0:
                continue
            r, g, b, _ = pixels[x, y]
            totals[0] += r
            totals[1] += g
            totals[2] += b
            count += 1
    if count == 0:
        return None
    return tuple(total // count for total in totals)


def trim_to_mask(image: Image.Image, mask: Image.Image, padding: int) -> tuple[Image.Image, Image.Image]:
    bbox = mask.getbbox()
    if not bbox:
        return image, mask
    left, top, right, bottom = bbox
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(image.width, right + padding)
    bottom = min(image.height, bottom + padding)
    return image.crop((left, top, right, bottom)), mask.crop((left, top, right, bottom))


def recolor(image: Image.Image, mask: Image.Image, color: tuple[int, int, int]) -> Image.Image:
    out = Image.new("RGBA", image.size, (*color, 0))
    solid = Image.new("RGBA", image.size, (*color, 255))
    out.alpha_composite(solid)
    out.putalpha(mask)
    return out


def tint_light_marks(image: Image.Image, color: tuple[int, int, int], threshold: float = 220) -> tuple[Image.Image, bool]:
    rgba = image.convert("RGBA")
    pixels = rgba.load()
    changed = False
    for y in range(rgba.height):
        for x in range(rgba.width):
            r, g, b, a = pixels[x, y]
            if a == 0:
                continue
            if luminance((r, g, b)) >= threshold:
                pixels[x, y] = (*color, a)
                changed = True
    return rgba, changed


def prepare_logo(
    source: Path,
    out_path: Path,
    theme: tuple[int, int, int],
    target_background: tuple[int, int, int],
    width: int,
    padding: int,
    force_tint: bool,
) -> str:
    image, renderer = load_source(source, width)
    mask = content_mask(image, threshold=8)
    image, mask = trim_to_mask(image, mask, padding)
    avg = average_content_color(image, mask)

    action = "preserved"
    if avg is not None:
        mark_lum = luminance(avg)
        bg_lum = luminance(target_background)
        if force_tint:
            image = recolor(image, mask, theme)
            action = "tinted-theme"
        elif bg_lum > 170:
            image, changed = tint_light_marks(image, theme)
            if changed:
                action = "tinted-light-marks"
            elif mark_lum > 210:
                image = recolor(image, mask, theme)
                action = "tinted-theme"
        elif mark_lum < 45 and bg_lum < 85:
            image = recolor(image, mask, (255, 255, 255))
            action = "tinted-white"
        elif image.getchannel("A").getextrema()[0] == 255:
            transparent = Image.new("RGBA", image.size, (255, 255, 255, 0))
            transparent.alpha_composite(image)
            image = transparent

    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)
    return f"{action}; renderer={renderer}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--theme", default="#750f6d", type=parse_hex_color)
    parser.add_argument("--target-background", default="#ffffff", type=parse_hex_color)
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--padding", type=int, default=8)
    parser.add_argument("--force-tint", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    action = prepare_logo(
        args.source,
        args.out,
        args.theme,
        args.target_background,
        args.width,
        args.padding,
        args.force_tint,
    )
    print(f"{args.source} -> {args.out} ({action})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
