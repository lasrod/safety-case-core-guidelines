# Review Profiles

Review profiles are authored in [content/tool_support/review_profiles.yaml](../content/tool_support/review_profiles.yaml) and generated into [dist/review_profiles.json](../dist/review_profiles.json).

Each profile contains:

- `id`
- `display_name`
- `description`
- `applies_to`, naming elements from `selectable_elements`
- `guideline_ids`
- `required_data`
- `optional_data`
- `data_rationale`, explaining why each required and optional data package is used by that profile
- `when_absent`, present where a required package can legitimately be unavailable

## Selecting a profile

Each selectable element maps to exactly one profile, so a tool resolves the profile from the selected element without asking the user. The elements of a profile all share one `element_role`, and the profile requires exactly one data package whose `role` is `selected_element` and whose `element_role` matches. Validation enforces all three rules.

That is the intended lookup: from the selected element, to its element role, to the profile, to the selected-element package that carries it.

## When required data is missing

A `when_absent` entry names a required package a tool may be unable to build, the guidelines of that profile which then cannot be assessed, and what the review should say instead. It exists so that a degraded review is a declared outcome rather than an improvised one, and so that two tools degrade the same way.

`evidence_review` carries one for `EVIDENCE_BASIS`. The artifacts an evidence basis describes — coverage, thresholds, scenario sets, configuration, limitations — are often not held by the tool at all, so without them a review can judge citation, control, and element role, but not sufficiency, and it must say so.

## Validation

Validation requires all `guideline_ids` to exist in [content/guidelines/](../content/guidelines/), all data package IDs to exist in [content/tool_support/data_packages.yaml](../content/tool_support/data_packages.yaml), each `data_rationale.required` / `data_rationale.optional` list to match the profile's `required_data` / `optional_data` list exactly, and each `when_absent` entry to name a required package of that profile and only guidelines that profile applies.

Coverage output in [generated/review_profile_coverage.md](../generated/review_profile_coverage.md) shows which guidelines are included in each profile and which guidelines are not mapped to any profile.

Profiles are intended as reusable review intents. They should stay focused enough for a tool or reviewer to request the right context without pulling in unrelated guideline families.
