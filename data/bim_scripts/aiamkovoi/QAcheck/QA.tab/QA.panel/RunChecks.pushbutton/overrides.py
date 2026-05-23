from Autodesk.Revit.DB import (
    OverrideGraphicSettings,
    Color,
    FillPatternElement,
    FillPatternTarget,
    FilteredElementCollector,
    Element
)


def get_solid_fill(doc):
    """Get a solid fill pattern ID. Works across Revit versions."""
    fills = FilteredElementCollector(doc)\
        .OfClass(FillPatternElement)\
        .ToElements()
    for f in fills:
        fp = f.GetFillPattern()
        if fp and fp.Target == FillPatternTarget.Drafting:
            try:
                if fp.IsSolidFill:
                    return f.Id
            except:
                pass
    # Fallback: search by name
    for f in fills:
        name = Element.Name.GetValue(f)
        if "Solid" in name:
            return f.Id
    return None


def apply_override(view, element_id, rgb, solid_fill_id=None):
    """Apply color override to an element in the active view."""
    color = Color(rgb[0], rgb[1], rgb[2])
    ogs = OverrideGraphicSettings()
    ogs.SetProjectionLineColor(color)
    ogs.SetSurfaceForegroundPatternColor(color)
    if solid_fill_id:
        ogs.SetSurfaceForegroundPatternId(solid_fill_id)
    view.SetElementOverrides(element_id, ogs)


def clear_all_overrides(doc, view):
    """Reset all element overrides in the active view."""
    all_ids = FilteredElementCollector(doc)\
        .WhereElementIsNotElementType()\
        .ToElementIds()
    blank = OverrideGraphicSettings()
    for eid in all_ids:
        view.SetElementOverrides(eid, blank)
