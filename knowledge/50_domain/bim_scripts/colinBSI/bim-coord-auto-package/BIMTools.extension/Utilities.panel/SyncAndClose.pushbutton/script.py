"""
SyncAndClose — Syncs with central, relinquishes all, closes document.
Requires confirmation. Only works on workshared models.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    TransactWithCentralOptions,
    SynchronizeWithCentralOptions,
    RelinquishOptions,
    WorksharingUtils,
)

from pyrevit import revit, script, forms

doc = revit.doc
uidoc = revit.uidoc
output = script.get_output()


def run():
    if not doc.IsWorkshared:
        forms.alert(
            "This model is not workshared. Sync and Close is only available "
            "for workshared (central) models.",
            exitscript=True,
        )
        return

    if not forms.alert(
        "Sync with central, relinquish all worksets, and close '{}'. "
        "This cannot be undone. Proceed?".format(doc.Title),
        yes=True,
        no=True,
    ):
        output.print_md("**Cancelled.**")
        return

    output.print_md("Syncing with central...")

    # Relinquish options
    relinquish_opts = RelinquishOptions(True)
    relinquish_opts.CheckedOutElements = True
    relinquish_opts.UserWorksets = True
    relinquish_opts.FamilyWorksets = True
    relinquish_opts.ViewWorksets = True
    relinquish_opts.StandardWorksets = True

    # Sync options
    sync_opts = SynchronizeWithCentralOptions()
    sync_opts.SetRelinquishOptions(relinquish_opts)
    sync_opts.Comment = "Sync and close via BIMTools"
    sync_opts.Compact = False

    twc_opts = TransactWithCentralOptions()

    doc.SynchronizeWithCentral(twc_opts, sync_opts)
    output.print_md("**Sync complete.** Closing document...")

    uidoc.Application.OpenAndActivateDocument(
        doc.PathName
    )  # re-activate to ensure close works
    doc.Close(False)  # False = do not save (already synced)


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
