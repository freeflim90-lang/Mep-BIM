"""
ClashStatusManager — Sets Clash_Status parameter on selected elements.
User selects elements, then chooses status from dialog.
Valid values: Open, In Progress, Resolved
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import Transaction, StorageType

from pyrevit import revit, script, forms

doc = revit.doc
uidoc = revit.uidoc
output = script.get_output()

STATUS_OPTIONS = ["Open", "In Progress", "Resolved"]
PARAM_NAME = "Clash_Status"


def run():
    selection = [doc.GetElement(eid) for eid in uidoc.Selection.GetElementIds()]

    if not selection:
        forms.alert(
            "Select one or more elements before running Clash Status Manager.",
            exitscript=True,
        )
        return

    status = forms.SelectFromList.show(
        STATUS_OPTIONS,
        title="Set Clash Status",
        button_name="Apply",
        multiselect=False,
    )

    if not status:
        output.print_md("**Cancelled.**")
        return

    updated = 0
    skipped = 0
    with Transaction(doc, "Set Clash Status") as t:
        t.Start()
        for elem in selection:
            p = elem.LookupParameter(PARAM_NAME)
            if p and p.StorageType == StorageType.String and not p.IsReadOnly:
                p.Set(status)
                updated += 1
            else:
                skipped += 1
        t.Commit()

    output.print_md(
        "**Clash_Status set to '{}'** — {} element(s) updated, {} skipped "
        "(no parameter or read-only).".format(status, updated, skipped)
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
