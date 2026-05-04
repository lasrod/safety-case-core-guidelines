"""Generate SCCG review profile, data package, and rule coverage reports."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from sccg_common import GENERATED, load_content_model, write_if_changed


def _bullet(items: list[str]) -> str:
    if not items:
        return "- None\n"
    return "".join(f"- {item}\n" for item in items)


def _warning(items: list[str], label: str) -> str:
    if not items:
        return f"No {label}.\n"
    return "\n".join(f"> WARNING: {item}" for item in items) + "\n"


def _profile_coverage(model: dict[str, Any]) -> str:
    usage: dict[str, list[str]] = defaultdict(list)
    guideline_ids = [guideline["id"] for guideline in model["guidelines"]]
    for profile in model["review_profiles"]:
        for guideline_id in profile.get("guideline_ids", []):
            usage[guideline_id].append(profile["id"])
    unmapped = [guideline_id for guideline_id in guideline_ids if not usage[guideline_id]]
    lines = ["# Review Profile Coverage", "", "## Guidelines by review profile", ""]
    for profile in model["review_profiles"]:
        lines.append(f"### {profile['display_name']} (`{profile['id']}`)")
        lines.append("")
        lines.append(_bullet(profile.get("guideline_ids", [])).rstrip())
        lines.append("")
    lines.extend(["## Review profiles by guideline", ""])
    for guideline_id in guideline_ids:
        lines.append(f"### {guideline_id}")
        lines.append("")
        lines.append(_bullet(usage[guideline_id]).rstrip())
        lines.append("")
    lines.extend(["## Guidelines not mapped to any review profile", "", _warning(unmapped, "unmapped guidelines")])
    return "\n".join(lines).rstrip() + "\n"


def _data_package_coverage(model: dict[str, Any]) -> str:
    usage: dict[str, list[str]] = defaultdict(list)
    data_package_ids = [package["id"] for package in model["data_packages"]]
    for profile in model["review_profiles"]:
        for package_id in profile.get("required_data", []) + profile.get("optional_data", []):
            usage[package_id].append(profile["id"])
    unused = [package_id for package_id in data_package_ids if not usage[package_id]]
    lines = ["# Data Package Coverage", "", "## Data packages by review profile", ""]
    for profile in model["review_profiles"]:
        lines.append(f"### {profile['display_name']} (`{profile['id']}`)")
        lines.append("")
        lines.append("Required data:")
        lines.append(_bullet(profile.get("required_data", [])).rstrip())
        lines.append("")
        lines.append("Optional data:")
        lines.append(_bullet(profile.get("optional_data", [])).rstrip())
        lines.append("")
    lines.extend(["## Review profiles by data package", ""])
    for package_id in data_package_ids:
        lines.append(f"### {package_id}")
        lines.append("")
        lines.append(_bullet(usage[package_id]).rstrip())
        lines.append("")
    lines.extend(["## Data packages not used by any review profile", "", _warning(unused, "unused data packages")])
    return "\n".join(lines).rstrip() + "\n"


def _rule_coverage(model: dict[str, Any]) -> str:
    precheck_usage: dict[str, list[str]] = defaultdict(list)
    tool_check_ids: set[str] = set()
    guideline_ids = [guideline["id"] for guideline in model["guidelines"]]
    for guideline in model["guidelines"]:
        for check in guideline.get("tool", {}).get("suggested_checks", []):
            tool_check_ids.add(check["id"])
    for precheck in model["prechecks"]:
        for guideline_id in precheck.get("related_guideline_ids", []):
            precheck_usage[guideline_id].append(precheck["id"])
    unreferenced_prechecks = [
        precheck["id"] for precheck in model["prechecks"] if precheck["id"] not in tool_check_ids
    ]
    lines = ["# Rule Coverage", "", "## Pre-checks by guideline", ""]
    for guideline_id in guideline_ids:
        lines.append(f"### {guideline_id}")
        lines.append("")
        lines.append(_bullet(precheck_usage[guideline_id]).rstrip())
        lines.append("")
    lines.extend(["## Related guidelines by pre-check", ""])
    for precheck in model["prechecks"]:
        lines.append(f"### {precheck['display_name']} (`{precheck['id']}`)")
        lines.append("")
        lines.append(_bullet(precheck.get("related_guideline_ids", [])).rstrip())
        lines.append("")
    lines.extend([
        "## Pre-checks not referenced by guideline tool metadata",
        "",
        _warning(unreferenced_prechecks, "unreferenced pre-checks"),
    ])
    return "\n".join(lines).rstrip() + "\n"


def build_outputs(model: dict[str, Any] | None = None) -> dict[Path, str]:
    if model is None:
        model = load_content_model()
    return {
        GENERATED / "review_profile_coverage.md": _profile_coverage(model),
        GENERATED / "data_package_coverage.md": _data_package_coverage(model),
        GENERATED / "rule_coverage.md": _rule_coverage(model),
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
        print("No change to coverage outputs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())