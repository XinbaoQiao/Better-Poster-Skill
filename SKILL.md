---
name: better-poster
description: Create modern academic Better Posters from paper PDFs, screenshots, or LaTeX source archives. Use when the user asks to design, distill, generate, revise, compile, or preview an academic conference poster using Better Poster, billboard-style poster, MIT Even Better Poster, multimodal paper-to-poster, teaser figure, visual abstract, HTML poster, or LaTeX poster workflows.
---

# Better Poster

Act as an academic poster design and production specialist. Turn a paper, figure screenshots, or LaTeX source archive into a readable Better Poster or MIT-style Even Better Poster with a dominant claim, visible evidence, and a reproducible preview workflow. HTML output is acceptable and often preferred for fast visual iteration; LaTeX remains available for print or venue requirements.

## Objective

Produce an end-to-end poster package:

- Distilled main claim in plain language.
- Center hero visual plan or generated teaser figure instructions.
- One branded QR code for the primary paper URL when available, preferably OpenReview.
- Filled HTML poster based on `template.html`, or LaTeX poster based on `template.tex` when requested.
- Preview image when local tools are available.
- Short visual QA notes and next edits.

## Layout Selection

Select a layout before writing files. State the selected layout and why in the poster brief.

- Classic Better Poster: Rafael/Morrison-style wide center claim, narrow sidebars, and one QR area. Use when the work has one simple, memorable finding.
- Even Better Poster technical: MIT-style claim band plus central evidence grid. Use for most CS/ML papers that need figures to justify the claim.
- Figure-heavy technical poster: claim title plus two or three large evidence panels and a compact method strip. Use when qualitative examples or result matrices are the main contribution.
- Portrait fallback: use only when the venue requires portrait format.

For technical papers, prefer the Even Better Poster technical layout: keep the main claim easy to understand from far away, but do not reduce the poster to one oversized sentence. Put the strongest figures in the main visual area, not in tiny sidebars.

Density budget:

- Main claim: 12 to 22 words when possible.
- Hero/evidence caption: 18 words or fewer.
- Left/context rail: 90 to 120 words total.
- Evidence cards: no more than four, each with one message, one figure, and one short caption.
- Each bullet or support sentence: 12 words or fewer when possible.
- Figures with axes must remain large enough for labels to be readable in preview.

## Input Routing

### PDF or Paper Text

1. Extract title, authors, abstract, problem, method, result, limitation, and conclusion.
2. Identify all figures/tables and rank them by relevance to the main claim.
3. Choose the hero visual: existing figure, cropped/composite figure, or newly generated schematic.
4. Rewrite content for poster scanning, not paper reading.

### Screenshots or Figure Images

1. Inspect visible panels, axes, legends, labels, qualitative examples, and captions.
2. Decide whether each image is hero, side evidence, or QR-linked supplemental material.
3. Preserve scientific meaning. Do not invent numbers, rankings, dataset names, labels, or visual evidence.
4. If the image is too dense, specify a crop, relabel, simplification, or schematic redraw.

### LaTeX Zip

1. Extract into a temporary directory.
2. Detect the root `.tex` by checking `\documentclass`, `\begin{document}`, `\title`, `\author`, bibliography commands, and figure includes.
3. Parse title, authors, abstract, section headings, figure captions, included graphics, and bibliography.
4. Prefer reusing existing figures from the source tree.
5. Build a new poster from `template.html` by default, or `template.tex` when LaTeX/PDF is requested; avoid mutating the paper source unless asked.
6. Generate the OpenReview QR code with `scripts/generate_qr.py` when an OpenReview URL is available.
7. Use `render_preview.py` to compile and render a preview when possible.

## Poster Distillation

Always create a poster brief before writing files:

```text
Main claim:
Audience:
Layout chosen:
Output format:
Problem:
Method in one sentence:
Most important evidence:
Hero visual:
Left column sections:
Right column sections:
QR target:
Potential misunderstanding to avoid:
```

Main claim rules:

- One sentence, 12 to 22 words when possible.
- Plain language before jargon.
- Include the concrete outcome if the paper has one.
- Avoid vague claims like "we propose a novel framework" unless the actual contribution is conceptual.

## Hero Visual Rules

Choose one:

- Existing figure: use when one figure directly proves or explains the main claim.
- Composite teaser: use when method plus result must be shown together.
- Generated schematic: use when the paper is method-heavy or existing figures are too dense.

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

Prefer clean vector-like scientific diagrams, readable labels, strong whitespace, and exact preservation of scientific quantities. Avoid decorative art.

## Output Production

Use `template.html` when the user wants fast visual iteration, a web-native poster, or a screenshot-style preview. Fill these areas:

- paper title, authors, venue, affiliation
- take-home message and subclaim
- graphical abstract or method sketch
- three exact highlights
- four evidence cards
- one OpenReview QR code
- contact/footer

Use `template.tex` when the user asks for LaTeX, Overleaf, PDF-first output, or a venue requires LaTeX/PDF. Fill these content areas:

- `PosterTitle`, `PosterAuthors`, `PosterAffiliations`
- `HeroClaim`, `HeroSubclaim`, `HeroFigure`, `HeroCaption`
- left column: `Why it matters`, `Method`, `Design choices`
- right column: `Top evidence`, `What to notice`, `Limitations`, `Scan for paper/code`

Keep paragraphs short. Convert paper prose into bullets or evidence-card captions. Use figure captions as interpretive labels, not full paper captions.

## QR Code

Default to one QR code: the primary paper page, preferably OpenReview. Venue pages such as ICML/ICLR/NeurIPS can be listed as text, but should not become QR codes unless the user explicitly asks for multiple QR targets.

```bash
python scripts/generate_qr.py \
  --url OpenReview=https://openreview.net/forum?id=... \
  --out-dir figures/qr
```

Rules:

- Use `OpenReview=URL` when an OpenReview link is available.
- Let the script auto-select the saved OpenReview logo for OpenReview URLs.
- Keep the generated QR code in `figures/qr/`; the script also writes `figures/qr/qr-snippet.tex`.
- Place the QR code in the right-column `Scan` area or another low-priority corner, never over the center hero claim or hero figure.
- Keep the single QR visually subordinate to the main claim, but large enough to scan from poster-session distance.
- If the user explicitly requests several QR targets, show them in a compact grid and keep OpenReview first.

When adapting a user's existing LaTeX:

- Keep relative paths.
- Copy or reference figures into a poster-local `figures/` directory.
- Prefer PDF/PNG/JPG figures already present.
- Avoid machine-specific absolute paths.
- Compile with `pdflatex` unless the document requires another engine.

## Preview Workflow

Use:

```bash
python render_preview.py template.tex --out-dir build
```

or:

```bash
python render_preview.py poster_source.zip --root poster.tex --out-dir build
```

If compilation fails, inspect the `.log` file and fix missing packages, missing graphics, undefined commands, or path issues. If preview rendering fails, keep the PDF and report the render dependency problem.

## Visual QA

Before finalizing, evaluate:

- First-glance test: the main finding is understandable in 5 to 10 seconds.
- Thumbnail test: the hierarchy is visible when zoomed out.
- Evidence test: at least one visible graphic or number supports the claim.
- Conversation test: side columns give enough detail for follow-up questions.
- QR test: the primary paper URL is represented as a scannable QR code in a low-priority scan area.
- Integrity test: no invented metrics, false visual emphasis, or misleading crops.
- Compile test: LaTeX builds and preview renders when tools are available.

## Output Format

Return:

- Poster brief.
- Files changed or generated.
- Preview command and result.
- Visual QA notes.
- Suggested next edit, if one is clearly useful.
