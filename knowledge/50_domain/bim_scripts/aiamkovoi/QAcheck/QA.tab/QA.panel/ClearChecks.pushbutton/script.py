# -*- coding: utf-8 -*-
"""Clear all QA color overrides from the active view. Silent."""

from Autodesk.Revit.DB import (
    FilteredElementCollector,
    OverrideGraphicSettings,
    Transaction
)
from pyrevit import revit

doc = revit.doc
view = doc.ActiveView

all_ids = FilteredElementCollector(doc)\
    .WhereElementIsNotElementType()\
    .ToElementIds()

blank = OverrideGraphicSettings()

with Transaction(doc, "Clear SmartCheck Overrides") as t:
    t.Start()
    for eid in all_ids:
        view.SetElementOverrides(eid, blank)
    t.Commit()
