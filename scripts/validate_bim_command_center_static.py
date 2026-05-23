#!/usr/bin/env python3
"""Static validation for BIM Command Center source changes that do not require Revit."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADDIN = ROOT / "260519 소스 폴더" / "01_Revit_Addins" / "Addin Dashboard"
COMMANDS_JSON = ADDIN / "commands.json"
COMMERCIAL = ADDIN / "CommercialFeatures"
CONFIGS = COMMERCIAL / "Configs"
CSPROJ = ADDIN / "BIMCommandCenter.csproj"


EXPECTED_CONFIGS = [
    "settings_profile_sample.json",
    "view_template_copy_rules.json",
    "type_batch_definitions.json",
    "tag_text_aligner_rules.json",
    "project_cleanup_rules.json",
    "schedule_excel_export_rules.json",
]

EXPECTED_CLASSES = [
    "BIMCommandCenter.CommercialFeatures.Commands.SettingsProfileCommand",
    "BIMCommandCenter.CommercialFeatures.Commands.ViewTemplateCopierCommand",
    "BIMCommandCenter.CommercialFeatures.Commands.TypeBatchDefinerCommand",
    "BIMCommandCenter.CommercialFeatures.Commands.TagTextAlignerCommand",
    "BIMCommandCenter.CommercialFeatures.Commands.ProjectCleanupLiteCommand",
    "BIMCommandCenter.CommercialFeatures.Commands.ScheduleExcelExportCommand",
]


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    if not COMMANDS_JSON.exists():
        errors.append(f"missing: {COMMANDS_JSON.relative_to(ROOT)}")
        commands = {}
    else:
        commands = load_json(COMMANDS_JSON)

    if CSPROJ.exists():
        try:
            ET.parse(CSPROJ)
        except ET.ParseError as exc:
            errors.append(f"{CSPROJ.relative_to(ROOT)}: invalid XML: {exc}")
    else:
        errors.append(f"missing: {CSPROJ.relative_to(ROOT)}")

    for config in EXPECTED_CONFIGS:
        path = CONFIGS / config
        if not path.exists():
            errors.append(f"missing config: {path.relative_to(ROOT)}")
            continue
        try:
            data = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        if not data.get("feature"):
            errors.append(f"{path.relative_to(ROOT)}: missing feature")
        if not isinstance(data.get("version"), int):
            errors.append(f"{path.relative_to(ROOT)}: version must be an integer")

    command_items: list[dict] = []
    for category in commands.get("categories", []):
        command_items.extend(category.get("commands", []))

    registered_classes = {item.get("className") for item in command_items}
    for class_name in EXPECTED_CLASSES:
        if class_name not in registered_classes:
            errors.append(f"commands.json missing className: {class_name}")

        simple_name = class_name.split(".")[-1]
        matching_sources = list(COMMERCIAL.rglob(f"{simple_name}.cs"))
        if not matching_sources:
            errors.append(f"missing source file for class: {class_name}")
            continue
        source = matching_sources[0].read_text(encoding="utf-8")
        if f"class {simple_name}" not in source:
            errors.append(f"{matching_sources[0].relative_to(ROOT)}: class declaration not found")

    if errors:
        print("BIM Command Center static validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("BIM Command Center static validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
