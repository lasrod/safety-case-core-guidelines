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


- [dist/sccg.full.json](dist/sccg.full.json): Complete normalized SCCG model, including guidelines, review profiles, data packages, and pre-checks.

- [dist/review_profiles.json](dist/review_profiles.json): Review profile registry for selecting review intent and expected tool context.

- [dist/data_packages.json](dist/data_packages.json): Data package registry describing the context a tool may provide to a review workflow.

- [dist/data_package_diagram_layout.json](dist/data_package_diagram_layout.json): Fixed diagram layout for review-profile visualizations, with SEL centered and all other package types pinned to stable positions.

- [dist/prechecks.json](dist/prechecks.json): Deterministic candidate checks that a tool can run before human or AI judgment.

- [dist/sccg.rules.jsonl](dist/sccg.rules.jsonl): One guideline per JSONL line for retrieval or rule loading.

- [dist/ai_rule_export.jsonl](dist/ai_rule_export.jsonl): AI-oriented export with one SCCG guideline per line and tool-facing metadata.

- [dist/vectorstore_manifest.json](dist/vectorstore_manifest.json): Recommended ingestion files and metadata fields for retrieval systems.

- [schemas/sccg.schema.json](schemas/sccg.schema.json): JSON Schema contract for the canonical document metadata model.

- [schemas/guideline_category.schema.json](schemas/guideline_category.schema.json): JSON Schema contract for authored guideline category files.

- [schemas/references.schema.json](schemas/references.schema.json): JSON Schema contract for the reference source registry.

- [schemas/review_profiles.schema.json](schemas/review_profiles.schema.json): JSON Schema contract for authored review profiles.

- [schemas/data_packages.schema.json](schemas/data_packages.schema.json): JSON Schema contract for data package metadata.

- [schemas/data_package_diagram_layout.schema.json](schemas/data_package_diagram_layout.schema.json): JSON Schema contract for review-profile diagram layout metadata.

- [schemas/prechecks.schema.json](schemas/prechecks.schema.json): JSON Schema contract for deterministic pre-check metadata.

- [schemas/ai_rule_export.schema.json](schemas/ai_rule_export.schema.json): JSON Schema contract for AI rule export rows.


### Review workflow model

1. Select an assurance-case element.
2. Choose the review profile that matches the intended review question.
3. Collect the required data packages and any useful optional data.
4. Run deterministic pre-checks where they exist.
5. Apply guideline judgment and cite SCCG guideline IDs in the result.
<!-- END GENERATED: tool-overview -->

<!-- BEGIN GENERATED: review-profiles -->
### Claim review

Complete review of a selected claim (goal), covering wording, context, decomposition, evidence support, reasoning soundness, and sufficiency.

- Profile ID: `claim_review`
- Applies to: GSN Goal, CAE Claim
- Required data: SEL, PARENT, CHILDREN, STRATEGY, DIRECT_CONTEXT, INHERITED_CONTEXT, EVIDENCE_PATH
- Optional data: EVIDENCE_ITEM, EVIDENCE_BASIS, PROJECT_GLOSSARY, STANDARD_LINKS, CHANGE_HISTORY
- Guidelines: CL.1, CL.2, CL.3, CL.4, CL.5, CL.6, AR.1, AR.3, AR.4, AR.5, AR.6, AR.7, EV.1, EV.3, EV.9, SU.1, SU.4, SU.5, SU.6, SU.8, SU.9, SU.11, LF.1, LF.2, LF.3, LF.4, LF.5, LF.6, LF.7, RD.1, RD.2, RD.3, RD.4, RD.5, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/claim_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected claim is the subject of the whole review. Its wording drives CL.1, CL.2, CL.3, CL.4, CL.5, CL.6, RD.2, RD.4, and LF.6, and its scope drives every structural, evidential, and sufficiency check applied to the claim.

- `PARENT`: The parent claim or reasoning step is needed to check that the claim preserves inherited scope and terminology (AR.5), still supports the branch above it, and does not merely restate it (LF.1).

- `CHILDREN`: Child elements are the decomposition and first support step below the claim. They are required for CL.2, CL.6, AR.4, LF.1, and LF.2, and to check whether evidence is attached at the correct level.

- `STRATEGY`: The connecting strategy or reasoning element shows whether the inference is made explicit rather than inferred from wording (AR.1) and whether support adds independent reasoning rather than restating the claim (LF.1); its absence is itself a finding.

- `DIRECT_CONTEXT`: Context, assumptions, and justifications attached to the claim determine whether scope, definitions, and dependencies are externalized rather than hidden in the claim text (CL.3, AR.3, AR.6, AR.7, RD.1, RD.6) and whether limitations are visible where the claim is read (RD.3, SU.9).

- `INHERITED_CONTEXT`: Scope and assumptions carried down from ancestors bound how broad or absolute the claim may be (CL.5, AR.5, RD.6) and reveal hidden or contradicted limitations under SU.9.

- `EVIDENCE_PATH`: The path from the claim to its evidence is required to judge traceable support (EV.1), correct claim subject (EV.3), premise relevance (LF.2), representativeness (LF.5), and omission of expected or contrary evidence (LF.7, SU.6, SU.8).


Optional data:
- `EVIDENCE_ITEM`: Metadata for terminal evidence helps confirm that the traced support is precise and controlled where the claim's credibility depends on the cited artifact (EV.1, EV.3).

- `EVIDENCE_BASIS`: Coverage, thresholds, scenarios, and limitations help judge whether the evidence is sufficient for the claim's scope, not merely relevant (LF.5, LF.7, SU.6, SU.8).

- `PROJECT_GLOSSARY`: Controlled definitions of terms such as safe, acceptable, nominal, or ODD resolve apparent ambiguity or overloaded wording (CL.4, AR.6).

- `STANDARD_LINKS`: Linked standard requirements help confirm that decomposition or scope claims that appeal to a standard are grounded rather than vague (AR.6), and that reused safety credit is tied to a real conformance basis (SU.5).

- `CHANGE_HISTORY`: Prior findings, review comments, and baseline state show whether the claim has been challenged, whether reused credit still applies (SU.5), and whether monitoring or open-issue commitments exist (SU.4, SU.11).



### Strategy review

Complete review of a selected strategy or reasoning step, covering whether the inference between the parent claim and its supporting claims is explicit and sound.

- Profile ID: `strategy_review`
- Applies to: GSN Strategy, CAE Argument
- Required data: SEL, PARENT, CHILDREN, DIRECT_CONTEXT
- Optional data: INHERITED_CONTEXT, EVIDENCE_PATH, PROJECT_GLOSSARY, STANDARD_LINKS, CHANGE_HISTORY
- Guidelines: AR.1, AR.2, EV.9, SU.1, LF.1
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/strategy_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected strategy or reasoning element is the object of review. AR.1 and AR.2 require it to make the inference rule explicit, and LF.1 requires checking that it adds independent support rather than restating the parent.

- `PARENT`: A strategy can only be judged against the claim it supports. AR.2 asks whether it explains how the parent is decomposed or argued, and LF.1 whether the reasoning merely restates the parent.

- `CHILDREN`: The supporting elements are needed to judge whether the reasoning rule actually produces this child set and whether the decomposition is complete, relevant, and non-circular (AR.2, LF.1).

- `DIRECT_CONTEXT`: Strategies rely on local scope, decomposition criteria, and dependencies that must be visible to decide whether the reasoning is valid for the branch (AR.1, AR.2).


Optional data:
- `INHERITED_CONTEXT`: Inherited scope and assumptions help confirm that the strategy does not silently override ancestor terminology or boundaries (AR.2 consistency).

- `EVIDENCE_PATH`: The descendant evidence path is useful when the reasoning relies on undocumented system knowledge (EV.9) or leaves plausible challenges to the decomposition unaddressed (SU.1).

- `PROJECT_GLOSSARY`: The glossary resolves project-specific decomposition categories, functions, hazards, or ODD terms used in the reasoning rule.

- `STANDARD_LINKS`: Standard links help verify that a decomposition claiming to follow a standard or external structure is grounded rather than a vague appeal to authority (AR.2).

- `CHANGE_HISTORY`: Prior findings and review comments reveal whether plausible challenges to the reasoning step have already been raised and left unaddressed (SU.1).



### Evidence review

Complete review of a selected evidence item (solution), covering reviewability, control, citation precision, sufficiency, and inferential fit to the supported claim.

- Profile ID: `evidence_review`
- Applies to: GSN Solution, CAE Evidence
- Required data: SEL, EVIDENCE_ITEM, EVIDENCE_BASIS, PARENT
- Optional data: DIRECT_CONTEXT, EVIDENCE_PATH, PROJECT_GLOSSARY, STANDARD_LINKS, CHANGE_HISTORY
- Guidelines: AR.1, EV.1, EV.2, EV.4, EV.5, EV.6, EV.7, EV.8, SU.1, SU.3, SU.6, SU.7, SU.8, LF.2, LF.5, LF.7, RD.1
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/evidence_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected solution or evidence reference is the element under review. It identifies which artifact is cited and what role it plays, which is the basis for AR.1, EV.1, and RD.1.

- `EVIDENCE_ITEM`: Artifact metadata such as type, owner, version, date, status, location, and cited section is required to judge whether the evidence type is reviewable and the citation precise, controlled, and stable (EV.2, EV.4, EV.7, EV.8).

- `EVIDENCE_BASIS`: Scope, coverage, thresholds, scenarios, configurations, and limitations are required to judge sufficiency and inferential fit rather than citation hygiene alone (EV.5, EV.6, LF.5, LF.7, SU.3, SU.6, SU.7, SU.8).

- `PARENT`: The claim the evidence supports is required to judge relevance to the immediate claim (LF.2), a correct and traceable evidence path (EV.1), and whether the inferential link is explained (EV.6).


Optional data:
- `DIRECT_CONTEXT`: The claim's local scope and assumptions define what the evidence must cover and help detect evidence that is relevant to a neighboring or broader claim but not sufficient here (LF.2, EV.5).

- `EVIDENCE_PATH`: The path from claim to this evidence helps confirm traceable support and correct attachment level, especially where intermediate claims are skipped (EV.1, LF.2).

- `PROJECT_GLOSSARY`: The glossary resolves controlled terms used in the artifact or its acceptance criteria so the evidence is interpreted consistently.

- `STANDARD_LINKS`: Standard links confirm that an evidence type or acceptance criterion that appeals to a standard is grounded rather than assumed (EV.2, EV.5).

- `CHANGE_HISTORY`: Prior findings, review comments, and baseline state identify unstable, challenged, stale, or dismissed evidence (EV.7, EV.8, SU.1, SU.6).



### Assumption review

Complete review of a selected assumption, covering whether it is explicit, bounded, correctly placed, monitorable, and not hiding an unsupported claim.

- Profile ID: `assumption_review`
- Applies to: GSN Assumption, CAE Assumption
- Required data: SEL, DIRECT_CONTEXT, INHERITED_CONTEXT
- Optional data: PARENT, CHANGE_HISTORY, PROJECT_GLOSSARY
- Guidelines: AR.1, AR.3, AR.7, SU.2, SU.4, SU.9, SU.10, RD.1, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/assumption_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected assumption is the dependency under review. SU.2, SU.9, SU.10, AR.3, AR.7, and RD.6 require checking whether it is explicit, bounded, monitorable, and correctly placed, while AR.1 and RD.1 check that it is used and signposted for its role.

- `DIRECT_CONTEXT`: Assumptions and justifications attached at the selected point expose the reasonableness basis, the monitoring expectation, and whether the condition should instead be context or a claim (SU.2, SU.9).

- `INHERITED_CONTEXT`: Assumptions often propagate from ancestors, so inherited context is required to detect conflicts, over-broad inherited dependencies, or limitations otherwise hidden from the branch (RD.6, SU.10).


Optional data:
- `PARENT`: The scope and argument location the assumption qualifies help decide whether it is local, should be inherited more broadly, or should be converted into a claim that requires support (SU.9).

- `CHANGE_HISTORY`: Prior findings and baseline state show whether the assumption is monitored, has been challenged, or needs a defined re-assessment trigger (SU.2, SU.4).

- `PROJECT_GLOSSARY`: Controlled definitions help judge whether the assumption is specific enough to be checked, challenged, and monitored (SU.10).



### Justification review

Complete review of a selected justification or warrant, covering whether it explains local rationale without replacing needed argument or evidence.

- Profile ID: `justification_review`
- Applies to: GSN Justification, CAE Warrant, CAE Side-warrant, CAE Side-claim
- Required data: SEL, PARENT
- Optional data: STRATEGY, EVIDENCE_PATH, EVIDENCE_ITEM, EVIDENCE_BASIS, CHANGE_HISTORY
- Guidelines: AR.1, AR.8, AR.9, EV.5, SU.3, SU.5, SU.7, LF.3, LF.4, RD.1, RD.5
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/justification_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected justification or warrant is the object of review. AR.8, AR.9, EV.5, SU.3, SU.5, LF.3, LF.4, RD.1, and RD.5 all require inspecting what the rationale actually says and whether it names the responsible actor.

- `PARENT`: A justification can only be judged against the element or inference it is attached to. AR.8 asks whether it replaces evidence or argument, and AR.9 whether it explains this exact parent rather than a different issue elsewhere in the branch.


Optional data:
- `STRATEGY`: When the justification explains a decomposition or inference choice, the strategy shows whether it is local rationale for that step or is trying to carry the argument itself (AR.8, AR.9).

- `EVIDENCE_PATH`: The evidence path helps detect rationale used as hidden support, arguments from ignorance, and low-risk claims resting only on simulation or uneventful operation (AR.8, LF.3, SU.7).

- `EVIDENCE_ITEM`: When the justification cites expert review, prior practice, or proven-in-use evidence, artifact metadata shows whether the cited basis is controlled and reviewable rather than unsupported opinion (SU.3, SU.5).

- `EVIDENCE_BASIS`: Coverage, thresholds, and comparison basis help judge sufficiency appeals and unjustified comparisons or distinctions (EV.5, LF.4, SU.7).

- `CHANGE_HISTORY`: Prior review comments, unresolved findings, and baseline shifts show whether the justification has been challenged, whether agency is clear (RD.5), and whether reused safety credit still applies (SU.5).



### Context review

Complete review of a selected context element, covering whether it provides sufficient, relevant, and consistent scope and definitions for the claim it qualifies.

- Profile ID: `context_review`
- Applies to: GSN Context, CAE Context
- Required data: SEL, PARENT
- Optional data: INHERITED_CONTEXT, PROJECT_GLOSSARY, STANDARD_LINKS
- Guidelines: AR.1, AR.3, AR.6, AR.7, SU.9, RD.1, RD.3, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/context_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected context element is the object of review. AR.1, AR.3, AR.6, AR.7, RD.1, and RD.3 require checking whether it is used for its role and whether it supplies clear scope, definitions, and operating conditions.

- `PARENT`: The claim or element the context qualifies is required to judge whether the context is sufficient and relevant for interpreting that claim (AR.6), whether scope and dependencies are correctly externalized to it (AR.3, AR.7), and whether limitations are visible where the claim is read (RD.3, RD.6).


Optional data:
- `INHERITED_CONTEXT`: Ancestor scope and assumptions show whether this context is consistent with, or silently narrows or contradicts, inherited limits (RD.6, SU.9).

- `PROJECT_GLOSSARY`: Controlled definitions confirm that terms introduced or relied on by the context are used consistently across the branch (AR.6).

- `STANDARD_LINKS`: When the context cites external standards or operating constraints, standard links help verify the reference is relevant and not used as vague or hidden context (AR.3).



### Challenge review

Complete review of a selected counter claim or defeater, covering whether the challenge is stated explicitly and carried to a visible resolution.

- Profile ID: `challenge_review`
- Applies to: GSN Counter Claim, CAE Defeater
- Required data: SEL, PARENT
- Optional data: CHILDREN, DIRECT_CONTEXT, CHANGE_HISTORY
- Guidelines: SU.11
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/challenge_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected counter claim or defeater is the challenge under review. SU.11 requires checking whether the challenge is stated explicitly as a distinct element rather than left in review comments or reviewer intuition.

- `PARENT`: The claim, reasoning step, or evidence being challenged is required to judge whether the challenge is relevant to its target and whether the branch has been updated to resolve it (SU.11).


Optional data:
- `CHILDREN`: Supporting elements added in response show whether the challenge was resolved by added evidence, a narrowed claim, or new assumptions and monitoring (SU.11).

- `DIRECT_CONTEXT`: Context and assumptions attached to the challenge or its target help judge whether the challenge is in scope and how its resolution constrains the affected claim (SU.11).

- `CHANGE_HISTORY`: Review comments, prior findings, and proposal history show whether the challenge was rejected, sustained, or left as a visible and traceable open issue (SU.11).
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
