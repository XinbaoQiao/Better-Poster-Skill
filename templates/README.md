# Poster templates

This directory contains the template entry points for Better Poster Skill.

## 风格 1：主结论看板

- `classic.tex`: LaTeX version for the claim-billboard layout.
- `classic.html`: standalone HTML version with the same 23/54/23 billboard structure.

Use this mode when the user wants a minimal, claim-first poster.

Design requirements:

- The center column is the dominant claim billboard. Use the default 23/54/23 width split, and widen the center before deleting essential conclusion content.
- The center claim typography matches `docs/previews/classic.svg`: Inter/Arial/sans fallback, 900-equivalent weight, 76mm/86mm size-to-leading ratio, and the same font size/weight/leading on every center line. White / medium-gray / darker-gray groups may be used, but one color does not need to equal one sentence.
- The QR/download row stays in the bottom band of the center column: QR on the left, a scan icon immediately to the QR's right, and matching text on the right. Align both the scan icon and text block to the QR centerline.
- Contact belongs inside the scan text, directly below the paper/OpenReview caption.
- The left column is theory-first: full proposition statements, theorem statements, corollaries, assumptions, and key equations before narrative filler. Theorem/proposition card titles and bodies should be black; theorem cards are stronger by size/weight, proposition cards are smaller/subdued. Avoid lemma cards unless explicitly requested.
- The left column bottom contains only pure institution emblems when available; no badge border, no institution-name text, and no contact line. Normalize affiliation sub-units to parent institutions, order logos by the first author's affiliation order, show all resolved logos, and left-align the strip with the title.
- Before rendering multiple logos, trim transparent or near-background whitespace with `scripts/normalize_institution_logos.py`; place pure emblems with fixed target height and compact equal spacing so their top and bottom edges align. If a wide mark would collide, reduce the poster logo size or use a pure-emblem source rather than a wordmark.
- The center claim should use `\posterclaimblock{...}` by default. Keep all center lines at the same size and line spacing; use three to five short lines when the conclusion needs more content.
- Conference/venue logos from `assets/logos` belong at the bottom of the right column and should use the same target height as institution emblems. HTML may use SVG directly, while pdflatex should include renderer-verified PDF or high-resolution PNG conversions of SVG sources, for example `ICML-logo-pdflatex.pdf`, after previewing for crop or incomplete-render issues.
- Title text, section headings, central billboard, and selected accents should use the selected institution palette. Use one strong primary color for single-color institutions; use a coordinated primary/secondary pair for dual-color institutions. Do not color theorem/proposition card titles.
- If a logo file is unavailable, the institution area stays blank.
- Text, figures, QR blocks, and logos must stay inside their own panel. If content overflows, remove lower-priority details rather than letting panels collide. Always inspect the rendered bottom edge; LaTeX may not warn when later content is clipped.

## 风格 2：证据画布

- `evenbetter.tex`: LaTeX version with a central claim, hero visual, evidence cards, and QR area.
- `evenbetter.html`: standalone HTML version of the same enhanced layout.

Use this mode when a technical poster needs visible central evidence, a hero figure, or a stronger conversation layer.

Design requirements:

- Preserve the appropriate 2:1 wide canvas hierarchy for the selected mode.
- The center column adds a claim-first title, hero visual, evidence cards, and a bottom-centered QR/download block.
- The left column bottom should use the same pure-emblem branding rule unless the user requests a text badge.

## Shared class

- `betterposter.cls`: lightweight class used by both LaTeX templates.

The class intentionally exposes a Better Poster-style interface with `betterposter{main}{left}{right}` and `maincolumn{claim}{qr-block}`.

Additional shared helpers include `qrcode{qr-path}{scan-icon-path}{scan text}`, `inlineqrcodewithicon{...}{...}{...}`, `institutionbrand{logo-path}{Institution Name}{width}`, `institutionlogorow{first-logo}{second-logo}{height}`, `institutionlogo{logo-path}{height}`, `institutionlogostrip{...}`, `conferencelogo{logo-path}{height}`, `conferencelogostrip{...}`, `posterclaimblock{claim lines}`, `posterclaim{line1}{line2}{line3}` for strict three-tier posters, `propositioncard{title}{body}`, `theoremcard{title}{body}`, and `institutionpalette{primary-color}{secondary-color}`. Use `scripts/select_scan_icon.py`, `scripts/select_institution_logos.py`, `scripts/normalize_institution_logos.py`, and `scripts/select_institution_palette.py` before filling these helpers when affiliations are available.

## Preview commands

From the repository root:

```bash
python scripts/render_preview.py templates/classic.tex --out-dir build/classic-latex
python scripts/render_preview.py templates/evenbetter.tex --out-dir build/evenbetter-latex
python scripts/render_preview.py templates/classic.html --out-dir build/classic-html
python scripts/render_preview.py templates/evenbetter.html --out-dir build/evenbetter-html
```
