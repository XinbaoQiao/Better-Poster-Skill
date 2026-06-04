# Poster templates

This directory contains the template entry points for Better Poster Skill.

## Classic Better Poster

- `classic.tex`: LaTeX version, close to the Rafael Bailo / Mike Morrison #betterposter silhouette.
- `classic.html`: standalone HTML version with the same 20/60/20 billboard structure.

Use this mode when the user asks to replicate the Rafael Better Poster template or wants a minimal billboard-style poster.

Design requirements:

- The center column is the dominant claim billboard.
- The QR/download block is centered in the bottom band of the center column.
- The left column bottom contains the institution logo slot, institution name, and contact line.
- If a logo file is unavailable, the template still renders a visible institution-logo placeholder plus the institution name.

## MIT-informed EvenBetter Poster

- `evenbetter.tex`: LaTeX version with a central claim, hero visual, evidence cards, and QR area.
- `evenbetter.html`: standalone HTML version of the same enhanced layout.

Use this mode when a technical poster needs visible central evidence, a hero figure, or a stronger conversation layer.

Design requirements:

- Preserve the 20/60/20 Better Poster silhouette.
- The center column adds a claim-first title, hero visual, evidence cards, and a bottom-centered QR/download block.
- The left column bottom contains the same institution logo + institution name + contact brand block.

## Shared class

- `betterposter.cls`: lightweight class used by both LaTeX templates.

The class intentionally exposes a Better Poster-style interface with `betterposter{main}{left}{right}` and `maincolumn{claim}{qr-block}`.

Additional shared helpers include `qrcode{...}{...}{...}` and `institutionbrand{logo-path}{Institution Name}{width}`.

## Preview commands

From the repository root:

```bash
python render_preview.py templates/classic.tex --out-dir build/classic-latex
python render_preview.py templates/evenbetter.tex --out-dir build/evenbetter-latex
python render_preview.py templates/classic.html --out-dir build/classic-html
python render_preview.py templates/evenbetter.html --out-dir build/evenbetter-html
```
