# Better Poster Skill

[中文版](README.zh-CN.md)

Better Poster Skill helps a code agent turn a paper PDF, figure screenshots, extracted paper text, or a LaTeX source archive into a Better Poster-style academic poster.

The default template follows a claim-first academic poster silhouette: white sidebars, one saturated central billboard, a very large plain-English main finding, a bottom-centered QR/download block in the center column, theory claims on the left, experimental evidence on the right, and pure institution emblems at the bottom-left when available. The canvas is intentionally wide, with width at least twice the height.

## Usage Notes And Limitations

This repository currently provides a stabilized CUHK style1 base template, general template rules, and experience parameters from one topic-specific example. Some topic-specific tuning is included at this stage. AI-generated poster text, formula compression, theory summaries, and space allocation may not fully match every author's intended emphasis. Before submission, presentation, or distribution, users should manually check and refine the poster against the source paper, author preferences, venue requirements, and final rendered output.

This tool is best understood as a reusable poster scaffold and visual constraint system. It does not replace author judgment about scientific wording, formula fidelity, citation accuracy, figure cropping, or final layout tradeoffs.

## CUHK Template Preview

![CUHK style1 template](examples/cuhk_mock_style1/style1.png)

## What It Provides

- A reusable CUHK style1 poster template with a 2:1 wide canvas and a claim-first visual hierarchy.
- A second evidence-oriented style for papers that need a central hero figure or result panel.
- Editable LaTeX and standalone HTML outputs, with matching visual structure when both are requested.
- A growing example library under `examples/`, intended as a reference for successful layouts, density, wording style, and visual hierarchy.
- Built-in support for QR rows, institution emblems, conference marks, and institution-aware color palettes. These are handled by the code agent during generation; users do not need to run separate asset commands.

## Design Rules

### CUHK Style1

- Fixed 2:1 landscape canvas with a 23/54/23 left/center/right column structure.
- Left column contains the title, authors, `Introduction`, and `Theory`; author affiliations are not repeated under the author line.
- Center column is reserved for the large plain-English conclusion and the bottom QR/download row.
- Right column contains methodology, results, evidence, conclusion, and a final `References` section.
- Institution identity appears through the bottom-left logo strip when a supported emblem is available.
- Conference or venue identity appears at the bottom of the right column when available.
- Visible template text stays generic and academic; the base template does not include explanatory placeholder sentences such as "fill this section".

### Center Claim

The center claim is the poster's main billboard. It should be concise, plain-language, and understandable in a few seconds. The preferred source is the paper's conclusion; the agent may use primary results only to make that conclusion concrete.

Style1 always uses three visual tiers:

| Tier | Role | Maximum visible lines |
|---|---|---|
| White | Core conclusion | 3 |
| Middle gray | Key result or extension | 2 |
| Lower gray | Final impact or takeaway | 1 |

The center text should use consistent size, weight, and line spacing across tiers. A one-sentence center is encouraged when it naturally captures the paper, but it is not mandatory.

### Theory And References

- The left column is bulletless, including theory cards and compact summaries.
- `Theory` should explain propositions, lemmas, theorems, corollaries, assumptions, or key equations in a compressed but faithful way.
- Each theory card should be followed by a short plain-language line explaining what that statement says.
- Left-column citation labels use the information structure `[author + venue/journal + year]`, rendered for example as `(Shumailov et al., Nature 2024)`, rather than numeric-only tags such as `[1]`.
- The right-column `References` section is visually lighter than the main body text.

## Inputs

| Input | Accepted examples | Notes |
|---|---|---|
| Paper content | PDF, LaTeX source archive, Markdown/text extraction, pasted paper sections | Required for factual poster generation. |
| Output choice | `latex`, `html`, or `both` | Defaults to both when not specified. |
| Layout mode | `style1`, `style2`, or `auto` | `style1` is the default claim-first layout. |
| URLs | Paper, code, project, slides, OpenReview | Used for the poster QR/download area. |
| Institution / affiliation | Institution name or author affiliation text | Used for emblem and palette selection when supported. |
| Figures / screenshots | Method figures, result figures, qualitative examples | Used when they directly support the main claim. |
| Contact line | Email, project page, lab page | Placed near the QR/download area when provided. |

## How To Use

Ask a code agent with this repository installed to generate or revise a poster from the paper materials. The agent should read the paper, choose the closest layout, integrate QR/branding/palette assets when possible, render previews when dependencies are available, and report any unresolved placeholders.

Example prompt:

```text
Use $better-poster to generate an academic conference poster from this paper.

Paper source:
- [attach paper.pdf, provide a LaTeX source archive, or paste paper sections]

Preferences:
- Layout mode: auto
- Output: both LaTeX and HTML
- Paper URL: [optional]
- Code URL: [optional]
- Institution / affiliation: [optional]
- Contact line: [optional]
- Key figures to reuse: [optional]
```

## Outputs

Depending on the requested format and local dependencies, the agent returns:

- Editable LaTeX poster source.
- Standalone HTML poster source.
- Rendered PDF/PNG previews for visual checking.
- Integrated QR/download rows when URLs are provided.
- Institution and conference branding when supported assets are available.
- A short summary of changed files, preview locations, and any remaining manual checks.

Preview artifacts are generated outside the repository by default under `/tmp/better-poster-preview/`. A legacy in-repo `build/` directory is ignored by Git and can be deleted at any time.

## Installation

```bash
mkdir -p ~/.codex/skills
cp -R Better-Poster-Skill ~/.codex/skills/better-poster
```

After installation, call the repository through the agent:

```text
Use $better-poster to generate a poster from this paper.
```

## Automatic Asset Handling

The code agent handles poster assets as part of generation:

- QR rows are created from provided paper, code, project, or slides URLs.
- Institution emblems are selected when the affiliation can be matched to supported assets.
- Conference or venue marks are added when a matching asset is available.
- Institution-aware colors are used when supported; otherwise the agent chooses a high-contrast academic palette.

Users only need to provide the source paper materials and any URLs or affiliation details they want reflected in the poster.

## References

- Rafael Bailo, Better Poster LaTeX template: https://github.com/rafaelbailo/betterposter-latex-template
- MIT Communication Lab, Toward an Even Better Poster: https://mitcommlab.mit.edu/be/2023/09/27/toward-an-evenbetterposter-improving-the-betterposter-template/

## License

This repository remains MIT licensed. The included `templates/betterposter.cls` is a lightweight compatible implementation for this skill and is not a vendored copy of Rafael Bailo's GPL-licensed class.

Review institution logo copyright, trademark, and attribution requirements before redistributing generated logo files.

Suggestions, issues, and improvements are welcome.

[中文版](README.zh-CN.md)
