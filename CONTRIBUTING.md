# Contributing

Thank you for contributing to the Safety Case Core Guidelines.

## Where to make changes

The canonical source is [data/guidelines.yaml](data/guidelines.yaml). The published page [index.md](index.md) is **generated** from that YAML between these marker blocks:

- `<!-- BEGIN GENERATED: quick-index -->` / `<!-- END GENERATED: quick-index -->`
- `<!-- BEGIN GENERATED: guidelines -->` / `<!-- END GENERATED: guidelines -->`

- Edit `data/guidelines.yaml` for any change to a guideline (text, examples, references, tool guidance).
- Do not edit the generated region of `index.md` by hand — it will be overwritten and CI will reject out-of-sync pull requests.
- Preamble, scope, and "how to use" in `index.md` are still hand-maintained outside the markers.

## Scope

Contributions are welcome for:
- clarification of existing guideline text
- correction of errors or inconsistencies
- improvement of examples and review prompts
- additional publicly supportable references
- improvements to `tool_guidance` metadata
- formatting and navigation improvements
- creation of new guidelines

## Contribution principles

- Keep the text clear, concise, and review-oriented.
- Prefer one clear point per guideline entry.
- Preserve the existing guideline structure where practical.
- Keep examples realistic and easy to review.
- Avoid promotional or unnecessary wording.
- Avoid copying protected source text. Use paraphrasing and cite the source where relevant.
- Prefer publicly accessible references where possible.

## ID stability

Guideline `id` values (for example `CL.3`, `EV.7`) are stable identifiers. Do not renumber existing guidelines. When adding a new guideline:

- pick the next unused number suffix in the relevant category
- set `category` to the two-letter prefix
- the generator orders guidelines within a category by the numeric suffix of the `id`

If a guideline is retired, leave its id reserved rather than reusing the id.

Generated section anchors are ID-based. Keep IDs stable because external links and tools should target the ID anchor (for example `#cl1`) rather than title-derived anchors.

## Required fields per guideline

Every guideline entry must include:

- `id` (for example `CL.1`)
- `category` (matches the id prefix)
- `title`
- `guideline`
- `why`
- `review_prompts` (non-empty list)
- `example` with non-empty `bad`, `problem`, and `good` strings
- `references` (structured list of `{source_id, clauses?}` referencing entries in `reference_sources`)

At document root, `schema_version` is a strict compatibility contract and must match the currently supported value (`0.4.0`) unless a deliberate versioned migration is being performed.

No other top-level guideline fields are accepted. The previously supported `note`, `tags`, `number`, and `order` fields have been removed; do not reintroduce them.

## Tool guidance

Each guideline may carry an optional `tool_guidance` block consumed by tools that build on these guidelines (linters, advisors, AI prompts). It is not rendered on the site. Keep it:

- specific to the guideline
- concise
- focused on what a tool would need to detect or check

Fields: `applicable_elements`, `detection_hints`, and `suggested_checks` (each with `id` and `description`).

## References

When proposing a new reference:
- ensure it is relevant to the specific guideline
- cite the specific source, not only a general document name
- if it is a new source, add it once to `reference_sources` and reference its `source_id` from each guideline that uses it
- if a guideline needs more specific wording than the canonical source name, set `display_name` on that specific `references` entry for that guideline
- avoid adding references that do not materially support the guideline

## Regenerating and validating locally

Requires Python 3.11+.

```
pip install -r requirements.txt
python scripts/validate_guidelines.py
python scripts/generate_index.py
```

The generator is idempotent — running it twice produces the same `index.md`.

## Pull request checklist

Before opening a pull request, please confirm:

- [ ] Changes were made in `data/guidelines.yaml` (not in the generated region of `index.md`).
- [ ] `python scripts/validate_guidelines.py` passes.
- [ ] `python scripts/generate_index.py` was run and the resulting `index.md` is committed.
- [ ] Running the generator a second time produces no diff (idempotency).
- [ ] No guideline `id` was renumbered or reused.
- [ ] Any new reference source was added to `reference_sources`.
- [ ] The PR description identifies affected guideline IDs and any reference updates.

## Major changes

For significant structural changes (schema, category set, marker layout, generator behavior), please open an issue first so the proposal can be discussed before drafting a larger update.

## License

By contributing to this repository, you agree that your contribution will be released under the same license as this project.