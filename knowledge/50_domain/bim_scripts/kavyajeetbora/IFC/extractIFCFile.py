import ifcopenshell
import ifcopenshell.util.element as Element
import time
import pandas as pd
from tqdm import tqdm

def tabulate_pset_data(psets):
    psets_dict = {}
    for pset_name in psets.keys():
        for prop_name in psets[pset_name].keys():
            psets_dict[pset_name+"."+prop_name] = psets[pset_name][prop_name]

    return psets_dict

def extract_IFC_data_by_elements(file, class_name):
    elements = file.by_type(class_name)
    data = []
    for elem in elements:
        ## get the basic info
        basic_info = elem.get_info()
        basic_info['Level'] = Element.get_container(elem).Name if Element.get_container(elem) else ""

        ## get the psets
        psets = Element.get_psets(elem, psets_only=True)
        psets_data = tabulate_pset_data(psets)

        qtos = Element.get_psets(elem, qtos_only=True)
        qtos_data = tabulate_pset_data(qtos)

        final_data = basic_info | psets_data | qtos_data  ## This concatenation of dictionaries is only available in python >= 3.9

        data.append(final_data)

    return data

def wrtie_data_to_excel(ifc_file_path):

    start_time = time.time()
    file = ifcopenshell.open(ifc_file_path)

    element_types = set([x.is_a() for x in file.by_type('IfcBuildingElement')])

    with pd.ExcelWriter(r'export/IFC_data.xlsx', engine='xlsxwriter') as writer:
        for element_type in tqdm(element_types, unit=" element type"):
            data = extract_IFC_data_by_elements(file, element_type)
            df = pd.DataFrame(data)
            df = df.dropna(axis=1, how='all')
            df.to_excel(writer, sheet_name=element_type)

    print(f"Excel file exported successfully in {(time.time()-start_time):.2f}")