# Safety Case Core Guidelines

## Purpose

This document consolidates review guidance for safety cases into one guideline-based review framework that can be cited during reviews.

The intent is to make review findings shorter, more consistent, and better anchored in external sources. Instead of writing `this claim is vague`, a reviewer should be able to cite a guideline ID and rely on this guideline for the explanation, rationale, and example.

This guideline deliberately follows a structured format:
- short guideline IDs
- one clear point per entry
- explanation of why the point matters
- review prompts and examples
- an explicit reference basis for the item

## Source policy

These guidelines draw on several source classes. The wording in this document is intended to paraphrase source material and established practice rather than reproduce source text. Direct quotations should be avoided unless they are brief, explicitly marked, and clearly attributed.

These guidelines draw on several source classes:

1. **Normative / regulatory sources**  
   Used where an item operationalizes a stated requirement or accepted regulatory expectation.  
   Examples: UL 4600, ISO/IEC/IEEE 15026-2, IEC 61508, ISO 26262, ISO 21448, ISO/PAS 8800, UNECE ADS regulations and guidance.

2. **Argumentation / assurance-structure sources**  
   Used where an item concerns claims, arguments, context, assumptions, evidence, traceability, or case architecture.  
   Examples: GSN Community Standard v3, CAE guidance, OMG SACM.

3. **Cross-domain safety-case practice sources**  
   Used where an item reflects established safety-case development, review, maintenance, and challenge practice across industries.  
   Examples: ONR Safety Assessment Principles and TAGs, EASA guidance, UK MOD RA 1205, NPSA guidance.

4. **Research / explanatory sources**  
   Used where an item concerns common argument defects, evidence sufficiency, reusable argument patterns, confidence, or review methods.  
   Examples: Kelly & McDermid, Hawkins et al., Weaver et al., Greenwell et al.


## License

Â© 2026 Jesper BrÃ¤nnstrÃ¶m

This work is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0).

To view a copy of this license, visit https://creativecommons.org/licenses/by/4.0/


## Guideline ID scheme

- CL.x - Claim guidance
- AR.x - Argument structure and decomposition guidance
- EV.x - Evidence guidance
- SU.x - Sufficiency, uncertainty, and pitfall guidance
- LF.x - Logical fallacy guidance
- RD.x - Rhetorical device guidance

## Recommended template

Each guideline entry should keep this shape:

### CL.n: Guideline title

**Guideline**
One sentence stating what shall be done or avoided.

**Why**
Why the guideline matters for argument quality and review quality.

**Review prompts**
- Questions a reviewer should ask when applying the guideline.

**Example**
- Direct and realistic bad and better patterns.

**References**
- List the applicable source references only.

## How to use the guidelines in reviews

Example review comments:

- `CL.4`: Claim is structurally ambiguous. Reword so the object and property are clear.
- `AR.2`: The decomposition rule is hidden in the claim text. Make the strategy explicit.
- `EV.4`: Evidence reference is too broad. Point to the exact section, figure, table, or dataset actually used.
- `SU.6`: Operational feedback includes potentially contrary evidence, but the argument dismisses it without a defensible basis.
- `LF.3`: This branch argues from ignorance; absence of discovered evidence is being treated as evidence of absence.
- `RD.4`: The wording uses promotional language that makes the claim sound stronger than it is.

<!-- BEGIN GENERATED: quick-index -->
## Quick index


### CL. Claim guidance



- `CL.1` [Write each claim as a falsifiable proposition](#cl1-write-each-claim-as-a-falsifiable-proposition)

- `CL.2` [Put one main claim in one goal](#cl2-put-one-main-claim-in-one-goal)

- `CL.3` [Avoid the essay-in-the-box](#cl3-avoid-the-essay-in-the-box)

- `CL.4` [Avoid ambiguity and overloaded wording](#cl4-avoid-ambiguity-and-overloaded-wording)

- `CL.5` [Bound vague and universal qualifiers](#cl5-bound-vague-and-universal-qualifiers)

- `CL.6` [Do not mix different logical steps in one claim](#cl6-do-not-mix-different-logical-steps-in-one-claim)



### AR. Argument structure and decomposition guidance



- `AR.1` [Let structure carry the argument](#ar1-let-structure-carry-the-argument)

- `AR.2` [State the inference step explicitly](#ar2-state-the-inference-step-explicitly)

- `AR.3` [Use context and assumptions deliberately](#ar3-use-context-and-assumptions-deliberately)

- `AR.4` [Match claim precision to the level of the argument](#ar4-match-claim-precision-to-the-level-of-the-argument)

- `AR.5` [Keep scope and terminology consistent across decomposition](#ar5-keep-scope-and-terminology-consistent-across-decomposition)

- `AR.6` [Provide the context needed to interpret the claim](#ar6-provide-the-context-needed-to-interpret-the-claim)

- `AR.7` [Keep context out of claim text unless context is itself the claim](#ar7-keep-context-out-of-claim-text-unless-context-is-itself-the-claim)

- `AR.8` [Use justification only for local rationale, not as hidden support](#ar8-use-justification-only-for-local-rationale-not-as-hidden-support)

- `AR.9` [Match each justification to the element it justifies](#ar9-match-each-justification-to-the-element-it-justifies)



### EV. Evidence guidance



- `EV.1` [Make the evidence-support path explicit for every claim](#ev1-make-the-evidence-support-path-explicit-for-every-claim)

- `EV.2` [Use evidence types that can be independently reviewed](#ev2-use-evidence-types-that-can-be-independently-reviewed)

- `EV.3` [Claim the fact supported by the evidence, not the document](#ev3-claim-the-fact-supported-by-the-evidence-not-the-document)

- `EV.4` [Cite precise evidence locations; avoid annex dumping](#ev4-cite-precise-evidence-locations-avoid-annex-dumping)

- `EV.5` [Make the basis for evidence sufficiency explicit](#ev5-make-the-basis-for-evidence-sufficiency-explicit)

- `EV.6` [Explain how the evidence supports or refutes the claim](#ev6-explain-how-the-evidence-supports-or-refutes-the-claim)

- `EV.7` [Keep evidence controlled: owner, version, date, status, repository](#ev7-keep-evidence-controlled-owner-version-date-status-repository)

- `EV.8` [Cite fixed evidence, not live mutable content](#ev8-cite-fixed-evidence-not-live-mutable-content)

- `EV.9` [Do not argue directly from undocumented system knowledge](#ev9-do-not-argue-directly-from-undocumented-system-knowledge)



### SU. Sufficiency, uncertainty, and pitfall guidance



- `SU.1` [Identify and address plausible challenges to claims, reasoning, and evidence](#su1-identify-and-address-plausible-challenges-to-claims-reasoning-and-evidence)

- `SU.2` [Make assumptions explicit and justify why they are reasonable](#su2-make-assumptions-explicit-and-justify-why-they-are-reasonable)

- `SU.3` [Do not rely on uncorroborated expert judgment alone](#su3-do-not-rely-on-uncorroborated-expert-judgment-alone)

- `SU.4` [Monitor claims that cannot be fully supported at design time](#su4-monitor-claims-that-cannot-be-fully-supported-at-design-time)

- `SU.5` [Do not reuse safety credit from another context without showing it still applies](#su5-do-not-reuse-safety-credit-from-another-context-without-showing-it-still-applies)

- `SU.6` [Do not dismiss operational feedback because it is non-reproducible or non-injury](#su6-do-not-dismiss-operational-feedback-because-it-is-non-reproducible-or-non-injury)

- `SU.7` [Do not argue low risk from operational experience or unvalidated simulation alone](#su7-do-not-argue-low-risk-from-operational-experience-or-unvalidated-simulation-alone)

- `SU.8` [Do not assume human data or human-designed tests cover autonomy-specific failures](#su8-do-not-assume-human-data-or-human-designed-tests-cover-autonomy-specific-failures)

- `SU.9` [Document unstated assumptions at the point of use](#su9-document-unstated-assumptions-at-the-point-of-use)

- `SU.10` [Keep assumptions bounded, specific, and monitorable](#su10-keep-assumptions-bounded-specific-and-monitorable)

- `SU.11` [Turn plausible reviewer challenges into explicit Counter Claims and resolve them](#su11-turn-plausible-reviewer-challenges-into-explicit-counter-claims-and-resolve-them)



### LF. Logical fallacy guidance


These guideline entries identify reasoning errors that weaken safety arguments. They are intended to support the development and review of safety cases by helping authors and reviewers examine whether claims, strategies, and evidence are argued soundly.



- `LF.1` [Avoid circular reasoning](#lf1-avoid-circular-reasoning)

- `LF.2` [Avoid irrelevant premises](#lf2-avoid-irrelevant-premises)

- `LF.3` [Avoid arguing from ignorance](#lf3-avoid-arguing-from-ignorance)

- `LF.4` [Avoid unjustified comparison or unjustified distinction](#lf4-avoid-unjustified-comparison-or-unjustified-distinction)

- `LF.5` [Avoid sample-size and representativeness fallacies](#lf5-avoid-sample-size-and-representativeness-fallacies)

- `LF.6` [Avoid pseudo-precision](#lf6-avoid-pseudo-precision)

- `LF.7` [Avoid omission of key evidence and ignoring counter-evidence](#lf7-avoid-omission-of-key-evidence-and-ignoring-counter-evidence)



### RD. Rhetorical device guidance


These guideline entries identify presentation choices that affect how safety arguments are understood and reviewed. They help distinguish between wording that improves clarity and wording that increases confidence without increasing support.



- `RD.1` [Use explicit signposting of argument element roles](#rd1-use-explicit-signposting-of-argument-element-roles)

- `RD.2` [Use scoped claims and qualified confidence language](#rd2-use-scoped-claims-and-qualified-confidence-language)

- `RD.3` [Make limitations, objections, and responses explicit](#rd3-make-limitations-objections-and-responses-explicit)

- `RD.4` [Avoid promotional and inflated language](#rd4-avoid-promotional-and-inflated-language)

- `RD.5` [Avoid passive voice when it hides agency](#rd5-avoid-passive-voice-when-it-hides-agency)

- `RD.6` [Do not bury important limitations or hidden assumptions](#rd6-do-not-bury-important-limitations-or-hidden-assumptions)
<!-- END GENERATED: quick-index -->

<!-- BEGIN GENERATED: guidelines -->
## CL. Claim rules

### CL.1: Write each claim as a falsifiable proposition

**Guideline**

State each claim as a sentence that can in principle be shown true or false.

**Why**

A safety case is built from claims that can be challenged, supported, or refuted. Statements that are merely labels, headings, slogans, or references are poor safety claims.

**Review prompts**
- Could a reviewer tell what would make this claim false?
- Is this a proposition, or only a topic label?
- Is the claim understandable without extra interpretation?

**Example**
- Bad: Brake monitor safety
- Better: Brake monitor response time meets the defined acceptance criterion.

**References**

References: ISO/IEC/IEEE 15026-2:2022, OMG SACM 2.3, CAE concise guidance, UL 4600 4.2.9; 5.2.3.1(a), GSN v3 1:2.3.2

### CL.2: Put one main claim in one goal

**Guideline**

Do not bundle multiple distinct properties, conclusions, or obligations into one goal.

**Why**

Bundled claims hide missing decomposition, make evidence assignment unclear, and produce review findings that are hard to localize.

**Review prompts**
- Does the statement contain more than one property?
- Would different evidence sets be needed for different parts of the claim?
- Could one part of the statement be acceptable while another could fail?

**Example**
- Bad: `Planning software is safe and secure.`
- Better: `Planning software safety is acceptable.`
  - And separately: `Planning software cybersecurity is acceptable.`

**References**

References: ISO/IEC/IEEE 15026-2:2022, OMG SACM 2.3, CAE concise guidance, UL 4600 5.2.3, GSN v3 1:2.3.2

### CL.3: Avoid the essay-in-the-box

**Guideline**

Do not pack argument structure, scope, decomposition topics, and caveats into a single claim. Keep the claim short, and express the rest through context, strategy, assumptions, and sub-claims.

**Why**

When a claim contains the whole story, reviewers cannot clearly see what is being claimed, what constrains the claim, and how the argument is intended to proceed. In GSN, that information should be visible in the structure, not hidden inside one sentence.

**Review prompts**
- Is the goal text trying to describe both the claim and its decomposition?
- Is scope that should be in context embedded in the claim text?
- Are included topics listed in the claim instead of being expressed as sub-claims?
- Would the argument become clearer if the parent claim were shortened and the included topics moved into strategy and child claims?

**Example**
- Bad: The product concept and system design, including faults, failures, interfaces, dependencies, degraded operation and transitions to safe states, are acceptably safe for operation within the defined ODD.
- Better:
  - Goal: Design safety is acceptable.
  - Context: Applies within the defined ODD.
  - Strategy: Argument by decomposition over safety-relevant design topics.
  - Possible sub-claims:
    - Fault handling safety is acceptable.
    - Failure response safety is acceptable.
    - Safety-relevant interfaces are acceptable.
    - Safety-relevant dependencies are acceptable.
    - Degraded operation safety is acceptable.
    - Transitions to safe states are acceptable.

**Note**
Rewrite the parent as one short claim, move scope to context, move the reasoning to strategy, and express included topics as child claims.

**References**

References: UL 4600 5.2.3; 5.3.2.1(a), GSN v3 1:2.3.3

### CL.4: Avoid ambiguity and overloaded wording

**Guideline**

Write claims so that their meaning is clear enough that competent reviewers are likely to understand them in the same way.

**Why**

Ambiguous claims undermine review, traceability, and evidence relevance. This guideline directly supports UL 4600’s requirement to avoid substantive ambiguity in claims and arguments.

**Review prompts**
- Could two competent reviewers understand the claim differently?
- Is the object of the claim clear?
- Is the property being claimed clear?

**Example**
- Bad: Software requirements development is acceptably safe.
- Better: The process used to develop software functional requirements is acceptably controlled.

**References**

References: Greenwell et al. 2006 (linguistic fallacies: ambiguity, vagueness, suppressed quantification), NPSA CAE Concepts, UL 4600 5.2.3; 5.2.3.1(d), GSN v3 2:5.4.1-2:5.4.3

### CL.5: Bound vague and universal qualifiers

**Guideline**

Do not leave broad evaluative terms or universal qualifiers unbounded. This includes terms such as safe, timely, effective, normal, robust, all, every, and never.

**Why**

Terms such as safe, timely, effective, normal, robust, all, every, and never can sound stronger or broader than the argument actually shows unless they are properly bounded.

**Review prompts**
- Is the term bounded by context, lower-level argument, or linked criteria?
- If safe is used, is it clear what safety judgment is being claimed at this level?
- Is the scope of all, every, or never explicitly defined?
- Would the claim remain reviewable if read on its own?

**Example**
- Example A Acceptable when bounded: The item is acceptably safe for operation within the defined ODD.
- Example B Bad: The monitor provides timely mitigation. Better: Upon detection of condition C4, the monitor initiates minimum risk maneuver entry within the defined threshold.

**References**

References: Greenwell et al. 2006 (linguistic fallacies: ambiguity, vagueness, suppressed quantification), NPSA CAE Concepts, UL 4600 5.2.3; 5.2.3.1(d), GSN v3 2:5.5.1-2:5.6.1

### CL.6: Do not mix different logical steps in one claim

**Guideline**

Do not combine identification, adequacy, implementation, validation, and sufficiency in one claim unless the claim is intentionally kept at a higher level and the need for later decomposition is explicit

**Why**

These are different claim types with different evidence and different review questions.

**Review prompts**
- Is this claim actually several claims chained together?
- Would different teams or documents support different parts?
- Should the branch be decomposed before evidence is attached?

**Example**
- Bad: All identified hazards have been mitigated and validated.
  - Better parent: Hazards are acceptably addressed.
  - Possible sub-claims:
    - Hazards are identified.
    - Defined mitigations are implemented.
    - Validation evidence is sufficient.

**References**

References: ISO/IEC/IEEE 15026-2:2022, OMG SACM 2.3, CAE concise guidance, UL 4600 5.2.3; 5.3.1; 5.3.2, GSN v3 1:2.3.2-1:2.3.3

## AR. Argument structure and decomposition rules

### AR.1: Let structure carry the argument

**Guideline**

Use goals for claims, strategies for reasoning and decomposition approach, context for scope and definitions when needed, assumptions for dependencies when needed, justifications for local rationale when needed, and solutions for evidence references.

**Why**

When one GSN element is used to do another element’s job, the argument becomes harder to inspect, review, and challenge.

**Review prompts**
- Is the goal text carrying reasoning that belongs in a strategy?
- Is local scope or meaning hidden inside the claim instead of expressed through context?
- Is an assumption or justification hidden in claim or strategy text?
- Is a solution being used as if it were a claim?
- Is a justification being used as if it were support?

**Example**
- Better pattern:
  - Goal: Functional design safety is acceptable.
  - Strategy: Argument by autonomy hazard topic.
  - Context: Functional design refers to the ISO 26262 functional design scope for the item.
  - Justification: This claim is included because the project requires ISO 26262 compliance.
  - Possible sub-claims:
    - Functional safety requirements are defined.
    - Required safety mechanisms are defined.
    - Safety-relevant interfaces are defined.

**References**

References: OMG SACM 2.3, ONR claims-arguments-evidence guidance, EASA safety case definition, NPSA CAE blocks / connection rules, UL 4600 5.2.3; 5.3.2.1(a), GSN v3 1:2.2.10-1:2.2.19; 1:2.3.2-1:2.3.6

### AR.2: State the inference step explicitly

**Guideline**

State how the parent claim is being decomposed or argued; do not make the reviewer infer the decomposition rule from wording alone.

**Why**

A hidden reasoning step is a common source of argument gaps.

**Review prompts**
- Is the decomposition rule visible?
- Would another reviewer derive the same child-claim set?
- Does the strategy explain why these children support this parent?

**Example**
- Bad: Perception, planning, control, timing, and interfaces are adequately addressed.
  - Better goal: Autonomy function safety is acceptable.
  - Better strategy: Argument by decomposition over autonomy function topics identified by UL 4600.
  - Justification (if needed): This decomposition follows the autonomy-related topics that UL 4600 requires the safety case to address.
  - Possible sub-claims:
    - ODD-related safety is acceptable.
    - Sensing safety is acceptable.
    - Perception safety is acceptable.
    - Machine learning and AI technique safety is acceptable.
    - Planning safety is acceptable.
    - Prediction safety is acceptable.
    - Trajectory and control safety is acceptable.
    - Actuation safety is acceptable.
    - Timing safety is acceptable.

**References**

References: OMG SACM 2.3, ONR claims-arguments-evidence guidance, EASA safety case definition, NPSA CAE blocks / connection rules, UL 4600 5.3.2.1(a); 5.3.2.1(a)(1), GSN v3 1:2.3.3; CAE guidance on connection rules and explicit reasoning

### AR.3: Use context and assumptions deliberately

**Guideline**

Put information that explains how a claim should be understood into context elements, and put conditions that must hold for the claim to remain valid into assumption elements, unless that information is itself the claim being made.

**Why**

This keeps claims readable and makes it clear which information defines the claim’s scope and meaning, and which information the argument depends on being true.

**Review prompts**
- Is this text making the claim itself, or only explaining how the claim should be interpreted?
- Is any condition required for the claim to hold embedded in the claim text instead of stated explicitly?
- Should this information be shown as context, as an assumption, or as part of the claim itself?
- Would the branch be clearer if scope moved to context and dependencies moved to assumptions?

**Example**
- Bad: The braking controller is acceptably safe in Highway ODD during automated mode with valid localization and nominal power supply.
  - Better goal: Braking controller safety is acceptable.
  - Better context: Applies in Highway ODD. / Applies in automated mode.
  - Better assumptions: Valid localization available. / Nominal power supply conditions apply.

**References**

References: OMG SACM 2.3, ONR claims-arguments-evidence guidance, EASA safety case definition, NPSA CAE blocks / connection rules, UL 4600 5.2.3; 5.4.1.3(a)(11), GSN v3 1:2.2.10-1:2.2.18

### AR.4: Match claim precision to the level of the argument

**Guideline**

Keep upper-level claims short and stable; make evidence-facing claims precise enough to assess.

**Why**

Top-level claims need readability and stability. Lower-level claims need assessability.

**Review prompts**
- Is a high-level claim overloaded with low-level detail?
- Is a leaf claim too vague to assess against evidence?
- Could the claim stay short because linked criteria already make it objective?

**Example**
- Examples of increasing precision at different levels of the argument, not necessarily adjacent nodes:
  - Upper level: Functional design safety is acceptable.
  - Lower level: Sensing-related hazards are identified.
  - Evidence-facing level: Detection timing meets the defined acceptance criterion.

**References**

References: UL 4600 5.2.3; 5.4.2.1(b), GSN v3 Part 2 §2:2

### AR.5: Keep scope and terminology consistent across decomposition

**Guideline**

Do not silently redefine the object, scope, or meaning of key terms as the argument decomposes.

**Why**

Silent redefinition can leave higher-level claims only partially supported while appearing complete.

**Review prompts**
- Does a key term mean the same thing at parent and sub-claim levels?
- Has scope narrowed without being stated?
- Is inherited context still valid at this level?

**Example**
- Bad pattern:
  - Parent claim: Software safety is acceptable.
  - Strategy: Argument by software component type.
  - Child claims:
    - Application software safety is acceptable.
    - Middleware software safety is acceptable.
- Problem: the parent claim refers to all software, but the child claims silently narrow the scope to only part of the software. The branch appears complete while leaving other software out of scope without saying so.

**References**

References: UL 4600 5.2.3, GSN v3 1:2.2.11; 2:5.5.3

### AR.6: Provide the context needed to interpret the claim

**Guideline**

Provide the context needed for the reviewer to understand the claim’s subject, intended meaning, scope, operating conditions, and key definitions.

**Why**

This guideline is about whether the branch contains enough context at all. In GSN, claims are asserted in a specified context. A claim that lacks essential context can look stronger than intended or become hard to review consistently because different readers may supply different meanings or boundaries.

**Review prompts**
- What must the reviewer know for this claim to be true or false?
- Are key terms defined where needed?
- Is any necessary scope or operating condition explicit?
- Would two independent reviewers understand the claim in the same way?

**Example**
- Bad: Perception performance is acceptable.
- Problem: Perception performance is not defined, so different reviewers may understand different outputs, measures, or success conditions.
  - Better goal: Perception performance is acceptable.
  - Better context: Perception performance refers to object detection, classification, and tracking performance as defined in Specification PER-01.

**References**

References: OMG SACM 2.3, ONR claims-arguments-evidence guidance, EASA safety case definition, NPSA CAE blocks / connection rules, UL 4600 5.2.3, GSN v3 1:2.2.10-1:2.2.11; 1:2.3.5

### AR.7: Keep context out of claim text unless context is itself the claim

**Guideline**

Do not pack claim text with qualifiers, definitions, interface conditions, or dependency clauses when those are better represented as context or assumption elements.

**Why**

This guideline is about placement, not completeness. Context or assumptions embedded in claim text blur element roles, make scope and dependency changes harder to see, and often create claims that are harder to review and maintain.

**Review prompts**
- Which words in this claim are really qualifiers rather than the claim itself?
- Is the claim mixing its core assertion with local context or dependencies?
- Could the goal remain stable if a configuration, interface condition, or dependency changed?
- Should one or more qualifiers be moved to context or assumptions?

**Example**
- Bad: Planner safety is acceptable with valid localization and nominal interface timing.
  - Better goal: Planner safety is acceptable.
  - Better context: Planner refers to the motion planning function defined in architecture element PLN-01.
  - Better assumptions: Valid localization is available. / Nominal interface timing conditions apply.

**References**

References: OMG SACM 2.3, ONR claims-arguments-evidence guidance, EASA safety case definition, NPSA CAE blocks / connection rules, UL 4600 5.2.3; 5.3.2.1(a), GSN v3 1:2.2.10-1:2.2.13; CAE guidance on avoiding free-form conversational argumentation

### AR.8: Use justification only for local rationale, not as hidden support

**Guideline**

Use a justification element only to explain why the wording, boundary, or reasoning choice for a goal or strategy is acceptable; do not use justification as proof that a claim is true.

**Why**

In GSN, a justification explains a local wording or structuring choice; it does not provide the proof that makes the claim true. Treating justification as proof hides missing strategy, sub-claims, or evidence.

**Review prompts**
- Is the justification explaining why the element is acceptable, or trying to carry evidential weight?
- Ensure that removing the justification would not remove the real support for the claim. Should this material actually be a strategy, context, assumption, sub-claim, or solution?

**Example**
- Bad: Goal Brake hazards are adequately addressed. with justification Because tests were passed.
- Better: Use evidence and sub-claims for test support. Reserve justification for local rationale such as why a hazard grouping or decomposition choice is acceptable.

**References**

References: OMG SACM 2.3, ONR claims-arguments-evidence guidance, EASA safety case definition, NPSA CAE blocks / connection rules, UL 4600 5.2.3; 5.3.2.1(a), GSN v3 1:2.2.14; 1:2.3.6

### AR.9: Match each justification to the element it justifies

**Guideline**

A justification shall address the exact goal or strategy to which it is attached and shall not explain some different issue elsewhere in the branch.

**Why**

Misaligned justifications create false confidence and often reveal that the real concern is missing context, missing decomposition, or missing evidence.

**Review prompts**
- Does the justification answer why this exact claim or strategy formulation is acceptable?
- Is it local, or is it trying to justify the whole branch?
- Could the same text be pasted onto many different elements without change?

**Example**
- Bad: Goal Sensor faults are adequately addressed. with justification The item is intended for highway use.
- Better: Put highway use in context and use any justification to explain a local choice such as why a particular fault grouping is appropriate.

**References**

References: OMG SACM 2.3, ONR claims-arguments-evidence guidance, EASA safety case definition, NPSA CAE blocks / connection rules, UL 4600 5.2.3, GSN v3 1:2.2.14-1:2.2.19

## EV. Evidence rules

### EV.1: Make the evidence-support path explicit for every claim

**Guideline**

Show, for each claim, the evidence path that supports it, either directly or through stated sub-claims and intermediate arguments.

**Why**

A safety case without traceability cannot be effectively reviewed or maintained.

**Review prompts**
- Can the reviewer identify the intended evidence path without having to infer it?
- Is it clear which evidence path ultimately supports this claim?
- Would two reviewers follow the same trace to the same evidence?

**Example**
- Bad pattern:
  - Claim: Detection timing is acceptable.
  - Linked solution: System validation report.
- Problem: the reviewer cannot tell which test, section, or lower-level argument is intended to show that detection timing is acceptable. The trace exists only in the author’s head.

**References**

References: ONR guidance on clear trail from claims through argument to evidence, UNECE ADS safety case clauses, UL 4600 5.4.1.1(a); 5.4.1.6.1, GSN v3 2:3.7.3

### EV.2: Use evidence types that can be independently reviewed

**Guideline**

Do not use evidence unless its artifact type is defined for safety case use and the artifact meets the criteria required for that type, so that it can be reviewed and assessed consistently.

**Why**

A reviewer should be able to recognize what kind of evidence is being used, what makes it acceptable for this purpose, and how it should be interpreted. If an artifact is not an approved evidence type, or does not meet the criteria required for that type, it becomes difficult to review consistently and easy to misuse in a safety argument.

**Review prompts**
- Is the evidence type clearly defined?
- Is the expected structure or content of the artifact defined?
- Is it clear how the artifact is to be interpreted?
- Is there a defined basis for reviewing, validating, or accepting this evidence type?
- Could an independent reviewer examine the artifact consistently without relying on undocumented local knowledge?

**Example**
- Bad pattern:
  - Claim: Perception validation evidence is sufficient for this claim.
  - Evidence: Engineer working file WF-27.
- Problem:
  - The artifact is being used as safety case evidence, but it is not an approved evidence type for this purpose, or it is not shown to meet the criteria required for that evidence type. The reviewer therefore cannot assess it consistently as acceptable evidence.
- Better pattern:
  - Claim: Perception validation evidence is sufficient for this claim.
  - Evidence: Perception validation report PVR-08, rev B.
  - Context: Validation report is an approved evidence type for this kind of claim.
  - Evidence basis: The cited artifact meets the defined criteria for that evidence type.

**References**

References: Weaver et al., Software Safety Arguments: Towards a Systematic Categorisation of Evidence, Hawkins et al., A New Approach to Creating Clear Safety Arguments, CAE Concepts / Building Blocks, UL 4600 5.2.2; 5.2.2.1(a)-(b)

### EV.3: Claim the fact supported by the evidence, not the document

**Guideline**

Write the claim as the fact or property being supported; do not make the goal say that a report, analysis, or test proves the safety conclusion.

**Why**

Evidence usually supports a specific fact or bounded property, not the whole safety conclusion by itself.

**Review prompts**
- Is the goal naming a document instead of a supported property?
- Is the evidential link too large for the cited artifact?
- Would the claim remain meaningful if the artifact name changed?

**Example**
- Bad: TR-21 proves the braking controller is safe.
- Better: Braking controller stopping distance meets acceptance criterion AC-BRK-04.

**References**

References: UL 4600 5.4.2.1(c)(1), GSN v3 1:2.3.4; 2:3.7.3

### EV.4: Cite precise evidence locations; avoid annex dumping

**Guideline**

Reference the exact section, figure, table, dataset, or artifact portion that supports the claim when practical.

**Why**

Broad references to whole reports create the illusion of support without making the evidential link easy to review.

**Review prompts**
- Could a reviewer find the relevant support quickly?
- Is the cited location precise enough?
- Is the reference proportionate to the actual support being used?

**Example**
- Bad: See validation report.
- Better: See validation report VR-04, section 6.3, table 12, scenarios S14-S21.

**References**

References: ONR guidance on clear trail from claims through argument to evidence, UNECE ADS safety case clauses, UL 4600 5.4.1.1(a); 5.4.2.1(c)(1), GSN v3 2:3.7.4

### EV.5: Make the basis for evidence sufficiency explicit

**Guideline**

When a claim is supported by evidence, make clear what makes that evidence sufficient for that claim.

**Why**

A reviewer should not have to guess why a cited test, analysis, dataset, or review record is enough. The argument should make the sufficiency basis visible, such as relevant scope, configuration, scenario coverage, thresholds, acceptance conditions, and known limitations.

**Review prompts**
- What makes this evidence enough for this claim?
- Is the required scope, configuration, scenario set, or operating condition clear?
- Is any threshold, pass criterion, or completeness expectation stated?
- Are known limitations or uncovered conditions explicit?
- Is the branch showing only that the evidence is relevant, or also that it is enough?

**Example**
- Bad pattern:
  - Claim: Perception performance is acceptable.
  - Evidence: Perception validation report PVR-08.
- Problem: The report is cited, but the argument does not state what coverage, thresholds, configurations, or limitations make that report sufficient for this claim.
- Better pattern:
  - Claim: Perception performance is acceptable for ODD-A daytime operation.
  - Evidence: Perception validation report PVR-08.
  - Context: Applies to software build SB-14 and sensor configuration C3.
  - Justification: Sufficiency is based on scenario coverage SC-21, acceptance thresholds AC-PER-04 to AC-PER-07, and the stated exclusion of dense fog conditions.

**References**

References: Weaver et al., Software Safety Arguments: Towards a Systematic Categorisation of Evidence, Hawkins et al., A New Approach to Creating Clear Safety Arguments, CAE Concepts / Building Blocks, UL 4600 5.4.2.1(b)-(c); 5.3.2.1(a)(1)

### EV.6: Explain how the evidence supports or refutes the claim

**Guideline**

Ensure the inferential link between claim and evidence is explicitly documented and reviewable. The documentation shall explain how the cited evidence supports the claim, and where relevant how it reveals limitations or possible refutation.

**Why**

Evidence does not speak for itself. The safety case or linked assessment record must explain why the evidence bears on the claim.

**Review prompts**
- Is it explicit why this evidence matters for this claim?
- Is the inferential link documented in a reviewable form?
- Does the documentation explain only support, or also limitations and possible refutation?
- Has confirmation bias been considered?

**Example**
- Bad pattern:
  - GSN claim: Detection timing meets acceptance criterion AC-DET-07.
  - GSN solution: Timing test report TR-18, section 5.2.
- Problem: the evidence is linked, but the reason it supports the claim is not explicitly documented anywhere reviewable.
- Better pattern:
  - Claim: Detection timing meets acceptance criterion AC-DET-07.
  - Solution: Timing test report TR-18, section 5.2.
  - Linked assessment documentation explains:
    - why TR-18 is relevant to this claim
    - which scenarios, configurations, or conditions are covered
    - any uncovered limitations or possible refutation
  - Example CSE note:
  - TR-18 shows measured detection latency below AC-DET-07 for scenarios S1-S12 in configuration C4. This supports the claim for that scenario set and configuration. Degraded sensor mode D3 is not covered and remains outside the supported scope.

**References**

References: Weaver et al., Software Safety Arguments: Towards a Systematic Categorisation of Evidence, Hawkins et al., A New Approach to Creating Clear Safety Arguments, CAE Concepts / Building Blocks, UL 4600 5.4.2.1(c)(1)-(2)

### EV.7: Keep evidence controlled: owner, version, date, status, repository

**Guideline**

Evidence cited in the safety case should be under configuration or document control, with clear ownership, version or revision, date, status, and a stable retrieval location. Do not rely on mutable live documents as evidence unless the cited version is fixed or the change process explicitly triggers re-assessment of the affected claim.

**Why**

Uncontrolled or mutable evidence is hard to verify, maintain, and re-assess. If a cited artifact can change after review, the argument may silently lose validity while still appearing supported.

**Review prompts**
- Who owns the evidence?
- Which version or revision is being cited?
- Is the evidence retrieved from a controlled location?
- Is the cited artifact fixed, or can it still change?
- If it is a live document, is there an explicit mechanism that re-assesses affected claims when the document changes?
- Is its status clear, for example draft, in review, approved, or released?

**Example**
- Bad: Evidence: Test summary on team wiki.
- Problem: The cited source has no fixed revision, no clear approval state, and no stable retrieval point for future review.
- Better:
  - Evidence: Test summary TSR-11, rev D, approved 2026-03-14, owner Safety Validation Team, stored in the controlled evidence repository.

**Note**
If a live source is used operationally, the cited version and the re-assessment trigger are both defined explicitly.

This control information does not need to be stored inside the safety case argument itself. It may be managed in a linked repository, evidence register, document management system, or other controlled mechanism, provided the cited evidence remains uniquely identifiable, retrievable, and stable for review.

**References**

References: RA 1205, ONR, AVSC CSE 3.8; 6.1; Table 2, UL 4600 5.2.2; 5.4.2.1(b)

### EV.8: Cite fixed evidence, not live mutable content

**Guideline**

Do not cite live mutable content as evidence unless the cited state is fixed, versioned, archived, or otherwise controlled so that the reviewed argument always refers to the same content.

**Why**

This rule is the specific citation case of EV.7. If cited evidence can change after review, the safety case may appear supported while its actual evidential basis has changed or disappeared. This breaks reproducibility, reviewability, and configuration control.

**Review prompts**
- Could this cited content change without the safety case being updated?
- Is the cited state fixed, versioned, or archived?
- Can a future reviewer retrieve the exact same content that was reviewed?
- If the source is live, is there an explicit process that triggers re-assessment of affected claims when it changes?

**Example**
- Bad: See braking verification page in Confluence.
- Better: See Braking Verification Plan BVP-04, rev C, approved 2026-03-11.
- Also acceptable: See archived snapshot of Confluence page CP-118, version 17, captured 2026-03-11.

**References**

References: RA 1205, ONR, AVSC CSE 3.8; 6.1; Table 2, UL 4600 5.1.1.1(b)-(c); 5.2.2; 5.4.1.1(a)

### EV.9: Do not argue directly from undocumented system knowledge

**Guideline**

Do not support claims by relying on undocumented engineering knowledge, design understanding, or verbal explanation. Claims about system behavior, design, interfaces, mitigations, or operating limits should be grounded in controlled documentation or other identified evidence.

**Why**

A safety case should argue from reviewable evidence, not from what engineers happen to know. When system knowledge is written directly into the safety case without a supporting source, the argument becomes hard to verify, hard to maintain, and difficult to assess for completeness. It also becomes unclear whether the claim is supported by an approved design basis or only by current team understanding.

**Review prompts**
- Is this claim supported by controlled documentation or other identified evidence?
- Is the safety case describing how the system works instead of arguing from documented sources?
- Would the claim still be supportable if the original engineer were unavailable?
- Should this material be moved to a specification, design description, interface definition, hazard analysis, or other work product and then cited as evidence?

**Example**
- Bad pattern:
  - Claim: `Unsafe torque requests are prevented during degraded localization.` The safety case includes a free-text explanation of the controller behavior, but the relevant design basis is not identified through context and no supporting artifacts are linked.
- Problem: the branch relies on undocumented system knowledge written into the safety case itself rather than on explicit specification context and reviewable evidence.
- Better pattern:
  - Claim: `Unsafe torque requests are prevented during degraded localization.` Context identifies the relevant braking control design specification, degraded-mode requirements, and interface definition.
  - Evidence supports that the specified behavior is implemented and verified.
  - The safety case argues from those documented artifacts instead of serving as the primary description of the design.

**References**

References: UL 4600 5.1.1.2(e); 5.3.2.1(a)(2); 5.7.1.6.1, GSN v3 2:3.7.3; CAE guidance on explicit argument structure and avoidance of free-form argumentation

## SU. Sufficiency, uncertainty, and pitfall rules

### SU.1: Identify and address plausible challenges to claims, reasoning, and evidence

**Guideline**

Where a reviewer could reasonably question whether a claim, reasoning step, evidence item, assumption, or stated scope is valid, complete, applicable, or sufficiently reliable, make that challenge explicit and address it where needed.

**Why**

A credible safety case should not only present supporting material. It should also make important doubts visible and show how they are handled. This fits well with GSN-style review, where challenge is used to test whether a claim, inference, or supporting material still stands when subjected to scrutiny.

**Review prompts**
- What could invalidate this claim or reasoning step?
- What assumptions, confounders, uncertainties, or biases are relevant here?
- Could this evidence be incomplete, misleading, or outside the supported scope?
- Is the challenge really against the claim, the reasoning, the evidence, an assumption, or the stated scope?
- Are important doubts visible in the argument, or left unstated?

**Example**
- Bad pattern:
  - Claim: Hazard analysis is complete for the defined ODD.
  - Evidence: Hazard analysis report HAR-03.
- Problem: a reviewer could reasonably ask whether the analysis covered scenarios introduced after the most recent ODD revision, whether the chosen method has known coverage limits for emergent multi-actor interactions, and whether the ODD assumptions still hold. None of these challenges are visible in the argument.
- Better pattern:
  - Claim: Hazard analysis is complete for the defined ODD.
  - Evidence: Hazard analysis report HAR-03.
  - Challenge: The analysis may not cover scenarios introduced after the most recent ODD revision.
  - Response: Change-impact review CIR-12 confirms newly added scenarios were re-examined.
  - Challenge: The chosen method has known coverage limits for emergent multi-actor interactions.
  - Response: Supplementary scenario-based analysis SBA-04 addresses that gap.

**References**

References: CAE Review and Challenge, CAE Defeaters, RA 1205, UL 4600 5.3.2.2(a); 5.4.2.2(b), GSN v3 dialectic/challenge concepts

### SU.2: Make assumptions explicit and justify why they are reasonable

**Guideline**

Do not rely on hidden assumptions. State assumptions explicitly, explain why they are reasonable, and ensure they are monitored or otherwise controlled where needed.

**Why**

Unstated or weakly founded assumptions are a common cause of later argument invalidation. That aligns well with UL 4600’s treatment of assumptions and lifecycle monitoring. GSN also treats assumptions as a distinct element type, so checking whether something is really an assumption is appropriate.

**Review prompts**
- What must be true for this branch to hold?
- Why is this assumption reasonable, and how would we know if it became false?
- Is this really an assumption, or should it instead be represented as context, a claim, or evidence?

**Example**
- Bad pattern:
  - Claim: Localization accuracy is acceptable within the defined ODD.
  - The argument silently relies on the assumption that map data used at runtime is current, but this assumption is not recorded.
- Problem: a reviewer cannot judge whether the assumption is reasonable, whether it is monitored, or what would invalidate it. If the assumption fails, the affected claim may silently lose support.
- Better pattern:
  - Claim: Localization accuracy is acceptable within the defined ODD.
  - Assumption: Map data used at runtime is no more than 7 days out of date.
  - Justification: Map update process MAP-PROC-02 enforces a 7-day refresh cycle and is monitored by KPI MAP-KPI-01.
  - Re-assessment trigger: Sustained KPI breach or change to the map update process.

**References**

References: UL 4600 5.4.1.3(a)(11); 5.4.2.2(a)(3); 5.4.1.6.2, GSN v3 0:4.6; 1:2.2.17

### SU.3: Do not rely on uncorroborated expert judgment alone

**Guideline**

Do not rely on expert judgment alone unless its basis, limits, and corroborating support are stated, or the residual uncertainty is monitored over the lifecycle where appropriate.

**Why**

Expert opinion may be useful, but unsupported opinion is weak support and can easily outstate what is actually known.

**Review prompts**
- Is the opinion supported by data, literature, documented analysis, or another explicit technical basis?
- Is the context of applicability clear and argued?
- If the opinion remains weakly supported, is lifecycle monitoring in place where needed?

**Example**
- Bad pattern:
  - Claim: Residual risk is acceptable.
  - Evidence: Safety review board statement that residual risk is considered acceptable.
- Problem: expert judgment is being used as the sole basis for the claim, with no analysis, data, or independent corroboration that a reviewer can examine.
- Better pattern:
  - Claim: Residual risk is acceptable.
  - Evidence: Quantitative risk analysis QRA-09 showing residual risk below the defined threshold.
  - Evidence: Operational data summary ODS-03 covering 18 months of comparable exposure with no injury-class events.
  - Expert review: Safety review board record SRB-2026-04 confirming the analysis method, inputs, and conclusion are consistent with established practice.
  - Note: Expert review is corroborating, not substituting for, the underlying analysis and data.

**References**

References: UL 4600 5.4.2.2(a)(1); 5.4.2.6.3, AVSC CSE 6.1-6.3

### SU.4: Monitor claims that cannot be fully supported at design time

**Guideline**

When a claim cannot be fully supported at design time, make the remaining uncertainty explicit and define lifecycle monitoring that can confirm or challenge the claim during operation.

**Why**

Some claims depend partly on assumptions, limited evidence, or expected field behavior. In such cases, the safety case should not hide the remaining uncertainty. It should explain it and define how operation will provide feedback.

**Review prompts**
- What part of this claim is not fully supported at design time?
- Can that remaining uncertainty only be reduced through operational or field data?
- Is lifecycle monitoring defined for that uncertainty?
- Are reassessment triggers identified?

**Example**
- Claim: Unexpected roadside object class X is sufficiently rare that residual risk is acceptable.
- Current support: design-time analysis suggests object class X is rare, but the available data is limited and does not fully establish its operational frequency.
- Acceptable treatment:
  - state explicitly that the rarity assumption is not fully confirmed at design time
  - define field monitoring for the occurrence of roadside object class X
  - define reassessment triggers, for example if observed frequency or associated incidents exceed threshold T
- Not acceptable:
  - treat the rarity assumption as fully proven without any operational follow-up

**References**

References: ISO 21448:2022 12.3-12.4; 13.1-13.4, UL 4600 5.4.2.2(a); 5.4.2.3(c)

### SU.5: Do not reuse safety credit from another context without showing it still applies

**Guideline**

Do not rely on safety credit from proven-in-use technology, legacy technology, COTS, prior assessments, standard conformance, or prior practice unless you show that the original context is sufficiently comparable to the current one.

**Why**

Safety confidence gained in one context does not automatically remain valid in another. Differences in operating environment, purpose, interfaces, duty cycle, autonomy role, or assumptions can invalidate the reuse.

**Review prompts**
- What safety confidence, evidence, or assessment result is being reused from another context?
- Is the original operating context sufficiently comparable to the current one?
- Have differences in purpose, environment, interfaces, or assumptions been identified?
- Have the limitations of the original assessment been stated?

**Example**
- Bad claim:
  - This camera is proven in use and is therefore acceptable for autonomous truck operation.
- Problem:
  - The claim takes safety credit from another context without showing that the original application, operating conditions, interfaces, and safety role are sufficiently comparable.
- Better claim:
  - Reuse of camera safety credit is justified for the current application.
  - Context:
  - Original application: conventional passenger vehicle ADAS use.
  - Current application: autonomous heavy truck operation.
  - Justification (if needed):
  - Safety credit may only be reused if the original and current contexts are shown to be sufficiently comparable in the aspects that matter to safety.
  - Possible subclaims:
    - The original and current operating environments are sufficiently comparable.
    - The original and current duty cycles are sufficiently comparable.
    - The original and current interfaces and installation conditions are sufficiently comparable.
    - The original and current safety roles and failure consequences are sufficiently comparable.
    - Any non-comparable differences are addressed by additional evidence or explicit limitations.

**References**

References: UL 4600 5.3.3.2(c); 5.3.2.2(b)-(c)

### SU.6: Do not dismiss operational feedback because it is non-reproducible or non-injury

**Guideline**

When a claim relies on operational experience, field monitoring, incident history, or proven-in-use style reasoning, do not dismiss incidents, near misses, anomalies, or failure reports merely because they have not recurred, cannot yet be reproduced, or did not lead to harm.

**Why**

Operational feedback is often used to support claims about residual risk, rarity, adequacy of existing controls, or continued acceptability in service. In those branches, non-injury or non-reproducibility does not make a signal irrelevant. Several weak signals together may show that the argument is less reliable than it appears.

**Review prompts**
- Is this branch relying on operational experience or field feedback as part of its support?
- Are incidents defined broadly enough to include near misses, close calls, and anomalies that could have led to harm?
- Is adverse operational feedback being screened out too aggressively?
- Is the argument considering the combined signal from multiple incidents or anomalies?
- Is adverse operational evidence explicitly recorded, evaluated, and addressed?

**Example**
- Bad pattern:
  - Claim: Residual risk from unexpected roadside object encounters is acceptable in operation.
  - Support used: field incident history and operational monitoring.
  - Safety case note: Three roadside-object anomalies were reported, but none caused injury and none could be reproduced, so they are not safety-relevant.
- Problem: the argument is using operational feedback, but dismisses adverse signals simply because they were non-injury and non-reproducible.
- Better pattern:
  - Claim: Residual risk from unexpected roadside object encounters is acceptable in operation.
  - Support used: field incident history and operational monitoring.
  - Safety case treatment: the three anomalies are recorded, grouped, and evaluated as adverse operational evidence. The argument explains whether they challenge the rarity assumption, whether they indicate a gap in object coverage, and whether reassessment or additional mitigation is required.

**References**

References: RA 1205 (living / managed safety case), ONR SAPs (reassess using lessons from failures), UL 4600 5.3.3.2(d)

### SU.7: Do not argue low risk from operational experience or unvalidated simulation alone

**Guideline**

Do not infer low risk for a known hazard solely from uneventful operational history or from simulation whose credibility for the claim has not been demonstrated.

**Why**

Operational exposure can miss catastrophic but rare outcomes. Simulation can miss modeling defects and abstraction errors.

**Review prompts**
- Is simulation alone being treated as enough to show low risk?
- Is operational history alone being treated as enough to show low risk?
- Has simulation validity for this claim not been shown?
- Are corroborating evidence, scenario limits, or model limitations missing?

**Example**
- Bad pattern:
  - Claim: Collision risk with cut-in vehicles is low.
  - Evidence: Simulation results SIM-12.
  - Justification: No collisions were observed in the simulation results, therefore the risk is low.
- Problem: the branch treats simulation results alone as sufficient proof that risk is low, without showing that the simulation is valid for this claim, that the modeled scenarios are adequate, or that important model limitations are understood.
- Better pattern:
  - Claim: Collision risk with cut-in vehicles is acceptably low.
  - Evidence: Simulation results SIM-12.
  - Evidence: Track test report TR-08.
  - Evidence: Field incident review FR-03.
  - The argument explains: why SIM-12 is valid for this hazard and what scenario space it covers what limitations remain in the simulation model how TR-08 corroborates important behaviors in representative test conditions how FR-03 is used to check whether operational experience challenges the claim

**References**

References: UNECE ADS safety case clauses on simulation credibility and consistency across virtual, track, and real-world testing, ISO 21448:2022, UL 4600 5.3.3.2(i)-(j); 5.4.2.1(c)

### SU.8: Do not assume human data or human-designed tests cover autonomy-specific failures

**Guideline**

Do not assume that human-operated data sets or human-designed test plans are sufficient to cover autonomy-specific failures or edge cases.

**Why**

Autonomous systems can encounter operating situations and failure combinations that are uncommon in human driving. Human-derived data and human-designed tests may therefore miss important autonomy-specific risks.

**Review prompts**
- Is the claim supported mainly by human-operated data or human-designed tests?
- Could the autonomous system encounter situations or create hazards that are uncommon in human driving?
- Are autonomy-specific failure modes and edge cases explicitly considered?
- Is there evidence that the test basis covers autonomy-specific failures, not only human-driving situations?

**Example**
- Bad pattern:
  - Claim: Planning failure modes are adequately covered by the test set.
  - Evidence: Scenario Selection Report SSR-04.
  - Justification: The scenario set is based on human-driven fleet data and therefore covers relevant road situations.
- Problem: the branch assumes that human-driven data is enough to cover planning failures, but the autonomous planner may enter unusual states or produce behaviors that human drivers would not normally create.
- Better pattern:
  - Claim: Planning failure modes are adequately covered by the test set.
  - Evidence: Scenario Selection Report SSR-04.
  - Evidence: Planner Failure Analysis Report PFA-03.
  - Evidence: Edge Case Test Specification ETS-07.
  - Justification: Coverage is based not only on human-driven scenarios, but also on autonomy-specific planner failure analysis and identified edge cases.

**References**

References: ISO 21448:2022 7.1-7.4; 9.1-9.3; 10-11, UL 4600 5.3.3.2(e); 5.3.3.2(g); 5.4.2.2(b)

### SU.9: Document unstated assumptions at the point of use

**Guideline**

When a claim or reasoning step depends on something that is not currently stated, make that dependency explicit at the point where it constrains the argument, using an assumption, context element, or subclaim as appropriate.

**Why**

Hidden dependencies are a common reason for late argument invalidation. Making them visible helps the reviewer see what the branch depends on and decide whether that dependency should remain an assumption, be stated as context, or be argued as a claim.

**Review prompts**
- What must be true for this claim or strategy to hold, but is not currently stated?
- Is the hidden dependency local to the claim, or to the reasoning step?
- Should this dependency be represented as an assumption, as context, or as a claim that must be proved?

**Example**
- Bad pattern:
  - Claim: Localization integrity is sufficient for safe fallback.
- Problem: the branch depends on an unstated condition about localization performance during fallback, but that dependency is only implicit.
- Better pattern:
  - Claim: Localization integrity is sufficient for safe fallback.
  - Assumption: Localization integrity remains within bound L1 during fallback maneuver.
- Or, if that dependency should be argued rather than assumed:
  - Claim: Localization integrity is sufficient for safe fallback.
  - Subclaim: Localization integrity remains within bound L1 during fallback maneuver.
  - Evidence: Fallback localization analysis report FLA-03.

**References**

References: UL 4600 5.4.1.3(a)(11); 5.4.1.6.2; 5.4.2.2(a)(3), GSN v3 0:4.6; 1:2.2.12; 1:2.2.17

### SU.10: Keep assumptions bounded, specific, and monitorable

**Guideline**

Do not use assumptions that are broader than the claim scope or so vague that they cannot be checked, challenged, or monitored.

**Why**

Over-broad assumptions can make a claim appear closed while removing most of its review value. If an argument depends on an assumption, the assumption should be narrow enough to understand, evaluate, and monitor where needed.

**Review prompts**
- Is the assumption matched to the scope of the claim it constrains?
- Can the assumption be checked, challenged, or monitored?
- Does the assumption hide several different dependencies that should be separated?
- Would the branch become clearer if the assumption were narrowed or split?

**Example**
- Bad pattern:
  - Claim: Traffic signal interpretation is sufficiently reliable for safe intersection handling.
  - Assumption: Infrastructure behaves correctly.
- Problem: the assumption is too broad. It does not identify which infrastructure, which behaviors, which authorities, or what kinds of failure are being assumed away.
- Better pattern:
  - Claim: Traffic signal interpretation is sufficiently reliable for safe intersection handling.
  - Assumption: Within the defined ODD, traffic signals managed by the identified road authorities are assumed to conform to the referenced control standard.
  - Monitoring / follow-up support where needed: Violations are tracked through field feedback and incident analysis.
- Or, if several dependencies are actually involved:
  - Assumption: Traffic signal installations in the defined ODD conform to the referenced control standard.
  - Assumption: Detected traffic signal anomalies are captured through field feedback.

**References**

References: UL 4600 5.4.2.2(a)(3); 10.5.1.2(b),(h); 12.5.1.2(c)(1); 12.5.2.2(b), GSN v3 1:2.2.12; 1:2.2.17

### SU.11: Turn plausible reviewer challenges into explicit Counter Claims and resolve them

**Guideline**

When review raises a plausible What if X? challenge, make that challenge explicit as a Counter Claim and resolve it visibly in the safety case. The resolution may reject the Counter Claim, narrow or revise the original claim, add supporting evidence, introduce assumptions and monitoring, or leave a visible open issue if the matter is not yet resolved.

**Why**

A credible safety case should not leave plausible challenges only in review comments or reviewer intuition. Good reviews expose weaknesses early. Making the challenge explicit helps ensure that it is either resolved properly or left visible until it is resolved.

**Review prompts**
- What exactly is the reviewer challenge?
- Should this challenge be made explicit as a Counter Claim?
- Has the Counter Claim been rejected, sustained, or left unresolved?
- If sustained, has the original branch been updated appropriately?
- If unresolved, is the open issue visible and traceable?

**Example**
- Initial branch:
  - Claim: Fallback behavior is acceptably safe.
- Reviewer challenge:
  - What if localization drops out during fallback?
- Make the challenge explicit:
  - Counter Claim: Fallback behavior is not acceptably safe if localization drops out during fallback.
  - Status: Undeveloped (while analysis is ongoing)
- Possible resolution 1 — Counter Claim rejected:
  - Evidence: Fallback localization analysis FLA-04.
  - Evidence: Fallback test report FTR-09.
  - Updated Claim: Fallback behavior is acceptably safe.
- Possible resolution 2 — Counter Claim sustained, original claim narrowed:
  - Updated Claim: Fallback behavior is acceptably safe under conditions with validated localization continuity.
- Possible resolution 3 — Counter Claim partly sustained, assumption plus monitoring added:
  - Claim: Fallback behavior is acceptably safe.
  - Assumption: Localization continuity is maintained during fallback.
  - Monitoring: Localization continuity violations are tracked through operational monitoring and incident review.
- Possible resolution 4 — not yet resolved:
  - Open Issue: Impact of localization dropout during fallback remains unresolved and requires additional analysis.

**References**

References: CAE Review and Challenge, CAE Defeaters, RA 1205, UL 4600 5.3.2.2(a); 5.3.2.3(c)(1)-(2); 5.4.2.2(b); 5.4.2.3(a), GSN v3 dialectic/challenge concepts

## LF. Logical fallacy rules

These guideline entries identify reasoning errors that weaken safety arguments. They are intended to support the development and review of safety cases by helping authors and reviewers examine whether claims, strategies, and evidence are argued soundly.

### LF.1: Avoid circular reasoning

**Guideline**

Do not support a claim by restating it, renaming it, or assuming it in the support.

**Why**

Circular support creates the appearance of argument without adding any new support.

**Review prompts**
- Would the support still work if the parent claim were not assumed true?
- Is the same conclusion being repeated with different words?

**Example**
- Bad claim: The system is acceptably safe because the safety case shows acceptable safety.

**References**

References: Greenwell et al. 2006 — Circular Reasoning, UL 4600 5.3.3.1(a); 5.3.3.2(a); 5.3.3

### LF.2: Avoid irrelevant premises

**Guideline**

Do not use evidence or supporting statements that may be true but do not support the immediate claim being made.

**Why**

A common defect is to attach true or relevant material to the wrong claim, so the branch appears supported even though the actual inference is missing.

**Review prompts**
- Does this evidence support this exact claim?
- Is the evidence only relevant to a different or neighboring claim?
- Is the missing support actually a different intermediate claim that has not been stated?

**Example**
- Bad claim: Brake fault handling is acceptable.
  - Bad evidence: Brake fault handling requirements are documented.
- Problem: documented requirements may be necessary, but they do not by themselves show that brake fault handling is acceptable.
- Better pattern:
  - Claim: Brake fault handling is acceptable.
  - Subclaim: Brake fault handling requirements are correctly defined.
  - Subclaim: Implemented brake fault handling satisfies the defined requirements.
  - Evidence: Brake fault handling requirements specification BRS-04.
  - Evidence: Brake fault handling verification report BVR-09.

**References**

References: Greenwell et al. 2006 — Irrelevant Premise / Using the Wrong Reasons, UL 4600 5.3.3.1(a); 5.3.3.2(a); 5.3.2.1(a)(1)

### LF.3: Avoid arguing from ignorance

**Guideline**

Do not treat lack of discovered evidence against a claim as positive evidence for the claim.

**Why**

Not finding a problem is not the same as showing that the problem does not exist. Claims about completeness or absence need support from the search basis, scope, and adequacy of the methods used.

**Review prompts**
- Is not found being treated as does not exist?
- Is the claim really about completeness of the search, rather than absolute absence?
- Was the search for contrary evidence demonstrably adequate for the stated scope?

**Example**
- Bad pattern:
  - Claim: No other credible hazards exist.
  - Evidence: HARA report HAR-03.
  - Justification: The HARA identified all relevant hazards, and no further hazards were found.
- Problem: the branch treats the absence of newly discovered hazards as proof that no other credible hazards exist.
- Better pattern:
  - Claim: Hazard identification is sufficiently complete for the defined scope.
  - Context: Applies to the defined item, ODD, and lifecycle scope.
  - Evidence: HARA report HAR-03.
  - Evidence: STPA report STP-02.
  - Evidence: Hazard review record HRR-07.
  - Justification: Complementary hazard identification methods and review coverage have been applied for the defined scope.

**References**

References: Greenwell et al. 2006 — Arguing from Ignorance, UL 4600 5.3.3.1(a); 5.3.3.2(a); 5.4.2.3(a)

### LF.4: Avoid unjustified comparison or unjustified distinction

**Guideline**

Do not claim that one case is equivalent to, safer than, better than, or different from another unless the basis of comparison or distinction is explicit and relevant to the claim being made.

**Why**

Comparison-based arguments can look persuasive while hiding differences in scope, operating conditions, metrics, evidence quality, or confidence. Distinctions can also be misused to dismiss relevant comparators without showing why the difference matters.

**Review prompts**
- What exactly is being compared or distinguished?
- Is the basis of comparison or distinction explicit?
- Are the compared cases matched in scope, operating conditions, metrics, and confidence level?
- If a difference is claimed, is it shown why that difference matters to the argument?

**Example**
- Bad pattern:
  - Claim: The autonomous vehicle is safer than a human driver.
  - Evidence: Simulation report SIM-09.
  - Justification: The autonomous vehicle had fewer simulated collisions than the human-driver baseline.
- Problem: the comparison may be unjustified if the simulation conditions, scenario coverage, driver model, metrics, and confidence are not shown to be appropriate and comparable.
- Better pattern:
  - Claim: For the defined ODD and stated comparison metric, the autonomous vehicle has lower collision rate than the specified human-driver baseline.
  - Context: Comparison applies to ODD-A, metric M1, and baseline definition BD-02.
  - Evidence: Simulation report SIM-09.
  - Evidence: Baseline comparison report BCR-03.
  - Evidence: Scenario validity report SVR-04.
  - Justification: The compared cases use matched scope, scenarios, metrics, and confidence basis.

**References**

References: Greenwell et al. 2006 — Unjustified Comparison, Unjustified Distinction, UL 4600 5.3.3.1(a); 5.3.3.2(a); 5.3.3.2(c)

### LF.5: Avoid sample-size and representativeness fallacies

**Guideline**

Do not generalize too far from too little data, or from data that does not match the operating context being claimed.

**Why**

A small or skewed data set can support only a correspondingly narrow claim.

**Review prompts**
- Is the sample size adequate for the confidence implied?
- Does the data distribution match the ODD and edge cases?
- Is the claim broader than the sample supports?

**Example**
- Bad pattern:
  - Claim: The item is acceptably safe across the defined ODD.
  - Evidence: Road test report RTR-05 covering 12 daylight highway runs in dry conditions.
  - Justification: No safety-critical events were observed during testing.
- Problem: the claim covers the full ODD, but the evidence covers only a small and narrow subset of operating conditions. The sample is too limited in size and representativeness to support the broader claim.
- Better pattern:
  - Claim: The item is acceptably safe for the tested daytime highway subset of the ODD.
  - Context: Applies only to dry daytime highway operation under the conditions covered in RTR-05.
  - Evidence: Road test report RTR-05.
- Or, if the broader claim is to be kept:
  - Claim: The item is acceptably safe across the defined ODD.
  - Evidence: Road test report RTR-05.
  - Evidence: Night and weather test report NWT-03.
  - Evidence: Scenario coverage analysis SCA-04.
  - Evidence: Edge-case test report ETR-02.
  - Justification: The combined evidence set provides coverage across the claimed ODD, including relevant distributions and edge cases.

**References**

References: Greenwell et al. 2006 — Insufficient Sample Size, Unrepresentative Sample

### LF.6: Avoid pseudo-precision

**Guideline**

Do not present numerical precision beyond what the evidence, model, assumptions, or method can justify.

**Why**

A highly precise number can give a false impression of certainty. When uncertainty, confidence, model limits, or input assumptions are weak, the stated precision should reflect that.

**Review prompts**
- Does the number imply a level of certainty the method cannot support?
- Are uncertainty, assumptions, and confidence bounds stated where needed?
- Is the stated precision greater than the quality of the underlying evidence or model?
- Would a rounded value or bounded statement better reflect the real knowledge state?

**Example**
- Bad pattern:
  - Claim: Residual collision risk is 3.742 x 10^-7 per hour.
  - Evidence: Quantitative risk analysis report QRA-05.
- Problem: the stated value suggests a level of certainty that may not be justified by the model assumptions, input data quality, scenario coverage, or confidence bounds.
- Better pattern:
  - Claim: Residual collision risk is below the accepted threshold for the defined operating conditions.
  - Context: Applies under the assumptions and scenario scope defined in QRA-05.
  - Evidence: Quantitative risk analysis report QRA-05.
  - Justification: The result is reported with precision consistent with model uncertainty and stated confidence.
- Or, where a numeric claim is still appropriate:
  - Claim: Residual collision risk is estimated to be on the order of 10^-7 per hour for the defined operating conditions.
  - Context: Estimate is subject to the assumptions, uncertainty, and confidence limits stated in QRA-05.
  - Evidence: Quantitative risk analysis report QRA-05.

**References**

References: Greenwell et al. 2006 — Pseudo-Precision

### LF.7: Avoid omission of key evidence and ignoring counter-evidence

**Guideline**

Do not omit evidence that a skeptical reviewer would naturally expect, and do not leave known contrary evidence unanswered.

**Why**

A safety case becomes misleading when it presents only supporting material and leaves out evidence that could weaken, limit, or challenge the claim.

**Review prompts**
- What evidence would a critical reviewer reasonably expect to see for this claim?
- Is any known anomaly, failure, exclusion, or limitation being left unaddressed?
- Does the omitted material affect the meaning, scope, or credibility of the claim?
- Is contrary evidence explicitly addressed rather than silently ignored?

**Example**
- Bad pattern:
  - Claim: Sensor robustness is acceptable.
  - Evidence: Sensor performance test report SPR-08.
  - Justification: The reported test results show robust detection performance.
- Problem: the branch cites supportive performance results but omits known obscuration, contamination, or environmental degradation evidence that a reviewer would naturally expect for a robustness claim.
- Better pattern:
  - Claim: Sensor robustness is acceptable for the defined conditions.
  - Evidence: Sensor performance test report SPR-08.
  - Evidence: Obscuration test report OTR-03.
  - Evidence: Environmental degradation test report EDR-05.
  - Justification: The argument addresses both supporting and limiting evidence for the claimed operating conditions.
- Or, if contrary evidence exists:
  - Claim: Sensor robustness is acceptable for the defined conditions.
  - Evidence: Sensor performance test report SPR-08.
  - Evidence: Environmental degradation anomaly review EAR-02.
  - Context: Claim excludes heavy mud obscuration beyond the tested condition range.
  - Justification: Known degradation limits are explicitly addressed and reflected in the claim scope.

**References**

References: Greenwell et al. 2006 — Omission of Key Evidence, Ignoring Available Counter-Evidence

## RD. Rhetorical device rules

These guideline entries identify presentation choices that affect how safety arguments are understood and reviewed. They help distinguish between wording that improves clarity and wording that increases confidence without increasing support.

### RD.1: Use explicit signposting of argument element roles

**Guideline**

Make it clear whether a statement is functioning as a claim, evidence reference, context, assumption, or justification.

**Why**

Review becomes harder when the reader must infer the role of a statement. Clear signposting reduces confusion between argument elements and makes the structure easier to inspect.

**Review prompts**
- Is the reader forced to infer the role of the statement?
- Are claims, context, assumptions, and justifications mixed together?
- Is evidence clearly identifiable as evidence rather than explanation or claim text?

**Example**
- Bad pattern:
  - The braking controller is safe in automated mode with valid localization because tests passed.
- Problem: the sentence mixes claim, context, assumption, and evidential reasoning in one statement.
- Better pattern:
  - Claim: Braking controller safety is acceptable.
  - Context: Applies in automated mode.
  - Assumption: Valid localization is available.
  - Evidence: Brake controller verification report BVR-09.
  - Justification (if needed): The cited verification evidence is relevant to the defined operating conditions.

**References**

References: UL 4600 5.3.3.1(b); 5.3.3.2(b), GSN v3 1:2.2.10-1:2.2.19; 1:2.3.2-1:2.3.6

### RD.2: Use scoped claims and qualified confidence language

**Guideline**

State the operating scope and use confidence language that reflects the actual support and any open issues.

**Why**

Safety cases should communicate justified confidence, not absolute assurance when support is partial, bounded, or still open in some respects.

**Review prompts**
- Is the scope of the claim explicit?
- Is unresolved uncertainty visible?
- Does the wording overstate closure?
- Does the confidence language match the actual support?

**Example**
- Bad: The item is safe.
- Better: The item is acceptably safe for daytime urban operation in ODD-A under assumptions A1-A4, with open issue OI-03 for night rain behavior.

**References**

References: UL 4600 5.3.3.1(b); 5.3.3.2(b); 5.2.3.3(d)

### RD.3: Make limitations, objections, and responses explicit

**Guideline**

Make relevant limitations, plausible objections, and uncertainty sources explicit, together with how they are addressed in the argument.

**Why**

A safety case is easier to review and trust when it shows not only supporting material, but also the important limits and challenges that affect confidence in the claim.

**Review prompts**
- Are important limitations visible at the point where they affect the claim?
- Are plausible objections or challenges addressed explicitly?
- Is unresolved doubt hidden, or made visible through scope restriction, assumptions, monitoring, or open issues?

**Example**
- Bad pattern:
  - Claim: Perception robustness is acceptable.
  - Evidence: Simulation report SIM-04.
  - Evidence: Road test report RTR-07.
- Problem: the branch presents supporting evidence, but does not make visible that occlusion behavior is only partly covered and remains a relevant challenge to the claim.
- Better pattern:
  - Claim: Perception robustness is acceptable for the defined visible-object conditions.
  - Context: Claim excludes object occlusion cases beyond the tested coverage defined in OCS-02.
  - Evidence: Simulation report SIM-04.
  - Evidence: Road test report RTR-07.
  - Open Issue: Robustness under severe occlusion remains unresolved and requires additional evidence.
- Or, if the objection is addressed rather than excluded:
  - Claim: Perception robustness is acceptable for the defined visible-object conditions.
  - Evidence: Simulation report SIM-04.
  - Evidence: Road test report RTR-07.
  - Evidence: Occlusion test report OTR-03.
  - Justification: The relevant occlusion challenge is explicitly addressed by the added evidence.

**References**

References: CAE Review and Challenge, CAE Defeaters, RA 1205, ONR / EASA guidance as applicable

### RD.4: Avoid promotional and inflated language

**Guideline**

Do not use promotional, boastful, or image-enhancing language in the safety case.

**Why**

Safety arguments should build confidence through explicit claims, reasoning, and evidence, not through language intended to impress the reader.

**Review prompts**
- Does the wording sound promotional rather than argumentative?
- Would the sentence lose nothing important if the praise-like wording were removed?
- Is the wording trying to create confidence through tone rather than support?

**Example**
- Bad claim: A world-class, cutting-edge safety architecture delivers outstanding assurance.
- Better claim: The architecture prevents hazardous actuation for fault classes F1-F4 under assumptions A1-A3.

**References**

References: CAE Summarising and Communication, OMG SACM 2.3, EASA / RA 1205 safety case communication language

### RD.5: Avoid passive voice when it hides agency

**Guideline**

Do not use passive wording when the identity of the actor matters to understanding, reviewing, or challenging the argument.

**Why**

When a review, judgment, approval, or decision is stated without naming who performed it, accountability becomes harder to inspect and challenge.

**Review prompts**
- Who performed the review, judgment, or approval?
- Does the wording hide who is responsible?
- Would naming the actor improve traceability or auditability?

**Example**
- Bad: It was determined that the claim is adequately supported.
- Better: Safety review board SRB-02 reviewed evidence E12-E19 and concluded that the claim is adequately supported.

**References**

References: RA 1205 (ASSC owner, evidence owners, Safety Statement responsibilities), HSE review guidance on qualified, objective review

### RD.6: Do not bury important limitations or hidden assumptions

**Guideline**

Do not hide important limitations or assumptions in appendices, footnotes, or free text that is not directly connected to the claim they qualify.

**Why**

A safety case should make important boundaries visible where the claim is read. If key limitations or assumptions are easy to miss, the claim can appear stronger or broader than the argument really supports.

**Review prompts**
- Is an important limitation easy to miss?
- Is an important assumption stated explicitly as an assumption, or only implied elsewhere?
- Would a reviewer be misled by reading only the main branch?
- Should the limitation or dependency be made visible through context, an assumption, or a narrower claim?

**Example**
- Bad pattern:
  - Claim: Perception robustness is acceptable.
  - Evidence: Perception validation report PVR-08.
  - A later appendix states that the reported results exclude heavy rain, dense fog, and severe occlusion.
- Problem: the main claim appears broad, but important limiting conditions are only visible outside the main branch.
- Better pattern:
  - Claim: Perception robustness is acceptable for the validated visibility conditions.
  - Context: Claim excludes heavy rain, dense fog, and severe occlusion beyond the tested range defined in PVR-08.
  - Evidence: Perception validation report PVR-08.
- Or, where the dependency is really an assumption:
  - Claim: Perception robustness is acceptable.
  - Assumption: Visibility conditions remain within the validated range defined in PVR-08.
  - Evidence: Perception validation report PVR-08.

**References**

References: CAE Defeaters, RA 1205, UNECE ADS safety case assumptions language
<!-- END GENERATED: guidelines -->
