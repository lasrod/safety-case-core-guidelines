# Pre-checks

Pre-checks are authored in [content/tool_support/prechecks.yaml](../content/tool_support/prechecks.yaml) and generated into [dist/prechecks.json](../dist/prechecks.json).

A pre-check defines a deterministic candidate signal:

- `id`
- `display_name`
- `related_guideline_ids`
- `expected_data`
- `result_type`
- `description`
- `interpretation`

Pre-checks do not implement tool-specific logic. They define what a deterministic tool could look for and how the result should be interpreted.

Validation requires all related guideline IDs and expected data package IDs to exist. Coverage output in [generated/rule_coverage.md](../generated/rule_coverage.md) shows which guidelines have related pre-checks and which pre-checks are not referenced by guideline tool metadata.