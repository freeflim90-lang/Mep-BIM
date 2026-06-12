# from ifcopenshell import geom, util
# import ifcopenshell

# def create_polygonal_face_set(self):
#     items = []
#     for i in range(0, len(self.settings["vertices"])):
#         coordinates = self.file.createIfcCartesianPointList3D(
#             [self.convert_si_to_unit(v) for v in self.settings["vertices"][i]]
#         )
#         faces = [self.file.createIfcIndexedPolygonalFace([v + 1 for v in f]) for f in self.settings["faces"][i]]
#         items.append(self.file.createIfcPolygonalFaceSet(coordinates, None, faces))
#     return self.file.createIfcShapeRepresentation(
#         self.settings["context"], self.settings["context"].ContextIdentifier, "Tessellation", items
#     )


# # Parse the OBJ file
# with open('diamond.obj', 'r') as obj_file:
#     lines = obj_file.readlines()

# verticeListList = []
# faceList = []

# for line in lines:
#     if line.startswith('v '):
#         _, x, y, z = line.strip().split()
#         verticeListList.append((float(x), float(y), float(z)))
#     elif line.startswith('f '):
#         _, v1, v2, v3 = line.strip().split()
#         faceList.append((int(v1), int(v2), int(v3)))

# # Create an IFC file
# ifc_file = ifcopenshell.file(schema="IFC4")
# ifc_file.create_entity('IfcProject')
# ## ifcopenshell.open

# # for i in range (0, len(vertices)):
# #     vertice = vertices[i]


# #     coordinates = self.file.createIfcCartesianPointList3D(
# #             [self.convert_si_to_unit(v) for v in self.settings["vertices"][i]]
# #         )
# #         faces = [self.file.createIfcIndexedPolygonalFace([v + 1 for v in f]) for f in self.settings["faces"][i]]
# #         items.append(self.file.createIfcPolygonalFaceSet(coordinates, None, faces))
# #     return self.file.createIfcShapeRepresentation(
# #         self.settings["context"], self.settings["context"].ContextIdentifier, "Tessellation", items
# #     )






# # # # Create the Cartesian point list
# # # point_list = ifc_file.create_entity('IfcCartesianPointList3D')
# # # point_list.CoordList = [[x, y, z] for x, y, z in vertices]

# # # # Create the indexed polygonal face
# # # indexed_face = ifc_file.create_entity('IfcIndexedPolygonalFace')
# # # indexed_face.Coordinates = point_list
# # # indexed_face.PolygonalFace = [[v1, v2, v3] for v1, v2, v3 in faces]

# # # # Create the polygonal face set
# # # face_set = ifc_file.create_entity('IfcPolygonalFaceSet')
# # # face_set.Faces = [indexed_face]

# # # # Create the shape representation
# # # shape_rep = ifc_file.create_entity('IfcShapeRepresentation')
# # # shape_rep.RepresentationType = 'Brep'
# # # shape_rep.RepresentationIdentifier = 'Body'
# # # shape_rep.ContextOfItems = ifc_file.get_inverse(shape_rep).get_related_type(ifcopenshell.entity_instance("IfcGeometricRepresentationContext"))
# # # shape_rep.Items = [face_set]

# # # # Associate the shape representation with the project
# # # project = ifc_file.by_type('IfcProject')[0]
# # # project.RepresentationContexts.append(shape_rep)

# # # # Save the IFC file
# # # ifc_file.write('diamond.ifc')

# # create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)



# # person = ifcopenshell.api.run("owner.add_person", ifc_file, identification="SBE", family_name="SBE@AAJ", given_name="SBE")
# # org = ifcopenshell.api.run("owner.add_organisation", ifc_file, identification="AAJ", name="AAJ")
# # user = ifcopenshell.api.run("owner.add_person_and_organisation", ifc_file, person=person, organisation=org)
# # application = ifcopenshell.api.run("owner.add_application", ifc_file)
# # project = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcProject", name="TEST")
# # lengthunit = ifcopenshell.api.run("unit.add_si_unit", ifc_file, unit_type="LENGTHUNIT", name="METRE")
# # unitAssignment = ifcopenshell.api.run("unit.assign_unit", ifc_file, units=[lengthunit])
# # model = ifcopenshell.api.run("context.add_context", ifc_file, context_type="Model")
# # context = ifcopenshell.api.run("context.add_context", ifc_file, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW",parent=model,)
# # site = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcSite", name="My Site")
# # building = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBuilding", name="My Building")
# # storey = ifcopenshell.api.run("root.create_entity", ifc_file, ifc_class="IfcBuildingStorey", name="My Storey")
# # aggregation1 = ifcopenshell.api.run("aggregate.assign_object", ifc_file, product=site, relating_object=project)
# # aggregation2 = ifcopenshell.api.run("aggregate.assign_object", ifc_file, product=building, relating_object=site)
# # aggregation3 = ifcopenshell.api.run("aggregate.assign_object", ifc_file, product=storey, relating_object=building)

# # history = ifcopenshell.api.run("owner.create_owner_history", ifc_file)
# origin = ifc_file.createIfcAxis2Placement3D(ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)), ifc_file.createIfcDirection((0.0, 0.0, 1.0)),ifc_file.createIfcDirection((1.0, 0.0, 0.0)),)
# placement = ifc_file.createIfcLocalPlacement(None, origin)



# indexedPolygonalFace1 = ifc_file.createIfcIndexedPolygonalFace((1,2,3,4))
# indexedPolygonalFace2 = ifc_file.createIfcIndexedPolygonalFace((6,2,3,7))
# indexedPolygonalFace3 = ifc_file.createIfcIndexedPolygonalFace((7,3,4,8))
# indexedPolygonalFace4 = ifc_file.createIfcIndexedPolygonalFace((8,4,1,5))
# indexedPolygonalFace5 = ifc_file.createIfcIndexedPolygonalFace((1,4,3,2))
# indexedPolygonalFace6 = ifc_file.createIfcIndexedPolygonalFace((6,7,8,5))
# cartesianPointList3d = ifc_file.createIfcCartesianPointList3D(CoordList=((0.,0.,0.),(1.,0.,0.),(1.,1.,0.),(0.,1.,0.),(0.,0.,2.),(1.,0.,2.),(1.,1.,2.),(0.,1.,2.)))
# polygonalFaceSet = ifc_file.createIfcPolygonalFaceSet(Faces=[indexedPolygonalFace1, indexedPolygonalFace2, indexedPolygonalFace3, indexedPolygonalFace4, indexedPolygonalFace5, indexedPolygonalFace6])
# # proxy2 = ifcopenshell.api.run("root.create_entity", ifc_file, "IfcExtrudedAreaSolid")
# # shapeRep = ifc_file.createIfcShapeRepresentation(ContextOfItems=ifc_file.context, RepresentationIdentifier='Body', RepresentationType='Tesselation', Items=[polygonalFaceSet,])
# # ifcopenshell.api.run("geometry.assign_representation", ifc_file, product=proxy2, representation=shapeRep)
# # containment = ifcopenshell.api.run("spatial.assign_container", ifc_file, product=proxy2, relating_structure=storey)

# coordinates = []
# items = []
# for i in range(0, len(verticeListList)):
#     coordinates = ifc_file.createIfcCartesianPointList3D(
#         ([vertix for vertix in verticeListList[i]])
#     )
#     faces = [ifc_file.createIfcIndexedPolygonalFace([v + 1 for v in f]) for f in faceList[i]]
#     items.append(ifc_file.createIfcPolygonalFaceSet(coordinates, None, faces))

# a = ifc_file.createIfcShapeRepresentation(
#         # self.settings["context"], 
#         # self.settings["context"].ContextIdentifier, 
#         None,None,
#         "Tessellation", items
# )

# print(a)

import ifcopenshell

# Create an IFC file
ifc_file = ifcopenshell.file()

# Create the origin
origin = ifc_file.createIfcAxis2Placement3D(
    Location=ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)),
    Axis=ifc_file.createIfcDirection((0.0, 0.0, 1.0)),
    RefDirection=ifc_file.createIfcDirection((1.0, 0.0, 0.0))
)

# Create the placement
placement = ifc_file.createIfcLocalPlacement(
    PlacementRelTo=None,
    RelativePlacement=origin
)

# Create the indexed polygonal faces
indexedPolygonalFace1 = ifc_file.createIfcIndexedPolygonalFace((1, 2, 3, 4))
indexedPolygonalFace2 = ifc_file.createIfcIndexedPolygonalFace((6, 2, 3, 7))
indexedPolygonalFace3 = ifc_file.createIfcIndexedPolygonalFace((7, 3, 4, 8))
indexedPolygonalFace4 = ifc_file.createIfcIndexedPolygonalFace((8, 4, 1, 5))
indexedPolygonalFace5 = ifc_file.createIfcIndexedPolygonalFace((1, 4, 3, 2))
indexedPolygonalFace6 = ifc_file.createIfcIndexedPolygonalFace((6, 7, 8, 5))

# Create the Cartesian point list
cartesianPointList3d = ifc_file.createIfcCartesianPointList3D(
    CoordList=((0., 0., 0.), (1., 0., 0.), (1., 1., 0.), (0., 1., 0.), (0., 0., 2.), (1., 0., 2.), (1., 1., 2.), (0., 1., 2.))
)

# Create the polygonal face set
polygonalFaceSet = ifc_file.createIfcPolygonalFaceSet(
    Faces=[indexedPolygonalFace1, indexedPolygonalFace2, indexedPolygonalFace3, indexedPolygonalFace4, indexedPolygonalFace5, indexedPolygonalFace6]
)

ifc_file.write("output.ifc")