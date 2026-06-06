# Better Poster Skill

[中文版](README.zh-CN.md)

Better Poster Skill helps a code agent turn paper materials into an editable academic poster in a Better Poster-style layout.

You can use it when you have a paper PDF, LaTeX source archive, extracted paper text, figures, screenshots, project links, or an existing poster draft that needs to be redesigned.

## Preview

![CUHK style1 template](examples/cuhk_mock_style1/style1.png)

## What This Project Provides

- Reusable academic poster templates for claim-first and evidence-focused poster layouts.
- Editable LaTeX poster output.
- Standalone HTML poster output when requested.
- Rendered PDF/PNG previews when local dependencies are available.
- Automatic QR/download rows from provided paper, code, project, or slide links.
- Institution and conference branding support when matching assets are available.
- A growing `examples/` library that helps the agent reuse successful poster structures and visual patterns for new papers.

## What To Prepare

Provide as much of the following as available:

| Item | Examples |
|---|---|
| Paper content | PDF, LaTeX source archive, Markdown/text extraction, pasted sections |
| Output format | LaTeX, HTML, or both |
| Links | Paper, code, project page, slides, OpenReview |
| Affiliation | Institution name or author affiliation text |
| Figures | Method figures, result plots, qualitative examples, screenshots |
| Contact | Email, project page, lab page |
| Preference | Target venue, poster size, preferred style, content emphasis |

The paper content is the most important input. Extra links and affiliation details help the agent build the QR area and branding.

## How To Use

Install this repository as a Codex skill, then ask the code agent to generate or revise a poster from your paper materials.

```bash
mkdir -p ~/.codex/skills
cp -R Better-Poster-Skill ~/.codex/skills/better-poster
```

Example request:

```text
Use $better-poster to generate an academic poster from this paper.

Paper source:
- [attach paper.pdf, provide a LaTeX source archive, or paste paper sections]

Preferences:
- Output: both LaTeX and HTML
- Paper URL: [optional]
- Code URL: [optional]
- Institution / affiliation: [optional]
- Contact line: [optional]
- Key figures to reuse: [optional]
```

The agent will read the paper materials, choose a suitable poster structure, integrate available assets, generate the requested source files, and render previews when possible.

## Outputs

Depending on your request and local dependencies, the agent can return:

- Poster source files.
- Rendered previews for visual checking.
- QR/download area connected to your supplied links.
- Institution and conference branding when supported.
- A short summary of generated files, preview locations, and remaining manual checks.

## User Check

Before submission, presentation, or distribution, manually verify:

- Scientific wording and main claims.
- Formula and theorem compression.
- Figure cropping and captions.
- Citation accuracy.
- Author, affiliation, venue, and logo usage.
- Final rendered layout.

AI-assisted poster generation can speed up drafting, but the final academic judgment remains with the authors.

## References

- Rafael Bailo, Better Poster LaTeX template: https://github.com/rafaelbailo/betterposter-latex-template
- MIT Communication Lab, Toward an Even Better Poster: https://mitcommlab.mit.edu/be/2023/09/27/toward-an-evenbetterposter-improving-the-betterposter-template/

## License

This repository remains MIT licensed. The included `templates/betterposter.cls` is a lightweight compatible implementation for this skill and is not a vendored copy of Rafael Bailo's GPL-licensed class.

Review institution logo copyright, trademark, and attribution requirements before redistributing generated logo files.

[中文版](README.zh-CN.md)
