# Schema Reference

Schemas are stored in [schemas/](../schemas/) and validate authored content plus AI export rows.

- [schemas/sccg.schema.json](../schemas/sccg.schema.json) validates [content/sccg.yaml](../content/sccg.yaml).
- [schemas/references.schema.json](../schemas/references.schema.json) validates [content/references.yaml](../content/references.yaml).
- [schemas/guideline_category.schema.json](../schemas/guideline_category.schema.json) validates each file in [content/guidelines/](../content/guidelines/).
- [schemas/review_profiles.schema.json](../schemas/review_profiles.schema.json) validates [content/tool_support/review_profiles.yaml](../content/tool_support/review_profiles.yaml).
- [schemas/data_packages.schema.json](../schemas/data_packages.schema.json) validates [content/tool_support/data_packages.yaml](../content/tool_support/data_packages.yaml).
- [schemas/data_package_diagram_layout.schema.json](../schemas/data_package_diagram_layout.schema.json) validates [content/tool_support/data_package_diagram_layout.yaml](../content/tool_support/data_package_diagram_layout.yaml).
- [schemas/prechecks.schema.json](../schemas/prechecks.schema.json) validates [content/tool_support/prechecks.yaml](../content/tool_support/prechecks.yaml).
- [schemas/authoring_guidance.schema.json](../schemas/authoring_guidance.schema.json) validates [content/tool_support/authoring_guidance.yaml](../content/tool_support/authoring_guidance.yaml).
- [schemas/ai_rule_export.schema.json](../schemas/ai_rule_export.schema.json) validates individual rows emitted to [dist/ai_rule_export.jsonl](../dist/ai_rule_export.jsonl).

JSON Schema validates local structure. [scripts/validate.py](../scripts/validate.py) performs cross-file checks that schemas cannot express reliably, including duplicate IDs, guideline category consistency, reference integrity, review profile references, pre-check references, legacy field rejection, and generated-output freshness.

It also enforces the contract rules a consuming tool relies on: one profile per selectable element, one selected-element package per profile matching its element role, guideline `applicable_elements` drawn only from the published element vocabulary, one selected-element package per pre-check, `when_absent` entries confined to their profile's required data and guidelines, an authoring guidance set covering every category, and `expected` marker lists that match their own guideline's good example.

## Versions

Two version numbers are published, and they answer different questions.

- `schema_version` is the version of the published contract: the file names under [dist/](../dist/), their top-level keys, and their field names. A major change means a consumer may need to change code. It appears in every authored file, every tool-facing file, and every rule row, and is pinned by a `const` in each schema.
- `sccg_version` in [content/sccg.yaml](../content/sccg.yaml) is the version of the guideline content, and moves whenever guidelines, examples, profiles, or checks change.

The current contract is `2.0.0`. What changed from `1.0.0`, and what a consumer has to do about it, is recorded in the versioning section of [tool-integration.md](../tool-integration.md).
