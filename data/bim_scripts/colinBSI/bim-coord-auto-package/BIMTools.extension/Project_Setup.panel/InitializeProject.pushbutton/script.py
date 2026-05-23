"""
InitializeProject — Runs all 5 Project Setup tools in sequence.
Requires confirmation before proceeding.
"""
import traceback

import clr
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import (
    Transaction,
    WorksetKind,
    FilteredWorksetCollector,
    ViewFamilyType,
    ViewFamily,
    View3D,
    View,
    FilteredElementCollector,
    FamilySymbol,
    BuiltInCategory,
    ViewSheet,
    ElementId,
    BrowserOrganization,
)

try:
    from Autodesk.Revit.DB import ParameterType
    TEXT_TYPE = ParameterType.Text
except ImportError:
    from Autodesk.Revit.DB import SpecTypeId
    TEXT_TYPE = SpecTypeId.String.Text

from Autodesk.Revit.DB import (
    ExternalDefinitionCreationOptions,
    BuiltInParameterGroup,
)

import os
import tempfile
import uuid

from pyrevit import revit, script, forms

doc = revit.doc
app = doc.Application
output = script.get_output()

# ---- Constants (mirrored from individual scripts) ----
STANDARD_WORKSETS = [
    "Shared Levels & Grids", "Arch", "Structure", "Mechanical",
    "Electrical", "Plumbing", "Civil", "Plant", "Links",
    "Coordination", "Scan",
]

PARAMS = [
    "Clash_Status", "Issue_ID", "Issue_Status",
    "Coordination_Zone", "Discipline", "Model_Author",
]
PARAM_GROUP_NAME = "BIM Coordination"

STANDARD_VIEWS = [
    "3D - Coordination", "3D - Navisworks", "3D - Clash Review",
    "3D - Worksets", "3D - Linked Models", "3D - QAQC",
    "3D - Scan Reference",
]

STANDARD_SHEETS = [
    ("G000", "Cover"), ("G001", "General Notes"),
    ("G100", "Level Plans"), ("G200", "Sections"),
    ("G300", "Coordination"),
]


# ---- Step functions ----

def step_worksets():
    if not doc.IsWorkshared:
        return "SKIP (model not workshared)"
    existing = {
        ws.Name
        for ws in FilteredWorksetCollector(doc)
        .OfKind(WorksetKind.UserWorkset).ToWorksets()
    }
    to_create = [n for n in STANDARD_WORKSETS if n not in existing]
    if not to_create:
        return "already exist"
    from Autodesk.Revit.DB import Workset as WS
    with Transaction(doc, "Create Worksets") as t:
        t.Start()
        for name in to_create:
            WS.Create(doc, name)
        t.Commit()
    return "created {}".format(len(to_create))


def step_shared_params():
    existing_params = set()
    it = doc.ParameterBindings.ForwardIterator()
    while it.MoveNext():
        existing_params.add(it.Key.Name)
    needed = [p for p in PARAMS if p not in existing_params]
    if not needed:
        return "already exist"

    lines = [
        "# This is a Revit shared parameter file.",
        "# Do not edit manually.",
        "*META\tVERSION\tMINVERSION",
        "META\t2\t1",
        "*GROUP\tID\tNAME",
        "GROUP\t1\t" + PARAM_GROUP_NAME,
        "*PARAM\tGUID\tNAME\tDATATYPE\tDATACATEGORY\tGROUP\tVISIBLE\tDESCRIPTION\tUSERMODIFIABLE\tHIDEWHENNOVALUEISASSIGNED",
    ]
    for name in PARAMS:
        lines.append("PARAM\t{}\t{}\tTEXT\t\t1\t1\t\t1\t0".format(str(uuid.uuid4()), name))
    spf_content = "\n".join(lines) + "\n"

    tmp_path = tempfile.mktemp(suffix=".txt")
    with open(tmp_path, "w") as f:
        f.write(spf_content)
    old_spf = app.SharedParametersFilename
    try:
        app.SharedParametersFilename = tmp_path
        def_file = app.OpenSharedParameterFile()
        pg = def_file.Groups.get_Item(PARAM_GROUP_NAME)
        cat = doc.Settings.Categories.get_Item(BuiltInCategory.OST_ProjectInformation)
        cat_set = app.Create.NewCategorySet()
        cat_set.Insert(cat)
        binding = app.Create.NewInstanceBinding(cat_set)
        with Transaction(doc, "Load Shared Parameters") as t:
            t.Start()
            for ext_def in pg.Definitions:
                if ext_def.Name in needed:
                    doc.ParameterBindings.Insert(ext_def, binding, BuiltInParameterGroup.PG_DATA)
            t.Commit()
    finally:
        app.SharedParametersFilename = old_spf
        try:
            os.remove(tmp_path)
        except OSError:
            pass
    return "added {}".format(len(needed))


def step_views():
    vft = None
    for v in FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements():
        if v.ViewFamily == ViewFamily.ThreeDimensional:
            vft = v
            break
    if vft is None:
        return "SKIP (no 3D ViewFamilyType)"
    existing = {
        v.Name
        for v in FilteredElementCollector(doc).OfClass(View).ToElements()
        if not v.IsTemplate
    }
    to_create = [n for n in STANDARD_VIEWS if n not in existing]
    if not to_create:
        return "already exist"
    with Transaction(doc, "Create 3D Views") as t:
        t.Start()
        for name in to_create:
            view = View3D.CreateIsometric(doc, vft.Id)
            view.Name = name
        t.Commit()
    return "created {}".format(len(to_create))


def step_sheets():
    existing = {
        s.SheetNumber
        for s in FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
    }
    to_create = [(n, nm) for n, nm in STANDARD_SHEETS if n not in existing]
    if not to_create:
        return "already exist"
    tbs = list(
        FilteredElementCollector(doc)
        .OfCategory(BuiltInCategory.OST_TitleBlocks)
        .OfClass(FamilySymbol).ToElements()
    )
    tb_id = tbs[0].Id if tbs else ElementId.InvalidElementId
    with Transaction(doc, "Create Sheets") as t:
        t.Start()
        for num, name in to_create:
            sheet = ViewSheet.Create(doc, tb_id)
            sheet.SheetNumber = num
            sheet.Name = name
        t.Commit()
    return "created {}".format(len(to_create))


def step_browser_org():
    all_orgs = list(BrowserOrganization.GetAllBrowserOrganization(doc))
    match = None
    for kw in ["discipline", "type"]:
        for org in all_orgs:
            if kw in org.Name.lower():
                match = org
                break
        if match:
            break
    if match is None:
        return "no matching org found — configure manually"
    BrowserOrganization.SetCurrentBrowserOrganizationForViews(doc, match.Id)
    return "applied '{}'".format(match.Name)


# ---- Main ----

def run():
    if not forms.alert(
        "Initialize Project will create worksets, parameters, views, and sheets.\n"
        "This is safe to run on a new project. Proceed?",
        yes=True, no=True,
    ):
        output.print_md("**Cancelled.**")
        return

    steps = [
        ("Worksets", step_worksets),
        ("Shared Parameters", step_shared_params),
        ("3D Views", step_views),
        ("Sheets", step_sheets),
        ("Browser Organization", step_browser_org),
    ]

    for label, fn in steps:
        try:
            result = fn()
            output.print_md("**{}:** {}".format(label, result))
        except Exception:
            output.print_md("**{} ERROR:**".format(label))
            output.print_md("```\n{}\n```".format(traceback.format_exc()))

    output.print_md("**Initialize Project complete.**")


try:
    run()
except Exception:
    output.print_md("**Fatal Error:**")
    output.print_md("```\n{}\n```".format(traceback.format_exc()))
