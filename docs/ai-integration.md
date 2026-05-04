# AI Integration

AI-oriented consumers should prefer generated files in [dist/](../dist/) rather than authored YAML.

Recommended files:

- [dist/ai_rule_export.jsonl](../dist/ai_rule_export.jsonl) contains one guideline per line with AI-friendly field names.
- [dist/sccg.rules.jsonl](../dist/sccg.rules.jsonl) contains one complete guideline rule per line.
- [dist/vectorstore_manifest.json](../dist/vectorstore_manifest.json) describes recommended files, metadata fields, and chunking guidance.
- [dist/sccg.full.json](../dist/sccg.full.json) contains the complete normalized model, including review profiles, data packages, and pre-checks.

For retrieval use cases, chunk JSONL files one guideline per line. Preserve `id`, `category`, `title`, `statement`, `rationale`, `review_prompts`, `references`, and `tool` metadata in the retrieval payload so results remain traceable to SCCG guideline IDs.

AI findings should cite guideline IDs rather than reproducing long guideline text. Pre-checks should be treated as candidate signals, not final findings.