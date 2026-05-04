"""Build deterministic tool-facing SCCG distribution artifacts."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from sccg_common import DIST, json_text, jsonl_text, load_content_model, public_model, write_if_changed, yaml_text


def _compact_guideline(guideline: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": guideline["id"],
        "category": guideline["category"],
        "title": guideline["title"],
        "statement": guideline["statement"],
        "rationale": guideline["rationale"],
        "review_prompts": guideline["review_prompts"],
        "reference_source_ids": [ref["source_id"] for ref in guideline.get("references", [])],
        "tool": guideline.get("tool", {}),
    }


def _rule_row(model: dict[str, Any], guideline: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": model["schema_version"],
        "sccg_version": model["sccg_version"],
        "id": guideline["id"],
        "category": guideline["category"],
        "title": guideline["title"],
        "statement": guideline["statement"],
        "rationale": guideline["rationale"],
        "review_prompts": guideline["review_prompts"],
        "examples": guideline["examples"],
        "references": guideline["references"],
        "tool": guideline.get("tool", {}),
    }


def _ai_rule_row(model: dict[str, Any], guideline: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "sccg_version": model["sccg_version"],
        "rule_id": guideline["id"],
        "category_id": guideline["category"],
        "title": guideline["title"],
        "statement": guideline["statement"],
        "rationale": guideline["rationale"],
        "review_prompts": guideline["review_prompts"],
        "examples": guideline["examples"],
        "references": guideline["references"],
        "tool": guideline.get("tool", {}),
    }


def build_outputs(model: dict[str, Any] | None = None) -> dict[Path, str]:
    if model is None:
        model = load_content_model()
    full = public_model(model)
    compact = {
        "schema_version": model["schema_version"],
        "sccg_version": model["sccg_version"],
        "document": {
            "title": model["document"]["title"],
            "license": model["document"].get("license"),
        },
        "categories": model["categories"],
        "guidelines": [_compact_guideline(guideline) for guideline in model["guidelines"]],
    }
    rule_rows = [_rule_row(model, guideline) for guideline in model["guidelines"]]
    ai_rule_rows = [_ai_rule_row(model, guideline) for guideline in model["guidelines"]]
    generated_exports = [
        "dist/sccg.full.json",
        "dist/sccg.full.yaml",
        "dist/sccg.compact.json",
        "dist/sccg.rules.jsonl",
        "dist/ai_rule_export.jsonl",
        "dist/review_profiles.json",
        "dist/data_packages.json",
        "dist/prechecks.json",
        "dist/vectorstore_manifest.json",
        "dist/research_metadata.json",
    ]
    vectorstore_manifest = {
        "schema_version": "1.0.0",
        "sccg_version": model["sccg_version"],
        "recommended_files": [
            {
                "path": "dist/sccg.rules.jsonl",
                "content_type": "application/jsonl",
                "purpose": "One SCCG guideline per line for retrieval or rule loading.",
            },
            {
                "path": "dist/ai_rule_export.jsonl",
                "content_type": "application/jsonl",
                "purpose": "AI-oriented rule export with one guideline per line.",
            },
            {
                "path": "dist/sccg.full.json",
                "content_type": "application/json",
                "purpose": "Complete normalized SCCG model.",
            },
        ],
        "metadata_fields": [
            "schema_version",
            "sccg_version",
            "id",
            "category",
            "title",
            "reference_source_ids",
            "review_profile_ids",
            "data_package_ids",
        ],
        "chunking_hint": "Use one guideline per JSONL line.",
    }
    research_metadata = {
        "schema_version": model["schema_version"],
        "sccg_version": model["sccg_version"],
        "guideline_count": len(model["guidelines"]),
        "category_count": len(model["categories"]),
        "review_profile_count": len(model["review_profiles"]),
        "data_package_count": len(model["data_packages"]),
        "precheck_count": len(model["prechecks"]),
        "category_ids": [category["id"] for category in model["categories"]],
        "generated_exports": generated_exports,
    }
    return {
        DIST / "sccg.full.json": json_text(full),
        DIST / "sccg.full.yaml": yaml_text(full),
        DIST / "sccg.compact.json": json_text(compact),
        DIST / "sccg.rules.jsonl": jsonl_text(rule_rows),
        DIST / "ai_rule_export.jsonl": jsonl_text(ai_rule_rows),
        DIST / "review_profiles.json": json_text(
            {
                "schema_version": model["schema_version"],
                "sccg_version": model["sccg_version"],
                "review_profiles": model["review_profiles"],
            }
        ),
        DIST / "data_packages.json": json_text(
            {
                "schema_version": model["schema_version"],
                "sccg_version": model["sccg_version"],
                "data_packages": model["data_packages"],
            }
        ),
        DIST / "prechecks.json": json_text(
            {
                "schema_version": model["schema_version"],
                "sccg_version": model["sccg_version"],
                "prechecks": model["prechecks"],
            }
        ),
        DIST / "vectorstore_manifest.json": json_text(vectorstore_manifest),
        DIST / "research_metadata.json": json_text(research_metadata),
    }


def main() -> int:
    changed = []
    for path, text in build_outputs().items():
        if write_if_changed(path, text):
            changed.append(path)
    if changed:
        for path in changed:
            print(f"Updated {path.relative_to(Path(__file__).resolve().parents[1])}")
    else:
        print("No change to dist outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())