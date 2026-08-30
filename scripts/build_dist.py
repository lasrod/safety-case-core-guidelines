"""Build deterministic tool-facing SCCG distribution artifacts."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from sccg_common import DIST, json_text, jsonl_text, load_content_model, public_model, write_if_changed, yaml_text


def _document_block(model: dict[str, Any]) -> dict[str, Any]:
    """Document identity carried by every tool-facing file.

    A tool that loads only the registries it needs should still be able to say
    which document, version, and licence it is quoting.
    """
    return {
        "title": model["document"]["title"],
        "purpose": model["document"]["purpose"],
        "license": model["document"].get("license"),
        "sccg_version": model["sccg_version"],
        "schema_version": model["schema_version"],
    }


def _compact_guideline(guideline: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": guideline["id"],
        "category": guideline["category"],
        "title": guideline["title"],
        "statement": guideline["statement"],
        "short_rule": guideline["short_rule"],
        "rationale": guideline["rationale"],
        "review_prompts": guideline["review_prompts"],
        "reference_source_ids": [ref["source_id"] for ref in guideline.get("references", [])],
        "tool": guideline.get("tool", {}),
    }


def _guideline_metadata(model: dict[str, Any], guideline: dict[str, Any]) -> dict[str, Any]:
    review_profile_ids = [
        profile["id"]
        for profile in model["review_profiles"]
        if guideline["id"] in profile.get("guideline_ids", [])
    ]
    data_package_ids = sorted(
        {
            package_id
            for profile in model["review_profiles"]
            if guideline["id"] in profile.get("guideline_ids", [])
            for package_id in profile.get("required_data", []) + profile.get("optional_data", [])
        }
    )
    return {
        "reference_source_ids": [ref["source_id"] for ref in guideline.get("references", [])],
        "review_profile_ids": review_profile_ids,
        "data_package_ids": data_package_ids,
    }


def _rule_row(model: dict[str, Any], guideline: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": model["schema_version"],
        "sccg_version": model["sccg_version"],
        "id": guideline["id"],
        "category": guideline["category"],
        "title": guideline["title"],
        "statement": guideline["statement"],
        "short_rule": guideline["short_rule"],
        "rationale": guideline["rationale"],
        "review_prompts": guideline["review_prompts"],
        "examples": guideline["examples"],
        "references": guideline["references"],
        "tool": guideline.get("tool", {}),
        **_guideline_metadata(model, guideline),
    }


def _ai_rule_row(model: dict[str, Any], guideline: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": model["schema_version"],
        "sccg_version": model["sccg_version"],
        "id": guideline["id"],
        "category": guideline["category"],
        "rule_id": guideline["id"],
        "category_id": guideline["category"],
        "title": guideline["title"],
        "statement": guideline["statement"],
        "short_rule": guideline["short_rule"],
        "rationale": guideline["rationale"],
        "review_prompts": guideline["review_prompts"],
        "examples": guideline["examples"],
        "references": guideline["references"],
        "tool": guideline.get("tool", {}),
        **_guideline_metadata(model, guideline),
    }


def build_authoring_guidance(model: dict[str, Any]) -> dict[str, Any]:
    """Authoring-time delivery set, resolved so a tool needs no second lookup.

    `core_rules` carries the condensation itself; `element_rules` says which
    profile's guidelines an element written now will be reviewed against, so a
    tool's writing guidance and its review criteria cannot drift apart.
    """
    guideline_by_id = {guideline["id"]: guideline for guideline in model["guidelines"]}
    guidance = model["authoring_guidance"]
    core_rules = [
        {
            "id": entry["id"],
            "category": guideline_by_id[entry["id"]]["category"],
            "short_rule": guideline_by_id[entry["id"]]["short_rule"],
            "statement": guideline_by_id[entry["id"]]["statement"],
            "reason": entry["reason"],
        }
        for entry in guidance["core_rules"]
    ]
    role_elements: dict[str, list[str]] = {}
    for element in model["selectable_elements"]:
        role_elements.setdefault(element["element_role"], []).append(element["element"])
    element_rules = [
        {
            "element_role": role,
            "elements": role_elements.get(role, []),
            "review_profile_id": profile["id"],
            "guideline_ids": profile["guideline_ids"],
        }
        for profile in model["review_profiles"]
        for role in [_profile_element_role(model, profile)]
    ]
    return {
        "schema_version": model["schema_version"],
        "sccg_version": model["sccg_version"],
        "document": _document_block(model),
        "description": guidance["description"],
        "usage": guidance["usage"],
        "core_rules": core_rules,
        "element_rules": element_rules,
    }


def _profile_element_role(model: dict[str, Any], profile: dict[str, Any]) -> str:
    role_by_element = {
        element["element"]: element["element_role"] for element in model["selectable_elements"]
    }
    return role_by_element[profile["applies_to"][0]]


def build_outputs(model: dict[str, Any] | None = None) -> dict[Path, str]:
    if model is None:
        model = load_content_model()
    full = public_model(model)
    compact = {
        "schema_version": model["schema_version"],
        "sccg_version": model["sccg_version"],
        "document": _document_block(model),
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
        "dist/data_package_diagram_layout.json",
        "dist/prechecks.json",
        "dist/authoring_guidance.json",
        "dist/vectorstore_manifest.json",
        "dist/research_metadata.json",
    ]
    vectorstore_manifest = {
        "schema_version": model["schema_version"],
        "sccg_version": model["sccg_version"],
        "document": _document_block(model),
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
            "short_rule",
            "reference_source_ids",
            "review_profile_ids",
            "data_package_ids",
        ],
        "chunking_hint": "Use one guideline per JSONL line.",
    }
    research_metadata = {
        "schema_version": model["schema_version"],
        "sccg_version": model["sccg_version"],
        "document": _document_block(model),
        "guideline_count": len(model["guidelines"]),
        "category_count": len(model["categories"]),
        "review_profile_count": len(model["review_profiles"]),
        "data_package_count": len(model["data_packages"]),
        "precheck_count": len(model["prechecks"]),
        "authoring_core_rule_count": len(model["authoring_guidance"]["core_rules"]),
        "selectable_element_count": len(model["selectable_elements"]),
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
                "document": _document_block(model),
                "selectable_elements": model["selectable_elements"],
                "review_profiles": model["review_profiles"],
            }
        ),
        DIST / "data_packages.json": json_text(
            {
                "schema_version": model["schema_version"],
                "sccg_version": model["sccg_version"],
                "document": _document_block(model),
                "availability_states": model["availability_states"],
                "data_packages": model["data_packages"],
            }
        ),
        DIST / "data_package_diagram_layout.json": json_text(
            {
                "schema_version": model["schema_version"],
                "sccg_version": model["sccg_version"],
                "document": _document_block(model),
                "review_profile_diagram_layout": model["review_profile_diagram_layout"],
            }
        ),
        DIST / "authoring_guidance.json": json_text(build_authoring_guidance(model)),
        DIST / "prechecks.json": json_text(
            {
                "schema_version": model["schema_version"],
                "sccg_version": model["sccg_version"],
                "document": _document_block(model),
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