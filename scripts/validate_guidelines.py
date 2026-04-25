"""Validate data/guidelines.yaml.

Runs JSON Schema validation plus custom invariants:
  * id matches ^[A-Z]{2}\\.\\d+$
  * id uniqueness
  * category prefix matches id
  * number matches numeric suffix of id
  * every references[].source_id exists in reference_sources
  * disallowed legacy keys (typical_fix, fix, notes, note_type) absent
    (also enforced by additionalProperties: false on the guideline object)

Exit code 0 on success, 1 on any failure.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "guidelines.yaml"
SCHEMA = ROOT / "schemas" / "guidelines.schema.json"

ID_RE = re.compile(r"^([A-Z]{2})\.(\d+)$")
DISALLOWED_KEYS = {"typical_fix", "fix", "notes", "note_type"}


def _load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    errors: list[str] = []

    data = _load_yaml(DATA)
    schema = _load_json(SCHEMA)

    validator = Draft7Validator(schema)
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(f"[schema] {loc}: {err.message}")

    sources = {s["id"] for s in data.get("reference_sources", [])}
    categories = {c["id"] for c in data.get("categories", [])}

    seen_ids: set[str] = set()
    for g in data.get("guidelines", []):
        gid = g.get("id", "<missing>")
        m = ID_RE.match(gid or "")
        if not m:
            errors.append(f"[id] {gid}: must match ^[A-Z]{{2}}\\.\\d+$")
            continue
        prefix, num_str = m.group(1), m.group(2)
        num = int(num_str)

        if gid in seen_ids:
            errors.append(f"[id] {gid}: duplicate id")
        seen_ids.add(gid)

        if g.get("category") != prefix:
            errors.append(f"[category] {gid}: category {g.get('category')!r} != id prefix {prefix!r}")
        if prefix not in categories:
            errors.append(f"[category] {gid}: prefix {prefix!r} not in categories")
        if g.get("number") != num:
            errors.append(f"[number] {gid}: number {g.get('number')!r} != id suffix {num}")

        for k in DISALLOWED_KEYS:
            if k in g:
                errors.append(f"[keys] {gid}: disallowed key {k!r}")

        for ref in g.get("references", []) or []:
            sid = ref.get("source_id")
            if sid and sid not in sources:
                errors.append(f"[references] {gid}: source_id {sid!r} not in reference_sources")

        ex = g.get("example") or {}
        if not (ex.get("markdown") or "").strip():
            errors.append(f"[example] {gid}: example.markdown is empty")

    if errors:
        sys.stderr.write("Validation FAILED:\n")
        for e in errors:
            sys.stderr.write(f"  - {e}\n")
        sys.stderr.write(f"\n{len(errors)} error(s).\n")
        return 1

    print(f"OK: {len(data.get('guidelines', []))} guidelines validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
