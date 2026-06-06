# Better Poster Skill

Better Poster Skill helps Codex, Claude, or other AI agents turn a paper PDF, figure screenshots, extracted paper text, or a LaTeX source archive into a Better Poster-style academic poster.

The default template follows a claim-first academic poster silhouette: white sidebars, one saturated central billboard, a very large plain-English main finding, a bottom-centered QR/download block in the center column, theory claims on the left, experimental evidence on the right, and pure institution emblems at the bottom-left when available. The canvas is intentionally wide, with width at least twice the height.

## 使用须知与局限性

本仓库当前阶段已经固化了 CUHK style1 基础模板、通用 Skill 规则和一个特定课题示例的经验参数。请注意：本阶段包含特定课题的实例化微调经验，AI 自动生成的特定文本、公式精炼、理论表述和空间分配不保证百分之百契合每位用户的个性化核心意图。用户在正式投稿、展示或分发前，必须根据论文原文、作者偏好、会议规范和最终渲染结果进行人工校验与微调。

本工具适合作为可复用的 poster scaffold 和视觉约束系统；它不会替代作者对科学表述、公式忠实性、引用准确性、图表裁剪和最终版面取舍的判断。

## CUHK Template Preview

![CUHK style1 template](examples/cuhk_mock_style1/style1.png)

Source: `examples/cuhk_mock_style1/style1.tex`; compiled PDF:
`examples/cuhk_mock_style1/style1.pdf`.

## 本阶段固化的 Skill 规范

### CUHK style1 骨架

- 固定 2:1 横向画布，默认 23/54/23 左/中/右三栏结构。
- 左栏固定为 `Introduction` 在上、`Theory` 在下；作者名下不显示 affiliation，机构身份只通过左下角纯校徽呈现。
- 中栏只承担主结论 billboard 和底部 QR/download row，不放方法段落、图表或解释性正文。
- 右栏承载 methodology/results/evidence/conclusion 等支持信息，并在最后追加 `References`。
- 左右侧栏整体保持靠上布局；通过 side-column vertical margin 控制整体位置，不用局部压缩 author 到 Introduction 的行距来伪造上移。
- 所有可视模板文本保持通用 academic sample text，不出现“此处填写”“请替换”等元语言说明。

### 中间色块行数限制

style1 中间 claim 必须使用白色 / 中灰 / 深灰三层色块层级，三层都要出现。通用物理行数上限为：

| Tier | 颜色角色 | 最大可视行数 |
|---|---|---|
| White | 主结论核心 | 3 行 |
| Middle gray | 关键结果或谓语延展 | 2 行 |
| Lower gray | 最终影响或落点 | 1 行 |

中心 claim 的内容优先从论文 conclusion 提炼；只有当 conclusion 缺失或过于含糊时，才回退到 primary result、abstract 或 introduction。文字应简洁、精炼、通俗易懂；可以是一句话，但不强制所有论文都压成一句话。所有中心行必须使用相同字号、字重和行距，`\claimtiervspace` 只作为同节奏换行使用。

### 左栏理论与引用格式

- 左栏禁止 bullet points，包括 compact lists 和 theorem/proposition cards。
- `Theory` 中每个 proposition / lemma / theorem / corollary card 之后，都必须加一行 `\posterstatementsummary{...}`，用更重要的非斜体摘要说明该理论结果“在讲什么”。
- 左栏正文和 theory-card title 中的引用标签使用 `[人名 + 会议/期刊 + 年份]` 这一信息结构，实际排版推荐形如 `(Shumailov et al., Nature 2024)`，避免 `[1]` 这种只靠文献表跳转的数字标签。
- 右栏 `References` 作为正式文献表可以继续使用编号条目，但排版要比正文更淡，例如 `\posterreferences{...}`。

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
| 🟢 preview artifacts | Optional compiled/rendered previews | `/tmp/better-poster-preview/.../*.pdf` and `*.png` by default when dependencies are available |
| 🟢 QR assets | Optional link assets | `figures/qr/*.png` generated from provided URLs |
| 🟢 institution / venue assets | Optional brand assets | `assets/institution-logos/current-logo.png`, optional institution logos, scan icons from `assets/scan-icons/`, and conference logos from `assets/conference-logos/` |

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
3. In `style1`, show all three center tiers and keep the physical line budget: white tier <=3 visible lines, middle gray tier <=2 lines, lower gray tier <=1 line, with identical center font size, weight, and leading.
4. In the left column, use citation labels with the information structure `[author + venue/journal + year]`, rendered for example as `(Shumailov et al., Nature 2024)`, not numeric tags such as `[1]`.
5. If `style2` is selected, place a hero visual and two evidence cards in the center column.
6. Generate QR codes for provided URLs.
7. Resolve institution logos only from the configured CSRankings top-100 list; normalize research institutes to parent institutions, order logos by the first author's affiliation order, show all resolved pure emblems, and leave the brand area blank only if no supported logo is available.
8. Normalize institution logo whitespace before rendering; logos in the same row use the same target height and compact equal spacing. If a wide mark would collide, reduce the poster logo size or use a pure-emblem source rather than a wordmark.
9. Place every center QR row as QR code, scan icon from `assets/scan-icons/`, then Scan text; put contact directly under the primary OpenReview/paper caption.
10. If a venue or conference URL is provided, put the venue logo at the bottom of the right column and size it like the institution emblems.
11. Align title and section styling with the selected institution palette; keep theorem/proposition card titles black, make theorem cards stronger than proposition cards, and keep card bodies black.
12. Produce the selected output formats and run preview commands if dependencies are available.
13. Ensure no text, figure, QR block, or logo overflows its panel; visually inspect the rendered bottom edge and remove lower-priority content if anything is clipped.
14. Return the poster brief, changed files, preview paths, and any unresolved placeholders.
```

## Files

- `templates/`: template source files. These are part of the skill.
- `examples/`: checked-in example posters. Keep example `.tex` and intentionally tracked example `.pdf` outputs here.
- Preview outputs are generated outside the repository by default under `/tmp/better-poster-preview/`. A legacy in-repo `build/` directory is ignored by Git and can be deleted at any time.
- `assets/`: reusable icons, logos, and built-in data assets. This is the largest source directory because it includes cached conference logo assets.
- `SKILL.md`: Codex skill instructions.
- `system_prompt.txt`: prompt for Claude or other multimodal agents.
- `templates/betterposter.cls`: lightweight Better Poster class compatible with the public command interface documented by Rafael Bailo's template.
- `templates/classic.tex`: style1 claim-billboard LaTeX template.
- `templates/evenbetter.tex`: style2 evidence-canvas LaTeX template.
- `templates/classic.html`: style1 claim-billboard HTML template.
- `templates/evenbetter.html`: style2 evidence-canvas HTML template.
- `examples/cuhk_mock_style1/style1.png`: README preview image for the CUHK style1 template.
- `assets/institution-data/csrankings_top100_institutions.json`: configured CSRankings top-100 institution seed list, aliases, and domains.
- `assets/institution-data/institution_palettes.json`: institution-aware primary/secondary color mappings.
- `scripts/render_preview.py`: compile LaTeX or render HTML/PDF previews.
- `scripts/generate_qr.py`: generate icon-centered QR codes for poster URLs.
- `scripts/select_scan_icon.py`: choose matching LaTeX PNG and HTML SVG QR/scan icons for scan rows.
- `scripts/select_institution_logos.py`: choose cached institution logos from first-author affiliation text.
- `scripts/select_institution_palette.py`: choose a LaTeX/CSS institution palette from affiliation text.
- `scripts/resolve_institution_logo.py`: infer/download an institution logo from source text or an explicit institution name.
- `assets/scan-icons/`: paired SVG/PNG QR scan icons; `scan-icon-manifest.txt` controls the random pool.
- `assets/institution-logos/`: institution logo assets and on-demand cache.
- `assets/institution-logos/top100-badges/`: CSRankings top-100 institution badge set with pure-logo and logo-with-name variants.
- `assets/institution-logos/top100-logo-bank/`: expanded CSRankings top-100 logo bank used by the selector.
- `assets/conference-logos/`: OpenReview and conference/venue logo assets for right-column venue marks and QR center icons.

Generated files such as `/tmp/better-poster-preview/`, legacy `build/`, `*.aux`, `*.log`, `*.out`, `*.fls`, and
`*.fdb_latexmk` are preview artifacts, not skill source.

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
python scripts/render_preview.py templates/classic.tex --out-dir /tmp/better-poster-preview/classic-latex
```

风格 2 LaTeX:

```bash
python scripts/render_preview.py templates/evenbetter.tex --out-dir /tmp/better-poster-preview/evenbetter-latex
```

风格 1 HTML:

```bash
python scripts/render_preview.py templates/classic.html --out-dir /tmp/better-poster-preview/classic-html
```

风格 2 HTML:

```bash
python scripts/render_preview.py templates/evenbetter.html --out-dir /tmp/better-poster-preview/evenbetter-html
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

If a conference or venue is known, add its logo at the bottom of the right column with `\conferencelogostrip{...}` and `\conferencelogo{path}{\institutionlogosize}`. HTML may use SVG directly. For `pdflatex`, keep the SVG source and include a renderer-verified PDF or high-resolution PNG derived from it, for example `assets/conference-logos/ICML-logo.svg` -> `assets/conference-logos/ICML-logo-pdflatex.pdf`. Preview the result because some converters produce bad crop boxes or incomplete renders.

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

The resolver only matches `assets/institution-data/csrankings_top100_institutions.json`. If the source institution is outside that list, or if no cached/resolved logo exists, `current-logo.png` is removed and the institution area is left blank. Logo downloads use Wikidata/Commons, Wikipedia page images, Clearbit logo lookup, Google favicon, and DuckDuckGo icon lookup as fallback sources.

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
