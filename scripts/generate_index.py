"""Generate the guideline sections of index.md from data/guidelines.yaml.

Replaces the content between
    <!-- BEGIN GENERATED: guidelines -->
    <!-- END GENERATED: guidelines -->
and also generates/splices the Quick index between
    <!-- BEGIN GENERATED: quick-index -->
    <!-- END GENERATED: quick-index -->
in index.md. The surrounding preamble/content remains hand-edited and preserved.

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
Q_BEGIN_MARK = "<!-- BEGIN GENERATED: quick-index -->"
Q_END_MARK = "<!-- END GENERATED: quick-index -->"


def _load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _slugify_anchor(text: str) -> str:
    text = text.lower().replace("_", " ")
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text).strip("-")


def _prepare(data: dict) -> tuple[list[dict], dict[str, list[dict]]]:
    categories = sorted(data.get("categories", []), key=lambda c: c["order"])
    guidelines = data.get("guidelines", [])
    by_cat: dict[str, list[dict]] = {c["id"]: [] for c in categories}
    for g in guidelines:
        item = dict(g)
        item["anchor"] = _slugify_anchor(f"{g['id']} {g['title']}")
        by_cat.setdefault(g["category"], []).append(item)
    for cid in by_cat:
        by_cat[cid].sort(key=lambda g: g["order"])
    return categories, by_cat


def _render_guidelines(categories: list[dict], by_cat: dict[str, list[dict]]) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        undefined=StrictUndefined,
        keep_trailing_newline=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tmpl = env.get_template("guidelines_section.md.j2")

    return tmpl.render(categories=categories, by_cat=by_cat)


def _render_quick_index(categories: list[dict], by_cat: dict[str, list[dict]]) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        undefined=StrictUndefined,
        keep_trailing_newline=False,
        trim_blocks=False,
        lstrip_blocks=False,
    )
    tmpl = env.get_template("quick_index.md.j2")

    return tmpl.render(categories=categories, by_cat=by_cat)



def _splice_between_markers(original: str, begin_mark: str, end_mark: str, generated: str) -> str:
    pattern = re.compile(
        rf"({re.escape(begin_mark)})(.*?)({re.escape(end_mark)})",
        re.DOTALL,
    )
    if not pattern.search(original):
        sys.stderr.write(
            "ERROR: index.md does not contain generation markers.\n"
            f"  Expected: {begin_mark} ... {end_mark}\n"
        )
        sys.exit(2)
    block = f"{begin_mark}\n{generated.rstrip()}\n{end_mark}"
    return pattern.sub(lambda _m: block, original, count=1)


def _splice_quick_index(original: str, generated: str) -> str:
    # Preferred mode: update the explicit quick-index generated block.
    if Q_BEGIN_MARK in original and Q_END_MARK in original:
        return _splice_between_markers(original, Q_BEGIN_MARK, Q_END_MARK, generated)

    # Migration mode: replace legacy hand-maintained "## Quick index" section
    # up to the guidelines generated block, then add quick-index markers.
    quick_header = "## Quick index"
    quick_start = original.find(quick_header)
    guidelines_start = original.find(BEGIN_MARK)
    if quick_start == -1 or guidelines_start == -1 or quick_start > guidelines_start:
        sys.stderr.write(
            "ERROR: index.md does not contain a migratable quick index section.\n"
            f"  Expected either markers {Q_BEGIN_MARK} ... {Q_END_MARK},\n"
            f"  or a '{quick_header}' section before {BEGIN_MARK}.\n"
        )
        sys.exit(2)

    block = f"{Q_BEGIN_MARK}\n{generated.rstrip()}\n{Q_END_MARK}\n\n"
    return f"{original[:quick_start]}{block}{original[guidelines_start:]}"


def main() -> int:
    data = _load_yaml(DATA)
    categories, by_cat = _prepare(data)
    quick_index = _render_quick_index(categories, by_cat)
    guidelines = _render_guidelines(categories, by_cat)
    original = INDEX.read_text(encoding="utf-8")
    updated = _splice_quick_index(original, quick_index)
    updated = _splice_between_markers(updated, BEGIN_MARK, END_MARK, guidelines)
    if updated != original:
        INDEX.write_text(updated, encoding="utf-8")
        print(f"Updated {INDEX.relative_to(ROOT)}")
    else:
        print(f"No change to {INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
