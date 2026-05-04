"""Validate SCCG authored content and generated outputs."""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator

from build_dist import build_outputs as build_dist_outputs
from build_site import render_index
from check_coverage import build_outputs as build_coverage_outputs
from sccg_common import (
    CONTENT,
    DIST,
    GUIDELINES_DIR,
    INDEX,
    LEGACY_GUIDELINE_KEYS,
    SCHEMAS,
    TOOL_SUPPORT_DIR,
    ID_RE,
    load_content_model,
    load_json,
    load_yaml,
)


def _schema_errors(instance: Any, schema_path: Path, label: str) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft7Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"[schema] {label} {location}: {error.message}")
    return errors


def _duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def _check_file_current(path: Path, expected: str, label: str) -> list[str]:
    if not path.exists():
        return [f"[generated] {label}: {path} is missing"]
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        return [f"[generated] {label}: {path} is out of date"]
    return []


def _validate_schemas() -> list[str]:
    errors: list[str] = []
    errors.extend(_schema_errors(load_yaml(CONTENT / "sccg.yaml"), SCHEMAS / "sccg.schema.json", "content/sccg.yaml"))
    errors.extend(_schema_errors(load_yaml(CONTENT / "references.yaml"), SCHEMAS / "references.schema.json", "content/references.yaml"))
    for path in sorted(GUIDELINES_DIR.glob("*.yaml")):
        errors.extend(_schema_errors(load_yaml(path), SCHEMAS / "guideline_category.schema.json", str(path.relative_to(CONTENT.parent))))
    errors.extend(_schema_errors(load_yaml(TOOL_SUPPORT_DIR / "review_profiles.yaml"), SCHEMAS / "review_profiles.schema.json", "content/tool_support/review_profiles.yaml"))
    errors.extend(_schema_errors(load_yaml(TOOL_SUPPORT_DIR / "data_packages.yaml"), SCHEMAS / "data_packages.schema.json", "content/tool_support/data_packages.yaml"))
    errors.extend(_schema_errors(load_yaml(TOOL_SUPPORT_DIR / "prechecks.yaml"), SCHEMAS / "prechecks.schema.json", "content/tool_support/prechecks.yaml"))
    return errors


def _validate_cross_references(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    reference_ids = {source["id"] for source in model["reference_sources"]}
    category_ids = {category["id"] for category in model["categories"]}
    guideline_ids = [guideline["id"] for guideline in model["guidelines"]]
    data_package_ids = {package["id"] for package in model["data_packages"]}

    for duplicate_id in _duplicates([source["id"] for source in model["reference_sources"]]):
        errors.append(f"[references] duplicate source id {duplicate_id!r}")
    for duplicate_id in _duplicates([category["id"] for category in model["categories"]]):
        errors.append(f"[categories] duplicate category id {duplicate_id!r}")
    for duplicate_id in _duplicates(guideline_ids):
        errors.append(f"[guidelines] duplicate guideline id {duplicate_id!r}")
    for duplicate_id in _duplicates([profile["id"] for profile in model["review_profiles"]]):
        errors.append(f"[review_profiles] duplicate profile id {duplicate_id!r}")
    for duplicate_id in _duplicates([precheck["id"] for precheck in model["prechecks"]]):
        errors.append(f"[prechecks] duplicate pre-check id {duplicate_id!r}")

    for category_id, file_name in model["_category_files"].items():
        if file_name != f"{category_id}.yaml":
            errors.append(f"[categories] category {category_id!r} is in file {file_name!r}, expected {category_id}.yaml")
    for path in sorted(GUIDELINES_DIR.glob("*.yaml")):
        category_document = load_yaml(path)
        category_id = category_document.get("category", {}).get("id")
        if path.stem != category_id:
            errors.append(f"[categories] {path.name}: category id {category_id!r} does not match file name")
        for guideline in category_document.get("guidelines", []):
            guideline_id = guideline.get("id", "<missing>")
            if guideline.get("category") != category_id:
                errors.append(
                    f"[guidelines] {path.name} {guideline_id}: category {guideline.get('category')!r} "
                    f"does not match file category {category_id!r}"
                )
            if isinstance(guideline_id, str) and category_id and not guideline_id.startswith(f"{category_id}."):
                errors.append(
                    f"[guidelines] {path.name} {guideline_id}: id prefix does not match file category {category_id!r}"
                )

    valid_guideline_ids = set(guideline_ids)
    for guideline in model["guidelines"]:
        guideline_id = guideline.get("id", "<missing>")
        match = ID_RE.match(guideline_id or "")
        if not match:
            errors.append(f"[guidelines] {guideline_id}: must match ^[A-Z]{{2}}\\.\\d+$")
            continue
        prefix = match.group(1)
        if guideline.get("category") != prefix:
            errors.append(f"[guidelines] {guideline_id}: category {guideline.get('category')!r} != id prefix {prefix!r}")
        if prefix not in category_ids:
            errors.append(f"[guidelines] {guideline_id}: category prefix {prefix!r} is not defined")
        for key in LEGACY_GUIDELINE_KEYS:
            if key in guideline:
                errors.append(f"[guidelines] {guideline_id}: legacy key {key!r} is not allowed")
        for reference in guideline.get("references", []):
            source_id = reference.get("source_id")
            if source_id not in reference_ids:
                errors.append(f"[guidelines] {guideline_id}: reference source_id {source_id!r} is not defined")

    for profile in model["review_profiles"]:
        for guideline_id in profile.get("guideline_ids", []):
            if guideline_id not in valid_guideline_ids:
                errors.append(f"[review_profiles] {profile['id']}: guideline_id {guideline_id!r} is not defined")
        for package_id in profile.get("required_data", []) + profile.get("optional_data", []):
            if package_id not in data_package_ids:
                errors.append(f"[review_profiles] {profile['id']}: data package {package_id!r} is not defined")

    for precheck in model["prechecks"]:
        for guideline_id in precheck.get("related_guideline_ids", []):
            if guideline_id not in valid_guideline_ids:
                errors.append(f"[prechecks] {precheck['id']}: guideline_id {guideline_id!r} is not defined")
        for package_id in precheck.get("expected_data", []):
            if package_id not in data_package_ids:
                errors.append(f"[prechecks] {precheck['id']}: data package {package_id!r} is not defined")
    return errors


def _validate_generated(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for path, expected in build_dist_outputs(model).items():
        errors.extend(_check_file_current(path, expected, str(path)))
    ai_export_schema = load_json(SCHEMAS / "ai_rule_export.schema.json")
    ai_export_validator = Draft7Validator(ai_export_schema)
    ai_export_path = DIST / "ai_rule_export.jsonl"
    if ai_export_path.exists():
        for line_number, line in enumerate(ai_export_path.read_text(encoding="utf-8").splitlines(), start=1):
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                errors.append(f"[schema] dist/ai_rule_export.jsonl line {line_number}: {error.msg}")
                continue
            for schema_error in sorted(ai_export_validator.iter_errors(row), key=lambda item: list(item.absolute_path)):
                location = "/".join(str(part) for part in schema_error.absolute_path) or "<root>"
                errors.append(
                    f"[schema] dist/ai_rule_export.jsonl line {line_number} {location}: {schema_error.message}"
                )
    original_index = INDEX.read_text(encoding="utf-8")
    errors.extend(_check_file_current(INDEX, render_index(original_index, model), "index.md"))
    for path, expected in build_coverage_outputs(model).items():
        errors.extend(_check_file_current(path, expected, str(path)))
    return errors


def main() -> int:
    errors = _validate_schemas()
    model = load_content_model()
    errors.extend(_validate_cross_references(model))
    errors.extend(_validate_generated(model))

    if errors:
        sys.stderr.write("Validation FAILED:\n")
        for error in errors:
            sys.stderr.write(f"  - {error}\n")
        sys.stderr.write(f"\n{len(errors)} error(s).\n")
        return 1
    print(
        "OK: "
        f"{len(model['guidelines'])} guidelines, "
        f"{len(model['review_profiles'])} review profiles, "
        f"{len(model['data_packages'])} data packages, "
        f"{len(model['prechecks'])} pre-checks validated."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())