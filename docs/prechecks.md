# Pre-checks

Pre-checks are authored in [content/tool_support/prechecks.yaml](../content/tool_support/prechecks.yaml) and generated into [dist/prechecks.json](../dist/prechecks.json).

A pre-check defines a deterministic candidate signal:

- `id`
- `display_name`
- `related_guideline_ids`
- `expected_data`
- `result_type`, either `boolean_candidate` or `missing_fields`
- `description`
- `fires_when`
- `interpretation`

Pre-checks do not implement tool-specific logic. They define what a deterministic tool could look for and how the result should be interpreted.

## `fires_when` is the definition

`description` says what the check is about; `fires_when` says exactly when it reports a candidate, including which element it runs on. It is written to be precise enough that two tools implement the same check.

A tool that answers a different question must not report the pre-check's id. Reporting a pre-check id for a different check is worse than reporting no id: a tool that says `check-explicit-strategy` found nothing will be read as having run SCCG's check, and it has not.

`expected_data` names exactly one selected-element package, which is what identifies the element the check runs on. `check-explicit-strategy`, for example, expects `SELECTED_CLAIM`, `CHILDREN`, and `STRATEGY`: it fires on a claim that has children and no reasoning step, not on a strategy that develops into nothing.

## Two registries, deliberately separate

There are two sets of check identifiers, and they answer different questions.

- A guideline's `tool.suggested_checks` names a check a tool *might* implement for that guideline, with a description of what it would examine. Most guidelines have one; some have two.
- `prechecks` is the published subset that carries a full contract: expected data, a result type, a firing condition, and SCCG's own wording for how far the result may be trusted.

Every pre-check id is also a `suggested_checks` id — validation enforces that — so a finding and a pre-check line up. The reverse does not hold: a `suggested_checks` id is not a pre-check, and a tool implementing one should not present it as though it carried the pre-check contract.

## Interpretation

Pre-check results are candidate signals, not findings. The `interpretation` string is carried so that a tool reports the limit along with the result rather than paraphrasing it away, and so that a reviewer sees the difference between "a check fired" and "the argument is defective".

Validation requires all related guideline IDs and expected data package IDs to exist. Coverage output in [generated/rule_coverage.md](../generated/rule_coverage.md) shows which guidelines have related pre-checks and which pre-checks are not referenced by guideline tool metadata.
