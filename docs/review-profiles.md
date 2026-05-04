# Review Profiles

Review profiles are authored in [content/tool_support/review_profiles.yaml](../content/tool_support/review_profiles.yaml) and generated into [dist/review_profiles.json](../dist/review_profiles.json).

Each profile contains:

- `id`
- `display_name`
- `description`
- `applies_to`
- `guideline_ids`
- `required_data`
- `optional_data`

Validation requires all `guideline_ids` to exist in [content/guidelines/](../content/guidelines/) and all data package IDs to exist in [content/tool_support/data_packages.yaml](../content/tool_support/data_packages.yaml).

Coverage output in [generated/review_profile_coverage.md](../generated/review_profile_coverage.md) shows which guidelines are included in each profile and which guidelines are not mapped to any profile.

Profiles are intended as reusable review intents. They should stay focused enough for a tool or reviewer to request the right context without pulling in unrelated guideline families.