# Institution logo cache

This directory is the default cache location for institution logos resolved by:

```bash
python scripts/resolve_institution_logo.py --institution "Massachusetts Institute of Technology"
```

or inferred from a source file/directory:

```bash
python scripts/resolve_institution_logo.py --source paper.tex
python scripts/resolve_institution_logo.py --source source_archive_dir
```

The templates look for:

```text
assets/institutions/current-logo.png
```

from the repository root, referenced as `../assets/institutions/current-logo.png` inside `templates/*.tex` and `templates/*.html`.

## Notes

- Logos are downloaded on demand rather than vendored into the repository.
- The resolver uses the public CSRankings institutions list as an institution-name candidate source when available.
- The image lookup falls back through Wikipedia/Wikidata/Commons.
- Review each logo's copyright, trademark, and attribution requirements before public redistribution.
- Generated logo image files and metadata JSON are ignored by `.gitignore` by default.
