# Better Poster Skill

Better Poster Skill helps Codex, Claude, or other AI agents turn a paper PDF, figure screenshots, extracted paper text, or a LaTeX source archive into a Better Poster-style academic poster.

The default template follows a claim-first academic poster silhouette: white sidebars, one saturated central billboard, a very large plain-English main finding, a bottom-centered QR/download block in the center column, theory claims on the left, experimental evidence on the right, and pure institution emblems at the bottom-left when available. The canvas is intentionally wide, with width at least twice the height.

## Template previews

### 风格 1：主结论看板

![风格 1 preview](docs/previews/classic.svg)

Use this for a minimal claim-first poster with a dominant central finding and a bottom scan row.

### 风格 2：证据画布

![风格 2 preview](docs/previews/evenbetter.svg)

Use this when the paper needs a hero visual, visible central evidence, or a stronger technical conversation layer.

## Quick configuration

### Inputs

| Status | Input | Accepted formats / parameters | If omitted |
|---|---|---|---|
| 🔴 **REQUIRED** | Paper content | `paper.pdf`, LaTeX source zip/project, Markdown/text, or pasted paper sections | The agent has no scientific source and should not generate a factual poster. |
| 🔴 **REQUIRED** | Output format choice | `latex`, `html`, or `both` | Defaults to `both` so the poster is editable and printable. |
| 🔴 **REQUIRED** | Layout mode | `style1`, `style2`, or `auto` (`classic`/`evenbetter` remain accepted aliases) | Defaults to `auto`: `style1` for a claim billboard, `style2` when central evidence/hero visual is needed. |
| 🟡 **OPTIONAL** | Paper / code / project URLs | `Paper=...`, `Code=...`, `Project=...`, `Slides=...` | QR area remains as a placeholder or uses only provided links. |
| 🟡 **OPTIONAL** | Institution / affiliation | Institution name, affiliation text, or source file containing affiliation | Institution brand area stays blank unless a configured CSRankings top-100 logo is cached/resolved. |
| 🟡 **OPTIONAL** | Figures / screenshots | Existing method figure, result figure, hero visual, or qualitative examples | Agent uses text-only evidence blocks or figure placeholders. |
| 🟡 **OPTIONAL** | Palette | `auto`, institution-aware, `imperial`, `empirical`, `theory`, `methods`, `plum`, `amber` | Agent chooses a high-contrast palette from affiliations or paper style. |
| 🟡 **OPTIONAL** | Contact line | Email, website, lab page | Contact line is omitted or left as a placeholder. |

### Output formats

| Select | Output | Files produced |
|---|---|---|
| 🔵 `latex` | LaTeX poster only | `templates/classic.tex` for style1 or `templates/evenbetter.tex` for style2, plus `templates/betterposter.cls` |
| 🔵 `html` | Standalone HTML poster only | `templates/classic.html` for style1 or `templates/evenbetter.html` for style2 |
| 🔵 `both` | LaTeX + HTML poster | Matching LaTeX and HTML versions with the same scientific content |
| 🟢 preview artifacts | Optional compiled/rendered previews | `build/.../*.pdf` and `build/.../*.png` when dependencies are available |
| 🟢 QR assets | Optional link assets | `figures/qr/*.png` generated from provided URLs |
| 🟢 institution / venue assets | Optional brand assets | `assets/institutions/current-logo.png`, optional institution logos, scan icons from `assets/icons/`, and conference logos from `assets/logos/` |

## Sample user prompt

Copy this prompt into an agent that has the `better-poster` skill installed. Replace the bracketed fields.

```text
Use $better-poster to generate an academic conference poster from the following paper materials.

Paper source:
- [Attach paper.pdf OR provide LaTeX source zip OR paste abstract/method/results]

Required choices:
- Layout mode: [auto | style1 | style2]
- Output formats: [both | latex | html]

Optional inputs:
- Paper URL: [Paper=https://...]
- Code URL: [Code=https://...]
- Project URL: [Project=https://...]
- Institution / affiliation: [e.g., The Chinese University of Hong Kong]
- Contact line: [email or project contact]
- Preferred palette: [auto | imperial | empirical | theory | methods | plum | amber]
- Key figures to reuse: [figure filenames, screenshots, or “auto-rank figures”]

Generation requirements:
1. Extract a plain-language center claim block from the paper, using the conclusion section/field as the primary baseline and preserving the core result instead of leaving the center sparse.
2. Preserve the claim-first visual hierarchy: about 23/54/23 columns on a 2:1 wide canvas, a saturated center claim block, and a bottom-centered QR block.
3. If `style2` is selected, place a hero visual and two evidence cards in the center column.
4. Generate QR codes for provided URLs.
5. Resolve institution logos only from the configured CSRankings top-100 list; normalize research institutes to parent institutions, order logos by the first author's affiliation order, show all resolved pure emblems, and leave the brand area blank only if no supported logo is available.
6. Normalize institution logo whitespace before rendering; logos in the same row use the same target height and compact equal spacing. If a wide mark would collide, reduce the poster logo size or use a pure-emblem source rather than a wordmark.
7. Place every center QR row as QR code, scan icon from `assets/icons/`, then Scan text; put contact directly under the primary OpenReview/paper caption.
8. If a venue or conference URL is provided, put the venue logo at the bottom of the right column and size it like the institution emblems.
9. Align title and section styling with the selected institution palette; keep theorem/proposition card titles black, make theorem cards stronger than proposition cards, and keep card bodies black.
10. Produce the selected output formats and run preview commands if dependencies are available.
11. Ensure no text, figure, QR block, or logo overflows its panel; visually inspect the rendered bottom edge and remove lower-priority content if anything is clipped.
12. Return the poster brief, changed files, preview paths, and any unresolved placeholders.
```

## Files

- `SKILL.md`: Codex skill instructions.
- `system_prompt.txt`: prompt for Claude or other multimodal agents.
- `templates/`: all poster templates and shared LaTeX class.
- `templates/betterposter.cls`: lightweight Better Poster class compatible with the public command interface documented by Rafael Bailo's template.
- `templates/classic.tex`: style1 claim-billboard LaTeX template.
- `templates/evenbetter.tex`: style2 evidence-canvas LaTeX template.
- `templates/classic.html`: style1 claim-billboard HTML template.
- `templates/evenbetter.html`: style2 evidence-canvas HTML template.
- `docs/previews/`: static template preview diagrams used in this README.
- `data/csrankings_top100_institutions.json`: configured CSRankings top-100 institution seed list, aliases, and domains.
- `data/institution_palettes.json`: institution-aware primary/secondary color mappings.
- `scripts/render_preview.py`: compile LaTeX or render HTML/PDF previews.
- `scripts/generate_qr.py`: generate icon-centered QR codes for poster URLs.
- `scripts/select_scan_icon.py`: choose matching LaTeX PNG and HTML SVG QR/scan icons for scan rows.
- `scripts/select_institution_logos.py`: choose cached institution logos from first-author affiliation text.
- `scripts/select_institution_palette.py`: choose a LaTeX/CSS institution palette from affiliation text.
- `scripts/resolve_institution_logo.py`: infer/download an institution logo from source text or an explicit institution name.
- `assets/icons/`: clean line-style QR/scan icons as paired SVG/PNG assets; `scan-icon-manifest.txt` controls the random pool.
- `assets/institutions/`: on-demand institution logo cache.
- `assets/logos/`: saved OpenReview and conference logo assets for right-column venue marks and QR center icons.

## Install

```bash
mkdir -p ~/.codex/skills
cp -R Better-Poster-Skill ~/.codex/skills/better-poster
```

## Basic usage

For 风格 1:

```text
Use $better-poster style1 mode and output both LaTeX and HTML.
```

For 风格 2:

```text
Use $better-poster style2 mode and output both LaTeX and HTML. Include a hero visual and central evidence cards.
```

## Preview commands

风格 1 LaTeX:

```bash
python scripts/render_preview.py templates/classic.tex --out-dir build/classic-latex
```

风格 2 LaTeX:

```bash
python scripts/render_preview.py templates/evenbetter.tex --out-dir build/evenbetter-latex
```

风格 1 HTML:

```bash
python scripts/render_preview.py templates/classic.html --out-dir build/classic-html
```

风格 2 HTML:

```bash
python scripts/render_preview.py templates/evenbetter.html --out-dir build/evenbetter-html
```

The preview script copies/compiles the source and renders PNG previews when local dependencies are available. It also warns when obvious placeholder text remains.

## QR codes

Every center QR row includes a scan icon immediately to the right of the QR code. Choose or override the paired LaTeX/HTML icon before filling the templates:

```bash
python scripts/select_scan_icon.py --format both
```

Use the printed `latex=...` path for LaTeX and `html=...` for HTML so both formats share the same selected QR/scan icon.

Generate the primary paper QR with the label `Paper` so the templates can use `figures/qr/01-paper.png` automatically:

```bash
python scripts/generate_qr.py \
  --url Paper=https://example.com/paper \
  --url Code=https://github.com/user/repo \
  --out-dir figures/qr
```

The primary QR block is centered in the bottom band of the center column. Each QR row keeps the QR image on the left, a scan icon immediately to its right, and the corresponding text on the right, with the icon and text aligned to the QR image centerline. Put the contact line directly under the primary QR caption.

`scripts/generate_qr.py` selects a scan icon by default. Pass `--scan-icon PATH` to force a specific PNG/PDF icon or `--scan-icon none` only when the user explicitly asks to omit it.

## Institution branding

Resolve supported CSRankings top-100 institution logos explicitly from cache only. For affiliations, normalize research institutes and labs to their parent institution, order available logos by the first author's affiliation order, and show all resolved pure emblems left-aligned with the title:

```bash
python scripts/select_institution_logos.py \
  --text "NUS (Chongqing) Research Institute; Zhejiang University"
```

Use `--max-institutions N` only when the user explicitly asks to cap the logo strip. Normalize logo whitespace first, then place every resolved logo with `\institutionlogostrip{...}` and repeated `\institutionlogo{path}{\institutionlogosize}` entries; the template keeps fixed target height, top/bottom alignment, and compact equal spacing.

If a conference or venue is known, add its logo at the bottom of the right column with `\conferencelogostrip{...}` and `\conferencelogo{path}{\institutionlogosize}`. HTML may use SVG directly. For `pdflatex`, keep the SVG source and include a renderer-verified PDF or high-resolution PNG derived from it, for example `assets/logos/ICML-logo.svg` -> `assets/logos/ICML-logo-pdflatex.pdf`. Preview the result because some converters produce bad crop boxes or incomplete renders.

Resolve/download a single institution logo explicitly:

```bash
python scripts/resolve_institution_logo.py \
  --institution "Massachusetts Institute of Technology"
```

Allow network fallback on cache miss:

```bash
python scripts/resolve_institution_logo.py \
  --institution "Massachusetts Institute of Technology" \
  --download
```

Infer the institution from a LaTeX/text source:

```bash
python scripts/resolve_institution_logo.py --source paper.tex --download
```

The resolver only matches `data/csrankings_top100_institutions.json`. If the source institution is outside that list, or if no cached/resolved logo exists, `current-logo.png` is removed and the institution area is left blank. Logo downloads use Wikidata/Commons, Wikipedia page images, Clearbit logo lookup, Google favicon, and DuckDuckGo icon lookup as fallback sources.

The templates live one directory below the repository root, so LaTeX figure paths inside `templates/*.tex` use `../figures/...` and `../assets/...`.

## Color palettes

Prefer institution-aware colors when affiliations are available:

```bash
python scripts/select_institution_palette.py \
  --text "NUS (Chongqing) Research Institute; Zhejiang University" \
  --format all
```

The emitted LaTeX snippet sets `institutionprimary`, `institutionsecondary`, and `\institutionpalette{...}{...}`. The emitted CSS variables set `--institution-primary` and `--institution-secondary`. Single-color institutions can use the same primary/secondary value; dual-color institutions use coordinated pairs such as blue plus orange.

The templates keep the side columns white and use the selected palette only for the central billboard, title text, section headings, and selected core accents. Theorem/proposition card titles and bodies stay black; theorem cards are visually stronger through size/weight, while proposition cards are smaller/subdued. If no institution palette is selected, use one of these palette names/classes:

- `imperial` / `theme-imperial`
- `empirical` / `theme-empirical`
- `theory` / `theme-theory`
- `methods` / `theme-methods`
- `plum` / `theme-plum`
- `amber` / `theme-amber`

Use high-contrast central text. Amber uses dark text; the other palettes use white text.

## References

- Rafael Bailo, Better Poster LaTeX template: https://github.com/rafaelbailo/betterposter-latex-template
- MIT Communication Lab, Toward an Even Better Poster: https://mitcommlab.mit.edu/be/2023/09/27/toward-an-evenbetterposter-improving-the-betterposter-template/

## License

This repository remains MIT licensed. The included `templates/betterposter.cls` is a lightweight compatible implementation for this skill and is not a vendored copy of Rafael Bailo's GPL-licensed class.

Review institution logo copyright, trademark, and attribution requirements before redistributing generated logo files.

Suggestions, issues, and improvements are welcome.
