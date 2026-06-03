# Better Poster Skill

Better Poster Skill helps Codex, Claude, or other AI agents generate Better Poster-style academic posters from a paper PDF, screenshots, or a LaTeX source archive.

## Files

- `SKILL.md`: Codex skill instructions.
- `system_prompt.txt`: prompt for Claude or other multimodal agents.
- `template.tex`: LaTeX poster template.
- `render_preview.py`: compile LaTeX and render a PNG preview.
- `scripts/generate_qr.py`: generate icon-centered QR codes for poster URLs.
- `assets/logos/`: saved OpenReview, ICML, ICLR, and NeurIPS logo assets.

## Install

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R Better-Poster-Skill "${CODEX_HOME:-$HOME/.codex}/skills/better-poster"
```

## Use

```text
Use $better-poster to turn this paper PDF into a Better Poster.
```

To preview the template:

```bash
python render_preview.py template.tex --out-dir build
```

To generate QR codes:

```bash
python scripts/generate_qr.py --url OpenReview=https://openreview.net/forum?id=... --out-dir figures/qr
```

## References

- Rafael Bailo, Better Poster LaTeX template: https://github.com/rafaelbailo/betterposter-latex-template
- MIT Communication Lab, Toward an Even Better Poster: https://mitcommlab.mit.edu/be/2023/09/27/toward-an-evenbetterposter-improving-the-betterposter-template/

Suggestions, issues, and improvements are welcome.
