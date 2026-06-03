# Better Poster Skill

An AI skill for turning research papers, screenshots, or LaTeX source archives into modern academic posters based on the Better Poster idea and the MIT "Even Better Poster" refinement.

It helps an agent:

- distill a paper into a clear poster claim;
- plan the center hero section and teaser figure;
- generate a Better Poster style LaTeX poster;
- compile the poster and render a preview image.

## Files

- `SKILL.md`: Codex skill instructions.
- `system_prompt.txt`: prompt for Claude or other multimodal long-context agents.
- `template.tex`: Better Poster LaTeX skeleton.
- `render_preview.py`: helper script for LaTeX compile and PNG preview rendering.

## Install

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R Better-Poster-Skill "${CODEX_HOME:-$HOME/.codex}/skills/better-poster"
```

Example use:

```text
Use $better-poster to turn this paper PDF into a MIT-style Better Poster.
```

## Preview

```bash
python render_preview.py template.tex --out-dir build
```

## References

- Rafael Bailo, Better Poster LaTeX template: https://github.com/rafaelbailo/betterposter-latex-template
- MIT Communication Lab, Toward an Even Better Poster: https://mitcommlab.mit.edu/be/2023/09/27/toward-an-evenbetterposter-improving-the-betterposter-template/

Suggestions, issues, and improvements are welcome.
