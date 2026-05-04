# Tool Support

SCCG tool support is authored under [content/tool_support/](../content/tool_support/) and generated into [dist/](../dist/).

The source files are:

- [content/tool_support/review_profiles.yaml](../content/tool_support/review_profiles.yaml) maps review intents to guideline IDs and data package IDs.
- [content/tool_support/data_packages.yaml](../content/tool_support/data_packages.yaml) defines context packages a tool may provide to a review workflow.
- [content/tool_support/prechecks.yaml](../content/tool_support/prechecks.yaml) defines deterministic candidate checks.

Generated consumers should usually read:

- [dist/review_profiles.json](../dist/review_profiles.json)
- [dist/data_packages.json](../dist/data_packages.json)
- [dist/prechecks.json](../dist/prechecks.json)
- [dist/sccg.full.json](../dist/sccg.full.json)

Validation ensures every review profile and pre-check references existing guideline IDs and data package IDs.

## Data packages

A data package describes information that may be available to a tool or reviewer, such as the selected element, parent element, evidence item, or change history. `required_fields` and `optional_fields` describe shape expectations; they do not prescribe a tool-specific API.

## Review profiles

A review profile groups guidelines for a common review intent. Profiles identify applicable notation elements, guideline IDs, required data packages, and optional data packages.

## Pre-checks

Pre-checks are deterministic candidate checks. They can identify cases worth review, but their `interpretation` field should make clear that reviewer or AI judgment is still required.