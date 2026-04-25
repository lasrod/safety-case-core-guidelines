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

- pick the next unused number in the relevant category
- set `category` to the two-letter prefix and `number` to the integer suffix
- set `order` to `number * 10` (the generator orders guidelines within a category by `order`)

If a guideline is retired, leave its id reserved and document the change in `migration_notes` rather than reusing the id.

## Required fields per guideline

Every guideline entry must include:

- `id` (for example `CL.1`)
- `category` (matches the id prefix)
- `number` (matches the id suffix)
- `order`
- `title`
- `guideline`
- `why`
- `review_prompts` (non-empty list)
- `example` with non-empty `markdown` and structured `cases`
- `references` (structured list of `{source_id, clauses?}` referencing entries in `reference_sources`)

The only optional generic field is `note` — used for short clarifying notes that should appear on the page after the example. The legacy keys `typical_fix`, `fix`, `notes`, and `note_type` are not allowed; if you need to add a note, use the single `note` field.

## Tool guidance

Each guideline may carry an optional `tool_guidance` block consumed by tools that build on these guidelines (linters, advisors, AI prompts). It is not rendered on the site. Keep it:

- specific to the guideline
- concise
- focused on what a tool would need to detect or check

Fields: `applicable_elements`, `detection_hints`, `suggested_checks` (each with `id` and `description`), and `suggested_ai_prompt`.

## References

When proposing a new reference:
- ensure it is relevant to the specific guideline
- cite the specific source, not only a general document name
- if it is a new source, add it once to `reference_sources` and reference its `source_id` from each guideline that uses it
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