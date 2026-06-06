# Institution logo cache

This directory is the default runtime cache location for institution logos resolved by:

```bash
python scripts/resolve_institution_logo.py --institution "Massachusetts Institute of Technology"
```

or inferred from a source file/directory:

```bash
python scripts/resolve_institution_logo.py --source paper.tex --download
python scripts/resolve_institution_logo.py --source source_archive_dir --download
```

The templates look for:

```text
assets/institution-logos/current-logo.png
assets/institution-logos/current-institution.txt
```

from the repository root, referenced as `../assets/institution-logos/current-logo.png` inside `templates/*.tex` and `templates/*.html`.

## Behavior

- The resolver only matches institutions configured in `assets/institution-data/csrankings_top100_institutions.json`.
- On a cache hit, it copies `assets/institution-logos/cache/<institution-slug>.png` to `assets/institution-logos/current-logo.png`.
- On a cache miss, the logo area stays blank unless `--download` is passed.
- With `--download`, the resolver tries Wikidata/Commons, Wikipedia page images, Clearbit logo lookup, Google favicon, and DuckDuckGo icon lookup.
- If no supported institution or logo is found, `current-logo.png` is removed so the poster brand area remains blank.

## Notes

- Generated logo image files and metadata JSON are ignored by `.gitignore` by default.
- University logos and seals may be copyrighted or trademarked. Review each generated logo before redistributing it.
