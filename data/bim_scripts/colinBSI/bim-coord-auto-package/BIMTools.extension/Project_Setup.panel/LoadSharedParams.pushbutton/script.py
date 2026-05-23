"""
LoadSharedParams — Adds 6 BIM coordination parameters to Project Information.
Idempotent: skips parameters that already exist in the model.

Parameters added (all Text type, Project Information category):
  Clash_Status, Issue_ID, Issue_Status, Coordination_Zone, Discipline, Model_Author

Note: For Revit 2022+ replace ParameterType.Text with
      SpecTypeId.String.Text (ForgeTypeId). The logic is identical.
"""
import os
import tempfile
import traceback
import uuid

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    Transaction,
    BuiltInCategory,
    BuiltInParameterGroup,
    ExternalDefinitionCreationOptions,
)

try:
    # Revit 2021 and earlier
    from Autodesk.Revit.DB import ParameterType
    TEXT_TYPE = ParameterType.Text
    USE_FORGE = False
except ImportError:
    # Revit 2022+
    from Autodesk.Revit.DB import SpecTypeId
    TEXT_TYPE = SpecTypeId.String.Text
    USE_FORGE = True

from pyrevit import revit, script

doc = revit.doc
app = doc.Application
output = script.get_output()

PARAMS = [
    "Clash_Status",
    "Issue_ID",
    "Issue_Status",
    "Coordination_Zone",
    "Discipline",
    "Model_Author",
]
GROUP_NAME = "BIM Coordination"


def build_spf_content():
    lines = [
        "# This is a Revit shared parameter file.",
        "# Do not edit manually.",
        "*META\tVERSION\tMINVERSION",
        "META\t2\t1",
        "*GROUP\tID\tNAME",
        "GROUP\t1\t" + GROUP_NAME,
        "*PARAM\tGUID\tNAME\tDATATYPE\tDATACATEGORY\tGROUP\tVISIBLE\tDESCRIPTION\tUSERMODIFIABLE\tHIDEWHENNOVALUEISASSIGNED",
    ]
    for name in PARAMS:
        guid = str(uuid.uuid4())
        lines.append(
            "PARAM\t{}\t{}\tTEXT\t\t1\t1\t\t1\t0".format(guid, name)
        )
    return "\n".join(lines) + "\n"


def run():
    # Check which params already exist
    existing_params = set()
    it = doc.ParameterBindings.ForwardIterator()
    while it.MoveNext():
        existing_params.add(it.Key.Name)

    needed = [p for p in PARAMS if p not in existing_params]
    if not needed:
        output.print_md("**Done:** All 6 parameters already exist in this model.")
        return

    # Write temp shared parameter file
    tmp_path = tempfile.mktemp(suffix=".txt")
    with open(tmp_path, "w") as f:
        f.write(build_spf_content())

    old_spf = app.SharedParametersFilename
    try:
        app.SharedParametersFilename = tmp_path
        def_file = app.OpenSharedParameterFile()
        param_group = def_file.Groups.get_Item(GROUP_NAME)

        # Build category set for Project Information
        cat = doc.Settings.Categories.get_Item(
            BuiltInCategory.OST_ProjectInformation
        )
        cat_set = app.Create.NewCategorySet()
        cat_set.Insert(cat)
        binding = app.Create.NewInstanceBinding(cat_set)

        with Transaction(doc, "Load Shared Parameters") as t:
            t.Start()
            for ext_def in param_group.Definitions:
                if ext_def.Name not in needed:
                    continue
                doc.ParameterBindings.Insert(
                    ext_def, binding, BuiltInParameterGroup.PG_DATA
                )
            t.Commit()

    finally:
        app.SharedParametersFilename = old_spf
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    output.print_md(
        "**Added {} parameter(s):** {}".format(len(needed), ", ".join(needed))
    )
    skipped = len(PARAMS) - len(needed)
    if skipped:
        output.print_md("**Skipped {} already existing.**".format(skipped))


try:
    run()
except Exception:
    output.print_md("**Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
