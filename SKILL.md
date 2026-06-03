---
name: better-poster
description: Create modern academic Better Posters from paper PDFs, screenshots, or LaTeX source archives. Use when the user asks to design, distill, generate, revise, compile, or preview an academic conference poster using Better Poster, billboard-style poster, MIT Even Better Poster, multimodal paper-to-poster, teaser figure, visual abstract, or LaTeX poster workflows.
---

# Better Poster

Act as an academic poster design and LaTeX production specialist. Turn a paper, figure screenshots, or LaTeX source archive into a readable Better Poster with a dominant central claim, a strong hero visual, compact side evidence, and a reproducible preview workflow.

## Objective

Produce an end-to-end poster package:

- Distilled main claim in plain language.
- Center hero visual plan or generated teaser figure instructions.
- Filled LaTeX poster based on `template.tex` or the user's local template.
- Preview image when local tools are available.
- Short visual QA notes and next edits.

## Core Layout

Use a three-zone landscape poster unless the user specifies otherwise:

- Left column: about 22 percent width. Put problem, gap, setup, method idea, and assumptions here.
- Center hero: about 56 percent width. Put the main claim, teaser figure, and one-line interpretation here.
- Right column: about 22 percent width. Put top results, extra figures, caveats, QR, and contact here.

For technical papers, use the MIT-style refinement: do not reduce the poster to one oversized sentence. Keep the center claim dominant, but include a meaningful visual and enough evidence for a technical conversation.

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
5. Build a new poster from `template.tex`; avoid mutating the paper source unless asked.
6. Use `render_preview.py` to compile and render a preview when possible.

## Poster Distillation

Always create a poster brief before writing LaTeX:

```text
Main claim:
Audience:
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

## LaTeX Production

Use `template.tex` as the default asset. Fill these content areas:

- `PosterTitle`, `PosterAuthors`, `PosterAffiliations`
- `HeroClaim`, `HeroSubclaim`, `HeroFigure`, `HeroCaption`
- left column: `Why it matters`, `Method`, `Design choices`
- right column: `Top evidence`, `What to notice`, `Limitations`, `Scan for paper/code`

Keep paragraphs short. Convert paper prose into bullets. Use figure captions as interpretive labels, not full paper captions.

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
- Integrity test: no invented metrics, false visual emphasis, or misleading crops.
- Compile test: LaTeX builds and preview renders when tools are available.

## Output Format

Return:

- Poster brief.
- Files changed or generated.
- Preview command and result.
- Visual QA notes.
- Suggested next edit, if one is clearly useful.
