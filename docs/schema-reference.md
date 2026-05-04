# Schema Reference

Schemas are stored in [schemas/](../schemas/) and validate authored content plus AI export rows.

- [schemas/sccg.schema.json](../schemas/sccg.schema.json) validates [content/sccg.yaml](../content/sccg.yaml).
- [schemas/references.schema.json](../schemas/references.schema.json) validates [content/references.yaml](../content/references.yaml).
- [schemas/guideline_category.schema.json](../schemas/guideline_category.schema.json) validates each file in [content/guidelines/](../content/guidelines/).
- [schemas/review_profiles.schema.json](../schemas/review_profiles.schema.json) validates [content/tool_support/review_profiles.yaml](../content/tool_support/review_profiles.yaml).
- [schemas/data_packages.schema.json](../schemas/data_packages.schema.json) validates [content/tool_support/data_packages.yaml](../content/tool_support/data_packages.yaml).
- [schemas/prechecks.schema.json](../schemas/prechecks.schema.json) validates [content/tool_support/prechecks.yaml](../content/tool_support/prechecks.yaml).
- [schemas/ai_rule_export.schema.json](../schemas/ai_rule_export.schema.json) validates individual rows emitted to [dist/ai_rule_export.jsonl](../dist/ai_rule_export.jsonl).

JSON Schema validates local structure. [scripts/validate.py](../scripts/validate.py) performs cross-file checks that schemas cannot express reliably, including duplicate IDs, guideline category consistency, reference integrity, review profile references, pre-check references, legacy field rejection, and generated-output freshness.

The authored schema version is `1.0.0`. The SCCG content version is stored separately as `sccg_version` in [content/sccg.yaml](../content/sccg.yaml).