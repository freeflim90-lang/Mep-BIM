# -*- coding: utf-8 -*-
"""Auto-color elements by parameter — multi-category, parameter list from model."""

import colorsys

from Autodesk.Revit.DB import (
    FilteredElementCollector,
    BuiltInCategory,
    Transaction,
    OverrideGraphicSettings,
    Color,
    FillPatternElement,
    FillPatternTarget,
    Element
)
from pyrevit import script, revit, forms

doc = revit.doc
view = doc.ActiveView
output = script.get_output()
output.close_others()


# --- Helpers ---

def get_solid_fill(doc):
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
    for f in fills:
        name = Element.Name.GetValue(f)
        if "Solid" in name:
            return f.Id
    return None


def apply_color(view, eid, rgb, fill_id):
    color = Color(rgb[0], rgb[1], rgb[2])
    ogs = OverrideGraphicSettings()
    ogs.SetProjectionLineColor(color)
    ogs.SetSurfaceForegroundPatternColor(color)
    if fill_id:
        ogs.SetSurfaceForegroundPatternId(fill_id)
    view.SetElementOverrides(eid, ogs)


def get_param_value(doc, el, param_name):
    if param_name == "Type Name":
        el_type = doc.GetElement(el.GetTypeId())
        return Element.Name.GetValue(el_type) if el_type else "(no type)"

    # Instance first
    param = el.LookupParameter(param_name)

    # Fallback to type
    if param is None or not param.HasValue:
        el_type = doc.GetElement(el.GetTypeId())
        if el_type:
            param = el_type.LookupParameter(param_name)

    if param and param.HasValue:
        val = param.AsString()
        if val is None:
            val = param.AsValueString() or "(empty)"
        return val

    return "(empty)"


def collect_parameter_names(doc, bic_list, limit=30):
    """Scan elements in selected categories, return common parameter names."""
    param_names = set()
    param_names.add("Type Name")

    for bic in bic_list:
        elements = FilteredElementCollector(doc)\
            .OfCategory(bic)\
            .WhereElementIsNotElementType()\
            .ToElements()

        # Sample up to 5 elements per category
        for el in list(elements)[:5]:
            for p in el.Parameters:
                if p.Definition:
                    param_names.add(p.Definition.Name)

            # Also type parameters
            el_type = doc.GetElement(el.GetTypeId())
            if el_type:
                for p in el_type.Parameters:
                    if p.Definition:
                        param_names.add(p.Definition.Name)

    param_names.discard("Type Name")
    return ["Type Name"] + sorted(param_names)


# --- Category selection (checkboxes, Floors pre-selected) ---

CAT_OPTIONS = {
    "Floors": BuiltInCategory.OST_Floors,
    "Walls": BuiltInCategory.OST_Walls,
    "Doors": BuiltInCategory.OST_Doors,
    "Rooms": BuiltInCategory.OST_Rooms,
    "Structural Columns": BuiltInCategory.OST_StructuralColumns,
    "Structural Framing": BuiltInCategory.OST_StructuralFraming,
    "Windows": BuiltInCategory.OST_Windows,
}

selected_cats = forms.SelectFromList.show(
    sorted(CAT_OPTIONS.keys()),
    title="Auto-Color: Select Categories",
    multiselect=True,
    default=["Floors"]
)

if not selected_cats:
    script.exit()

bic_list = [CAT_OPTIONS[c] for c in selected_cats]

# --- Parameter selection (dropdown from model) ---

param_list = collect_parameter_names(doc, bic_list)

param_name = forms.SelectFromList.show(
    param_list,
    title="Auto-Color: Select Parameter",
    multiselect=False,
    default="Type Name"
)

if not param_name:
    script.exit()

# --- Fade option ---
fade_others = forms.alert(
    "Fade unselected elements to 50% transparency?",
    yes=True, no=True
)

# --- Collect and group ---

solid_fill_id = get_solid_fill(doc)
value_map = {}
colored_ids = set()
total_elements = 0

for bic in bic_list:
    elements = FilteredElementCollector(doc)\
        .OfCategory(bic)\
        .WhereElementIsNotElementType()\
        .ToElements()

    for el in elements:
        val = get_param_value(doc, el, param_name)
        if val not in value_map:
            value_map[val] = []
        value_map[val].append(el.Id)
        colored_ids.add(el.Id)
        total_elements += 1

if not value_map:
    output.print_md("No elements found.")
    script.exit()

# --- Generate colors ---

distinct_values = sorted(value_map.keys())
n = len(distinct_values)


def generate_colors(count):
    colors = []
    for i in range(count):
        hue = i / float(count)
        r, g, b = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        colors.append((int(r * 255), int(g * 255), int(b * 255)))
    return colors


palette = generate_colors(n)
color_map = dict(zip(distinct_values, palette))

# --- Apply ---

with Transaction(doc, "SmartCheck Auto-Color") as t:
    t.Start()

    # Color selected elements
    for val, eids in value_map.items():
        rgb = color_map[val]
        for eid in eids:
            apply_color(view, eid, rgb, solid_fill_id)

    # Fade everything else to 50% transparency
    if fade_others:
        all_ids = FilteredElementCollector(doc)\
            .WhereElementIsNotElementType()\
            .ToElementIds()

        fade_ogs = OverrideGraphicSettings()
        fade_ogs.SetSurfaceTransparency(50)

        for eid in all_ids:
            if eid not in colored_ids:
                view.SetElementOverrides(eid, fade_ogs)

    t.Commit()

# --- Legend with proportional bars ---

cats_str = ", ".join(selected_cats)
output.print_md("# Auto-Color: {} by {}".format(cats_str, param_name))
output.print_md("---")

max_count = max(len(v) for v in value_map.values())

for val in distinct_values:
    rgb = color_map[val]
    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb)
    count = len(value_map[val])
    bar_pct = int(round(100.0 * count / max_count)) if max_count > 0 else 0

    output.print_html(
        '<div style="margin:3px 0;display:flex;align-items:center;">'
        '<span style="display:inline-block;width:14px;height:14px;min-width:14px;'
        'background:{color};border:1px solid #999;margin-right:8px;'
        'border-radius:2px;"></span>'
        '<span style="width:180px;min-width:180px;font-size:12px;'
        'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'
        '<strong>{name}</strong></span>'
        '<div style="flex:1;background:#eee;height:16px;border-radius:3px;'
        'margin:0 8px;overflow:hidden;">'
        '<div style="width:{pct}%;background:{color};height:100%;'
        'border-radius:3px;"></div></div>'
        '<span style="font-size:11px;color:#666;min-width:30px;'
        'text-align:right;">{count}</span>'
        '</div>'.format(
            color=hex_color,
            name=val,
            pct=bar_pct,
            count=count
        )
    )

# --- Summary ---
output.print_md("---")

output.print_md("**{} values**, **{} elements** across **{}**".format(
    n, total_elements, cats_str
))
