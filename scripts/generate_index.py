"""Generate the per-guideline section of index.md from data/guidelines.yaml.

Replaces the content between
    <!-- BEGIN GENERATED: guidelines -->
    <!-- END GENERATED: guidelines -->
in index.md. Preamble (Purpose ... Quick index) is hand-edited and preserved.

Output is deterministic. Run repeatedly without spurious diffs.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "guidelines.yaml"
TEMPLATES = ROOT / "templates"
INDEX = ROOT / "index.md"

BEGIN_MARK = "<!-- BEGIN GENERATED: guidelines -->"
END_MARK = "<!-- END GENERATED: guidelines -->"


def _load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _render(data: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        undefined=StrictUndefined,
        keep_trailing_newline=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tmpl = env.get_template("guidelines_section.md.j2")

    categories = sorted(data.get("categories", []), key=lambda c: c["order"])
    guidelines = data.get("guidelines", [])
    by_cat: dict[str, list[dict]] = {c["id"]: [] for c in categories}
    for g in guidelines:
        by_cat.setdefault(g["category"], []).append(g)
    for cid in by_cat:
        by_cat[cid].sort(key=lambda g: g["order"])

    return tmpl.render(categories=categories, by_cat=by_cat)


def _splice(original: str, generated: str) -> str:
    pattern = re.compile(
        rf"({re.escape(BEGIN_MARK)})(.*?)({re.escape(END_MARK)})",
        re.DOTALL,
    )
    if not pattern.search(original):
        sys.stderr.write(
            "ERROR: index.md does not contain generation markers.\n"
            f"  Expected: {BEGIN_MARK} ... {END_MARK}\n"
        )
        sys.exit(2)
    block = f"{BEGIN_MARK}\n{generated.rstrip()}\n{END_MARK}"
    return pattern.sub(lambda _m: block, original, count=1)


def main() -> int:
    data = _load_yaml(DATA)
    generated = _render(data)
    original = INDEX.read_text(encoding="utf-8")
    updated = _splice(original, generated)
    if updated != original:
        INDEX.write_text(updated, encoding="utf-8")
        print(f"Updated {INDEX.relative_to(ROOT)}")
    else:
        print(f"No change to {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
