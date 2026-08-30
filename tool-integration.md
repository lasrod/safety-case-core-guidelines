---
title: Tool integration
description: Secondary documentation for engineers integrating SCCG into review tooling, authoring tools, AI assistants, and MCP servers.
---

# Tool integration

This page is for engineers who want to integrate SCCG into a tool. The main guidelines remain on the home page; this page explains the machine-readable assets, how to carry SCCG into an authoring or AI-assisted workflow, and the generated review-profile documentation that sits behind them.

## What this page covers

- Which generated files tools should consume.
- How to carry SCCG into an AI, agent, or MCP integration, and what such a tool may and may not claim.
- How review profiles describe reusable review features.
- Which data packages a tool needs to provide for each profile, and what a review may still conclude when one is missing.
- Which deterministic pre-checks are available as candidate signals.
- How element names map onto notation-neutral element roles.

<!-- BEGIN GENERATED: tool-overview -->
## Tool-facing assets

Tools should normally consume generated files in `dist/` rather than authored YAML in `content/`.

### Core files


- [dist/sccg.full.json](dist/sccg.full.json): Complete normalized SCCG model, including guidelines, review profiles, data packages, and pre-checks.

- [dist/review_profiles.json](dist/review_profiles.json): Review profile registry for selecting review intent and expected tool context.

- [dist/data_packages.json](dist/data_packages.json): Data package registry describing the context a tool may provide to a review workflow.

- [dist/data_package_diagram_layout.json](dist/data_package_diagram_layout.json): Fixed diagram layout for review-profile visualizations, with the selected-element package centered and all other package types pinned to stable positions.

- [dist/prechecks.json](dist/prechecks.json): Deterministic candidate checks that a tool can run before human or AI judgment.

- [dist/authoring_guidance.json](dist/authoring_guidance.json): Authoring-time delivery set: the condensed core rules, and the review profile each element role will be judged under.

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

- [schemas/authoring_guidance.schema.json](schemas/authoring_guidance.schema.json): JSON Schema contract for the authoring-time guidance set.

- [schemas/ai_rule_export.schema.json](schemas/ai_rule_export.schema.json): JSON Schema contract for AI rule export rows.


### Review workflow model

1. Select an assurance-case element.
2. Choose the review profile that matches the intended review question.
3. Collect the required data packages and any useful optional data.
4. Run deterministic pre-checks where they exist.
5. Apply guideline judgment and cite SCCG guideline IDs in the result.

### Authoring workflow model

1. Deliver the authoring guidance set below while the author or agent is writing.
2. Write or change an element.
3. Run the mechanical checks the tool implements, and report which checks ran.
4. Offer the repair each guideline prescribes, rather than rewriting the argument.
5. Leave judgment to a review; authoring-time checks are not a conformance statement.

### Element vocabulary

A review profile applies to notation elements. `element_role` is the notation-neutral role behind them: a tool whose internal model is neither GSN nor CAE maps its own element types onto the role, and presents element names in the notation its users see.

| Element | Notation | Element role |
| --- | --- | --- |
| GSN Goal | GSN | `claim` |
| GSN Strategy | GSN | `strategy` |
| GSN Solution | GSN | `evidence` |
| GSN Context | GSN | `context` |
| GSN Assumption | GSN | `assumption` |
| GSN Justification | GSN | `justification` |
| GSN Counter Claim | GSN | `challenge` |
| CAE Claim | CAE | `claim` |
| CAE Argument | CAE | `strategy` |
| CAE Evidence | CAE | `evidence` |
| CAE Context | CAE | `context` |
| CAE Assumption | CAE | `assumption` |
| CAE Warrant | CAE | `justification` |
| CAE Side-warrant | CAE | `justification` |
| CAE Side-claim | CAE | `justification` |
| CAE Defeater | CAE | `challenge` |


### Data package availability

A tool that cannot supply a package should say which of these applies, rather than omitting the package silently. A review told nothing cannot tell absent data from an unimplemented source, and may report a sufficiency finding that is an artifact of what it was not shown.

- `available`: The package is supplied and carries the data the profile expects.
- `not_implemented`: The tool has no source for this package at all.
- `empty`: The tool has a source for this package and this case has nothing in it.
- `withheld`: The data exists and was deliberately not shared with the review, for example by a consent or confidentiality decision.
<!-- END GENERATED: tool-overview -->

## Integrating with AI assistants, agents, and MCP servers

The review workflow above assumes a tool asking for a judgment about an element that already exists. A tool with an AI assistant, an agent integration, or an MCP server also has a second moment to serve: the one where an author or a model is writing. SCCG applies at both, and a tool that carries it only into review will correct at review time what it could have prevented at writing time.

Nothing in this section is a separate standard. It is guidance on which published asset serves which channel, and on what a tool may claim once it has used them.

### Which asset serves which channel

| Channel | Asset | Notes |
| --- | --- | --- |
| Session or system instructions, including an MCP server's `initialize` instructions | `dist/authoring_guidance.json`, `core_rules` | One line per guideline, already condensed. Short enough to carry unprompted, and every guideline family is represented. |
| A resource the client reads on demand, such as an MCP resource | `dist/sccg.compact.json`, or `dist/sccg.rules.jsonl` for one guideline per line | The full catalog. Address a single guideline by its id so a client can re-read one rule cheaply. |
| Guidance for a specific authoring job | `dist/authoring_guidance.json`, `element_rules` | Names the review profile the written element will be judged under, and its guideline ids. Deriving the guidance from the profile is what stops writing criteria and review criteria drifting apart. |
| Retrieval or vector store | `dist/vectorstore_manifest.json` | Recommended files, metadata fields, and chunking. |
| The result of a write, staging, or save call | `tool.markers`, `tool.thresholds`, `tool.suggested_checks`, `tool.repair` | Mechanical signals a tool can decide, and the repair SCCG prescribes for each. |
| A review | `dist/review_profiles.json`, `dist/data_packages.json`, `dist/prechecks.json` | The review workflow model above. |

### What an AI or agent integration should do

1. **Quote rather than paraphrase.** Use `short_rule` or `statement` verbatim and cite the guideline id. A paraphrase becomes the tool's rule, and drifts from SCCG at the next revision.
2. **Carry the version.** Every tool-facing JSON file carries a `document` block alongside top-level `schema_version` and `sccg_version`, and every JSONL row carries both versions. A finding that cites a guideline id without a version cannot be reproduced later.
3. **Say what was checked.** An empty finding list means the checks that ran found nothing, not that the argument conforms. Report which check ids ran and which guidelines were not examined.
4. **Treat pre-checks and markers as candidate signals.** Carry each pre-check's `interpretation` text through to whoever reads the result. A marker hit is a prompt to look, not a finding.
5. **Never present mechanical results as SCCG conformance.** Most of SCCG can only be judged by a reader. A green result from the decidable subset says nothing about the rest.
6. **Offer the repair; do not apply it silently.** `tool.repair` states the shape of the repair SCCG prescribes, in the notation-neutral element roles. Which repair is right, and whether it is right at all, is the author's decision.
7. **Report data availability honestly.** When a data package cannot be supplied, say which availability state applies. A review told nothing will assume the data does not exist and may report a finding that is an artifact of what it was not shown.
8. **Do not invent word lists or thresholds.** Where a guideline publishes `markers` or `thresholds`, use them; where it does not, the guideline is judgment-level for now. Propose an addition here rather than inventing a private list, so that two tools do not enforce two different rules under the same guideline id.
9. **Record who performed a review.** An agent that reviews argument it wrote itself has not produced an independent review, and a clean result from such a review should be marked as such wherever a person decides on it.

### Mapping SCCG element names onto a tool's own model

SCCG names elements in GSN and CAE, because those are the notations reviewers and authors read. `element_role` is the notation-neutral role behind each name, and it is the intended mapping point for a tool whose internal model is neither: map the tool's own element types onto the role, keep presenting element names in the notation the user sees, and match review profiles by the elements of that notation.

The same roles are used by `tool.repair` and by the selected-element data packages, so one mapping serves element selection, profile selection, and repair rendering.

### The examples are a test corpus

Every guideline carries an `examples.bad` and an `examples.good`, and a tool implementing a mechanical check can hold the check against them: it should fire on the bad example and stay silent on the good one. That makes the examples part of the published contract, not illustration. They are treated as stable and are not reworded without a version change.

<!-- BEGIN GENERATED: authoring-guidance -->
The SCCG subset a tool should deliver while an author or an AI agent is writing, rather than when a review is run. Every guideline still applies; this set names the rules that are most often broken at the moment of writing and short enough to carry in a system prompt, an editor hint, or an agent's session instructions.

Render each rule from the guideline's short_rule field and cite its id. Do not paraphrase, and do not present this set as SCCG conformance; it is a delivery subset, not a reduced standard.

### Core rules

| Guideline | Rule |
| --- | --- |
| [CL.1](index.md#cl1) | State each claim as a short proposition a reviewer could judge true or false. |
| [CL.2](index.md#cl2) | Put one claim in one goal; separate properties that need different evidence. |
| [CL.3](index.md#cl3) | Keep claim text short: scope belongs in context, reasoning in a strategy, topics in sub-claims. |
| [CL.5](index.md#cl5) | Bound every evaluative or universal qualifier in the claim, its context, or a defined term. |
| [CL.6](index.md#cl6) | Do not chain identification, implementation, and validation in one claim; decompose them. |
| [AR.1](index.md#ar1) | Let each element do its own job: claims assert, reasoning elements explain, evidence elements cite. |
| [AR.2](index.md#ar2) | State the decomposition or inference rule explicitly instead of leaving it to be inferred. |
| [AR.3](index.md#ar3) | Make scope, definitions, operating conditions, and dependencies explicit rather than implied. |
| [EV.1](index.md#ev1) | Give every claim a path to evidence, or mark it undeveloped deliberately. |
| [EV.3](index.md#ev3) | Claim the fact the evidence establishes, not the document that holds it. |
| [EV.4](index.md#ev4) | Cite the exact section, table, figure, or test identifier, not a whole report. |
| [EV.8](index.md#ev8) | Cite a fixed, versioned, or archived state, never live mutable content. |
| [SU.2](index.md#su2) | State assumptions explicitly, justify why each is reasonable, and monitor them where needed. |
| [SU.9](index.md#su9) | State a dependency where it constrains the argument, as an assumption, context, or claim. |
| [LF.1](index.md#lf1) | Support a claim with independent grounds, never by restating or renaming it. |
| [LF.3](index.md#lf3) | Do not argue from absence: nothing found is not evidence that nothing exists. |
| [RD.1](index.md#rd1) | Signpost each element's role in its wording so no reader has to guess what it does. |
| [RD.4](index.md#rd4) | Use no promotional language; persuade through structure and evidence. |


### Review criteria by element role

An element written now is reviewed later under one profile. A tool delivering authoring guidance for an element should draw it from that profile, so that writing guidance and review criteria cannot drift apart.

| Element role | Elements | Review profile | Guidelines |
| --- | --- | --- | --- |
| `claim` | GSN Goal, CAE Claim | `claim_review` | CL.1, CL.2, CL.3, CL.4, CL.5, CL.6, AR.1, AR.3, AR.4, AR.5, AR.6, AR.7, EV.1, EV.3, EV.9, SU.1, SU.4, SU.5, SU.6, SU.8, SU.9, SU.11, LF.1, LF.2, LF.3, LF.4, LF.5, LF.6, LF.7, RD.1, RD.2, RD.3, RD.4, RD.5, RD.6 |
| `strategy` | GSN Strategy, CAE Argument | `strategy_review` | AR.1, AR.2, EV.9, SU.1, LF.1 |
| `evidence` | GSN Solution, CAE Evidence | `evidence_review` | AR.1, EV.1, EV.2, EV.4, EV.5, EV.6, EV.7, EV.8, SU.1, SU.3, SU.6, SU.7, SU.8, LF.2, LF.5, LF.7, RD.1 |
| `assumption` | GSN Assumption, CAE Assumption | `assumption_review` | AR.1, AR.3, AR.7, SU.2, SU.4, SU.9, SU.10, RD.1, RD.6 |
| `justification` | GSN Justification, CAE Warrant, CAE Side-warrant, CAE Side-claim | `justification_review` | AR.1, AR.8, AR.9, EV.5, SU.3, SU.5, SU.7, LF.3, LF.4, RD.1, RD.5 |
| `context` | GSN Context, CAE Context | `context_review` | AR.1, AR.3, AR.6, AR.7, SU.9, RD.1, RD.3, RD.6 |
| `challenge` | GSN Counter Claim, CAE Defeater | `challenge_review` | SU.11 |
<!-- END GENERATED: authoring-guidance -->

## Versioning and compatibility

Two version numbers are published, and they answer different questions.

- `schema_version` is the version of the published contract: the file names in `dist/`, the top-level keys in each file, and the field names within them. A major change means a consumer may need to change code. It appears in every tool-facing file and in every rule row.
- `sccg_version` is the version of the guideline content: the guidelines, their wording, examples, profiles, and checks. It moves whenever the content changes, including when the contract does not.

What a tool may rely on being stable within a `schema_version` major:

- The file names under `dist/` and the top-level keys in each of them.
- Guideline ids, review profile ids, data package ids, pre-check ids, and check ids.
- The meaning of a published pre-check, as stated by its `fires_when` sentence. A tool that answers a different question must not report that pre-check's id.
- The `examples.bad` and `examples.good` of each guideline, as described above.

Changes in `2.0.0`, from `1.0.0`: the generic `SEL` data package was replaced by one selected-element package per element role (`SELECTED_CLAIM`, `SELECTED_STRATEGY`, `SELECTED_EVIDENCE`, `SELECTED_CONTEXT`, `SELECTED_ASSUMPTION`, `SELECTED_JUSTIFICATION`, `SELECTED_CHALLENGE`). A consumer that built a package literally named `SEL` should instead build the one package in the profile's `required_data` whose `role` is `selected_element`, which is also how the diagram layout now names its centre slot. Data packages gained `role`, selectable elements gained `element_role`, guidelines gained `short_rule` and optional `markers`, `thresholds`, and `repair`, pre-checks gained `fires_when`, and profiles may carry `when_absent`. Everything else is additive.

<!-- BEGIN GENERATED: review-profiles -->
### Claim review

Complete review of a selected claim (goal), covering wording, context, decomposition, evidence support, reasoning soundness, and sufficiency.

- Profile ID: `claim_review`
- Applies to: GSN Goal, CAE Claim
- Selected element package: `SELECTED_CLAIM`
- Required data: SELECTED_CLAIM, PARENT, CHILDREN, STRATEGY, DIRECT_CONTEXT, INHERITED_CONTEXT, EVIDENCE_PATH
- Optional data: EVIDENCE_ITEM, EVIDENCE_BASIS, PROJECT_GLOSSARY, STANDARD_LINKS, CHANGE_HISTORY
- Guidelines: CL.1, CL.2, CL.3, CL.4, CL.5, CL.6, AR.1, AR.3, AR.4, AR.5, AR.6, AR.7, EV.1, EV.3, EV.9, SU.1, SU.4, SU.5, SU.6, SU.8, SU.9, SU.11, LF.1, LF.2, LF.3, LF.4, LF.5, LF.6, LF.7, RD.1, RD.2, RD.3, RD.4, RD.5, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/claim_review.svg)

#### Data package rationale

Required data:
- `SELECTED_CLAIM`: The selected claim is the subject of the whole review. Its wording drives CL.1, CL.2, CL.3, CL.4, CL.5, CL.6, RD.2, RD.4, and LF.6, and its scope drives every structural, evidential, and sufficiency check applied to the claim.

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
- Selected element package: `SELECTED_STRATEGY`
- Required data: SELECTED_STRATEGY, PARENT, CHILDREN, DIRECT_CONTEXT
- Optional data: INHERITED_CONTEXT, EVIDENCE_PATH, PROJECT_GLOSSARY, STANDARD_LINKS, CHANGE_HISTORY
- Guidelines: AR.1, AR.2, EV.9, SU.1, LF.1
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/strategy_review.svg)

#### Data package rationale

Required data:
- `SELECTED_STRATEGY`: The selected strategy or reasoning element is the object of review. AR.1 and AR.2 require it to make the inference rule explicit, and LF.1 requires checking that it adds independent support rather than restating the parent.

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
- Selected element package: `SELECTED_EVIDENCE`
- Required data: SELECTED_EVIDENCE, EVIDENCE_ITEM, EVIDENCE_BASIS, PARENT
- Optional data: DIRECT_CONTEXT, EVIDENCE_PATH, PROJECT_GLOSSARY, STANDARD_LINKS, CHANGE_HISTORY
- Guidelines: AR.1, EV.1, EV.2, EV.4, EV.5, EV.6, EV.7, EV.8, SU.1, SU.3, SU.6, SU.7, SU.8, LF.2, LF.5, LF.7, RD.1
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/evidence_review.svg)

#### Data package rationale

Required data:
- `SELECTED_EVIDENCE`: The selected solution or evidence reference is the element under review. It identifies which artifact is cited and what role it plays, which is the basis for AR.1, EV.1, and RD.1.

- `EVIDENCE_ITEM`: Artifact metadata such as type, owner, version, date, status, location, and cited section is required to judge whether the evidence type is reviewable and the citation precise, controlled, and stable (EV.2, EV.4, EV.7, EV.8).

- `EVIDENCE_BASIS`: Scope, coverage, thresholds, scenarios, configurations, and limitations are required to judge sufficiency and inferential fit rather than citation hygiene alone (EV.5, EV.6, LF.5, LF.7, SU.3, SU.6, SU.7, SU.8).

- `PARENT`: The claim the evidence supports is required to judge relevance to the immediate claim (LF.2), a correct and traceable evidence path (EV.1), and whether the inferential link is explained (EV.6).


Optional data:
- `DIRECT_CONTEXT`: The claim's local scope and assumptions define what the evidence must cover and help detect evidence that is relevant to a neighboring or broader claim but not sufficient here (LF.2, EV.5).

- `EVIDENCE_PATH`: The path from claim to this evidence helps confirm traceable support and correct attachment level, especially where intermediate claims are skipped (EV.1, LF.2).

- `PROJECT_GLOSSARY`: The glossary resolves controlled terms used in the artifact or its acceptance criteria so the evidence is interpreted consistently.

- `STANDARD_LINKS`: Standard links confirm that an evidence type or acceptance criterion that appeals to a standard is grounded rather than assumed (EV.2, EV.5).

- `CHANGE_HISTORY`: Prior findings, review comments, and baseline state identify unstable, challenged, stale, or dismissed evidence (EV.7, EV.8, SU.1, SU.6).


#### When required data cannot be supplied
- `EVIDENCE_BASIS` absent: Without an evidence basis the review can judge citation, control, and element role, but not whether the evidence is sufficient for the claim. Report the remaining findings, state that sufficiency was not assessed, and do not report an absent basis as a finding against the argument. Not assessable without it: EV.5, EV.6, SU.3, SU.6, SU.7, SU.8, LF.5, LF.7.



### Assumption review

Complete review of a selected assumption, covering whether it is explicit, bounded, correctly placed, monitorable, and not hiding an unsupported claim.

- Profile ID: `assumption_review`
- Applies to: GSN Assumption, CAE Assumption
- Selected element package: `SELECTED_ASSUMPTION`
- Required data: SELECTED_ASSUMPTION, DIRECT_CONTEXT, INHERITED_CONTEXT
- Optional data: PARENT, CHANGE_HISTORY, PROJECT_GLOSSARY
- Guidelines: AR.1, AR.3, AR.7, SU.2, SU.4, SU.9, SU.10, RD.1, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/assumption_review.svg)

#### Data package rationale

Required data:
- `SELECTED_ASSUMPTION`: The selected assumption is the dependency under review. SU.2, SU.9, SU.10, AR.3, AR.7, and RD.6 require checking whether it is explicit, bounded, monitorable, and correctly placed, while AR.1 and RD.1 check that it is used and signposted for its role.

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
- Selected element package: `SELECTED_JUSTIFICATION`
- Required data: SELECTED_JUSTIFICATION, PARENT
- Optional data: STRATEGY, EVIDENCE_PATH, EVIDENCE_ITEM, EVIDENCE_BASIS, CHANGE_HISTORY
- Guidelines: AR.1, AR.8, AR.9, EV.5, SU.3, SU.5, SU.7, LF.3, LF.4, RD.1, RD.5
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/justification_review.svg)

#### Data package rationale

Required data:
- `SELECTED_JUSTIFICATION`: The selected justification or warrant is the object of review. AR.8, AR.9, EV.5, SU.3, SU.5, LF.3, LF.4, RD.1, and RD.5 all require inspecting what the rationale actually says and whether it names the responsible actor.

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
- Selected element package: `SELECTED_CONTEXT`
- Required data: SELECTED_CONTEXT, PARENT
- Optional data: INHERITED_CONTEXT, PROJECT_GLOSSARY, STANDARD_LINKS
- Guidelines: AR.1, AR.3, AR.6, AR.7, SU.9, RD.1, RD.3, RD.6
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/context_review.svg)

#### Data package rationale

Required data:
- `SELECTED_CONTEXT`: The selected context element is the object of review. AR.1, AR.3, AR.6, AR.7, RD.1, and RD.3 require checking whether it is used for its role and whether it supplies clear scope, definitions, and operating conditions.

- `PARENT`: The claim or element the context qualifies is required to judge whether the context is sufficient and relevant for interpreting that claim (AR.6), whether scope and dependencies are correctly externalized to it (AR.3, AR.7), and whether limitations are visible where the claim is read (RD.3, RD.6).


Optional data:
- `INHERITED_CONTEXT`: Ancestor scope and assumptions show whether this context is consistent with, or silently narrows or contradicts, inherited limits (RD.6, SU.9).

- `PROJECT_GLOSSARY`: Controlled definitions confirm that terms introduced or relied on by the context are used consistently across the branch (AR.6).

- `STANDARD_LINKS`: When the context cites external standards or operating constraints, standard links help verify the reference is relevant and not used as vague or hidden context (AR.3).



### Challenge review

Complete review of a selected counter claim or defeater, covering whether the challenge is stated explicitly and carried to a visible resolution.

- Profile ID: `challenge_review`
- Applies to: GSN Counter Claim, CAE Defeater
- Selected element package: `SELECTED_CHALLENGE`
- Required data: SELECTED_CHALLENGE, PARENT
- Optional data: CHILDREN, DIRECT_CONTEXT, CHANGE_HISTORY
- Guidelines: SU.11
- Diagram: [SVG diagram](assets/generated/review_profile_diagrams/challenge_review.svg)

#### Data package rationale

Required data:
- `SELECTED_CHALLENGE`: The selected counter claim or defeater is the challenge under review. SU.11 requires checking whether the challenge is stated explicitly as a distinct element rather than left in review comments or reviewer intuition.

- `PARENT`: The claim, reasoning step, or evidence being challenged is required to judge whether the challenge is relevant to its target and whether the branch has been updated to resolve it (SU.11).


Optional data:
- `CHILDREN`: Supporting elements added in response show whether the challenge was resolved by added evidence, a narrowed claim, or new assumptions and monitoring (SU.11).

- `DIRECT_CONTEXT`: Context and assumptions attached to the challenge or its target help judge whether the challenge is in scope and how its resolution constrains the affected claim (SU.11).

- `CHANGE_HISTORY`: Review comments, prior findings, and proposal history show whether the challenge was rejected, sustained, or left as a visible and traceable open issue (SU.11).
<!-- END GENERATED: review-profiles -->

<!-- BEGIN GENERATED: prechecks -->
### Claim has children but no explicit reasoning step

Detects candidate cases where a claim is decomposed without an explicit reasoning step.

- Pre-check ID: `check-explicit-strategy`
- Expected data: SELECTED_CLAIM, CHILDREN, STRATEGY
- Related guidelines: AR.2
- Result type: `boolean_candidate`
- Fires when: The selected claim has at least one supporting child element and no strategy or reasoning element between the claim and those children. It does not fire on a strategy that has no children; that is a different defect and is not this pre-check.
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.


### Claim has no evidence path

Detects candidate cases where a claim has no path to evidence and is not intentionally undeveloped.

- Pre-check ID: `check-evidence-trace`
- Expected data: SELECTED_CLAIM, EVIDENCE_PATH
- Related guidelines: EV.1
- Result type: `boolean_candidate`
- Fires when: No descendant of the selected claim is an evidence element, and the claim is not marked undeveloped.
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.


### Evidence reference too broad

Detects candidate cases where an evidence element cites a broad artifact without a precise location.

- Pre-check ID: `check-evidence-citation-precision`
- Expected data: SELECTED_EVIDENCE, EVIDENCE_ITEM
- Related guidelines: EV.4
- Result type: `boolean_candidate`
- Fires when: The selected evidence element names an artifact but neither its text nor the evidence item's cited_section identifies a section, clause, table, figure, dataset, or test identifier within it.
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.


### Evidence missing control attributes

Detects evidence references without useful control attributes such as owner, version, status, date, or location.

- Pre-check ID: `check-evidence-control-attributes`
- Expected data: SELECTED_EVIDENCE, EVIDENCE_ITEM
- Related guidelines: EV.7
- Result type: `missing_fields`
- Fires when: The evidence item carries none of owner, version, status, date, or location, and no such attribute is stated in the selected evidence element's text. The result names which of those fields are missing.
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.


### Live mutable evidence reference

Detects evidence references that appear to point to mutable live documents without a fixed version.

- Pre-check ID: `check-evidence-state-fixed`
- Expected data: SELECTED_EVIDENCE, EVIDENCE_ITEM
- Related guidelines: EV.8
- Result type: `boolean_candidate`
- Fires when: The evidence reference carries a mutable-source marker (see the EV.8 markers) and carries no fixing marker such as a revision, version, snapshot, or capture date.
- Interpretation: Candidate finding only; reviewer or AI judgment is still required.
<!-- END GENERATED: prechecks -->
