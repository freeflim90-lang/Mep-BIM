import csv
import os
import re
import ifcopenshell

def set_storey(ifc_loc):
    new_filename = ifc_loc.replace('.ifc', '_clean.ifc')
    ifc = ifcopenshell.open(ifc_loc)
    owner_history = ifc.by_type('IfcOwnerHistory')[0]
    base_storey = None
    storeys = ifc.by_type("IfcBuildingStorey")
    for storey in storeys:
        if storey.Elevation == 0:
            base_storey = storey
    if base_storey is None:
        base_storey = storeys[0]
    if base_storey is None:
        return "Не найдены этажи"
    elem_list = []
    rel_list = []
    for elem in ifc:
        if hasattr(elem, "ContainedInStructure") and elem.ContainedInStructure:
            rels = [rel for rel in elem.ContainedInStructure if rel.RelatingStructure != base_storey]
            rel_list.extend(rels)
            if len(rels)>0:
                elem_list.append(elem)
    rel_id = ifcopenshell.guid.new()
    for rel in rel_list:
        try:
            ifc.remove(rel)
        except:
            pass
    for stor in storeys:
        if stor != base_storey : ifc.remove(stor)
    rel = ifc.create_entity( "IfcRelContainedInSpatialStructure", GlobalId=rel_id, OwnerHistory=owner_history, Name="Containment", Description=None, RelatedElements=elem_list, RelatingStructure=base_storey)
    ifc.write(new_filename)

if __name__ == "__main__":
    script_path = os.path.abspath(os.path.dirname(__file__))
    work_path = os.path.abspath(os.getcwd())
    ifc_file = []
    for file in os.listdir(work_path):
        if file.endswith('.ifc') and not file.endswith('_clean.ifc'):
            ifc_file.append(os.path.join(work_path, file))
            print(os.path.join(work_path, file))
    assert len(ifc_file) > 0
    for ifc_loc in ifc_file:
        print(ifc_loc, set_storey(ifc_loc))
    print('End')