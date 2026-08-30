"""Validate SCCG authored content and generated outputs."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft7Validator

from build_dist import build_outputs as build_dist_outputs
from build_site import MarkerError, render_index
from build_tool_docs import MarkerError as ToolDocMarkerError, build_outputs as build_tool_doc_outputs
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


def _load_yaml_for_validation(path: Path, label: str) -> tuple[Any | None, list[str]]:
    try:
        data = load_yaml(path)
    except FileNotFoundError:
        return None, [f"[schema] {label}: file is missing"]
    except yaml.YAMLError as error:
        return None, [f"[schema] {label}: YAML parse error: {error}"]
    if not isinstance(data, dict):
        return None, [f"[schema] {label} <root>: YAML does not parse to a mapping"]
    return data, []


def _load_json_for_validation(path: Path, label: str) -> tuple[Any | None, list[str]]:
    try:
        data = load_json(path)
    except FileNotFoundError:
        return None, [f"[schema] {label}: file is missing"]
    except json.JSONDecodeError as error:
        return None, [f"[schema] {label}: JSON parse error: {error.msg}"]
    return data, []


def _safe_schema_errors(instance: Any, schema_path: Path, label: str) -> list[str]:
    schema, errors = _load_json_for_validation(schema_path, str(schema_path))
    if errors:
        return errors
    validator = Draft7Validator(schema)
    result = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.absolute_path)):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        result.append(f"[schema] {label} {location}: {error.message}")
    return result


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
    schema_targets = [
        (CONTENT / "sccg.yaml", SCHEMAS / "sccg.schema.json", "content/sccg.yaml"),
        (CONTENT / "references.yaml", SCHEMAS / "references.schema.json", "content/references.yaml"),
        (TOOL_SUPPORT_DIR / "review_profiles.yaml", SCHEMAS / "review_profiles.schema.json", "content/tool_support/review_profiles.yaml"),
        (TOOL_SUPPORT_DIR / "data_packages.yaml", SCHEMAS / "data_packages.schema.json", "content/tool_support/data_packages.yaml"),
        (TOOL_SUPPORT_DIR / "data_package_diagram_layout.yaml", SCHEMAS / "data_package_diagram_layout.schema.json", "content/tool_support/data_package_diagram_layout.yaml"),
        (TOOL_SUPPORT_DIR / "prechecks.yaml", SCHEMAS / "prechecks.schema.json", "content/tool_support/prechecks.yaml"),
        (TOOL_SUPPORT_DIR / "authoring_guidance.yaml", SCHEMAS / "authoring_guidance.schema.json", "content/tool_support/authoring_guidance.yaml"),
    ]
    for data_path, schema_path, label in schema_targets:
        instance, load_errors = _load_yaml_for_validation(data_path, label)
        errors.extend(load_errors)
        if instance is not None:
            errors.extend(_safe_schema_errors(instance, schema_path, label))
    for path in sorted(GUIDELINES_DIR.glob("*.yaml")):
        label = str(path.relative_to(CONTENT.parent))
        instance, load_errors = _load_yaml_for_validation(path, label)
        errors.extend(load_errors)
        if instance is not None:
            errors.extend(_safe_schema_errors(instance, SCHEMAS / "guideline_category.schema.json", label))
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
    for duplicate_id in _duplicates([package["id"] for package in model["data_packages"]]):
        errors.append(f"[data_packages] duplicate data package id {duplicate_id!r}")
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
        data_rationale = profile.get("data_rationale", {})
        rationale_checks = [
            ("required", "required_data"),
            ("optional", "optional_data"),
        ]
        for rationale_key, data_key in rationale_checks:
            expected_ids = profile.get(data_key, [])
            actual_ids = [entry.get("id") for entry in data_rationale.get(rationale_key, [])]
            if actual_ids != expected_ids:
                errors.append(
                    f"[review_profiles] {profile['id']}: data_rationale.{rationale_key} ids must match "
                    f"{data_key} exactly; expected {expected_ids!r}, got {actual_ids!r}"
                )

    element_usage: dict[str, list[str]] = defaultdict(list)
    for profile in model["review_profiles"]:
        for element in profile.get("applies_to", []):
            element_usage[element].append(profile["id"])
    for element, profile_ids in sorted(element_usage.items()):
        if len(profile_ids) > 1:
            errors.append(
                f"[review_profiles] element {element!r} is claimed by multiple profiles "
                f"{sorted(profile_ids)!r}; each element type must map to exactly one review profile"
            )

    selectable = model.get("selectable_elements", [])
    for duplicate_element in _duplicates([entry["element"] for entry in selectable]):
        errors.append(f"[selectable_elements] duplicate element {duplicate_element!r}")
    selectable_ids = {entry["element"] for entry in selectable}
    # Every clickable element must resolve to exactly one profile (totality of the tool lookup).
    for entry in selectable:
        element = entry["element"]
        mapped = element_usage.get(element, [])
        if not mapped:
            errors.append(
                f"[selectable_elements] element {element!r} maps to no review profile; every selectable "
                "element must be reviewable via exactly one profile"
            )
    # Every element a profile claims must be a declared selectable element (no strays or typos).
    for profile in model["review_profiles"]:
        for element in profile.get("applies_to", []):
            if element not in selectable_ids:
                errors.append(
                    f"[review_profiles] {profile['id']}: applies_to element {element!r} is not declared in "
                    "selectable_elements"
                )

    suggested_check_ids = {
        check["id"]
        for guideline in model["guidelines"]
        for check in guideline.get("tool", {}).get("suggested_checks", [])
    }
    for precheck in model["prechecks"]:
        if precheck["id"] not in suggested_check_ids:
            errors.append(f"[prechecks] {precheck['id']}: id is not referenced by any guideline tool.suggested_checks")
        for guideline_id in precheck.get("related_guideline_ids", []):
            if guideline_id not in valid_guideline_ids:
                errors.append(f"[prechecks] {precheck['id']}: guideline_id {guideline_id!r} is not defined")
        for package_id in precheck.get("expected_data", []):
            if package_id not in data_package_ids:
                errors.append(f"[prechecks] {precheck['id']}: data package {package_id!r} is not defined")
    return errors


def _matches_any(terms: list[str], text: str) -> bool:
    """Whether any published marker term appears in the text.

    Word-boundary, case-insensitive matching, which is how the tool integration
    page tells a tool to match them.
    """
    return any(
        re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text, flags=re.IGNORECASE)
        for term in terms
    )


def _validate_tool_contract(model: dict[str, Any]) -> list[str]:
    """Invariants a consuming tool is entitled to rely on.

    These are the rules a tool would otherwise have to rediscover by reading the
    data: that one element resolves to one profile, that one profile has one
    selected-element package, that guideline element names come from the
    published vocabulary, and that a degraded review has a stated meaning.
    """
    errors: list[str] = []
    guideline_ids = {guideline["id"] for guideline in model["guidelines"]}
    package_by_id = {package["id"]: package for package in model["data_packages"]}
    role_by_element = {
        element["element"]: element["element_role"] for element in model["selectable_elements"]
    }
    selectable_names = set(role_by_element)

    for duplicate_id in _duplicates([state["id"] for state in model["availability_states"]]):
        errors.append(f"[availability_states] duplicate state id {duplicate_id!r}")

    selected_by_element_role: dict[str, list[str]] = defaultdict(list)
    for package in model["data_packages"]:
        is_selected = package["role"] == "selected_element"
        has_element_role = "element_role" in package
        if is_selected and not has_element_role:
            errors.append(f"[data_packages] {package['id']}: a selected_element package must declare element_role")
        if not is_selected and has_element_role:
            errors.append(f"[data_packages] {package['id']}: element_role is only for selected_element packages")
        if is_selected and has_element_role:
            selected_by_element_role[package["element_role"]].append(package["id"])
    for element_role, package_ids in sorted(selected_by_element_role.items()):
        if len(package_ids) > 1:
            errors.append(
                f"[data_packages] element role {element_role!r} has more than one selected-element package "
                f"{sorted(package_ids)!r}"
            )
    for element_role in sorted(set(role_by_element.values())):
        if element_role not in selected_by_element_role:
            errors.append(
                f"[data_packages] element role {element_role!r} is selectable but has no selected-element package"
            )

    for profile in model["review_profiles"]:
        roles = {role_by_element[element] for element in profile.get("applies_to", []) if element in role_by_element}
        if len(roles) > 1:
            errors.append(
                f"[review_profiles] {profile['id']}: applies_to mixes element roles {sorted(roles)!r}; "
                "a profile reviews one kind of element"
            )
        selected_ids = [
            package_id
            for package_id in profile.get("required_data", [])
            if package_by_id.get(package_id, {}).get("role") == "selected_element"
        ]
        if len(selected_ids) != 1:
            errors.append(
                f"[review_profiles] {profile['id']}: required_data must contain exactly one selected-element "
                f"package, found {sorted(selected_ids)!r}"
            )
        elif roles:
            expected_role = next(iter(roles))
            actual_role = package_by_id[selected_ids[0]].get("element_role")
            if actual_role != expected_role:
                errors.append(
                    f"[review_profiles] {profile['id']}: selected-element package {selected_ids[0]!r} is for "
                    f"element role {actual_role!r}, but the profile applies to {expected_role!r} elements"
                )
        for package_id in profile.get("optional_data", []):
            if package_by_id.get(package_id, {}).get("role") == "selected_element":
                errors.append(
                    f"[review_profiles] {profile['id']}: selected-element package {package_id!r} cannot be optional"
                )
        for entry in profile.get("when_absent", []):
            if entry["id"] not in profile.get("required_data", []):
                errors.append(
                    f"[review_profiles] {profile['id']}: when_absent names {entry['id']!r}, which is not required data"
                )
            for guideline_id in entry["unassessable_guideline_ids"]:
                if guideline_id not in profile.get("guideline_ids", []):
                    errors.append(
                        f"[review_profiles] {profile['id']}: when_absent {entry['id']} names guideline "
                        f"{guideline_id!r}, which this profile does not apply"
                    )
        for duplicate_id in _duplicates([entry["id"] for entry in profile.get("when_absent", [])]):
            errors.append(f"[review_profiles] {profile['id']}: duplicate when_absent entry {duplicate_id!r}")

    for precheck in model["prechecks"]:
        selected_ids = [
            package_id
            for package_id in precheck.get("expected_data", [])
            if package_by_id.get(package_id, {}).get("role") == "selected_element"
        ]
        if len(selected_ids) != 1:
            errors.append(
                f"[prechecks] {precheck['id']}: expected_data must name exactly one selected-element package, "
                f"so that the element the check runs on is unambiguous, found {sorted(selected_ids)!r}"
            )

    for guideline in model["guidelines"]:
        guideline_id = guideline["id"]
        tool = guideline.get("tool", {})
        for element in tool.get("applicable_elements", []):
            if element not in selectable_names:
                errors.append(
                    f"[guidelines] {guideline_id}: applicable element {element!r} is not a declared selectable element"
                )
        for duplicate_kind in _duplicates([entry["kind"] for entry in tool.get("markers", [])]):
            errors.append(f"[guidelines] {guideline_id}: duplicate marker kind {duplicate_kind!r}")
        for entry in tool.get("markers", []):
            for duplicate_term in _duplicates(entry["terms"]):
                errors.append(f"[guidelines] {guideline_id}: marker {entry['kind']} repeats term {duplicate_term!r}")
            for term in entry["terms"]:
                if term != term.strip() or term != term.lower():
                    errors.append(
                        f"[guidelines] {guideline_id}: marker term {term!r} must be lower case and trimmed"
                    )
        for entry in tool.get("markers", []):
            # An `expected` list says its terms are what a compliant element
            # looks like, so the guideline's own good example has to contain at
            # least one of them. A list that its own good example fails would
            # make every conforming element a candidate finding.
            if entry["effect"] == "expected" and not _matches_any(entry["terms"], guideline["examples"]["good"]):
                errors.append(
                    f"[guidelines] {guideline_id}: expected marker {entry['kind']} matches nothing in this "
                    "guideline's own good example"
                )
        for duplicate_threshold in _duplicates([entry["id"] for entry in tool.get("thresholds", [])]):
            errors.append(f"[guidelines] {guideline_id}: duplicate threshold id {duplicate_threshold!r}")
        for entry in tool.get("repair", []):
            if entry["action"] == "add_element" and "element_role" not in entry:
                errors.append(
                    f"[guidelines] {guideline_id}: repair action 'add_element' must name the element_role to add"
                )
            if entry.get("element_role") and entry["element_role"] not in selected_by_element_role:
                errors.append(
                    f"[guidelines] {guideline_id}: repair names element role {entry['element_role']!r}, "
                    "which is not a published element role"
                )

    guidance = model["authoring_guidance"]
    core_ids = [entry["id"] for entry in guidance["core_rules"]]
    for duplicate_id in _duplicates(core_ids):
        errors.append(f"[authoring_guidance] duplicate core rule {duplicate_id!r}")
    for core_id in core_ids:
        if core_id not in guideline_ids:
            errors.append(f"[authoring_guidance] core rule {core_id!r} is not a defined guideline")
    represented = {core_id.split(".", 1)[0] for core_id in core_ids}
    for category in model["categories"]:
        if category["id"] not in represented:
            errors.append(
                f"[authoring_guidance] category {category['id']!r} is represented by no core rule; a tool "
                "carrying only this set would never show that family"
            )

    centre = model["review_profile_diagram_layout"]["center"]
    if centre.get("role") != "selected_element":
        errors.append("[diagram_layout] the centre slot must carry role 'selected_element'")
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
    try:
        expected_index = render_index(original_index, model)
    except MarkerError as error:
        errors.append(f"[generated] index.md: {error}")
    else:
        errors.extend(_check_file_current(INDEX, expected_index, "index.md"))
    try:
        tool_doc_outputs = build_tool_doc_outputs(model)
    except ToolDocMarkerError as error:
        errors.append(f"[generated] tool-integration.md: {error}")
    else:
        for path, expected in tool_doc_outputs.items():
            errors.extend(_check_file_current(path, expected, str(path)))
    for path, expected in build_coverage_outputs(model).items():
        errors.extend(_check_file_current(path, expected, str(path)))
    return errors


def main() -> int:
    errors = _validate_schemas()
    if errors:
        sys.stderr.write("Validation FAILED:\n")
        for error in errors:
            sys.stderr.write(f"  - {error}\n")
        sys.stderr.write("\nSchema validation failed; skipped cross-reference and generated-output checks.\n")
        sys.stderr.write(f"\n{len(errors)} error(s).\n")
        return 1
    model = load_content_model()
    errors.extend(_validate_cross_references(model))
    errors.extend(_validate_tool_contract(model))
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
