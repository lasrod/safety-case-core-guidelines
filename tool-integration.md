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
### Claim wording review

Reviews whether a selected claim is clear, falsifiable, bounded, and not overloaded.

- Profile ID: `claim_wording_review`
- Applies to: GSN Goal, SACM Claim, CAE Claim
- Required data: SEL, DIRECT_CONTEXT
- Optional data: PARENT, CHILDREN, INHERITED_CONTEXT, PROJECT_GLOSSARY
- Guidelines: CL.1, CL.2, CL.3, CL.4, CL.5, CL.6, RD.4, LF.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/claim_wording_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected claim text is the direct subject of this review. CL.1, CL.2, CL.3, CL.4, CL.5, CL.6, RD.4, and LF.6 all require looking at the claim wording itself to judge whether it is a falsifiable proposition, asserts one main property, avoids essay-in-the-box packing, uses clear bounded language, avoids inflated wording, and does not create false precision.

- `DIRECT_CONTEXT`: Direct context explains the immediate scope, definitions, assumptions, and local constraints that may legitimately shape the claim wording. It is required because CL.3 and AR.3 distinguish concise claim text from context that should be represented separately; without direct context, a reviewer cannot tell whether missing qualifiers are properly externalized or accidentally hidden in the claim.


Optional data:
- `PARENT`: The parent helps check whether the selected claim wording preserves the intended scope and terminology from the branch above it. It is optional because many wording defects are visible in the selected claim and direct context, but the parent is useful for spotting silent scope shifts, over-narrowing, or wording that no longer supports the parent claim.

- `CHILDREN`: Child elements help detect whether the selected claim is bundling several different claims or decomposition topics that should be separated. This supports CL.2, CL.3, and CL.6, but it is optional because a pure wording review can still be performed when child structure is not available.

- `INHERITED_CONTEXT`: Inherited context shows scope and assumptions carried down from ancestors. It helps determine whether the claim appears broader or more absolute than the inherited limits allow, especially for CL.5 and RD.6 concerns, but it is optional because not every selected claim relies on inherited context.

- `PROJECT_GLOSSARY`: The glossary supports CL.4 by resolving project-specific terms that may otherwise look ambiguous or overloaded. It is optional because many wording issues can be judged directly, but glossary definitions are important when terms such as safe, acceptable, nominal, ODD, or system-specific component names have controlled meanings.



### Claim context review

Reviews whether the selected claim has enough context, scope, assumptions, and definitions.

- Profile ID: `claim_context_review`
- Applies to: GSN Goal, SACM Claim, CAE Claim
- Required data: SEL, DIRECT_CONTEXT, INHERITED_CONTEXT
- Optional data: PARENT, PROJECT_GLOSSARY, STANDARD_LINKS
- Guidelines: CL.4, CL.5, AR.3, SU.2, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/claim_context_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected claim is required because the review asks whether that claim has enough surrounding context to be interpreted consistently. CL.4, CL.5, AR.3, SU.2, and RD.6 can only be applied by comparing the claim wording with the context and assumptions that qualify it.

- `DIRECT_CONTEXT`: Direct context is the primary evidence that scope, definitions, operating conditions, dependencies, assumptions, and justifications are visible where the claim is read. It is required for AR.3 and SU.2 because the reviewer must see whether needed context and assumptions are explicit rather than hidden in prose.

- `INHERITED_CONTEXT`: Inherited context is required because a claim's meaning is often constrained by ancestor scope, assumptions, and definitions. RD.6 warns against hidden limitations, so the reviewer needs inherited context to check whether the selected claim is still bounded by visible upstream constraints and does not contradict or silently ignore them.


Optional data:
- `PARENT`: The parent helps explain where inherited context comes from and whether the selected claim aligns with the parent branch. It is optional because inherited context may already be available as a package, but the parent is useful when context inheritance or scope narrowing is unclear.

- `PROJECT_GLOSSARY`: The glossary helps determine whether terms in the claim or context have controlled project meanings. It supports CL.4 and AR.3 when terms are domain-specific, but it is optional because not every context review depends on glossary-defined terminology.

- `STANDARD_LINKS`: Standard links are useful when the claim context depends on external standards, compliance scope, or referenced operating constraints. They are optional because many claim-context reviews are purely local, but they help verify that cited standards are relevant and not used as vague or hidden context.



### Decomposition review

Reviews whether a selected claim is decomposed by clear child claims and reasoning, or whether a selected strategy or reasoning step explains why child claims support the parent claim.

- Profile ID: `decomposition_review`
- Applies to: GSN Goal, SACM Claim, CAE Claim, GSN Strategy, SACM ArgumentReasoning, CAE Argument
- Required data: SEL, PARENT, CHILDREN, STRATEGY, DIRECT_CONTEXT, INHERITED_CONTEXT
- Optional data: EVIDENCE_PATH, PROJECT_GLOSSARY
- Guidelines: CL.2, CL.3, CL.6, AR.1, AR.2, AR.4, AR.5, LF.1
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/decomposition_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected element is required because the profile may review either a parent claim being decomposed or a strategy/reasoning element that explains a decomposition. CL.2, CL.3, CL.6, AR.1, AR.2, AR.4, AR.5, and LF.1 all depend on understanding the selected element's role in the branch.

- `PARENT`: The parent is required because decomposition quality is judged against the claim or reasoning step being supported. AR.2 asks whether the decomposition rule explains how children support the parent, AR.5 asks whether scope and terminology remain consistent, and LF.1 requires checking that support does not merely restate the parent.

- `CHILDREN`: Child elements are required because they are the actual decomposition being reviewed. CL.2 and CL.6 require checking whether the child set separates different logical steps and is complete for the stated parent, while AR.1 and AR.2 require the branch structure to make the decomposition reviewable.

- `STRATEGY`: Strategy is required because AR.2 expects the inference or decomposition rule to be explicit rather than inferred from the child list. The strategy explains why these children, in this branch, are intended to support the parent and helps reveal missing or circular reasoning under LF.1.

- `DIRECT_CONTEXT`: Direct context is required because decomposition is only valid within the selected element's stated scope, definitions, and assumptions. AR.3, AR.4, and AR.5 require checking that local context is visible and that children or strategy do not silently change the branch scope.

- `INHERITED_CONTEXT`: Inherited context is required because parent scope and ancestor assumptions constrain what the decomposition is allowed to cover. It helps identify child claims that overreach, omit inherited scope, or silently narrow terminology across the branch, which is central to AR.5 and CL.6.


Optional data:
- `EVIDENCE_PATH`: The evidence path is optional but useful when decomposition completeness depends on whether child claims eventually reach appropriate evidence. It helps distinguish a structurally plausible decomposition from one that leaves unsupported leaves or jumps to evidence without intermediate claims.

- `PROJECT_GLOSSARY`: The glossary is optional because decomposition can often be assessed from the local branch, but it helps when strategy or child claims use controlled terms whose scope must remain consistent across parent and children under AR.5.



### Strategy review

Reviews whether a strategy or reasoning step explains the inference between parent and supporting claims.

- Profile ID: `strategy_review`
- Applies to: GSN Strategy, SACM ArgumentReasoning, CAE Argument
- Required data: SEL, PARENT, CHILDREN, DIRECT_CONTEXT
- Optional data: INHERITED_CONTEXT, PROJECT_GLOSSARY, STANDARD_LINKS
- Guidelines: AR.1, AR.2, AR.4, AR.5, LF.1
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/strategy_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected strategy or reasoning element is required because its text is the object of review. AR.1 and AR.2 require the strategy to make the inference rule explicit, and LF.1 requires checking whether the reasoning adds independent support rather than restating the conclusion.

- `PARENT`: The parent is required because a strategy can only be judged relative to the claim it is intended to support. AR.2 asks whether the strategy explains how the parent is decomposed or argued, and AR.5 asks whether the strategy preserves the parent's scope and terminology.

- `CHILDREN`: Children are required because the strategy must explain why these specific supporting elements are appropriate and sufficient for the parent. Without the children, the reviewer cannot judge whether the strategy is generic, incomplete, circular, or disconnected from the actual branch.

- `DIRECT_CONTEXT`: Direct context is required because strategies often rely on local scope, assumptions, decomposition criteria, or dependencies. AR.4 and AR.5 require those constraints to be visible so the reviewer can decide whether the reasoning is valid for the branch.


Optional data:
- `INHERITED_CONTEXT`: Inherited context is optional but useful for confirming that the strategy does not silently override ancestor scope or assumptions. It supports AR.5 when the strategy uses terms or boundaries inherited from higher levels of the argument.

- `PROJECT_GLOSSARY`: The glossary is optional but useful when the strategy refers to project-specific decomposition categories, functions, hazards, ODD terms, or acceptance concepts. It supports consistent interpretation of the reasoning rule.

- `STANDARD_LINKS`: Standard links are optional but useful when a strategy claims to decompose by a standard, regulation, or external guidance structure. They help verify that the referenced decomposition basis is real, relevant, and not used as a vague appeal to authority.



### Evidence item review

Reviews whether an evidence item is precise, controlled, stable, and usable for review.

- Profile ID: `evidence_item_review`
- Applies to: GSN Solution, SACM ArtifactReference, CAE Evidence
- Required data: SEL, EVIDENCE_ITEM
- Optional data: EVIDENCE_BASIS, CHANGE_HISTORY
- Guidelines: EV.2, EV.4, EV.7, EV.8, SU.3, SU.7
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/evidence_item_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected evidence element is required because the profile reviews the evidence reference or solution as it appears in the case. The reviewer needs the selected element to know which artifact is being cited and what role it is playing in the argument.

- `EVIDENCE_ITEM`: Evidence item metadata is required because EV.2, EV.4, EV.7, and EV.8 ask whether the artifact type is reviewable, the cited location is precise, and the owner, version, date, status, and retrieval location are controlled and stable. Without this package, the profile cannot judge whether the evidence can be independently reviewed.


Optional data:
- `EVIDENCE_BASIS`: Evidence basis is optional but valuable when the review goes beyond citation hygiene to ask why the item is enough for its intended claim. It provides scope, thresholds, coverage, configurations, scenario sets, and limitations relevant to EV.5, EV.6, SU.3, and SU.7.

- `CHANGE_HISTORY`: Change history is optional because an evidence item can be reviewed from its current metadata, but prior findings, review comments, proposal history, and baseline changes help identify unstable, challenged, or stale evidence under EV.7 and EV.8.



### Evidence path review

Reviews whether the selected claim is ultimately supported by appropriate evidence.

- Profile ID: `evidence_path_review`
- Applies to: GSN Goal, SACM Claim, CAE Claim
- Required data: SEL, EVIDENCE_PATH, CHILDREN
- Optional data: STRATEGY, EVIDENCE_ITEM, EVIDENCE_BASIS, DIRECT_CONTEXT
- Guidelines: EV.1, EV.3, EV.5, EV.6, EV.9, LF.2, LF.5, LF.7
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/evidence_path_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected claim is required because the evidence path must be evaluated for the exact claim being supported. EV.1, EV.3, LF.2, LF.5, and LF.7 all depend on comparing the claim's wording and scope with the evidence chain below it.

- `EVIDENCE_PATH`: Evidence path is required because EV.1 explicitly requires the path from claim to evidence to be visible and traceable. The reviewer needs the path elements and terminal evidence items to determine whether the support can be followed without inference and whether two reviewers would trace the same support.

- `CHILDREN`: Children are required because they are the immediate first step below the selected claim. They help determine whether evidence is attached at the correct level, whether intermediate claims are skipped, and whether the branch avoids irrelevant premises under LF.2.


Optional data:
- `STRATEGY`: Strategy is optional but useful when the evidence path passes through intermediate reasoning. It explains how child claims and evidence are intended to support the selected claim and helps reveal missing inferential links under EV.6.

- `EVIDENCE_ITEM`: Evidence item metadata is optional but useful for checking whether the terminal evidence actually supports the selected claim with precise, controlled citations. It supports EV.4, EV.7, and EV.8 when path traceability depends on artifact quality.

- `EVIDENCE_BASIS`: Evidence basis is optional but important for judging sufficiency rather than mere traceability. It provides the coverage, criteria, scenarios, thresholds, and limitations needed for EV.5, EV.6, LF.5, and LF.7.

- `DIRECT_CONTEXT`: Direct context is optional but useful because the claim's local scope and assumptions define what the evidence must cover. It helps detect evidence that is relevant to a neighboring or broader claim but not sufficient for this claim's actual boundaries.



### Assumption review

Reviews whether assumptions are explicit, appropriate, and not hiding unsupported claims.

- Profile ID: `assumption_review`
- Applies to: GSN Assumption, SACM Claim, CAE Assumption
- Required data: SEL, DIRECT_CONTEXT, INHERITED_CONTEXT
- Optional data: PARENT
- Guidelines: AR.3, AR.7, SU.2, SU.9, SU.10, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/assumption_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected assumption or assumption-bearing claim is required because the review focuses on the actual dependency being asserted. SU.2, SU.9, SU.10, AR.3, AR.7, and RD.6 require checking whether the assumption is explicit, bounded, monitorable, and placed where it constrains the argument.

- `DIRECT_CONTEXT`: Direct context is required because assumptions and justifications attached at the selected point show whether the dependency is explicit and locally visible. It supports SU.2 and SU.9 by exposing the reasonableness basis, monitoring expectation, and whether a condition should instead be context or a claim.

- `INHERITED_CONTEXT`: Inherited context is required because assumptions often propagate from ancestors and constrain lower-level claims. The reviewer needs inherited assumptions to detect conflicts, over-broad inherited dependencies, or limitations that would otherwise be hidden from the selected branch under RD.6.


Optional data:
- `PARENT`: The parent is optional but useful for understanding the scope and argument location that the assumption qualifies. It helps decide whether the assumption is local to the selected element, should be inherited more broadly, or should be converted into a claim that requires support.



### Justification review

Reviews whether justifications explain rationale without replacing needed argument or evidence.

- Profile ID: `justification_review`
- Applies to: GSN Justification, SACM ArgumentReasoning, CAE Justification
- Required data: SEL, PARENT
- Optional data: STRATEGY, EVIDENCE_PATH, EVIDENCE_ITEM, CHANGE_HISTORY
- Guidelines: AR.8, AR.9, SU.3, SU.5, LF.3, RD.5
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/justification_review.svg)

#### Data package rationale

Required data:
- `SEL`: The selected justification is required because the review asks whether the justification text is local rationale or hidden support. AR.8, AR.9, SU.3, SU.5, LF.3, and RD.5 all require inspecting what the justification actually says.

- `PARENT`: The parent is required because a justification can only be judged against the element or inference it is attached to. AR.8 asks whether the justification is replacing evidence or argument, and AR.9 asks whether it explains this exact parent rather than a different issue elsewhere in the branch.


Optional data:
- `STRATEGY`: Strategy is optional but useful when the justification explains a decomposition or inference choice. It helps determine whether the justification is local rationale for that strategy or whether it is trying to carry the argument itself.

- `EVIDENCE_PATH`: Evidence path is optional but useful when the justification discusses evidence sufficiency, absence of contrary evidence, or why support is enough. It helps detect AR.8 misuse, SU.3 unsupported expert judgment, and LF.3 arguments from ignorance.

- `EVIDENCE_ITEM`: Evidence item metadata is optional but useful when the justification cites expert review, prior practice, proven-in-use evidence, or another artifact. It helps check whether the cited basis is controlled and reviewable rather than unsupported opinion.

- `CHANGE_HISTORY`: Change history is optional but valuable because prior review comments, unresolved findings, proposal changes, or baseline shifts can show whether the justification has been challenged, whether agency is clear under RD.5, and whether reused safety credit remains applicable under SU.5.
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
