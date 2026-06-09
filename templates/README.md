# Poster templates

This directory contains the template entry points for Better Poster Skill.

## 风格 1：主结论看板

- `classic.tex`: LaTeX version for the claim-billboard layout.
- `classic.html`: standalone HTML version with the same 23/54/23 billboard structure.

Use this mode when the user wants a minimal, claim-first poster.

Design requirements:

- The center column is the dominant claim billboard. Use the default 23/54/23 width split, and widen the center before deleting essential conclusion content.
- The CUHK style1 skeleton is fixed by default: left `Introduction`/`Theory`, center claim+QR only, right evidence sections ending in `References`, and bottom institution/conference logo strips. Do not add visible meta instructions or "fill here" guidance text to the poster itself.
- The center claim typography matches the CUHK style1 example in `examples/cuhk_mock_style1/`: Inter/Arial/sans fallback, 900-equivalent weight, 76mm/86mm size-to-leading ratio, and the same font size/weight/leading on every center line. White / medium-gray / darker-gray groups must all appear, but one color does not need to equal one sentence.
- The generic style1 center, including concrete example posters, derives its claim primarily from the paper conclusion and keeps it concise, refined, and plain-language. It may use one sentence only when that fits the paper. Keep this maximum visible line budget: white tier 3 lines, middle gray tier 2 lines, lower gray tier 1 line. `\claimtiervspace` is only a same-baseline line break, so every center line keeps identical spacing.
- The QR/download row stays in the bottom band of the center column: QR on the left, a scan icon immediately to the QR's right, and matching text on the right. Align both the scan icon and text block to the QR centerline.
- Contact belongs inside the scan text, directly below the paper/OpenReview caption.
- The left column contains `Introduction` followed by `Theory`; do not print an affiliation line under author names. Keep the whole left sidebar high by reducing the side-column vertical margin; do not only compress the author-to-Introduction gap. The Theory section prioritizes full proposition statements, theorem statements, corollaries, assumptions, and key equations. Theorem/proposition card titles and bodies should be black; theorem cards are stronger by size/weight, proposition cards are smaller/subdued. Avoid lemma cards unless explicitly requested.
- Left-column citation labels use the information structure `[author + venue/journal + year]`, rendered for example as `(Shumailov et al., Nature 2024)`, instead of numeric bracket tags such as `[1]`.
- After every proposition, lemma, theorem, or corollary card, add one outside-the-box `\posterstatementsummary{...}` line that concisely explains in plain language what the statement says. These theory summaries should be visually more important than full-paper guidance notes: non-italic, darker, and slightly larger or heavier.
- Keep the left column bulletless, including theorem/proposition cards and any compact lists.
- End the left sidebar content with `\posterfullpapernote{For more methodology and theoretical details, please refer to the full paper.}`.
- The left column bottom contains institution branding only; no badge border, no separate institution-name text, and no contact line. Normalize affiliation sub-units to parent institutions, order logos by the first author's affiliation order, show all resolved logos, and left-align the strip with the title.
- If the first author has exactly one resolved institution, prefer a logo-with-name/wordmark asset and place it with `\institutionwordmarklogo{...}{...}`. Before rendering multiple logos, trim transparent or near-background whitespace with `scripts/normalize_institution_logos.py`; place pure emblems through the bounded logo helpers so their top and bottom edges align and the strip stays inside the panel.
- The center claim should use `\posterclaimblock{...}` by default. Keep all center lines at the same size and line spacing.
- The right column ends with a `References` section. Render reference entries lighter than body text, for example with `\posterreferences{...}`, then add `\posterfullpapernote{For additional experimental results, please refer to the full paper.}`.
- Conference/venue logos from `assets/conference-logos` belong at the bottom of the right column and should use the bounded `\conferencelogostrip{...}` / `\conferencelogo{...}{\institutionlogosize}` helpers. HTML may use SVG directly, while pdflatex should include renderer-verified PDF or high-resolution PNG conversions of SVG sources, for example `ICML-logo-pdflatex.pdf`, after previewing for incomplete-render issues.
- Title text, section headings, central billboard, and selected accents should use the selected institution palette. Use one strong primary color for single-color institutions; use a coordinated primary/secondary pair for dual-color institutions. Do not color theorem/proposition card titles.
- If a logo file is unavailable, the institution area stays blank.
- Text, figures, QR blocks, and logos must stay inside their own panel. If content overflows, remove lower-priority details rather than letting panels collide. Always inspect the rendered bottom edge; LaTeX may not warn when later content is clipped.
- Source figures should remain complete by default. Scale them, select fewer figures, or choose another complete figure before considering any crop.

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

Additional shared helpers include `qrcode{qr-path}{scan-icon-path}{scan text}`, `inlineqrcodewithicon{...}{...}{...}`, `institutionbrand{logo-path}{Institution Name}{width}`, `institutionlogorow{first-logo}{second-logo}{height}`, `institutionlogo{logo-path}{height}`, `institutionwordmarklogo{logo-path}{height}`, `institutionlogostrip{...}`, `conferencelogo{logo-path}{height}`, `conferencelogostrip{...}`, `posterclaimblock{claim lines}`, `posterclaim{line1}{line2}{line3}` for strict three-tier posters, `posterreferences{entries}`, `propositioncard{title}{body}`, `lemmacard{title}{body}`, `theoremcard{title}{body}`, `posterstatementsummary{summary}`, and `institutionpalette{primary-color}{secondary-color}`. Use `scripts/select_scan_icon.py` or `scripts/select_phone_icon.py` for `assets/scan-icons/`, `scripts/select_institution_logos.py` for `assets/institution-logos/top100-logo-bank/`, `scripts/normalize_institution_logos.py`, and `scripts/select_institution_palette.py` for `assets/institution-data/` before filling these helpers when affiliations are available.

## Preview commands

From the repository root:

```bash
python scripts/render_preview.py templates/classic.tex --out-dir /tmp/better-poster-preview/classic-latex
python scripts/render_preview.py templates/evenbetter.tex --out-dir /tmp/better-poster-preview/evenbetter-latex
python scripts/render_preview.py templates/classic.html --out-dir /tmp/better-poster-preview/classic-html
python scripts/render_preview.py templates/evenbetter.html --out-dir /tmp/better-poster-preview/evenbetter-html
```
