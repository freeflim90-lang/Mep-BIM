# -*- coding: utf-8 -*-
"""Rule-based QA checker - Smart Views inside Revit."""

import json
import os
import sys

script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from Autodesk.Revit.DB import (
    FilteredElementCollector,
    BuiltInCategory,
    Transaction,
    Element
)
from pyrevit import script, revit

import engine
import overrides

doc = revit.doc
view = doc.ActiveView
output = script.get_output()
output.close_others()

CAT_MAP = {
    "OST_Walls": BuiltInCategory.OST_Walls,
    "OST_Floors": BuiltInCategory.OST_Floors,
    "OST_Doors": BuiltInCategory.OST_Doors,
    "OST_Windows": BuiltInCategory.OST_Windows,
    "OST_Rooms": BuiltInCategory.OST_Rooms,
    "OST_StructuralColumns": BuiltInCategory.OST_StructuralColumns,
    "OST_StructuralFraming": BuiltInCategory.OST_StructuralFraming,
    "OST_StructuralFoundation": BuiltInCategory.OST_StructuralFoundation,
    "OST_GenericModel": BuiltInCategory.OST_GenericModel,
}

rules_path = os.path.join(script_dir, "rules.json")
with open(rules_path, "r") as f:
    rules = json.load(f)

solid_fill_id = overrides.get_solid_fill(doc)

output.print_md("# SmartCheck QA Results")
output.print_md("View: **{}**".format(Element.Name.GetValue(view)))
output.print_md("Rules loaded: **{}**".format(len(rules)))
output.print_md("---")

total_issues = 0
total_checked = 0

with Transaction(doc, "SmartCheck QA") as t:
    t.Start()

    for rule in rules:
        cat_key = rule["category"]
        bic = CAT_MAP.get(cat_key)

        if not bic:
            output.print_md("[SKIP] Unknown category: {}".format(cat_key))
            continue

        elements = FilteredElementCollector(doc)\
            .OfCategory(bic)\
            .WhereElementIsNotElementType()\
            .ToElements()

        if not elements:
            continue

        matches = 0
        match_ids = []

        for el in elements:
            if rule["parameter"] == "Type Name":
                el_type = doc.GetElement(el.GetTypeId())
                param_value = Element.Name.GetValue(el_type) if el_type else ""
            else:
                # Try instance parameter first
                param = el.LookupParameter(rule["parameter"])

                # Fallback: check type parameter
                if param is None or not param.HasValue:
                    el_type = doc.GetElement(el.GetTypeId())
                    if el_type:
                        param = el_type.LookupParameter(rule["parameter"])

                # Read value
                if param and param.HasValue:
                    param_value = param.AsString()
                    if param_value is None:
                        param_value = param.AsValueString() or ""
                else:
                    param_value = ""

            if engine.evaluate(
                param_value,
                rule["condition"],
                rule.get("value")
            ):
                overrides.apply_override(
                    view, el.Id, rule["color"], solid_fill_id
                )
                matches += 1
                match_ids.append(el.Id)

        total_checked += len(elements)
        total_issues += matches

        if matches == 0:
            output.print_md(
                "[PASS] **{}** - all {} elements OK".format(
                    rule["name"], len(elements)
                )
            )
        else:
            output.print_md(
                "[FAIL] **{}** - **{}** of {} elements".format(
                    rule["name"], matches, len(elements)
                )
            )
            if rule.get("description"):
                output.print_md("  _{}_".format(rule["description"]))

            for eid in match_ids[:10]:
                print("  ID: {}".format(output.linkify(eid)))
            if len(match_ids) > 10:
                output.print_md(
                    "  _...and {} more_".format(len(match_ids) - 10)
                )

        output.print_md("")

    t.Commit()

# --- Visual summary bar ---
if total_checked > 0:
    pass_count = total_checked - total_issues
    pass_pct = int(round(100.0 * pass_count / total_checked))
    fail_pct = 100 - pass_pct
else:
    pass_pct = 100
    fail_pct = 0

output.print_md("---")
output.print_md("## Summary")

output.print_html(
    '<div style="width:100%;background:#eee;border-radius:6px;overflow:hidden;'
    'height:28px;margin:8px 0;display:flex;">'
    '<div style="width:{pass_pct}%;background:#4CAF50;height:100%;'
    'display:flex;align-items:center;justify-content:center;'
    'color:white;font-weight:bold;font-size:12px;">'
    '{pass_pct}%</div>'
    '<div style="width:{fail_pct}%;background:#F44336;height:100%;'
    'display:flex;align-items:center;justify-content:center;'
    'color:white;font-weight:bold;font-size:12px;">'
    '{fail_label}</div>'
    '</div>'.format(
        pass_pct=pass_pct,
        fail_pct=fail_pct,
        fail_label="{}%".format(fail_pct) if fail_pct > 5 else ""
    )
)

output.print_html(
    '<div style="display:flex;justify-content:space-between;font-size:12px;'
    'color:#555;margin-bottom:8px;">'
    '<span><strong>{}</strong> elements checked</span>'
    '<span style="color:#4CAF50;"><strong>{}</strong> passed</span>'
    '<span style="color:#F44336;"><strong>{}</strong> issues</span>'
    '</div>'.format(total_checked, total_checked - total_issues, total_issues)
)

if total_issues == 0:
    output.print_md("[PASS] **All checks passed**")
else:
    output.print_md("[!] **{} issues require attention**".format(total_issues))
