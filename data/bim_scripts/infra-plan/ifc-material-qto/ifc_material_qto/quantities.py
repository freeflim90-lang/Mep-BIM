def  _get_element_quantities(element):
    quantities = {
        "volume": 0.0,
    }

    for rel in getattr(element, "IsDefinedBy", []):
        if rel.is_a("IfcRelDefinesByProperties"):
            property_def = rel.RelatingPropertyDefinition

            if property_def.is_a("IfcElementQuantity"):
                for q in property_def.Quantities:
                    if q.is_a("IfcQuantityVolume"):
                        quantities["volume"] += q.VolumeValue
    
    return quantities

def _get_geometrical_quantities(settings, element):
    try:
        import ifcopenshell.geom
        import ifcopenshell.util.shape
    except ImportError:
        return { "volume": 0.0 }

    try:
        shape = ifcopenshell.geom.create_shape(settings, element)
        geometry = shape.geometry
        return { "volume": ifcopenshell.util.shape.get_volume(geometry) }
    
    except Exception:
        return { "volume": 0.0 }