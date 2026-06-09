---
name: better-poster
description: Create or revise academic conference posters in Better Poster style from paper PDFs, screenshots, LaTeX source archives, extracted paper text, or existing poster files. Use for LaTeX/HTML poster design, compilation, preview, QR/logo placement, visual QA, and claim-billboard or evidence-canvas poster workflows.
---

# Better Poster

Produce editable academic posters with a 2:1 wide canvas. Default to `style1`
unless the paper needs central evidence.

## Repository Map

- `templates/`: source templates and shared LaTeX class.
- `examples/`: checked-in successful poster examples and their source assets; use this as a growing reference library for future papers.
- `assets/`: reusable scan icons, institution logo assets, conference/venue logos, and `assets/institution-data/` JSON seed data.
- `scripts/`: deterministic helpers for QR codes, logos, palettes, and previews.
- Preview output defaults to the system temp directory, usually `/tmp/better-poster-preview/`; never treat preview output as source.

Core entry points:

- `templates/classic.tex` and `templates/classic.html`: style1 claim billboard.
- `templates/evenbetter.tex` and `templates/evenbetter.html`: style2 evidence canvas.
- `templates/betterposter.cls`: shared LaTeX layout commands.
- `scripts/render_preview.py`: compile/render local previews.

## Operating Rules

1. Choose and state layout mode, output format, palette, and reason before writing final sources.
2. Before creating a poster for a new paper, inspect `examples/` for the closest successful prior poster and reuse its proven layout patterns, density, wording style, logo handling, and visual hierarchy when appropriate.
3. Treat `examples/` as an expanding reference library, not as fixed template source: borrow structure and design decisions, but never copy scientific claims, numbers, citations, or figures unless they are supported by the current paper.
4. Concrete paper examples inherit the global template constraints unless the user explicitly requests a narrower task-specific override.
5. Prefer `style1` for claim-first posters; use `style2` only when central evidence or a hero figure is needed.
6. Use both LaTeX and HTML unless the user asks for one format.
7. Do not invent metrics, datasets, axes, rankings, captions, or visual evidence.
8. Keep paths relative. Do not write machine-specific absolute paths into generated poster files.
9. Never claim compilation/rendering succeeded unless the command actually ran.
10. If content clips or overflows, remove lower-priority content before shrinking text below readability.

## CUHK Style1 Contract

Use this as the default reusable foundation unless the user explicitly asks for another style:

- Keep the CUHK-style 2:1 wide canvas with a fixed asymmetric 25/54/21 left/center/right structure.
- Keep the whole side-column content high by using a compact side-column vertical margin; do not solve vertical placement by only compressing the author-to-Introduction gap.
- Keep visible template text generic and academic. Do not insert meta instructions such as "fill this section", "replace this text", or "method goes here".
- Keep all source paths relative and reusable across `templates/`, `examples/`, and new paper folders.
- Treat specific paper examples as applications of the global contract; do not write task-specific overrides into the general template unless the user explicitly asks to make them global.

## Style1 Rules

Use `templates/classic.tex` and/or `templates/classic.html`.

Layout:

- Preserve the 25/54/21 left/center/right structure on a 2:1 wide canvas.
- Center column contains only the huge claim block and bottom QR/download row.
- Left column contains `Introduction` followed by `Theory`.
- Right column contains method/results/evidence sections and ends with `References`.

Center claim:

- It must be understandable in 5 to 10 seconds.
- Hard gate: the center claim alone must let a viewer identify the poster's core theme and main contribution at a glance. If it does not answer "what is this poster about?" and "what is the main insight/contribution?", rewrite it before editing side content.
- Use `\posterclaimblock{...}` in LaTeX.
- Keep all center lines the same font size, weight, and leading.
- Derive the center claim primarily from the paper conclusion or lessons-learned section; use primary result evidence only to make the conclusion concrete, and use abstract/introduction only when the conclusion is unavailable or vague.
- Make the center wording concise, refined, and plain-language. Prefer the shortest wording that preserves the conclusion.
- Avoid generic effect-only slogans. Include the paper's key condition, mechanism, reversal, or implication when that is needed for the main contribution to be immediately clear.
- For insight-driven papers, prefer wording that exposes the paper's non-obvious tension, such as when an expected remedy becomes the failure mode.
- Prefer one plain-language sentence only when it naturally carries the conclusion; do not force a one-sentence claim when the paper needs more structure.
- Avoid adding mechanism, caveat, or synthesis phrases to the center unless they materially change the conclusion.
- Use all three white / middle gray / lower gray tiers for style1 hierarchy.
- Generic style1 tier budget: white max 3 lines, middle gray max 2 lines, lower gray max 1 line.
- Apply this tier budget to concrete paper examples by default; override only when the user explicitly requests a task-specific allocation.
- Use `\claimtiervspace` only as a same-baseline line break between color tiers; do not add extra vertical spacing between center lines.
- The physical tier budget is a visual constraint, not a semantic rule: one color tier does not have to equal one sentence.

Left column:

- Title and authors go at the top.
- Do not print an affiliation line under author names.
- Show institution identity only through the bottom logo strip.
- Keep the left column bulletless, including theorem/proposition cards.
- `Introduction` gives brief background.
- Move the left sidebar upward by reducing the side-column vertical margin; do not fake this by only compressing the author-to-Introduction gap.
- Format left-column citation labels with the information structure `[author + venue/journal + year]`, rendered for example as `(Shumailov et al., Nature 2024)`, not numeric tags such as `[1]`.
- `Theory` prioritizes propositions, theorems, assumptions, corollaries, and key equations.
- Use `\theoremcard{...}{...}` for strongest theory and `\propositioncard{...}{...}` for supporting statements.
- Use the asymmetric style1 width split with a wider left column when theory is present; theorem/proposition title legibility takes priority over matching left and right widths.
- Keep proposition, theorem, lemma, and corollary card titles on one physical line at a consistent title font size. Shorten labels or use the wider left column before relying on per-title scaling.
- After every proposition, lemma, theorem, or corollary card, add one outside-the-box plain-language line with `\posterstatementsummary{...}` explaining what the statement says.
- Keep each theory summary line concise, refined, and easy to understand; it should explain the statement, not add new technical content.
- Style theory summary lines as more important than full-paper guidance notes: non-italic, darker, and slightly larger or heavier than `\posterfullpapernote{...}`.
- End visible content with `\posterfullpapernote{For more methodology and theoretical details, please refer to the full paper.}`.

Right column:

- Put experimental conclusions, result figures, ablations, and what-to-notice notes here.
- Use bullet lists for `Takeaway` or `Experimental Takeaway` sections; keep each bullet concise and directly tied to the shown evidence or one explicitly named additional result.
- Append final section `References` after all other right-column sections.
- Render reference entries lighter than body text, for example with `\posterreferences{...}`.
- After references, add `\posterfullpapernote{For additional experimental results, please refer to the full paper.}`.
- Put conference/venue logos at the bottom when known.

QR row:

- Sequence is QR code, scan icon, then scan text.
- Contact belongs inside the scan text, directly below the primary caption.
- Select paired PNG/SVG scan icons with `scripts/select_scan_icon.py` (compatibility wrapper) or `scripts/select_phone_icon.py`; both read from `assets/scan-icons/`.
- If an OpenReview URL is available, make it the primary QR target and label it `OpenReview=...`; the QR image must include the OpenReview/site icon in the center.
- Generate QR images with `scripts/generate_qr.py --icon auto`; do not manually replace an OpenReview QR with a plain QR that lacks a center icon.
- OpenReview center icons come from `assets/site-icons/openreview.png`. If the asset is missing, add or restore that icon before regenerating QR images.

## Style2 Rules

Use `templates/evenbetter.tex` and/or `templates/evenbetter.html`.

- Keep the same wide-canvas hierarchy.
- Center contains claim-first title, concise subclaim, hero visual, evidence cards, and QR area.
- Use only when visible central evidence is necessary.
- Do not reduce a technical evidence poster to one oversized sentence.

## Input Workflow

Paper PDF/text:

1. Extract title, authors, abstract, method, results, conclusion, limitations, URLs, contact, and affiliations.
2. Use the conclusion as the primary source for the center claim; summarize from it before considering any other section.
3. Use primary results/evidence only to make the conclusion concrete; use abstract/introduction only for context when conclusion is unavailable or vague.
4. Rank figures by direct support for the center claim.

LaTeX source:

1. Work on a new poster; do not mutate the paper source unless asked.
2. Detect root `.tex` by `\documentclass`, `\begin{document}`, `\title`, `\author`, bibliography, and figure includes.
3. Prefer existing paper figures.
4. Generate QR codes when URLs are available.

Screenshots/figures:

1. Inspect axes, labels, legends, values, panels, and captions.
2. Decide whether the visual belongs in center, side column, or supplement.
3. Preserve scientific meaning; do not redraw quantitative claims without exact values.

## Required Brief

Before final source edits, keep this brief internally or report it when useful:

```text
Layout mode:
Output formats:
Palette:
Main claim:
Problem:
Method in one sentence:
Most important evidence:
Left sidebar sections:
Right sidebar sections:
QR targets:
Scan icon:
Institution logos:
Conference logo:
Potential misunderstanding to avoid:
```

## Assets

Institution logos:

- Normalize sub-units to parent institutions.
- Reject department, faculty, lab, program, and school-within-university lockups when the poster identity is the parent institution.
- For CUHK, use The Chinese University of Hong Kong university-level emblem or wordmark only; do not use Department of Computer Science and Engineering marks.
- Prefer curated logos from `assets/institution-logos/top100-logo-bank/` over runtime cache files.
- Order logos by first-author affiliation order when available.
- If the first author resolves to exactly one institution, prefer a logo-with-name/wordmark asset when available so the bottom strip feels intentionally filled.
- If multiple institutions resolve, show all resolved pure emblems unless the user asks for a cap.
- Normalize raster logo whitespace before placing multiple logos.
- Place logos with `\institutionlogostrip{...}` and `\institutionlogo{path}{\institutionlogosize}`.
- For one wide wordmark, place it with `\institutionwordmarklogo{path}{\institutionlogosize}` to cap width while preserving aspect ratio.
- Use the template logo helpers instead of manual `includegraphics` sizing; bottom logos must remain fully inside the left/right panel bounds.

Conference logos:

- Resolve from `assets/conference-logos/` when possible.
- Treat `assets/conference-logos/` as the only canonical in-repo conference logo directory; it is refreshed by `.github/workflows/sync-conference-logos.yml` from `CS-Conference-Logo-Maintainer` on the 10th day of each month.
- In style1, conference/venue logos are hard identity information: put them at the bottom of the right sidebar when the venue is known, and reduce lower-priority text rather than dropping the logo.
- For pdflatex, use renderer-verified PDF/PNG conversions of SVG sources.
- Use `\conferencelogostrip{...}` and `\conferencelogo{path}{\conferencelogosize}` so the general width/height caps apply.

Figures:

- Do not crop source figures by default.
- If a paper figure is dense, first scale the full figure, choose fewer figures, or use a different complete source figure.
- Crop a source figure only when the user explicitly requests it, and never crop in a way that changes axes, legends, labels, or scientific meaning.
- If a row contains exactly one figure, use a side-by-side image-text row when it improves scanability: left image/right text by default, or right image/left text when that fits the surrounding flow better. The same-row text must be vertically centered on the image's horizontal midline. In LaTeX, prefer `\posterimagetextrow{...}{...}{...}` for this layout.
- Center every visible figure title on its corresponding image. In LaTeX, prefer `\posterlabeledgraphic[...]{Title}{path}{fallback}` so the title and image share the same center axis.

Palette:

- Prefer institution-aware colors from `scripts/select_institution_palette.py`.
- Use one primary center color; keep sidebars white.
- Do not color theorem/proposition titles.

QR:

```bash
python scripts/generate_qr.py \
  --url OpenReview=https://openreview.net/forum?id=example \
  --url Code=https://github.com/user/repo \
  --out-dir figures/qr
```

Use `OpenReview=...` for the primary QR whenever the paper has an OpenReview page; templates can then reference `figures/qr/01-openreview.png`. Use `Paper=...` only when no OpenReview page is available. The script auto-detects known site URLs and pastes a center icon from `assets/site-icons/` or venue logo assets; known-site icon assets must exist before generation.

## Preview And QA

Render from repository root:

```bash
python scripts/render_preview.py templates/classic.tex --out-dir /tmp/better-poster-preview/classic-latex
python scripts/render_preview.py templates/evenbetter.tex --out-dir /tmp/better-poster-preview/evenbetter-latex
python scripts/render_preview.py templates/classic.html --out-dir /tmp/better-poster-preview/classic-html
python scripts/render_preview.py templates/evenbetter.html --out-dir /tmp/better-poster-preview/evenbetter-html
```

QA checklist:

- Main finding is clear at thumbnail scale.
- 25/54/21 claim-billboard hierarchy is obvious for style1.
- Center lines use consistent size/weight/leading.
- Every visible result is supported by source material.
- Source figures are shown complete unless the user explicitly requested a crop.
- QR and logos stay inside their panels.
- Left bottom institution logos and right bottom conference logos are visible when provided.
- Last right-column section and guidance line are visible above the bottom edge.
- LaTeX/HTML match when both are requested.

## Final Response

Report:

- What changed.
- Why it changed.
- Validation run or not run.
- Remaining preview limitations.
- Suggested concise commit message.
