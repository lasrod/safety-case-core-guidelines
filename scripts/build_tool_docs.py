"""Generate tool integration documentation and review profile diagrams."""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from sccg_common import ROOT, TEMPLATES, load_content_model, write_if_changed


TOOL_PAGE = ROOT / "tool-integration.md"
DIAGRAM_DIR = ROOT / "assets" / "generated" / "review_profile_diagrams"
OVERVIEW_BEGIN = "<!-- BEGIN GENERATED: tool-overview -->"
OVERVIEW_END = "<!-- END GENERATED: tool-overview -->"
PROFILE_BEGIN = "<!-- BEGIN GENERATED: review-profiles -->"
PROFILE_END = "<!-- END GENERATED: review-profiles -->"
PRECHECK_BEGIN = "<!-- BEGIN GENERATED: prechecks -->"
PRECHECK_END = "<!-- END GENERATED: prechecks -->"

KIND_BY_PACKAGE = {
    "SEL": "core",
    "PARENT": "structure",
    "CHILDREN": "structure",
    "STRATEGY": "structure",
    "DIRECT_CONTEXT": "context",
    "INHERITED_CONTEXT": "context",
    "EVIDENCE_ITEM": "evidence",
    "EVIDENCE_PATH": "evidence",
    "EVIDENCE_BASIS": "evidence",
    "PROJECT_GLOSSARY": "knowledge",
    "STANDARD_LINKS": "knowledge",
    "CHANGE_HISTORY": "history",
    "USER_REVIEW_INTENT": "knowledge",
}

KIND_STYLE = {
    "core": {"fill": "#eaf3fb", "stroke": "#1f4e79"},
    "structure": {"fill": "#f4ecf8", "stroke": "#7a3e9d"},
    "context": {"fill": "#edf8ee", "stroke": "#2f7d32"},
    "evidence": {"fill": "#fff4df", "stroke": "#b26a00"},
    "knowledge": {"fill": "#e8f6f7", "stroke": "#006d77"},
    "history": {"fill": "#f8efe6", "stroke": "#7b3f00"},
}

CATEGORY_LABELS = {
    "CL": "Claim guidance",
    "AR": "Argument structure and decomposition guidance",
    "EV": "Evidence guidance",
    "SU": "Sufficiency, uncertainty, and pitfall guidance",
    "LF": "Logical fallacy guidance",
    "RD": "Rhetorical device guidance",
}


class MarkerError(ValueError):
    pass


def _environment() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        undefined=StrictUndefined,
        keep_trailing_newline=False,
        trim_blocks=False,
        lstrip_blocks=False,
    )


def _splice_between_markers(original: str, begin_mark: str, end_mark: str, generated: str) -> str:
    pattern = re.compile(rf"({re.escape(begin_mark)})(.*?)({re.escape(end_mark)})", re.DOTALL)
    if not pattern.search(original):
        raise MarkerError(f"tool-integration.md does not contain generation markers {begin_mark} ... {end_mark}")
    block = f"{begin_mark}\n{generated.rstrip()}\n{end_mark}"
    return pattern.sub(lambda _match: block, original, count=1)


def _tool_assets() -> list[dict[str, str]]:
    return [
        {"path": "dist/sccg.full.json", "description": "Complete normalized SCCG model, including guidelines, review profiles, data packages, and pre-checks."},
        {"path": "dist/review_profiles.json", "description": "Review profile registry for selecting review intent and expected tool context."},
        {"path": "dist/data_packages.json", "description": "Data package registry describing the context a tool may provide to a review workflow."},
        {"path": "dist/data_package_diagram_layout.json", "description": "Fixed diagram layout for review-profile visualizations, with SEL centered and all other package types pinned to stable positions."},
        {"path": "dist/prechecks.json", "description": "Deterministic candidate checks that a tool can run before human or AI judgment."},
        {"path": "dist/sccg.rules.jsonl", "description": "One guideline per JSONL line for retrieval or rule loading."},
        {"path": "dist/ai_rule_export.jsonl", "description": "AI-oriented export with one SCCG guideline per line and tool-facing metadata."},
        {"path": "dist/vectorstore_manifest.json", "description": "Recommended ingestion files and metadata fields for retrieval systems."},
        {"path": "schemas/", "description": "JSON Schema contracts for authored content and exports."},
    ]


def _render_tool_sections(model: dict) -> tuple[str, str, str]:
    template = _environment().get_template("tool_integration.md.j2")
    rendered = template.render(
        assets=_tool_assets(),
        profiles=model["review_profiles"],
        prechecks=model["prechecks"],
    )
    sections = {
        "overview": [],
        "profiles": [],
        "prechecks": [],
    }
    current = None
    for line in rendered.splitlines():
        if line == "## Tool-facing assets":
            current = "overview"
        elif line == "## Review profiles":
            current = "profiles"
            continue
        elif line == "## Deterministic pre-checks":
            current = "prechecks"
            continue
        if current is not None:
            sections[current].append(line)
    return (
        "\n".join(sections["overview"]).strip(),
        "\n".join(sections["profiles"]).strip(),
        "\n".join(sections["prechecks"]).strip(),
    )


def render_tool_integration_page(original: str, model: dict | None = None) -> str:
    if model is None:
        model = load_content_model()
    overview, profiles, prechecks = _render_tool_sections(model)
    updated = _splice_between_markers(original, OVERVIEW_BEGIN, OVERVIEW_END, overview)
    updated = _splice_between_markers(updated, PROFILE_BEGIN, PROFILE_END, profiles)
    return _splice_between_markers(updated, PRECHECK_BEGIN, PRECHECK_END, prechecks)


def _guidelines_by_id(model: dict) -> dict[str, dict]:
    return {guideline["id"]: guideline for guideline in model["guidelines"]}


def _wrap_text(text: str, width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def _node_block(package: dict, x: int, y: int, dashed: bool) -> str:
    package_id = package["id"]
    kind = KIND_BY_PACKAGE.get(package_id, "knowledge")
    style = KIND_STYLE[kind]
    dash = ' stroke-dasharray="8 6"' if dashed else ""
    return (
        f'<rect x="{x}" y="{y}" width="224" height="102" rx="18" fill="{style["fill"]}" '
        f'stroke="{style["stroke"]}" stroke-width="2.5"{dash}/>'
        f'<rect x="{x}" y="{y}" width="224" height="30" rx="18" fill="{style["stroke"]}"/>'
        f'<text x="{x + 112}" y="{y + 21}" text-anchor="middle" font-size="15" font-weight="800" fill="white">{html.escape(package_id)}</text>'
        f'<text x="{x + 112}" y="{y + 58}" text-anchor="middle" font-size="18" font-weight="700" fill="#1c1c1c">{html.escape(package["display_name"])}</text>'
        f'<text x="{x + 112}" y="{y + 90}" text-anchor="middle" font-size="12" font-weight="700" fill="{style["stroke"]}">{html.escape(kind)}</text>'
    )


def _relationship_state(profile: dict) -> dict[str, str]:
    state_by_package_id: dict[str, str] = {}
    for package_id in profile.get("required_data", []):
        if package_id != "SEL":
            state_by_package_id[package_id] = "required"
    for package_id in profile.get("optional_data", []):
        if package_id != "SEL" and package_id not in state_by_package_id:
            state_by_package_id[package_id] = "optional"
    return state_by_package_id


def _status_node_block(package: dict, x: int, y: int, state: str, width: int, height: int) -> str:
    package_id = package["id"]
    kind = KIND_BY_PACKAGE.get(package_id, "knowledge")
    style = KIND_STYLE[kind]
    fill = style["fill"]
    stroke = style["stroke"]
    header_fill = style["stroke"]
    label_fill = style["stroke"]
    header_height = 26
    center_x = x + (width / 2)
    dash = ' stroke-dasharray="8 6"' if state == "optional" else ""
    return (
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="18" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="2.5"{dash}/>'
        f'<rect x="{x}" y="{y}" width="{width}" height="{header_height}" rx="18" fill="{header_fill}"/>'
        f'<text x="{center_x}" y="{y + 19}" text-anchor="middle" font-size="13" font-weight="800" fill="white">{html.escape(package_id)}</text>'
        f'<text x="{center_x}" y="{y + 50}" text-anchor="middle" font-size="15" font-weight="700" fill="#1c1c1c">{html.escape(package["display_name"])}</text>'
        f'<text x="{center_x}" y="{y + 72}" text-anchor="middle" font-size="10" font-weight="700" fill="{label_fill}">{html.escape(kind)}</text>'
    )


def _line(x1: float, y1: float, x2: float, y2: float, dashed: bool) -> str:
    dash = ' stroke-dasharray="10 8"' if dashed else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="#444" stroke-width="2.1"{dash} marker-end="url(#arrow)" opacity="0.92"/>'
    )


def render_review_profile_svg(
    profile: dict,
    package_by_id: dict[str, dict],
    category_order: list[str],
    diagram_layout: dict,
) -> str:
    width = diagram_layout["canvas"]["width"]
    height = diagram_layout["canvas"]["height"]
    center_node = diagram_layout["center"]
    center_x = center_node["x"] + (center_node.get("width", 220) / 2)
    center_y = center_node["y"] + (center_node.get("height", 94) / 2)
    node_width = 166
    node_height = 84
    relationship_state = _relationship_state(profile)
    node_fragments = []
    line_fragments = []
    for position in diagram_layout.get("package_positions", []):
        package_id = position["id"]
        x = position["x"]
        y = position["y"]
        package = package_by_id[package_id]
        state = relationship_state.get(package_id)
        if state is None:
            continue
        node_fragments.append(_status_node_block(package, x, y, state, node_width, node_height))
        line_fragments.append(
            _line(center_x, center_y, x + (node_width / 2), y + (node_height / 2), state == "optional")
        )

    category_groups: dict[str, list[str]] = {}
    for guideline_id in profile.get("guideline_ids", []):
        prefix = guideline_id.split(".", 1)[0]
        category_groups.setdefault(prefix, []).append(guideline_id)

    category_colors = {
        "CL": "#245a9c",
        "AR": "#7a3e9d",
        "EV": "#b26a00",
        "SU": "#2f7d32",
        "LF": "#006d77",
        "RD": "#be4b49",
    }

    category_blocks = []
    cat_y = 384
    for category_id in [prefix for prefix in category_order if prefix in category_groups]:
        guidelines = category_groups[category_id]
        color = category_colors.get(category_id, "#555")
        block = [
            f'<rect x="1060" y="{cat_y}" width="490" height="74" rx="16" fill="#fff" stroke="#e1e5ee"/>',
            f'<rect x="1060" y="{cat_y}" width="86" height="74" rx="16" fill="{color}"/>',
            f'<text x="1103" y="{cat_y + 31}" font-size="22" font-weight="800" fill="white" text-anchor="middle">{category_id}</text>',
            f'<text x="1103" y="{cat_y + 53}" font-size="11" font-weight="700" fill="white" text-anchor="middle">{len(guidelines)} rule{"s" if len(guidelines) != 1 else ""}</text>',
            f'<text x="1162" y="{cat_y + 23}" font-size="15" font-weight="700" fill="#222">{html.escape(CATEGORY_LABELS[category_id])}</text>',
        ]
        chip_x = 1162
        chip_y = cat_y + 38
        for guideline_id in guidelines:
            block.append(f'<rect x="{chip_x}" y="{chip_y}" width="54" height="24" rx="12" fill="#f7f8fb" stroke="{color}"/>')
            block.append(f'<text x="{chip_x + 27}" y="{chip_y + 17}" font-size="12" font-weight="800" fill="{color}" text-anchor="middle">{guideline_id}</text>')
            chip_x += 62
        category_blocks.append("".join(block))
        cat_y += 86

    applicable = profile.get("applies_to", [])
    applicable_blocks = []
    app_y = 160
    for item in applicable[:5]:
        applicable_blocks.append(
            f'<rect x="1060" y="{app_y}" width="230" height="28" rx="14" fill="#f5f7fb" stroke="#d9dfea"/>'
            f'<text x="1074" y="{app_y + 19}" font-size="13" fill="#222">{html.escape(item)}</text>'
        )
        app_y += 36
    if len(applicable) > 5:
        applicable_blocks.append(
            f'<text x="1060" y="{app_y + 16}" font-size="13" fill="#666">+ {len(applicable) - 5} more</text>'
        )

    description_lines = _wrap_text(profile["description"], 98)
    desc_svg = "".join(
        f'<text x="44" y="{119 + (index * 21)}" font-size="16" fill="#333">{html.escape(line)}</text>'
        for index, line in enumerate(description_lines)
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1040" viewBox="0 0 1600 1040">
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#444"/></marker></defs>
<rect width="{width}" height="{height}" fill="#ffffff"/>
<rect x="0" y="0" width="{width}" height="88" fill="#f7f8fb"/>
<text x="44" y="38" font-size="31" font-weight="800" fill="#111">{html.escape(profile['display_name'])}</text>
<text x="44" y="67" font-size="15" fill="#444">SCCG review profile: solid arrows = required data, dashed arrows = optional data</text>
{desc_svg}
<line x1="1030" y1="88" x2="1030" y2="1040" stroke="#dde1e8" stroke-width="2"/>
<rect x="44" y="170" width="952" height="770" rx="24" fill="#fbfcfe" stroke="#e1e5ee"/>
<circle cx="{center_x}" cy="{center_y}" r="282" fill="none" stroke="#edf0f5" stroke-width="2"/>
<circle cx="{center_x}" cy="{center_y}" r="392" fill="none" stroke="#f1f1f1" stroke-width="2" stroke-dasharray="8 10"/>
{''.join(line_fragments)}
<rect x="{center_node['x']}" y="{center_node['y']}" width="{center_node.get('width', 220)}" height="{center_node.get('height', 94)}" rx="18" fill="#eaf3fb" stroke="#1f4e79" stroke-width="2.5"/>
<rect x="{center_node['x']}" y="{center_node['y']}" width="{center_node.get('width', 220)}" height="30" rx="18" fill="#1f4e79"/>
<text x="{center_x}" y="{center_node['y'] + 21}" text-anchor="middle" font-size="15" font-weight="800" fill="white">SEL</text>
<text x="{center_x}" y="{center_node['y'] + 56}" text-anchor="middle" font-size="18" font-weight="700" fill="#1c1c1c">Selected element</text>
<text x="{center_x}" y="{center_node['y'] + 82}" text-anchor="middle" font-size="12" font-weight="700" fill="#1f4e79">core</text>
{''.join(node_fragments)}
<text x="1060" y="130" font-size="21" font-weight="800" fill="#111">Applicable elements</text>
{''.join(applicable_blocks)}
<text x="1060" y="360" font-size="21" font-weight="800" fill="#111">Rules by category</text>
{''.join(category_blocks)}
<text x="1060" y="{cat_y + 10}" font-size="21" font-weight="800" fill="#111">Data contract</text>
<text x="1060" y="{cat_y + 32}" font-size="14" font-weight="800" fill="#222">Required</text>
<text x="1060" y="{cat_y + 54}" font-size="13" fill="#333">{html.escape(', '.join(profile.get('required_data', [])) or 'None')}</text>
<text x="1060" y="{cat_y + 80}" font-size="14" font-weight="800" fill="#222">Optional</text>
<text x="1060" y="{cat_y + 102}" font-size="13" fill="#333">{html.escape(', '.join(profile.get('optional_data', [])) or 'None')}</text>
<text x="1060" y="1005" font-size="11" fill="#777">Generated from canonical SCCG review profile metadata.</text>
</svg>
'''


def render_diagram_index(model: dict) -> str:
    cards = []
    for profile in model["review_profiles"]:
        required_rationale = "".join(
            f"<li><code>{html.escape(item['id'])}</code>: {html.escape(item['rationale'])}</li>"
            for item in profile["data_rationale"]["required"]
        )
        optional_items = profile["data_rationale"]["optional"]
        optional_rationale = "".join(
            f"<li><code>{html.escape(item['id'])}</code>: {html.escape(item['rationale'])}</li>"
            for item in optional_items
        ) or "<li>None.</li>"
        cards.append(
            "<section class=\"card\">"
            f"<h2>{html.escape(profile['display_name'])}</h2>"
            f"<p>{html.escape(profile['description'])}</p>"
            f"<p><b>Required:</b> {html.escape(', '.join(profile.get('required_data', [])) or 'None')}</p>"
            f"<p><b>Optional:</b> {html.escape(', '.join(profile.get('optional_data', [])) or 'None')}</p>"
            f"<p><a href=\"{profile['id']}.svg\">Open SVG diagram</a></p>"
            f"<img src=\"{profile['id']}.svg\" alt=\"{html.escape(profile['display_name'])} diagram\"/>"
            "<h3>Data package rationale</h3>"
            "<h4>Required data</h4>"
            f"<ul>{required_rationale}</ul>"
            "<h4>Optional data</h4>"
            f"<ul>{optional_rationale}</ul>"
            "</section>"
        )
    return (
        "<!doctype html><html><head><meta charset=\"utf-8\"><title>SCCG Review Profile Diagrams</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;margin:32px;background:#f6f7fb;color:#222}.card{background:#fff;border:1px solid #e0e4ee;border-radius:18px;padding:20px;margin:0 0 28px;box-shadow:0 4px 16px rgba(0,0,0,.06)}img{max-width:100%;border:1px solid #e6e8ef;border-radius:12px}h1{margin-bottom:8px}h3{margin:24px 0 8px}h4{margin:16px 0 6px}li{margin:0 0 8px;line-height:1.45}code{background:#f3f5f9;border:1px solid #e1e5ee;border-radius:4px;padding:1px 4px}a{color:#245a9c}</style>"
        "</head><body><h1>SCCG Review Profile Diagrams</h1><p>These diagrams are generated from the canonical review profile and data package metadata.</p>"
        + "".join(cards)
        + "</body></html>"
    )


def build_outputs(model: dict | None = None) -> dict[Path, str]:
    if model is None:
        model = load_content_model()
    package_by_id = {package["id"]: package for package in model["data_packages"]}
    category_order = [entry["prefix"] for entry in model.get("id_scheme", []) if entry.get("prefix")]
    diagram_layout = model["review_profile_diagram_layout"]
    outputs = {
        TOOL_PAGE: render_tool_integration_page(TOOL_PAGE.read_text(encoding="utf-8"), model),
        DIAGRAM_DIR / "index.html": render_diagram_index(model),
    }
    for profile in model["review_profiles"]:
        outputs[DIAGRAM_DIR / f"{profile['id']}.svg"] = render_review_profile_svg(
            profile,
            package_by_id,
            category_order,
            diagram_layout,
        )
    return outputs


def main() -> int:
    changed = []
    for path, text in build_outputs().items():
        if write_if_changed(path, text):
            changed.append(path)
    if changed:
        for path in changed:
            print(f"Updated {path.relative_to(ROOT)}")
    else:
        print("No change to tool integration documentation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())