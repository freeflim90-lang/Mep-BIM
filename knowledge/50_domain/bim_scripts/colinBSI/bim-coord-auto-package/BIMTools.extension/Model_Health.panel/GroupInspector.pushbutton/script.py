"""
GroupInspector — Reports model groups, types, and instance counts.
Columns: RunDate, ModelName, GroupName, Type, InstanceCount, NestedCount
Read-only. No model changes.
"""
import traceback
from collections import defaultdict

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    Group,
    GroupType,
)

from bim_utils import write_csv, today

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "groups_report.csv"
HEADERS = [
    "RunDate", "ModelName", "GroupName", "GroupType",
    "InstanceCount", "NestedGroupCount",
]


def run():
    all_groups = list(FilteredElementCollector(doc).OfClass(Group).ToElements())
    all_types = list(FilteredElementCollector(doc).OfClass(GroupType).ToElements())

    if not all_groups:
        output.print_md("**No groups found in this model.**")
        return

    # Count instances per group type
    type_instance_count = defaultdict(int)
    for grp in all_groups:
        type_instance_count[grp.GroupType.Id.IntegerValue] += 1

    run_date = today()
    model_name = doc.Title
    rows = []
    for gt in all_types:
        # Count nested group types in this group type
        nested = 0
        for member_id in gt.GetMemberIds():
            member = doc.GetElement(member_id)
            if isinstance(member, Group):
                nested += 1

        cat_name = gt.Category.Name if gt.Category else "Unknown"
        rows.append([
            run_date, model_name,
            gt.Name,
            cat_name,
            type_instance_count.get(gt.Id.IntegerValue, 0),
            nested,
        ])

    rows.sort(key=lambda r: -r[4])
    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**Groups report written:** `{}`  \n"
        "{} group type(s), {} instance(s) total.".format(
            path, len(all_types), len(all_groups)
        )
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
