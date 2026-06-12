import ifcopenshell

#___WALL SEPARATED SPACES___

def build_walls_spaces(ifc_file_path):
    ifc_file = ifcopenshell.open(ifc_file_path)
    walls_spaces = []
    # Find all IfcWall entities
    walls = ifc_file.by_type("IfcWall")

    # Find all IfcSpace entities
    spaces = ifc_file.by_type("IfcSpace")

    # Create a dictionary to store walls and their related spaces
    wall_spaces = {}

    # Iterate through walls
    for wall in walls:
        wall_id = wall.id()
        wall_spaces[wall_id] = []

        # Find related IfcRelSpaceBoundary relationships for the wall
        space_boundaries = wall.ProvidesBoundaries

        for space_boundary in space_boundaries:
            if space_boundary.is_a("IfcRelSpaceBoundary"):
                # Check if the related space is an IfcSpace
                related_space = space_boundary.RelatingSpace
                if related_space.is_a("IfcSpace"):
                    wall_spaces[wall_id].append(related_space)

    # Get ifcspaces
    spaces = ifc_file.by_type("IfcSpace")

    # Print the results
    for wall_id, related_spaces in wall_spaces.items():
        wall_name = ifc_file[wall_id].Name
        space_names = [space.LongName for space in related_spaces]
        print(f"Wall '{wall_name}' separates spaces: {', '.join(space_names)}")
        walls_spaces.append({wall_name: space_names})        

    return walls_spaces

#___DATA WALLS LAYERS___

def build_WallsLayers(ifc_file_path):
    ifc_file = ifcopenshell.open (ifc_file_path)
    products = ifc_file.by_type('IfcProduct')

    s_wall = []
    n = 0
    for wall in ifc_file.by_type('IfcWall'):
        s_wall.append({'Code': wall.id()})
        s_wall[n]['Info'] = wall.get_info()
        s_wall[n]['Raw'] = wall
        n += 1

    for n in range(0, len(s_wall)):
        if s_wall[n]['Raw'].HasAssociations:
            s_wall[n]['MaterialLayerList'] = []
            for i in s_wall[n]['Raw'].HasAssociations:
                if i.is_a('IfcRelAssociatesMaterial'):
                    n_material = 0
                    for material in i.RelatingMaterial.MaterialLayers:
                        s_wall[n]['MaterialLayerList'].append({'Code': material.Material.Name})
                        s_wall[n]['MaterialLayerList'][n_material]["LayerThickness"] = material.LayerThickness
                        s_wall[n]['MaterialLayerList'][n_material]["Properties"] = {}
                        for PropertySet in material.Material.HasProperties:
                            for Property in PropertySet.Properties:
                                s_wall[n]['MaterialLayerList'][n_material]["Properties"][PropertySet.Name + ":" + Property.Name] = Property.NominalValue.wrappedValue
                        n_material += 1 
    import pprint
    pprint.pprint(s_wall)
    return s_wall

#___SPACES HEATED-UNHEATED___

def build_space_heated(ifc_file_path):
    # Open the IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Get all spaces in the IFC file
    spaces = ifc_file.by_type('IfcSpace')

    space_heated = {}
    for space in spaces:
        # Get the name of the space
        space_name = space.get_info()['Name']

        # Find the IFCPROPERTYSINGLEVALUE with the name "heated" for the space
        Is_Heated_Room = False
        for rel in space.IsDefinedBy:
            if rel.get_info()['type'] == 'IfcRelDefinesByProperties':
                for property_set in rel.RelatingPropertyDefinition:
                    if property_set == 'Altro':
                        for property in rel.RelatingPropertyDefinition.HasProperties:
                            if property.Name == 'Heated room':
                                Is_Heated_Room = property.NominalValue.wrappedValue
                                space_heated[space.get_info()['LongName']] = Is_Heated_Room

    return space_heated

class cm:
  def __init__(self,
                ClimateZone = '?',
                Operation_Type = 'BuildingRenovation',
                Operation_Type_Sub = 'BuildingEnvelope',
                walls = '?',
                CAM_FilePathAndName = '?'):
    self.ClimateZone = ClimateZone
    self.Operation_Type = Operation_Type
    self.Operation_Type_Sub = Operation_Type_Sub
    self.CAM_FilePathAndName = CAM_FilePathAndName
    
    import json
    file = open(CAM_FilePathAndName)
    self.cam = json.load(file)
    self.data = walls

  def Calc_ThResistance(self):
    result = 0
    for i in range(len(self.TMP_Thickness)):
      if self.TMP_ThConductivity[i] != 0:
        result += self.TMP_Thickness[i] / self.TMP_ThConductivity[i]
    return result

  def CHECK_IfCAM(self):
    UValue = round((1 / (self.Calc_ThResistance() + 0.04 + 0.13)),2)
    UValue_Maximum = self.cam['TypeOfOperation'][self.Operation_Type][self.Operation_Type_Sub]['UValues - Admitted'][self.ClimateZone]['Wall']
    Check = False
    Recommendation = ''
    if UValue <= UValue_Maximum:
      Check = True
    else:
      Recommendation = ' --> You are asked to add about ' + str(round(0.04 * (1/UValue_Maximum - 1/UValue),3)) + ' m of insulation layer (in case of conductivity = 0.040 W/(m²K))'
    print(self.TMP_Wall_Name + " -  UValue = " + str(UValue), 'W/m²K', '- Check is', Check, '(reference value:', UValue_Maximum,')', Recommendation)

  def CHECK_IfCAM_Loop(self):
    for n in range(0, len(self.data)):
      self.TMP_Wall_Name = self.data[n][0]
      #Wall.append(self.data[n][1])

      if self.data[n][1] == 'Muro da verificare':
        self.TMP_Thickness = self.data[n][4]
        self.TMP_ThConductivity = self.data[n][5]
        self.CHECK_IfCAM()

if __name__ == '__main__':
    ifc_file_path = (r"C:\....\...\Model.ifc") #INSERT_LOCAL_IFC_FILE_PATH_HERE

    WallsLayers = build_WallsLayers(ifc_file_path)
    WallsSpaces = build_walls_spaces(ifc_file_path)
    Spaces_Heated = build_space_heated(ifc_file_path)
    
    Walls_ToBeVerified = []
    for WallSpaces in WallsSpaces:
        key = list(WallSpaces.keys())[0]
        print(key)
        Heated_IsTrue = 0
        Heated_IsFalse = 0
        for environment in WallSpaces[key]:
            if Spaces_Heated[environment] == True:
                Heated_IsTrue = Heated_IsTrue + 1
            else:
                Heated_IsFalse = Heated_IsFalse + 1
        if Heated_IsTrue > 0 and Heated_IsFalse > 0:
            Walls_ToBeVerified.append(list(WallSpaces.keys())[0])
    print(Walls_ToBeVerified)

    walls = []
    for n_wall in range(len(WallsLayers)):
        wall_supp = []
        wall_supp.append(WallsLayers[n_wall]['Info']['Name'])
        if wall_supp[0] in Walls_ToBeVerified:
            wall_supp.append('Wall to be checked')
        wall_supp.append('-')
        try:
            MaterialLayerList = WallsLayers[n_wall]['MaterialLayerList']
            s_name = []
            s_thickness = []
            s_thcond = []
            for MaterialLayer in MaterialLayerList:
                s_name.append(MaterialLayer['Code'])
                s_thickness.append(MaterialLayer['LayerThickness'])
                s_thcond.append(MaterialLayer['Properties']['Pset_MaterialThermal:ThermalConductivity'])
            wall_supp.append(s_name)
            wall_supp.append(s_thickness)
            wall_supp.append(s_thcond)
            walls.append(wall_supp)
        except:
            wall_supp[1] = 'Wall cannot be verified due to absence of layers'
            wall_supp.append(wall_supp)

    CAM = cm(ClimateZone = 'Climate Zone F',
                Operation_Type = 'BuildingRenovation',
                Operation_Type_Sub = 'BuildingEnvelope',
                walls = walls,
                CAM_FilePathAndName = r"C:\...\...\ThermalTransmittanceLimits.json" #INSERT_JSON_file path with thermal transmittance limits
                )

    CAM.CHECK_IfCAM_Loop()
  











