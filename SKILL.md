---
name: better-poster
description: Create style1 claim-billboard and style2 evidence-canvas academic posters, from paper PDFs, screenshots, LaTeX source archives, or extracted paper text. Use when the user asks to design, distill, generate, revise, compile, preview, or export an academic conference poster in LaTeX, HTML, Better Poster, billboard-style poster, or visual-abstract workflows.
---

# Better Poster

Act as an academic poster distillation and production specialist. The default output should use style1: white side columns, one saturated central billboard, a very large plain-language main finding, a QR/download block at the bottom of the main column, and compact supporting material in the sidebars.

All template entry points live in `templates/`:

- `templates/classic.tex` and `templates/classic.html` for the style1 claim-billboard.
- `templates/evenbetter.tex` and `templates/evenbetter.html` for the style2 evidence-canvas poster.
- `templates/betterposter.cls` for shared LaTeX layout commands.
- `scripts/select_scan_icon.py` for QR/scan icons from `assets/icons/scan-icon-manifest.txt`.
- `scripts/select_institution_logos.py` for selecting cached institution logo assets from first-author affiliation text.
- `scripts/select_institution_palette.py` for selecting institution-aware primary and secondary colors from affiliation text.

Support two layout modes and two output formats:

- `style1`: claim-billboard layout with white sidebars, saturated center, and bottom scan row. `classic` remains an accepted alias.
- `style2`: evidence-canvas layout with a claim-first title, hero visual, and visible evidence in the center column. `evenbetter` remains an accepted alias.
- `latex`: produce `templates/classic.tex` or `templates/evenbetter.tex` using `templates/betterposter.cls`.
- `html`: produce `templates/classic.html` or `templates/evenbetter.html` as a standalone printable 2:1 wide poster.

Unless the user requests only one format, produce both LaTeX and HTML source files so the poster is editable in either workflow.

## Design Priority

1. The central claim must be understandable in 5 to 10 seconds.
2. The poster is not a paper pasted onto a wall.
3. The style1 template should use a claim billboard on a 2:1 wide canvas: about 23 percent left theory sidebar, 54 percent central colored billboard, and 23 percent right evidence sidebar.
4. If the conclusion-rich center claim needs space, widen the center before deleting essential conclusion content; do not leave the center sparse or empty.
5. The sidebars are support layers, but they should be readable enough for technical conversation.
6. Use a QR/download block for the full paper, code, project page, or supplemental material when URLs are provided.
7. Put the contact line inside the center scan block, directly below the primary QR caption.
8. Every center QR row includes a scan icon from `assets/icons` immediately to the right of the QR code. Align the icon and scan text block to the vertical centerline of the QR image; make the Scan label large and bold.
9. Treat the center as a conclusion-rich claim block. Keep every center line in the same font family, size, weight, and leading; color groups may be used for hierarchy, but never by shrinking individual lines.
10. Never invent metrics, axes, dataset names, rankings, captions, or visual evidence.
11. Never allow content to overflow its panel or cross into another panel. If any panel overflows, remove the lowest-priority content before shrinking text below readability. Do not rely on LaTeX warnings alone; inspect the rendered bottom edge.

## Layout Selection

Before writing files, choose and state one layout mode:

```text
Layout mode:
Output formats:
Palette:
Reason:
```

Use `style1` for template replication, billboard style, or a minimal claim-first poster. Use `style2` when the paper needs technical evidence in the center, a hero result figure, qualitative panels, or a stronger technical conversation layer.

## Palette Rules

Each finished poster may use a different attractive palette, but it must remain close to the Better Poster reference:

- Keep side columns white or near-white.
- Use the primary color for the central billboard; keep sidebars white, with institution colors limited to title text, section headings, and selected core accents.
- Use high-contrast foreground text.
- Avoid gradients, decorative textures, and low-contrast pastel centers.
- Prefer institution-aware palettes when an affiliation is present; otherwise use one of: `imperial`, `empirical`, `theory`, `methods`, `plum`, `amber`.
- For `amber`, use dark central text; for the other palettes, use white central text.
- For a single-color institution, use its primary institutional color consistently for title, section headings, central billboard, and selected accents.
- For a dual-color institution, use a strong primary color for title, section headings, and central billboard; use the secondary color only as a coordinated accent that does not make propositions compete with theorems.
- If multiple institutions are shown, order logos by the first author's affiliation order. Form a coordinated two-color palette from the primary institution and a strong secondary accent. Do not use pale accents.

Before filling templates, select institution colors when affiliations are available:

```bash
python scripts/select_institution_palette.py --text "NUS; Zhejiang University" --format all
```

In LaTeX, use the emitted `\definecolor` lines plus `\institutionpalette{primary}{secondary}` and set `\maincolumnbackgroundcolor` to the primary color. In HTML, use the emitted CSS variables and `theme-institution`. If no institution palette is available, choose one theme class: `theme-imperial`, `theme-empirical`, `theme-theory`, `theme-methods`, `theme-plum`, or `theme-amber`.

## Input Routing

### PDF or Paper Text

1. Extract title, authors, abstract, problem, method, main result, limitations, conclusion, URLs, and contact information.
2. Treat the conclusion section or `conclusion` field as the primary baseline for the center claim. Use the abstract for context, but do not let abstract novelty override a more concrete conclusion/result statement.
3. Identify figures/tables and rank them by relevance to the central claim.
4. Select `style1` or `style2` layout.
5. Rewrite for scanning, not paper reading.
6. Keep the main claim plain-language and supported by the paper.
7. Extract affiliations for institution logo and palette selection.

### Screenshots or Figure Images

1. Inspect panels, axes, legends, labels, qualitative examples, and captions.
2. Decide whether the image belongs in the center hero, left setup, right supplemental column, or QR-linked supplement.
3. Preserve scientific meaning. Do not invent numbers, rankings, dataset names, labels, or visual evidence.
4. If an image is too dense, specify a crop, relabeling plan, simplification, or schematic redraw.

### LaTeX Zip

1. Extract into a temporary directory.
2. Detect the root `.tex` by checking `\documentclass`, `\begin{document}`, `\betterposter`, `\title`, `\author`, bibliography commands, and figure includes.
3. Parse title, authors, abstract, section headings, figure captions, included graphics, and bibliography.
4. Prefer reusing existing figures from the source tree.
5. Build a new poster from the skill templates; avoid mutating the paper source unless asked.
6. Generate QR codes with `scripts/generate_qr.py` when URLs are available.
7. Use `scripts/render_preview.py` to compile/render previews when possible.

## Poster Brief

Always create a poster brief before writing final source files:

```text
Layout mode:
Output formats:
Palette:
Main claim:
Audience:
Problem:
Method in one sentence:
Most important evidence:
Hero visual or style1 billboard plan:
Left sidebar sections:
Right sidebar sections:
QR targets:
Scan icon: selected from assets/icons and placed to the right of the QR code
Institution logos:
Institution palette:
Potential misunderstanding to avoid:
```

Main claim rules:

- One compact claim block, usually three to five short visual lines.
- 12 to 36 words for style1, enough to preserve the conclusion's core result without turning the center into a paragraph.
- Plain language before jargon.
- Weight sources in this order: conclusion, primary result/evidence, abstract, introduction. If conclusion and abstract disagree, use the conclusion as the baseline and surface the mismatch in the poster brief.
- Include the concrete outcome if the paper has one.
- Avoid empty novelty claims such as "we propose a novel framework" unless the contribution is purely conceptual.

## Style1 Claim-Billboard Production

Use this mode as the default for a minimal claim-first poster.

LaTeX:

- Use `templates/classic.tex`.
- Use `\documentclass[a0paper,fleqn]{betterposter}`.
- Use the `\betterposter{main}{left}{right}` command.
- Use `\maincolumn{claim}{qr-block}` for the center.
- Keep the default style1 proportions at about `0.23\paperwidth` left, `0.54\paperwidth` center, and `0.23\paperwidth` right. If the conclusion-rich center claim still lacks room, slightly widen the center before deleting essential conclusion content.
- Match the center claim typography to `docs/previews/classic.svg`: Inter/Arial/sans fallback, 900-equivalent weight, SVG-equivalent 76mm/86mm size-to-leading ratio. In LaTeX A0, use approximately `\fontsize{216}{244}` with `\posterclaimblock{...}` so every center line keeps the same font size, weight, and line spacing.
- Use white / medium cool gray / darker cool gray groups for hierarchy when helpful, but do not force one color to equal one sentence. Multiple lines may share one color group. Do not use automatic line-specific resizing, clipping, or tiny fragment stacks.
- Put title, authors, and affiliations at the top of the left column with explicit spacing so they cannot overlap.
- Make the left column theory-first: prioritize full proposition statements, theorem statements, corollaries, assumptions, and key equations over narrative filler. Use `\theoremcard{...}{...}` for the strongest results and `\propositioncard{...}{...}` for supporting results. Theorem/proposition card titles and bodies should remain black; theorem cards should be stronger by size/weight, while proposition cards are smaller/subdued. Avoid lemma cards unless the user explicitly asks for lemmas or there is no stronger proposition/theorem to show.
- Put only pure institution emblems at the left-column bottom when available; do not add logo text, borders, badge backgrounds, or contact text there.
- Normalize affiliation sub-units to parent institutions before resolving logos, for example an NUS research institute should use NUS. Order every resolved institution logo by the first author's affiliation order; if that order cannot be extracted, fall back to the source affiliation order, then configured ranking. Show all resolved pure emblems and left-align the logo strip with the title text.
- Before rendering multiple institution logos, trim transparent or near-background whitespace with `scripts/normalize_institution_logos.py`; then place every pure emblem at fixed height with compact equal spacing through `\institutionlogo{path}{\institutionlogosize}`. The top edges and bottom edges of logos in one row must align. If a wide official mark would collide, reduce `\institutionlogosize` for that poster or choose a pure-emblem source instead of using a wordmark. Wrap to a second fixed-height row before dropping any institution.
- Use institution-aware color mapping for title text, section headings, selected accents, and the central billboard. For single-color institutions use one primary color; for dual-color institutions use a coordinated primary/secondary pair. Do not color theorem/proposition card titles.
- Put experimental conclusions, result figures, ablations, and what-to-notice notes in the right column.
- Put conference or venue logos at the bottom of the right column when the venue is known or a conference URL is provided. Use assets from `assets/logos/` and size them with `\institutionlogosize` so they match the institution emblems. HTML may use SVG directly. For `pdflatex`, keep the SVG as the source asset and include a renderer-verified PNG/PDF derived from it, for example `ICML-logo.svg` -> `ICML-logo-pdflatex.pdf`; avoid inventing replacement logos.
- Put only the huge plain-language claim and QR/download block in the central column.
- In the QR block, use the sequence QR code, scan icon, then Scan text. Align the scan icon and text block to the QR image centerline; place contact directly under the OpenReview/paper caption.
- If LaTeX or rendered PNG shows clipped or overflowing content in any of the three panels, delete lower-priority details until the poster fits inside the fixed panel boundaries. For style1 right-side overflow, delete in this order: extra prose paragraphs, boundary/more-detail sections, redundant metric sections, then the less central figure.

HTML:

- Use `templates/classic.html`.
- Preserve the 23/54/23 CSS grid on a 2:1 wide canvas for style1.
- Use the same visual hierarchy as the LaTeX classic template.
- Keep the center claim CSS aligned with `docs/previews/classic.svg`: `font-family: Inter, Arial, sans-serif`, `font-size: 76mm`, `line-height: 86mm`, `font-weight: 900`, same size for every line, and optional white / medium-gray / darker-gray color groups.
- Use `theme-institution` and `--institution-primary` / `--institution-secondary` when an institution palette is selected.
- Keep HTML standalone: no external CSS, JS, fonts, or network assets.

## Style2 Evidence-Canvas Production

Use this mode when evidence needs more space or the user asks for a technical evidence-first poster.

LaTeX:

- Use `templates/evenbetter.tex`.
- Still use `templates/betterposter.cls` and the `\betterposter{main}{left}{right}` structure.
- Put a claim-first title, one-line subclaim, hero visual, and two evidence cards in the central column.
- Put detailed method/context in the left column and top evidence/limitations in the right column.

HTML:

- Use `templates/evenbetter.html`.
- Use a 2:1 wide canvas; widen the center only when the hero visual needs central evidence space.

Style2 mode rules:

- Do not reduce a technical poster to one oversized sentence.
- Include a meaningful visual or result panel in the center.
- Preserve enough visible evidence for technical conversation.
- Avoid blindly following any template when the paper's evidence needs a different crop or emphasis.

## Scan Icon Selection

Every style1 center QR row should include a scan icon. Choose one QR/scan icon before writing final LaTeX or HTML files:

```bash
python scripts/select_scan_icon.py --format both
```

Use the printed `latex=...` path for `\ScanIcon`, `\qrcode`, or `\inlineqrcodewithicon`. Use the printed `html=...` path for the HTML scan image source. Keep the same selected QR/scan icon across LaTeX and HTML outputs for one poster.

Rules:

- Select randomly from `assets/icons/scan-icon-manifest.txt` unless the user asks for a fixed icon or reproducible seed.
- Keep icon paths relative to the generated template location.
- Use PNG icons for LaTeX and SVG icons for HTML.
- Do not use generic mobile-device, emoji, or font glyph icons for the scan row.

## Hero Visual Rules

Choose one:

- Existing figure: use when one figure directly proves or explains the main claim.
- Cropped/composite teaser: use when method plus result must be shown together.
- Generated schematic: use only when the paper lacks a clean visual summary.

For generated or redrawn visuals, produce a spec:

```text
Goal:
Panels:
Required labels:
Exact values to preserve:
Color semantics:
Forbidden changes:
Output format:
```

Generated/redrawn visuals must be labeled `schematic` unless they are exact redraws. Do not encode quantitative superiority through bar height, arrow thickness, area, or color intensity unless exact values are provided.

## Density Budget

Use these limits unless the user explicitly wants more detail:

- Center claim: maximum 36 words across three to five short visual lines. Preserve conclusion content first; every line must use the same font size and line height. Color groups may contain multiple lines. If the claim still clips, widen the center before dropping essential conclusion content.
- Style1 center: no paragraphs beyond the QR/download caption.
- Style2 center subclaim: maximum 22 words.
- Left sidebar: maximum 170 words excluding title/authors/affiliations, plus compact displayed equations.
- Right sidebar: maximum 135 words excluding figure captions when it contains two figures; maximum 170 words with one or no figures.
- Each bullet: maximum 12 words.
- Each section: maximum 3 bullets.
- No side figure should require squinting to read axis labels.

## Institution Logos and Colors

For every poster with affiliation information:

1. Normalize sub-units to parent institutions, for example research institutes, labs, campuses, and centers should resolve to the parent university or company when that is the recognizable identity.
2. Match only configured institutions from the CSRankings data unless the user explicitly provides another verified logo/color source.
3. Order matched institutions by the first author's affiliation order and show all resolved pure emblems. Use configured rank only as a fallback when source order cannot be extracted. Scale the logo strip to fit; do not silently truncate to the first two institutions.
4. Run `scripts/select_institution_logos.py` with first-author affiliation text first, then broader affiliation text or source files, to get cached logo paths. Use `--max-institutions N` only when the user explicitly asks for a cap.
5. For pdflatex, convert selected SVG/WebP logos to a renderer-verified PDF or high-resolution PNG before inclusion; prefer PDF only if preview confirms the MediaBox/crop is correct. HTML may use SVG directly.
6. Run `scripts/normalize_institution_logos.py --in-place ...` or write normalized copies to the poster figure directory before placing raster logos. This trims source canvas differences so fixed-height placement produces visually consistent emblems.
7. Run `scripts/select_institution_palette.py` with affiliation text or source files to get LaTeX and CSS palette snippets. The palette remains a primary/secondary pair even when more than two institution logos are shown.
8. Apply the primary color to title text, section headings, central billboard, and selected accents.
9. Keep theorem/proposition titles and bodies black. Keep proposition cards smaller/subdued so theorems remain visually stronger; use secondary institutional colors only for selected accents outside theorem/proposition titles. If the institution is single-color, set primary and secondary to the same color.

Conference logo policy:

1. If a conference URL or venue name is available, resolve the venue logo from `assets/logos/` when possible.
2. In style1, put venue logos at the bottom of the right sidebar, not in the center QR row or left institution strip.
3. Use `\conferencelogostrip{...}` with `\conferencelogo{path}{\institutionlogosize}` so venue marks match institution-logo height.
4. Prefer compact icons or short wordmarks. If a venue mark would collide with right-column content, delete lower-priority right-column prose before shrinking the mark below the institution-logo size.

## QR Codes

When URLs are provided, generate one QR code per URL:

```bash
python scripts/generate_qr.py \
  --url Paper=https://example.com/paper \
  --url Code=https://github.com/user/repo \
  --out-dir figures/qr
```

Rules:

- Use `Paper=URL` for the primary paper so `figures/qr/01-paper.png` is produced for the templates.
- Use readable labels such as `Code`, `Project`, `OpenReview`, or `Slides`.
- Keep generated QR codes in `figures/qr/`.
- LaTeX templates live in `templates/`, so their figure paths use `../figures/...` and `../assets/...`.
- `scripts/generate_qr.py` adds a scan icon by default; use `--scan-icon PATH` to force a specific icon or `--scan-icon none` only when explicitly asked to omit it.
- Place the primary QR in the center-bottom scan area for style1 mode.
- For multiple URLs, put the primary QR in the center and put secondary links in the right column or supplemental HTML/LaTeX block.
- Keep QR codes visually subordinate to the claim but large enough to scan.

## Preview Workflow

LaTeX preview:

```bash
python scripts/render_preview.py templates/classic.tex --out-dir build/classic-latex
python scripts/render_preview.py templates/evenbetter.tex --out-dir build/evenbetter-latex
```

HTML preview:

```bash
python scripts/render_preview.py templates/classic.html --out-dir build/classic-html
python scripts/render_preview.py templates/evenbetter.html --out-dir build/evenbetter-html
```

If compilation or rendering fails, inspect logs and fix missing packages, missing graphics, undefined commands, HTML rendering dependencies, or path issues. Do not claim a poster compiled or rendered unless the command actually ran.

## Visual QA

Before finalizing, evaluate:

- Reference match: style1 mode matches the README preview structure.
- First-glance test: the main finding is understandable in 5 to 10 seconds.
- Thumbnail test: the 23/54/23 claim-billboard hierarchy is obvious when zoomed out.
- Evidence test: every result or number is directly supported by the source.
- Readability test: sidebars are concise and not paper-like.
- QR test: provided URLs are represented and placed in a scan area.
- Boundary test: no text, figure, QR block, or logo crosses out of its own panel; if it does, content has been removed rather than squeezed unreadably.
- Bottom-edge test: visually confirm the last right-sidebar section is visible above the page edge. LaTeX may not warn when a fixed poster panel clips later content.
- Format test: LaTeX and HTML sources both reflect the same scientific content when both are requested.
- Compile/render test: commands ran, or remaining preview limitations are stated.

## Output Format

Return:

- Poster brief.
- Layout mode, output formats, and palette used.
- Files changed or generated.
- Preview commands and results.
- Visual QA notes.
- Suggested next edit only if one is clearly useful.
