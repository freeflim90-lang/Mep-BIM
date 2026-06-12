"""
BrowserOrg — Applies project browser organization by Type then Discipline.
Looks for an existing BrowserOrganization containing "Discipline" or "Type".
If none found, prints manual setup instructions.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import BrowserOrganization

from pyrevit import revit, script

doc = revit.doc
output = script.get_output()

PREFERRED_KEYWORDS = ["discipline", "type"]


def run():
    all_orgs = list(BrowserOrganization.GetAllBrowserOrganization(doc))

    # Find best match: prefer org whose name contains a keyword
    match = None
    for keyword in PREFERRED_KEYWORDS:
        for org in all_orgs:
            if keyword in org.Name.lower():
                match = org
                break
        if match:
            break

    if match is None:
        output.print_md("**No matching browser organization found.**")
        output.print_md(
            "To configure manually: View tab → User Interface → "
            "Browser Organization → Views tab → select or create "
            "a Type/Discipline grouping."
        )
        output.print_md(
            "**Available organizations:** {}".format(
                ", ".join(o.Name for o in all_orgs) or "none"
            )
        )
        return

    BrowserOrganization.SetCurrentBrowserOrganizationForViews(doc, match.Id)
    output.print_md(
        "**Applied browser organization:** {}".format(match.Name)
    )


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
