# Tool Support

SCCG tool support is authored under [content/tool_support/](../content/tool_support/) and generated into [dist/](../dist/).

The source files are:

- [content/tool_support/review_profiles.yaml](../content/tool_support/review_profiles.yaml) declares the selectable element vocabulary and maps review intents to guideline IDs and data package IDs.
- [content/tool_support/data_packages.yaml](../content/tool_support/data_packages.yaml) defines context packages a tool may provide to a review workflow, and the availability states a tool reports when it cannot provide one.
- [content/tool_support/prechecks.yaml](../content/tool_support/prechecks.yaml) defines deterministic candidate checks.
- [content/tool_support/authoring_guidance.yaml](../content/tool_support/authoring_guidance.yaml) names the guidelines a tool should deliver while an author or an AI agent is writing.

Generated consumers should usually read:

- [dist/review_profiles.json](../dist/review_profiles.json)
- [dist/data_packages.json](../dist/data_packages.json)
- [dist/prechecks.json](../dist/prechecks.json)
- [dist/authoring_guidance.json](../dist/authoring_guidance.json)
- [dist/sccg.full.json](../dist/sccg.full.json)

Validation ensures every review profile and pre-check references existing guideline IDs and data package IDs, and enforces the structural rules below.

## Element vocabulary

`selectable_elements` is the complete set of elements a review profile may apply to, named in GSN and CAE because those are the notations authors and reviewers see. Each entry carries an `element_role`: `claim`, `strategy`, `evidence`, `context`, `assumption`, `justification`, or `challenge`.

`element_role` is the mapping point for a tool whose internal model is neither GSN nor CAE. Map the tool's own element types onto the role, present element names in the notation the user sees, and match profiles by those names. The same roles are used by selected-element data packages and by `tool.repair`, so one mapping serves element selection, profile selection, and repair rendering.

A guideline's `tool.applicable_elements` may only use names from this vocabulary.

## Data packages

A data package describes information that may be available to a tool or reviewer.

Each package has a `role`:

- `selected_element` marks the package carrying the element under review. There is one per element role — `SELECTED_CLAIM`, `SELECTED_STRATEGY`, `SELECTED_EVIDENCE`, `SELECTED_CONTEXT`, `SELECTED_ASSUMPTION`, `SELECTED_JUSTIFICATION`, `SELECTED_CHALLENGE` — and every review profile requires exactly one of them. A tool that does not want to hard-code the seven names can find it by role.
- `supporting` marks everything supplied around the reviewed element.

`required_fields` are the fields a supplied package must carry; a list-valued field may be empty, and an absent field is not the same as an empty list. `optional_fields` are useful where the tool has them. Packages carrying a single element use `element_id`, `element_type`, and `text`, and array-valued fields contain elements of the same shape.

## Availability

A tool that cannot supply a package should report which state applies rather than omitting it silently: `available`, `not_implemented` (no source for it at all), `empty` (a source exists and this case has nothing in it), or `withheld` (the data exists and was deliberately not shared). A review told nothing assumes the data does not exist, and may report a sufficiency finding that is an artifact of what it was not shown.

Where a required package can legitimately be unavailable, the profile carries a `when_absent` entry naming which of its guidelines then cannot be assessed, and what the review should say instead. `evidence_review` carries one for `EVIDENCE_BASIS`: without it, a review can judge citation, control, and element role, but not sufficiency, and it must say so rather than reporting a degraded review as a complete one.

## Review profiles

A review profile groups guidelines for a common review intent. Profiles identify applicable notation elements, guideline IDs, required data packages, and optional data packages.

Each selectable element maps to exactly one profile, and each profile's elements all share one element role, so a tool can resolve the profile from the selected element without asking the user.

## Pre-checks

Pre-checks are deterministic candidate checks. They can identify cases worth review, but their `interpretation` field should make clear that reviewer or AI judgment is still required. Each pre-check's `fires_when` sentence defines the check: a tool that answers a different question must not report that pre-check's id.

## Authoring guidance

The authoring set is the SCCG subset a tool delivers while an element is being written, rather than when it is reviewed. `core_rules` is an ordered list of guidelines, each rendered from that guideline's own `short_rule`, with a recorded reason for its inclusion; every guideline category is represented. `element_rules` names the review profile each element role will be judged under, so a tool's authoring guidance and its review criteria come from the same source and cannot drift apart.

The set is a delivery subset, not a reduced standard. A tool must not present it as the whole of SCCG.
