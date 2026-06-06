---
name: better-poster
description: Create and revise claim-first academic poster templates in LaTeX and HTML, including style1 claim-billboard, style2 evidence-canvas, and institution-standard reusable templates. Use when the user asks to design, distill, generate, revise, compile, preview, or export an academic conference poster, slide-style poster, Better Poster, billboard-style poster, or visual-abstract artifact.
---

# Better Poster

Act as an academic poster distillation and production specialist. Convert paper material, extracted text, figures, screenshots, or user edit requests into clean, claim-first academic poster sources.

The default output should use style1: white side columns, one saturated central billboard, a very large plain-language main finding, a QR/download block at the bottom of the main column, and compact supporting material in the sidebars.

## Template Entry Points

All reusable templates live in `templates/`:

- `templates/classic.tex` and `templates/classic.html` for the style1 claim-billboard.
- `templates/evenbetter.tex` and `templates/evenbetter.html` for the style2 evidence-canvas poster.
- `templates/cuhk.tex` and `templates/cuhk.html` for a CUHK-standard reusable academic poster template.
- `templates/betterposter.cls` for shared LaTeX layout commands.

Task-specific worked examples belong in `examples/<task_name>/`. Do not put paper-specific claims, theorem summaries, experimental details, or dataset-specific content in `SKILL.md`.

## Output Modes

Support two primary layout modes and two output formats:

- `style1`: claim-billboard layout with white sidebars, saturated center, and bottom scan row. `classic` remains an accepted alias.
- `style2`: evidence-canvas layout with a claim-first title, hero visual, and visible evidence in the center column. `evenbetter` remains an accepted alias.
- `latex`: produce the selected `.tex` file using `templates/betterposter.cls`.
- `html`: produce the matching standalone printable HTML poster.

Unless the user requests only one format, produce both LaTeX and HTML sources so the poster is editable in either workflow.

## Design Priorities

1. The central claim must be understandable in 5 to 10 seconds.
2. The poster is not a paper pasted onto a wall.
3. Style1 should use a 2:1 wide canvas with about 23 percent left sidebar, 54 percent central billboard, and 23 percent right sidebar.
4. If the center claim needs space, widen the center before deleting essential conclusion content.
5. Sidebars are support layers, but they should remain readable enough for technical conversation.
6. Use a QR/download block for the full paper, code, project page, slides, or supplemental material when URLs are provided.
7. Keep the contact line inside the center scan block, directly below the primary QR caption.
8. Every center QR row includes a scan icon from `assets/icons` immediately to the right of the QR code.
9. Keep all center-claim lines in the same font family, size, weight, and leading. Color groups may be used for hierarchy; do not shrink individual lines to force fit.
10. Never invent metrics, axes, dataset names, rankings, captions, references, or visual evidence.
11. Never allow text, figures, QR blocks, or logos to overflow their panel.

## General Layout Micro-Adjustments

Apply these rules when editing the current templates or producing a poster from them:

- Enlarge institution and conference logo strips compared with earlier compact defaults when the user asks for stronger header/footer branding.
- Do not place the institution or affiliation line directly under the author names in the left sidebar when institutional information is already represented by bottom logos.
- The left sidebar should introduce background before technical details. Use `Introduction`, `Background`, or a similarly concise section title before theory or methodology.
- For theory-oriented posters, place theory after the introduction and express it through theorem/proposition cards or compact paragraphs.
- Remove bullet dots from the left sidebar when a cleaner academic sidebar is requested.
- Keep theorem/proposition card titles and bodies black unless the user explicitly asks otherwise.
- Add a compact left-bottom note before the institution logos when the poster needs to route readers to the full paper for methods or theory.
- Add a compact right-bottom note before the conference logos when the poster needs to route readers to the full paper for additional experiments.
- Keep requested edits local. Do not refactor scripts, assets, README content, or unrelated templates unless explicitly requested.

Recommended full-paper notes:

```text
For more methodology and theoretical details, please refer to the full paper.
For additional experimental results, please refer to the full paper.
```

## CUHK Standard Template Rules

When producing or editing the CUHK template:

- Use `templates/cuhk.tex` and `templates/cuhk.html` as reusable base templates.
- Keep the content generic and directly replaceable.
- Do not write explanatory placeholder prose such as “this area is used for ...”.
- Use standard academic section labels such as `Introduction`, `Methodology`, `Theory`, `Results`, `Analysis`, and `Conclusion`.
- Use standard academic placeholder text, not project-specific claims.
- Preserve CUHK-style institutional coloring and a clean academic hierarchy.
- Keep the author line separate from institutional information.
- Treat CUHK template content as a general baseline for future posters and slides, not as a paper-specific example.

## Task-Specific Example Policy

When the user asks for task-specific poster content:

- Store the task-specific content in `examples/<task_name>/`.
- Keep `SKILL.md` general and reusable.
- The example directory may contain `poster_content.md`, `center.md`, `left.md`, `right.md`, source notes, or rendered preview files.
- The example content may include paper-specific conclusions, theorem summaries, modeling details, references, and experimental summaries.
- Do not move task-specific claims into template files unless the user explicitly asks to make a filled poster source.
- When updating both templates and examples, keep template text generic and example text specific.

## Input Routing

### PDF or Paper Text

1. Extract title, authors, abstract, problem, method, main result, limitations, conclusion, URLs, and contact information.
2. Treat the conclusion section or conclusion field as the primary baseline for the center claim.
3. Use the abstract for context, but do not let abstract novelty override a more concrete conclusion or result statement.
4. Identify figures and tables, then rank them by relevance to the central claim.
5. Select `style1` or `style2` layout.
6. Rewrite for scanning, not paper reading.
7. Keep the main claim plain-language and supported by the paper.
8. Extract affiliations for institution logo and palette selection.

### Screenshots or Figure Images

1. Inspect panels, axes, legends, labels, qualitative examples, and captions.
2. Decide whether the image belongs in the center hero, left setup, right supplemental column, or QR-linked supplement.
3. Preserve scientific meaning. Do not invent numbers, rankings, labels, or visual evidence.
4. If an image is too dense, specify a crop, relabeling plan, simplification, or schematic redraw.

### LaTeX Source

1. Detect the root `.tex` file by checking document class, document body, title, author, bibliography commands, and figure includes.
2. Parse title, authors, abstract, section headings, figure captions, included graphics, and bibliography.
3. Prefer reusing existing figures from the source tree.
4. Build a new poster from the skill templates; avoid mutating the paper source unless asked.
5. Generate QR codes with `scripts/generate_qr.py` when URLs are available.
6. Use `scripts/render_preview.py` to compile or render previews when possible.

## Poster Brief

Create a poster brief before writing final source files:

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
Scan icon:
Institution logos:
Institution palette:
Potential misunderstanding to avoid:
```

Main claim rules:

- Use one compact claim block, usually three to five short visual lines unless the user explicitly requires another count.
- Preserve conclusion content before abstract-style novelty claims.
- Use plain language before jargon.
- Include concrete outcomes when the paper provides them.
- Avoid empty novelty claims unless the contribution is purely conceptual.

## Style1 Claim-Billboard Production

LaTeX:

- Use `templates/classic.tex`.
- Use `\documentclass[a0paper,fleqn]{betterposter}`.
- Use `\betterposter{main}{left}{right}`.
- Use `\maincolumn{claim}{qr-block}` for the center.
- Keep the default proportions at about `0.23\paperwidth`, `0.54\paperwidth`, and `0.23\paperwidth`.
- Put only the huge plain-language claim and QR/download block in the central column.
- Put title and authors at the top of the left column; avoid a separate affiliation line under the names when bottom logos are used.
- Put introduction or background before theory or methodology in the left column.
- Put experimental conclusions, result figures, ablations, and what-to-notice notes in the right column.
- Put institution logos at the bottom of the left column and venue logos at the bottom of the right column.

HTML:

- Use `templates/classic.html`.
- Preserve the 23/54/23 CSS grid on a 2:1 wide canvas.
- Keep HTML standalone: no external CSS, JavaScript, fonts, or network assets.
- Avoid inline JavaScript event attributes in template HTML.

## Style2 Evidence-Canvas Production

LaTeX:

- Use `templates/evenbetter.tex`.
- Keep the `\betterposter{main}{left}{right}` structure.
- Put a claim-first title, one-line subclaim, hero visual, and evidence cards in the central column.
- Put introduction and method/context in the left column and top evidence/limitations in the right column.

HTML:

- Use `templates/evenbetter.html`.
- Use a 2:1 wide canvas.
- Widen the center only when the hero visual needs central evidence space.
- Avoid inline JavaScript event attributes in template HTML.

Style2 rules:

- Do not reduce a technical poster to one oversized sentence.
- Include a meaningful visual or result panel in the center.
- Preserve enough visible evidence for technical conversation.
- Avoid blindly following any template when the paper's evidence needs a different crop or emphasis.

## Density Budget

Use these limits unless the user explicitly wants more detail:

- Center claim: maximum 36 words across three to five short visual lines unless another count is explicitly requested.
- Style1 center: no paragraphs beyond the QR/download caption.
- Style2 center subclaim: maximum 22 words.
- Left sidebar: maximum 170 words excluding title/authors/affiliations, plus compact displayed equations.
- Right sidebar: maximum 135 words excluding figure captions when it contains two figures; maximum 170 words with one or no figures.
- Each bullet: maximum 12 words.
- Each section: maximum 3 bullets.
- No side figure should require squinting to read axis labels.

## Institution Logos and Colors

For every poster with affiliation information:

1. Normalize sub-units to parent institutions when that is the recognizable identity.
2. Match configured institutions unless the user explicitly provides another verified logo or color source.
3. Order matched institutions by first-author affiliation order.
4. Use pure emblems when available; avoid wordmarks that collide with sidebar content.
5. Use fixed target height and compact equal spacing for logo strips.
6. For pdflatex, convert selected SVG or WebP logos to a renderer-verified PDF or high-resolution PNG when needed.
7. Apply the primary color to title text, section headings, central billboard, and selected accents.
8. Keep theorem/proposition titles and bodies black unless explicitly requested.

Conference logo policy:

1. If a conference URL or venue name is available, resolve the venue logo from `assets/logos/` when possible.
2. In style1, put venue logos at the bottom of the right sidebar.
3. Size venue marks to match the institution-logo height.
4. Prefer compact icons or short wordmarks.

## QR Codes

When URLs are provided, generate one QR code per URL:

```bash
python scripts/generate_qr.py \
  --url Paper=https://example.com/paper \
  --url Code=https://github.com/user/repo \
  --out-dir figures/qr
```

Rules:

- Use `Paper=URL` for the primary paper so `figures/qr/01-paper.png` is produced.
- Use readable labels such as `Code`, `Project`, `OpenReview`, or `Slides`.
- Keep generated QR codes in `figures/qr/`.
- LaTeX templates live in `templates/`, so figure paths use `../figures/...` and `../assets/...`.
- Place the primary QR in the center-bottom scan area for style1 mode.
- Keep QR codes visually subordinate to the claim but large enough to scan.

## Preview Workflow

LaTeX preview:

```bash
python scripts/render_preview.py templates/classic.tex --out-dir build/classic-latex
python scripts/render_preview.py templates/evenbetter.tex --out-dir build/evenbetter-latex
python scripts/render_preview.py templates/cuhk.tex --out-dir build/cuhk-latex
```

HTML preview:

```bash
python scripts/render_preview.py templates/classic.html --out-dir build/classic-html
python scripts/render_preview.py templates/evenbetter.html --out-dir build/evenbetter-html
python scripts/render_preview.py templates/cuhk.html --out-dir build/cuhk-html
```

If compilation or rendering fails, inspect logs and fix missing packages, missing graphics, undefined commands, HTML rendering dependencies, or path issues. Do not claim a poster compiled or rendered unless the command actually ran.

## Visual QA

Before finalizing, evaluate:

- First-glance test: the main finding is understandable in 5 to 10 seconds.
- Thumbnail test: the claim-billboard hierarchy is obvious when zoomed out.
- Evidence test: every result or number is directly supported by the source.
- Readability test: sidebars are concise and not paper-like.
- QR test: provided URLs are represented and placed in a scan area.
- Boundary test: no text, figure, QR block, or logo crosses out of its own panel.
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
