# Import libraries
import bpy
import random
import ifcopenshell
from bonsai.bim.ifc import IfcStore
import bonsai.tool as tool

# Load current model
model = IfcStore.get_file()         

# The wall with the smallest volume is green and the wall with the largest volume is red

walls = model.by_type("IfcWallStandardCase")

# Get volumes for all walls
volumes = []
wall_objects = []

for wall in walls:
    # Get the wall IFCOpenShell as the object in Blender
    obj = tool.Ifc.get_object(wall)
    
    if obj:
        # Get wall properties (psets)
        psets = ifcopenshell.util.element.get_psets(wall)
        volume = None
        if 'Dimensions' in psets:
            dimensions_quantities = psets['Dimensions']
            volume = dimensions_quantities.get('Volume')

        if volume:
            volumes.append(volume)
            wall_objects.append((obj, volume))  # Store Blender object with its volume

# Name the minimum and maximum volumes
min_volume = min(volumes)
max_volume = max(volumes)

# Function normalizes the volume between 0 and 1, and interpolates between green and red
def volume_to_color(volume, min_volume, max_volume):
    normalized_volume = (volume - min_volume) / (max_volume - min_volume)
    return (normalized_volume, 1.0 - normalized_volume, 0.0)  # (R, G, B) where red is max, green is min

# Assign colors to each object through its volume
for obj, volume in wall_objects:
    
    color = volume_to_color(volume, min_volume, max_volume)

    # Apply the color to the corresponding 3D object in Blender
    mat = bpy.data.materials.new(name="WallColor")
    mat.diffuse_color = (*color, 1)
    obj.active_material = mat
                
# Update the scene
bpy.context.view_layer.update()