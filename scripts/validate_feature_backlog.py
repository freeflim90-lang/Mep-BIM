#!/usr/bin/env python3
"""Validate commercial feature backlog docs and JSON config files."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "commercial_addins" / "BIM_Command_Center_For_Revit" / "08_feature_backlog"
CONFIG_DIR = BACKLOG / "phase1_configs"
SPEC_DIR = BACKLOG / "feature_specs"


def require_path(path: Path) -> list[str]:
    if path.exists():
        return []
    return [f"missing: {path.relative_to(ROOT)}"]


def validate_json_config(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.relative_to(ROOT)}: invalid JSON: {exc}"]

    for key in ("feature", "version"):
        if key not in data:
            errors.append(f"{path.relative_to(ROOT)}: missing key `{key}`")

    if not isinstance(data.get("version"), int):
        errors.append(f"{path.relative_to(ROOT)}: `version` must be an integer")

    return errors


def main() -> int:
    errors: list[str] = []
    errors.extend(require_path(BACKLOG / "BIMIZE_FEATURE_INTERNALIZATION.md"))
    errors.extend(require_path(BACKLOG / "PHASE1_SIMPLE_FEATURES.md"))

    expected_specs = [
        "01_Line_Cleanup_Lite.md",
        "02_Smart_Selector_Lite.md",
        "03_Workset_Inspector_Lite.md",
        "04_Link_Health_And_Reload.md",
        "05_Batch_Print_Assistant.md",
        "06_Sheet_View_Duplicator.md",
        "07_Schedule_Excel_Sync.md",
        "08_Settings_Profile_Manager.md",
        "09_View_Template_Copier.md",
        "10_Type_Batch_Definer.md",
        "11_Tag_Text_Aligner.md",
        "12_Project_Cleanup_Lite.md",
        "13_Schedule_Excel_Export.md",
    ]
    for spec in expected_specs:
        errors.extend(require_path(SPEC_DIR / spec))

    for config in sorted(CONFIG_DIR.glob("*.json")):
        errors.extend(validate_json_config(config))

    if errors:
        print("Feature backlog validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Feature backlog validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
