# AI, Agent, and MCP Integration

AI-oriented consumers should prefer generated files in [dist/](../dist/) rather than authored YAML. The published guidance for integrators is [tool-integration.md](../tool-integration.md); this page is the short form.

## Two moments, not one

SCCG's review workflow assumes a tool asking for a judgment about an element that already exists. A tool with an AI assistant, an agent integration, or an MCP server also serves the moment where an author or a model is *writing*. A tool that carries SCCG only into review corrects at review time what it could have prevented at authoring time.

## Which file for which job

- [dist/authoring_guidance.json](../dist/authoring_guidance.json) is the authoring-time set. `core_rules` is the condensation to carry in session or system instructions — one imperative line per guideline, each with its id, every guideline family represented. `element_rules` says which review profile an element of each role will be judged under, so the guidance a tool gives while writing is drawn from the criteria the review will apply.
- [dist/ai_rule_export.jsonl](../dist/ai_rule_export.jsonl) and [dist/sccg.rules.jsonl](../dist/sccg.rules.jsonl) carry one guideline per line, for retrieval or for addressing a single rule by id.
- [dist/sccg.compact.json](../dist/sccg.compact.json) is the whole catalog without the authoring-source detail, for a client that loads the rules once.
- [dist/vectorstore_manifest.json](../dist/vectorstore_manifest.json) describes recommended files, metadata fields, and chunking.
- [dist/sccg.full.json](../dist/sccg.full.json) is the complete normalized model, including review profiles, data packages, pre-checks, and the authoring set.

Every tool-facing file carries a `document` block with the title, purpose, licence, `sccg_version`, and `schema_version`, so a tool that loads only one registry can still say what it is quoting.

## Rules of the road

- Quote `short_rule` or `statement` verbatim and cite the guideline id. A paraphrase becomes the tool's rule and drifts from SCCG.
- Carry `sccg_version` into findings, so a result can be reproduced later.
- Report which checks ran. An empty finding list means the checks that ran found nothing, not that the argument conforms.
- Treat pre-checks and markers as candidate signals, and carry each pre-check's `interpretation` text through to the reader.
- Never present a mechanical result as SCCG conformance. Most of SCCG can only be judged by a reader.
- Offer the repair in `tool.repair` rather than applying it; the author decides.
- Report data package availability honestly, using the published states. A review told nothing assumes the data does not exist.
- Use published `markers` and `thresholds` rather than inventing word lists. Where a guideline has none, treat it as judgment-level.
- Record who performed a review. An agent reviewing argument it wrote itself has not produced an independent review.

For retrieval, chunk JSONL files one guideline per line, and preserve `id`, `category`, `title`, `short_rule`, `statement`, `rationale`, `review_prompts`, `references`, and `tool` metadata so results stay traceable to guideline IDs.
