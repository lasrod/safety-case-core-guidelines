# Safety Case Core Guidelines

Published site: https://lasrod.github.io/safety-case-core-guidelines/

This repository contains the source for the Safety Case Core Guidelines.

## Authoritative source

The canonical source of the guidelines is the structured data file:

- [data/guidelines.yaml](data/guidelines.yaml)

The human-readable site page [index.md](index.md) is **generated** from that YAML between the markers:

```
<!-- BEGIN GENERATED: guidelines -->
<!-- END GENERATED: guidelines -->
```

Everything outside those markers (preamble, scope, how to use, quick index) is hand-maintained.

Do not edit the generated section of `index.md` by hand. Edit `data/guidelines.yaml` instead and regenerate.

## Tooling consumers

Tools that build on these guidelines (linters, advisors, model prompts) should consume `data/guidelines.yaml` directly. The schema is defined in [schemas/guidelines.schema.json](schemas/guidelines.schema.json).

Each guideline carries an optional `tool_guidance` block (applicable elements, detection hints, suggested checks, and a suggested AI prompt). This block is metadata for tooling and does not appear on the published site.

## Regenerating the site page

Requires Python 3.11+.

```
pip install -r requirements.txt
python scripts/validate_guidelines.py
python scripts/generate_index.py
```

The generator is idempotent. Running it twice on the same YAML produces the same `index.md`.

CI runs both scripts and fails if `index.md` is not in sync with `data/guidelines.yaml`.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to contribute to this project.

## License

Licensed under CC BY 4.0.