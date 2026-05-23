"""
ZoneChecker — Lists elements missing a Coordination_Zone value.
Columns: RunDate, ModelName, ElementID, Category, Level, Workset
Outputs zone_check_report.csv. Read-only.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    StorageType,
    BuiltInParameter,
    BuiltInCategory,
)

from bim_utils import write_csv, today

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "zone_check_report.csv"
HEADERS = ["RunDate", "ModelName", "ElementID", "Category", "Level", "Workset"]

# Categories to check — skip annotation and view elements
SKIP_CATEGORIES = {
    int(BuiltInCategory.OST_Cameras),
    int(BuiltInCategory.OST_Views),
    int(BuiltInCategory.OST_Sheets),
    int(BuiltInCategory.OST_DetailComponents),
    int(BuiltInCategory.OST_TextNotes),
    int(BuiltInCategory.OST_Dimensions),
    int(BuiltInCategory.OST_GenericAnnotation),
}


def get_param_str(elem, bip):
    p = elem.get_Parameter(bip)
    if p:
        return p.AsString() or p.AsValueString() or ""
    return ""


def get_workset_name(elem):
    if not doc.IsWorkshared:
        return "N/A"
    ws_param = elem.get_Parameter(BuiltInParameter.ELEM_PARTITION_PARAM)
    if ws_param:
        ws_id = ws_param.AsElementId()
        ws = doc.GetWorksetTable().GetWorkset(ws_id)
        return ws.Name if ws else "Unknown"
    return "Unknown"


def run():
    all_elems = list(
        FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()
    )

    missing = []
    for elem in all_elems:
        try:
            cat = elem.Category
            if cat is None:
                continue
            if int(cat.Id.IntegerValue) in SKIP_CATEGORIES:
                continue
            p = elem.LookupParameter("Coordination_Zone")
            if p is None:
                continue
            val = p.AsString() if p.StorageType == StorageType.String else None
            if val:
                continue  # has a value — OK
            level = get_param_str(elem, BuiltInParameter.FAMILY_LEVEL_PARAM)
            if not level:
                level = get_param_str(elem, BuiltInParameter.SCHEDULE_LEVEL_PARAM)
            missing.append([
                today(), doc.Title,
                elem.Id.IntegerValue,
                cat.Name,
                level,
                get_workset_name(elem),
            ])
        except Exception:
            pass

    if not missing:
        output.print_md("**All elements have a Coordination_Zone value.**")
        return

    path = write_csv(FILENAME, HEADERS, missing)
    output.print_md(
        "**Zone check report written:** `{}`  \n"
        "{} element(s) missing Coordination_Zone.".format(path, len(missing))
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
