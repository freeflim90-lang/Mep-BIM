"""
InterferenceCheck — Runs Revit's built-in interference check via PostCommand.
Opens the native Revit Interference Check dialog.
"""
import traceback

import clr
clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import PostableCommand, RevitCommandId

from pyrevit import revit, script

uidoc = revit.uidoc
output = script.get_output()


def run():
    cmd_id = RevitCommandId.LookupPostableCommandId(PostableCommand.InterferenceCheck)
    uidoc.Application.PostCommand(cmd_id)
    output.print_md(
        "**Interference Check launched.** "
        "Select categories in the dialog, then click OK."
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
