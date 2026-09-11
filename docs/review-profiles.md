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
- `review_passes`, optional, splitting a large profile's guidelines by review question
- `when_absent`, optional, an exception to the general rule for missing data

## Selecting a profile

Each selectable element maps to exactly one profile, so a tool resolves the profile from the selected element without asking the user. The elements of a profile all share one `element_role`, and the profile requires exactly one data package whose `role` is `selected_element` and whose `element_role` matches. Validation enforces all three rules.

That is the intended lookup: from the selected element, to its element role, to the profile, to the selected-element package that carries it.

## Review passes

`claim_review` applies 33 guidelines, which is a long checklist for a person and a crowded request for a model: guidelines that answer the same kind of question are more often cited in each other's place when they arrive together. `review_passes` splits the profile into four questions (wording, structure, sufficiency, reasoning). Each guideline of the profile is in exactly one pass, so a reviewer can work through them in turn, and a tool can send one request per pass and merge the findings. Profile selection does not change: the element still resolves to one profile.

Two registry-level sentences make a fanned-out review the same across tools. `review_pass_instruction` is sent verbatim with each pass request, with `{question}` replaced by the pass's question. `review_pass_merge` says that a finding counts only for the pass that carries its guideline, so one cited under another pass's guideline is discarded, and that a review with a pass that did not complete is incomplete rather than clean.

## When data is missing

The data package registry publishes one rule, `when_unavailable`, for every profile and package: assess every guideline against the data that was supplied, never treat a missing package as a finding or as a reason to skip a guideline, and say which packages were unavailable. A profile does not need a statement of its own for that to hold.

A `when_absent` entry is the exception: it names a required package whose absence leaves some of the profile's guidelines with nothing to judge, and what the review should say instead. No profile carries one in the current content. `evidence_review` used to carry one for `EVIDENCE_BASIS`, but the guidelines it silenced turned out to be assessable from the argument itself, so the package is now optional and the general rule applies.

## Validation

Validation requires all `guideline_ids` to exist in [content/guidelines/](../content/guidelines/) and not be retired, all data package IDs to exist in [content/tool_support/data_packages.yaml](../content/tool_support/data_packages.yaml), each `data_rationale.required` / `data_rationale.optional` list to match the profile's `required_data` / `optional_data` list exactly, `review_passes` to list every guideline of the profile exactly once and nothing else, and each `when_absent` entry to name a required package of that profile and only guidelines that profile applies.

Coverage output in [generated/review_profile_coverage.md](../generated/review_profile_coverage.md) shows which guidelines are included in each profile and which guidelines are not mapped to any profile.

Profiles are intended as reusable review intents. They should stay focused enough for a tool or reviewer to request the right context without pulling in unrelated guideline families.
