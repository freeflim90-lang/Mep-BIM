import csv
import logging

import ifcopenshell
from ifcopenshell.util.element import get_material, get_materials
from ifcopenshell.util.unit import calculate_unit_scale

from ifc_material_qto.quantities import _get_element_quantities, _get_geometrical_quantities


def process_ifc(ifc_path, use_geometry):
    logging.info(f"Processing IFC: {ifc_path}")
    ifc = ifcopenshell.open(ifc_path)
    scale = calculate_unit_scale(ifc)
    settings = None
    if use_geometry:
        try:
            import ifcopenshell.geom as ifc_geom
            settings = ifc_geom.settings()
            settings.set(settings.USE_WORLD_COORDS, True)
        except ImportError:
            logging.warning("Geometry (ifcopenshell.geom) not available, falling back to IFC quantities")
            use_geometry = False
    
    material_data = {}
    for element in ifc.by_type("IfcElement"):
        material = get_material(element)
        if not material:
            continue

        quantities = _get_element_quantities(element)
        volume = quantities["volume"]

        if use_geometry and volume == 0:
            geometrical_quantities = _get_geometrical_quantities(settings, element)
            volume = geometrical_quantities["volume"] * (scale ** 3)

        if volume == 0:
            continue

        if material.is_a("IfcMaterialLayerSetUsage"):
            layers = material.ForLayerSet.MaterialLayers
            total_thickness = sum(layer.LayerThickness for layer in layers)
            if total_thickness == 0:
                continue

            for layer in layers:
                material_name = layer.Material.Name or "Unnamed material"
                ratio = layer.LayerThickness / total_thickness
                layer_volume = volume * ratio
                data = material_data.setdefault(
                    material_name,
                    { "volume": 0.0, "elements": 0 }
                )

                data["volume"] += layer_volume
                data["elements"] += 1
                logging.debug(f"{element} -> {material_name} -> {data}")
        else:
            materials = get_materials(element)
            for material in materials:
                material_name = material.Name or "Unnamed material"
                data = material_data.setdefault(
                    material_name,
                    { "volume": 0.0, "elements": 0 }
                )
                data["volume"] += volume
                data["elements"] += 1
                logging.debug(f"{element} -> {material_name} -> {data}")
        

    return material_data

def write_csv(material_data, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["material", "volume(m3)", "element_count"])

        for mat, data in material_data.items():
            writer.writerow([
                mat,
                round(data["volume"], 3),
                data["elements"]
            ])
        logging.info(f"Materials extracted in {output_path}")
