# Safety Case Core Guidelines

Published site: https://lasrod.github.io/safety-case-core-guidelines/

This repository contains the authored source, generated website page, and tool-facing distribution files for the Safety Case Core Guidelines (SCCG).

## Repository structure

- [content/](content/) is the authored source of truth.
- [dist/](dist/) contains generated files for tools and integrations.
- [generated/](generated/) contains generated coverage reports.
- [index.md](index.md) is the generated human-readable website page.
- [tool-integration.md](tool-integration.md) is the secondary GitHub Pages page for tool-facing integration guidance.
- [schemas/](schemas/) contains JSON Schema contracts for authored content and exports.
- [scripts/](scripts/) contains validation and build tooling.

Do not edit generated files by hand. Edit [content/](content/) and regenerate outputs.

## Authored content

The guideline source is split by responsibility:

- [content/sccg.yaml](content/sccg.yaml) contains document metadata, source policy, method guidance, ID scheme, and required section names.
- [content/references.yaml](content/references.yaml) contains the reference source registry.
- [content/guidelines/](content/guidelines/) contains one file per guideline category.
- [content/tool_support/](content/tool_support/) contains review profiles, data packages, review-profile diagram layout metadata, and deterministic pre-check metadata.

Guideline entries use the current field names `statement`, `rationale`, `examples`, and `tool`. The older monolithic `data/guidelines.yaml` source has been removed; [content/](content/) is canonical.

## Generated outputs

Tool-facing files are generated into [dist/](dist/):

- `sccg.full.json` and `sccg.full.yaml` contain the complete normalized model.
- `sccg.compact.json` contains a smaller guideline-focused model.
- `sccg.rules.jsonl` and `ai_rule_export.jsonl` provide one guideline per JSONL line.
- `review_profiles.json`, `data_packages.json`, `data_package_diagram_layout.json`, and `prechecks.json` expose tool-support registries.
- `vectorstore_manifest.json` describes recommended files and chunking guidance.
- `research_metadata.json` records deterministic counts and export metadata.

Coverage reports are generated into [generated/](generated/):

- `review_profile_coverage.md`
- `data_package_coverage.md`
- `rule_coverage.md`

Tool documentation assets are generated into [assets/generated/review_profile_diagrams/](assets/generated/review_profile_diagrams/):

- one SVG diagram per review profile
- `index.html` for direct browsing of the generated diagrams

These diagram assets are generated from canonical content and are ignored by Git. The GitHub Pages deployment workflow regenerates them before building the published site, so the public tool integration page can link to them without committing generated SVGs.

## Website generation

The human-readable page [index.md](index.md) is generated between these marker blocks:

```text
<!-- BEGIN GENERATED: quick-index -->
<!-- END GENERATED: quick-index -->

<!-- BEGIN GENERATED: guidelines -->
<!-- END GENERATED: guidelines -->
```

Everything outside those markers remains hand-maintained. Generated anchors are stable and ID-based, for example `#cl1` for `CL.1`.

The tool integration page [tool-integration.md](tool-integration.md) keeps hand-maintained introduction text and generated sections for tool assets, review profiles, and pre-checks.

## Commands

Requires Python 3.11+.

```bash
pip install -r requirements.txt
python scripts/build_dist.py
python scripts/build_site.py
python scripts/check_coverage.py
python scripts/validate.py
```

For local edits, the usual flow is:

```bash
python scripts/build_dist.py
python scripts/build_site.py
python scripts/check_coverage.py
python scripts/validate.py
```

CI runs the validation and generation commands and fails if tracked generated files are not committed. The ignored diagram assets under [assets/generated/review_profile_diagrams/](assets/generated/review_profile_diagrams/) are regenerated as needed and are not tracked.

GitHub Pages is deployed by a dedicated workflow that runs the same generation and validation commands before Jekyll builds the site artifact. This ensures generated diagram assets and tool-facing files are available on the published site even when they are ignored locally.

## Tooling consumers

Tools should consume [dist/](dist/) rather than the authored YAML unless they specifically need source-level authoring data. See [tool-integration.md](tool-integration.md), [docs/tool-support.md](docs/tool-support.md), [docs/ai-integration.md](docs/ai-integration.md), [docs/review-profiles.md](docs/review-profiles.md), and [docs/prechecks.md](docs/prechecks.md).

Schema details are summarized in [docs/schema-reference.md](docs/schema-reference.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidance.

## License

Licensed under CC BY 4.0.