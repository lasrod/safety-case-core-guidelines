"""Shared helpers for SCCG content loading and deterministic generation."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
GUIDELINES_DIR = CONTENT / "guidelines"
TOOL_SUPPORT_DIR = CONTENT / "tool_support"
SCHEMAS = ROOT / "schemas"
DIST = ROOT / "dist"
GENERATED = ROOT / "generated"
TEMPLATES = ROOT / "templates"
INDEX = ROOT / "index.md"

LEGACY_GUIDELINE_KEYS = {"guideline", "why", "example", "tool_guidance"}
ID_RE = re.compile(r"^([A-Z]{2})\.(\d+)$")


def load_yaml(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def json_text(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def jsonl_text(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)


def yaml_text(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=1000)


def write_if_changed(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def category_order_from_id_scheme(id_scheme: list[dict[str, Any]] | None) -> list[str]:
    if not id_scheme:
        return []
    return [entry["prefix"] for entry in id_scheme if isinstance(entry, dict) and entry.get("prefix")]


def category_sort_key(category_id: str, category_order: list[str]) -> tuple[int, str]:
    try:
        return (category_order.index(category_id), "")
    except ValueError:
        return (len(category_order), category_id)


def guideline_sort_key(guideline: dict[str, Any], category_order: list[str]) -> tuple[int, int, str]:
    guideline_id = guideline.get("id", "")
    match = ID_RE.match(guideline_id)
    if not match:
        return (len(category_order), 0, guideline_id)
    category_id, suffix = match.groups()
    return (category_sort_key(category_id, category_order)[0], int(suffix), guideline_id)


def slugify_anchor(text: str) -> str:
    text = text.lower().replace("_", " ")
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text).strip("-")


def format_references(refs: list[dict[str, Any]], source_names: dict[str, str]) -> str:
    parts: list[str] = []
    for ref in refs:
        source_id = ref.get("source_id", "")
        base = ref.get("display_name") or source_names.get(source_id) or source_id
        clauses = ref.get("clauses") or []
        if clauses:
            parts.append(f"{base} {'; '.join(clauses)}")
        else:
            parts.append(base)
    return ", ".join(parts)


def load_content_model() -> dict[str, Any]:
    sccg = load_yaml(CONTENT / "sccg.yaml")
    references = load_yaml(CONTENT / "references.yaml")
    review_profiles = load_yaml(TOOL_SUPPORT_DIR / "review_profiles.yaml")
    data_packages = load_yaml(TOOL_SUPPORT_DIR / "data_packages.yaml")
    data_package_diagram_layout = load_yaml(TOOL_SUPPORT_DIR / "data_package_diagram_layout.yaml")
    prechecks = load_yaml(TOOL_SUPPORT_DIR / "prechecks.yaml")
    category_order = category_order_from_id_scheme(sccg.get("id_scheme"))

    categories: list[dict[str, Any]] = []
    guidelines: list[dict[str, Any]] = []
    category_files: dict[str, str] = {}
    for path in sorted(GUIDELINES_DIR.glob("*.yaml")):
        category_document = load_yaml(path)
        category = category_document["category"]
        category_id = category["id"]
        category_files[category_id] = path.name
        categories.append(category)
        guidelines.extend(category_document.get("guidelines", []))

    categories.sort(key=lambda category: category_sort_key(category["id"], category_order))
    guidelines.sort(key=lambda guideline: guideline_sort_key(guideline, category_order))

    return {
        "schema_version": sccg["schema_version"],
        "sccg_version": sccg["sccg_version"],
        "document": sccg["document"],
        "source_policy": sccg["source_policy"],
        "method_application_guidance": sccg["method_application_guidance"],
        "id_scheme": sccg["id_scheme"],
        "required_guideline_sections": sccg["required_guideline_sections"],
        "reference_sources": references["reference_sources"],
        "categories": categories,
        "guidelines": guidelines,
        "review_profiles": review_profiles["review_profiles"],
        "selectable_elements": review_profiles["selectable_elements"],
        "data_packages": data_packages["data_packages"],
        "review_profile_diagram_layout": data_package_diagram_layout["review_profile_diagram_layout"],
        "prechecks": prechecks["prechecks"],
        "_category_files": category_files,
    }


def public_model(model: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in model.items() if not key.startswith("_")}


def guidelines_by_category(model: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    by_category = {category["id"]: [] for category in model["categories"]}
    source_names = {
        source["id"]: source["display_name"] for source in model["reference_sources"]
    }
    for guideline in model["guidelines"]:
        item = dict(guideline)
        item["anchor"] = slugify_anchor(guideline["id"])
        item["references_display"] = format_references(guideline.get("references", []), source_names)
        by_category.setdefault(guideline["category"], []).append(item)
    return by_category