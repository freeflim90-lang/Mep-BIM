"""
FindCADImports — Reports all CAD imports in the model.
Columns: RunDate, ModelName, ElementID, Name, Workset, ViewName
Read-only. No model changes.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import ImportInstance, WorksetKind, FilteredWorksetCollector

from bim_utils import write_csv, today, get_import_instances

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

FILENAME = "cad_imports_report.csv"
HEADERS = ["RunDate", "ModelName", "ElementID", "Name", "Workset", "ViewName"]


def get_workset_name(elem):
    if not doc.IsWorkshared:
        return "N/A"
    ws_param = elem.get_Parameter(
        __import__("Autodesk.Revit.DB", fromlist=["BuiltInParameter"]).BuiltInParameter.ELEM_PARTITION_PARAM
    )
    if ws_param:
        ws_id = ws_param.AsElementId()
        ws = doc.GetWorksetTable().GetWorkset(ws_id)
        return ws.Name if ws else "Unknown"
    return "Unknown"


def get_view_name(elem):
    view_id = elem.OwnerViewId
    if view_id and view_id.IntegerValue != -1:
        view = doc.GetElement(view_id)
        return view.Name if view else "Unknown"
    return "Model (not view-specific)"


def run():
    imports = get_import_instances(doc)
    if not imports:
        output.print_md("**No CAD imports found in this model.**")
        return

    run_date = today()
    model_name = doc.Title
    rows = []
    for imp in imports:
        rows.append([
            run_date,
            model_name,
            imp.Id.IntegerValue,
            imp.Category.Name if imp.Category else "Unknown",
            get_workset_name(imp),
            get_view_name(imp),
        ])

    path = write_csv(FILENAME, HEADERS, rows)
    output.print_md(
        "**CAD imports report written:** `{}`  \n"
        "{} import(s) found.".format(path, len(imports))
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
