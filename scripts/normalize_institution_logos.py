#!/usr/bin/env python3
"""Trim institution logo whitespace before fixed-height poster placement."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def alpha_bbox(image: Image.Image, alpha_threshold: int) -> tuple[int, int, int, int] | None:
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    if alpha.getextrema()[0] < alpha_threshold:
        mask = alpha.point(lambda value: 255 if value >= alpha_threshold else 0)
        return mask.getbbox()
    return None


def background_bbox(image: Image.Image, color_threshold: int) -> tuple[int, int, int, int] | None:
    rgba = image.convert("RGBA")
    width, height = rgba.size
    pixels = rgba.load()
    corners = [
        pixels[0, 0],
        pixels[width - 1, 0],
        pixels[0, height - 1],
        pixels[width - 1, height - 1],
    ]
    bg = tuple(sum(channel) // len(corners) for channel in zip(*corners))

    xs: list[int] = []
    ys: list[int] = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a < 16:
                continue
            delta = abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2])
            if delta > color_threshold:
                xs.append(x)
                ys.append(y)

    if not xs:
        return None
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def content_bbox(image: Image.Image, alpha_threshold: int, color_threshold: int) -> tuple[int, int, int, int]:
    bbox = alpha_bbox(image, alpha_threshold)
    if bbox:
        return bbox

    bbox = background_bbox(image, color_threshold)
    if bbox:
        left, top, right, bottom = bbox
        width, height = image.size
        if (right - left) * (bottom - top) < width * height * 0.98:
            return bbox

    return 0, 0, image.width, image.height


def normalize(path: Path, out_path: Path, alpha_threshold: int, color_threshold: int, padding: int) -> None:
    image = Image.open(path).convert("RGBA")
    left, top, right, bottom = content_bbox(image, alpha_threshold, color_threshold)
    cropped = image.crop((left, top, right, bottom))

    if padding > 0:
        canvas = Image.new("RGBA", (cropped.width + padding * 2, cropped.height + padding * 2), (255, 255, 255, 0))
        canvas.alpha_composite(cropped, (padding, padding))
        cropped = canvas

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(out_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logos", nargs="+", type=Path, help="PNG/JPG/WebP institution logos to normalize.")
    parser.add_argument("--out-dir", type=Path, help="Write normalized files here instead of modifying in place.")
    parser.add_argument("--in-place", action="store_true", help="Overwrite input files after trimming.")
    parser.add_argument("--alpha-threshold", type=int, default=8)
    parser.add_argument("--color-threshold", type=int, default=42)
    parser.add_argument("--padding", type=int, default=0, help="Transparent padding in pixels after trimming.")
    args = parser.parse_args()

    if bool(args.out_dir) == bool(args.in_place):
        parser.error("Use exactly one of --out-dir or --in-place.")

    for logo in args.logos:
        if args.in_place:
            out_path = logo
        else:
            out_path = args.out_dir / logo.name
        normalize(logo, out_path, args.alpha_threshold, args.color_threshold, args.padding)
        print(f"{logo} -> {out_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
