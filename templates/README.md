# Poster templates

This directory contains the template entry points for Better Poster Skill.

## Classic Better Poster

- `classic.tex`: LaTeX version, close to the Rafael Bailo / Mike Morrison #betterposter silhouette.
- `classic.html`: standalone HTML version with the same 20/60/20 billboard structure.

Use this mode when the user asks to replicate the Rafael Better Poster template or wants a minimal billboard-style poster.

## MIT-informed EvenBetter Poster

- `evenbetter.tex`: LaTeX version with a central claim, hero visual, evidence cards, and QR area.
- `evenbetter.html`: standalone HTML version of the same enhanced layout.

Use this mode when a technical poster needs visible central evidence, a hero figure, or a stronger conversation layer.

## Shared class

- `betterposter.cls`: lightweight class used by both LaTeX templates.

The class intentionally exposes a Better Poster-style interface:

```tex
\betterposter{main}{left}{right}
\maincolumn{claim}{qr-block}
```

## Preview commands

From the repository root:

```bash
python render_preview.py templates/classic.tex --out-dir build/classic-latex
python render_preview.py templates/evenbetter.tex --out-dir build/evenbetter-latex
python render_preview.py templates/classic.html --out-dir build/classic-html
python render_preview.py templates/evenbetter.html --out-dir build/evenbetter-html
```
