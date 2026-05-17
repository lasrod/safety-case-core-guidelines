"""Generate index.md from the normalized SCCG distribution model."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from build_tool_docs import MarkerError as ToolDocMarkerError, build_outputs as build_tool_doc_outputs
from sccg_common import DIST, INDEX, TEMPLATES, guidelines_by_category, load_content_model, load_json, write_if_changed


BEGIN_MARK = "<!-- BEGIN GENERATED: guidelines -->"
END_MARK = "<!-- END GENERATED: guidelines -->"
Q_BEGIN_MARK = "<!-- BEGIN GENERATED: quick-index -->"
Q_END_MARK = "<!-- END GENERATED: quick-index -->"


class MarkerError(ValueError):
    pass


def _load_model() -> dict:
    full_json = DIST / "sccg.full.json"
    if full_json.exists():
        return load_json(full_json)
    return load_content_model()


def _environment(trim_blocks: bool, lstrip_blocks: bool) -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        undefined=StrictUndefined,
        keep_trailing_newline=False,
        trim_blocks=trim_blocks,
        lstrip_blocks=lstrip_blocks,
    )


def _render_guidelines(model: dict) -> str:
    template = _environment(trim_blocks=True, lstrip_blocks=True).get_template("guidelines_section.md.j2")
    return template.render(categories=model["categories"], by_cat=guidelines_by_category(model))


def _render_quick_index(model: dict) -> str:
    template = _environment(trim_blocks=False, lstrip_blocks=False).get_template("quick_index.md.j2")
    return template.render(categories=model["categories"], by_cat=guidelines_by_category(model))


def _splice_between_markers(original: str, begin_mark: str, end_mark: str, generated: str) -> str:
    pattern = re.compile(rf"({re.escape(begin_mark)})(.*?)({re.escape(end_mark)})", re.DOTALL)
    if not pattern.search(original):
        raise MarkerError(
            "index.md does not contain generation markers. "
            f"Expected: {begin_mark} ... {end_mark}"
        )
    block = f"{begin_mark}\n{generated.rstrip()}\n{end_mark}"
    return pattern.sub(lambda _match: block, original, count=1)


def render_index(original: str, model: dict | None = None) -> str:
    if model is None:
        model = _load_model()
    quick_index = _render_quick_index(model)
    guidelines = _render_guidelines(model)
    updated = _splice_between_markers(original, Q_BEGIN_MARK, Q_END_MARK, quick_index)
    return _splice_between_markers(updated, BEGIN_MARK, END_MARK, guidelines)


def main() -> int:
    model = _load_model()
    original = INDEX.read_text(encoding="utf-8")
    try:
        updated = render_index(original, model)
    except MarkerError as error:
        sys.stderr.write(f"ERROR: {error}\n")
        return 2
    if write_if_changed(INDEX, updated):
        print(f"Updated {INDEX.relative_to(Path(__file__).resolve().parents[1])}")
    else:
        print(f"No change to {INDEX.relative_to(Path(__file__).resolve().parents[1])}")
    try:
        tool_outputs = build_tool_doc_outputs(model)
    except ToolDocMarkerError as error:
        sys.stderr.write(f"ERROR: {error}\n")
        return 2
    for path, text in tool_outputs.items():
        if write_if_changed(path, text):
            print(f"Updated {path.relative_to(Path(__file__).resolve().parents[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())