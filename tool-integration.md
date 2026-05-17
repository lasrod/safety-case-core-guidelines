---
title: Tool integration
description: Secondary documentation for engineers integrating SCCG review profiles and tool-support assets.
---

# Tool integration

This page is for engineers who want to integrate SCCG into review tooling. The main guidelines remain on the home page; this page explains the machine-readable assets and the generated review-profile documentation that sits behind them.

## What this page covers

- Which generated files tools should consume.
- How review profiles describe reusable review features.
- Which data packages a tool needs to provide for each profile.
- Which deterministic pre-checks are available as candidate signals.

<!-- BEGIN GENERATED: tool-overview -->
## Tool-facing assets

Tools should normally consume generated files in `dist/` rather than authored YAML in `content/`.

### Core files


- `dist/sccg.full.json`: Complete normalized SCCG model, including guidelines, review profiles, data packages, and pre-checks.

- `dist/review_profiles.json`: Review profile registry for selecting review intent and expected tool context.

- `dist/data_packages.json`: Data package registry describing the context a tool may provide to a review workflow.

- `dist/data_package_diagram_layout.json`: Fixed diagram layout for review-profile visualizations, with SEL centered and all other package types pinned to stable positions.

- `dist/prechecks.json`: Deterministic candidate checks that a tool can run before human or AI judgment.

- `dist/sccg.rules.jsonl`: One guideline per JSONL line for retrieval or rule loading.

- `dist/ai_rule_export.jsonl`: AI-oriented export with one SCCG guideline per line and tool-facing metadata.

- `dist/vectorstore_manifest.json`: Recommended ingestion files and metadata fields for retrieval systems.

- `schemas/`: JSON Schema contracts for authored content and exports.


### Review workflow model

1. Select an assurance-case element.
2. Choose the review profile that matches the intended review question.
3. Collect the required data packages and any useful optional data.
4. Run deterministic pre-checks where they exist.
5. Apply guideline judgment and cite SCCG guideline IDs in the result.
<!-- END GENERATED: tool-overview -->

<!-- BEGIN GENERATED: review-profiles -->
### Claim wording review

Reviews whether a selected claim is clear, falsifiable, bounded, and not overloaded.

- Profile ID: `claim_wording_review`
- Applies to: GSN Goal, SACM Claim, CAE Claim
- Required data: SEL, DIRECT_CONTEXT
- Optional data: PARENT, CHILDREN, INHERITED_CONTEXT, PROJECT_GLOSSARY
- Guidelines: CL.1, CL.2, CL.3, CL.4, CL.5, CL.6, RD.4, LF.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/claim_wording_review.svg)


### Claim context review

Reviews whether the selected claim has enough context, scope, assumptions, and definitions.

- Profile ID: `claim_context_review`
- Applies to: GSN Goal, SACM Claim, CAE Claim
- Required data: SEL, DIRECT_CONTEXT, INHERITED_CONTEXT
- Optional data: PARENT, PROJECT_GLOSSARY, STANDARD_LINKS
- Guidelines: CL.4, CL.5, AR.3, SU.2, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/claim_context_review.svg)


### Decomposition review

Reviews whether a selected claim is decomposed by clear child claims and reasoning, or whether a selected strategy or reasoning step explains why child claims support the parent claim.

- Profile ID: `decomposition_review`
- Applies to: GSN Goal, SACM Claim, CAE Claim, GSN Strategy, SACM ArgumentReasoning, CAE Argument
- Required data: SEL, PARENT, CHILDREN, STRATEGY, DIRECT_CONTEXT, INHERITED_CONTEXT
- Optional data: EVIDENCE_PATH, PROJECT_GLOSSARY
- Guidelines: CL.2, CL.3, CL.6, AR.1, AR.2, AR.4, AR.5, LF.1
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/decomposition_review.svg)


### Strategy review

Reviews whether a strategy or reasoning step explains the inference between parent and supporting claims.

- Profile ID: `strategy_review`
- Applies to: GSN Strategy, SACM ArgumentReasoning, CAE Argument
- Required data: SEL, PARENT, CHILDREN, DIRECT_CONTEXT
- Optional data: INHERITED_CONTEXT, PROJECT_GLOSSARY, STANDARD_LINKS
- Guidelines: AR.1, AR.2, AR.4, AR.5, LF.1
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/strategy_review.svg)


### Evidence item review

Reviews whether an evidence item is precise, controlled, stable, and usable for review.

- Profile ID: `evidence_item_review`
- Applies to: GSN Solution, SACM ArtifactReference, CAE Evidence
- Required data: SEL, EVIDENCE_ITEM
- Optional data: EVIDENCE_BASIS, CHANGE_HISTORY
- Guidelines: EV.2, EV.4, EV.7, EV.8, SU.3, SU.7
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/evidence_item_review.svg)


### Evidence path review

Reviews whether the selected claim is ultimately supported by appropriate evidence.

- Profile ID: `evidence_path_review`
- Applies to: GSN Goal, SACM Claim, CAE Claim
- Required data: SEL, EVIDENCE_PATH, CHILDREN
- Optional data: STRATEGY, EVIDENCE_ITEM, EVIDENCE_BASIS, DIRECT_CONTEXT
- Guidelines: EV.1, EV.3, EV.5, EV.6, EV.9, LF.2, LF.5, LF.7
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/evidence_path_review.svg)


### Assumption review

Reviews whether assumptions are explicit, appropriate, and not hiding unsupported claims.

- Profile ID: `assumption_review`
- Applies to: GSN Assumption, SACM Claim, CAE Assumption
- Required data: SEL, DIRECT_CONTEXT, INHERITED_CONTEXT
- Optional data: PARENT
- Guidelines: AR.3, AR.7, SU.2, SU.9, SU.10, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/assumption_review.svg)


### Justification review

Reviews whether justifications explain rationale without replacing needed argument or evidence.

- Profile ID: `justification_review`
- Applies to: GSN Justification, SACM ArgumentReasoning, CAE Justification
- Required data: SEL, PARENT
- Optional data: STRATEGY, EVIDENCE_PATH, EVIDENCE_ITEM, CHANGE_HISTORY
- Guidelines: AR.8, AR.9, SU.3, SU.5, LF.3, RD.5
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/justification_review.svg)
<!-- END GENERATED: review-profiles -->

<!-- BEGIN GENERATED: prechecks -->
### Goal has children but no explicit strategy

Detects candidate cases where a claim is decomposed without an explicit reasoning step.

- Pre-check ID: `check-explicit-strategy`
- Expected data: SEL, CHILDREN, STRATEGY
- Related guidelines: AR.2
- Result type: `boolean_candidate`
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.


### No evidence path

Detects candidate cases where a claim has no path to evidence and is not intentionally undeveloped.

- Pre-check ID: `check-evidence-trace`
- Expected data: SEL, EVIDENCE_PATH
- Related guidelines: EV.1
- Result type: `boolean_candidate`
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.


### Evidence reference too broad

Detects candidate cases where a solution cites a broad artifact without precise location.

- Pre-check ID: `check-evidence-citation-precision`
- Expected data: EVIDENCE_ITEM
- Related guidelines: EV.4
- Result type: `boolean_candidate`
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.


### Evidence missing control attributes

Detects evidence references without useful control attributes such as owner, version, status, date, or location.

- Pre-check ID: `check-evidence-control-attributes`
- Expected data: EVIDENCE_ITEM
- Related guidelines: EV.7
- Result type: `missing_fields`
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.


### Live mutable evidence reference

Detects evidence references that appear to point to mutable live documents without a fixed version.

- Pre-check ID: `check-evidence-state-fixed`
- Expected data: EVIDENCE_ITEM
- Related guidelines: EV.8
- Result type: `boolean_candidate`
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.
<!-- END GENERATED: prechecks -->
