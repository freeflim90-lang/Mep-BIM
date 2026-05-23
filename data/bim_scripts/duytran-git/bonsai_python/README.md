# Bonsai & Python
## An exercise using Python scripting with IfcOpenShell in Bonsai/Blender.
### The task:

My task was to create a Python script using IfcOpenShell in Bonsai/Blender. The colours of walls change based on the volumes of the walls. The wall with the smallest volume is green and the wall with the largest volume is red.

### How to Solve It:
The first thing I did was break down the task. Instead of randomly assigning colors, the script needed to find the volume of each wall and assign colors from red to green based on the volume.

![bonsai_exercise](https://github.com/user-attachments/assets/e1d4cc1b-7574-4e40-8a88-504cfdb9710d)

#### Step-by-Step:
##### 1. Loading the Model:

* Loading the IFC file into the script using IfcStore.get_file()

##### 2. Identifying Wall Objects:

* I used the method model.by_type("IfcWallStandardCase") to extract all wall objects from the IFC model.

##### 3. Extracting Volumes:

* For each wall, I retrieved its property sets (psets) using ifcopenshell.util.element.get_psets().

* From these property sets, we accessed the 'Dimensions' a􀆩ribute to retrieve the volume of each wall.

##### 4. Storing Wall Data:

* I created two lists: one to store the volumes of each wall and another to store the Blender object along with its corresponding volume. This made to later assign colors based on volume.

##### 5. Determining Volume Extremes:

* I identified the minimum and maximum volumes. These two values provided the range for mapping the wall volumes to a color gradient (from 0 to 1 = from green to red, color gradient is in middle)

##### 6. Mapping Volume to Color:

* With function, volume_to_color(), that normalized each wall’s volume between the smallest and largest volume. This function returned a color where green represented the smallest volume, and red represented the largest.

* Min-max feature scaling: Feature scaling is used to bring all values into the range [0,1]. This is also called unity-based normalization. This can be generalized to restrict the range of values in the dataset between any arbitrary points a and b.

* References: https://en.wikipedia.org/wiki/Normalization_(statistics)

##### 7. Assigning Colors to Walls:

* For each wall object, if the wall already had a material, I reused it. Otherwise, I created a new material and assigned it to the wall. The wall’s color was then set using mat.diffuse_color.

##### 8. Updating the Scene:

* Finally, I updated the scene in Blender to reflect the changes made to the wall materials using bpy.context.view_layer.update()

### Results:
* The walls with the smallest volumes were displayed in green, while the walls with the largest volumes were displayed in red. 

* And intermediate volumes were represented by colors transitioning from green to red.

![image](https://github.com/user-attachments/assets/0c7e8803-a316-4508-af49-78c2e7a30c4a)

![image](https://github.com/user-attachments/assets/55753917-7b88-46cd-82c2-41140e397f2d)





