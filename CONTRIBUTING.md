# Contributing

Thank you for contributing to the Safety Case Core Guidelines.

## Where to make changes

The canonical authored source is [content/](content/):

- Edit [content/sccg.yaml](content/sccg.yaml) for document metadata, policy, method guidance, ID scheme, and required sections.
- Edit [content/references.yaml](content/references.yaml) for reference source registry changes.
- Edit [content/guidelines/](content/guidelines/) for guideline text, examples, references, review prompts, and tool metadata.
- Edit [content/tool_support/](content/tool_support/) for review profiles, data packages, and pre-check metadata.

Do not edit [dist/](dist/), [generated/](generated/), generated regions of [index.md](index.md), generated regions of [tool-integration.md](tool-integration.md), or files in [assets/generated/review_profile_diagrams/](assets/generated/review_profile_diagrams/) by hand. They are rebuilt from [content/](content/).

## Generated files

[index.md](index.md) is generated between these marker blocks:

- `<!-- BEGIN GENERATED: quick-index -->` / `<!-- END GENERATED: quick-index -->`
- `<!-- BEGIN GENERATED: guidelines -->` / `<!-- END GENERATED: guidelines -->`

Preamble, scope, and usage text outside those markers remain hand-maintained.

[tool-integration.md](tool-integration.md) is also generated in part between these marker blocks:

- `<!-- BEGIN GENERATED: tool-overview -->` / `<!-- END GENERATED: tool-overview -->`
- `<!-- BEGIN GENERATED: review-profiles -->` / `<!-- END GENERATED: review-profiles -->`
- `<!-- BEGIN GENERATED: prechecks -->` / `<!-- END GENERATED: prechecks -->`

Review-profile SVG diagrams are generated into [assets/generated/review_profile_diagrams/](assets/generated/review_profile_diagrams/). These files are ignored by Git and should be regenerated locally when needed. The GitHub Pages deployment workflow also regenerates them before publishing the site.

## Guideline fields

Every guideline entry must include:

- `id`, for example `CL.1`
- `category`, matching the ID prefix
- `title`
- `statement`
- `rationale`
- `review_prompts`
- `examples` with non-empty `bad`, `problem`, and `good` strings
- `references`, using `source_id` values from [content/references.yaml](content/references.yaml)

Optional tool metadata belongs in `tool`. Do not reintroduce the legacy field names `guideline`, `why`, `example`, or `tool_guidance`.

## ID stability

Guideline IDs are stable identifiers. Do not renumber existing guidelines. When adding a new guideline:

- Pick the next unused number suffix in the relevant category.
- Set `category` to the two-letter prefix.
- Add it to the matching category file in [content/guidelines/](content/guidelines/).

If a guideline is retired, leave its ID reserved rather than reusing it. Generated anchors are ID-based, so external links and tools should target IDs such as `#cl1`.

## Tool support metadata

Review profiles map review intents to guideline IDs and data packages. Data packages describe expected review context. Pre-checks define deterministic candidate checks; they do not replace reviewer or AI judgment.

Keep tool-support metadata concise, deterministic, and linked only to existing guideline and data package IDs. Broken references fail validation.

## References

When proposing a new reference:

- Add the source once to [content/references.yaml](content/references.yaml).
- Reference it from guidelines using `references[].source_id`.
- Use `references[].clauses` where useful.
- Use `references[].display_name` only when a guideline needs a more specific display label.
- Avoid copying protected source text; paraphrase and cite instead.

## Local validation

Requires Python 3.11+.

```bash
pip install -r requirements.txt
python scripts/build_dist.py
python scripts/build_site.py
python scripts/check_coverage.py
python scripts/validate.py
```

The build scripts are deterministic. Running them repeatedly on unchanged content should produce no diff.

## Pull request checklist

Before opening a pull request, confirm:

- [ ] Changes were made in [content/](content/), not generated files.
- [ ] `python scripts/build_dist.py` was run.
- [ ] `python scripts/build_site.py` was run.
- [ ] `python scripts/check_coverage.py` was run.
- [ ] `python scripts/validate.py` passes.
- [ ] `git diff --exit-code` passes after generated files are committed.
- [ ] No guideline ID was renumbered or reused.
- [ ] Any new references, review profile links, data package links, or pre-check links validate.

## License

By contributing to this repository, you agree that your contribution will be released under the same license as this project.