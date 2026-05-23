# IfcOpenShell & Python
## An exercise of IfcOpenShell

### The task:
From an IFC file (BIM4EEB-TUD-2x3.ifc), make a dictionary of all walls (IfcWallStandardCase) that have windows (IfcWindow), each wall described with its
- GUID
- dimensions
- the total window area of the wall

### Requirements of the Python code:
#### The main part of the code should be wrapped in the main() function, for example:
def main(model_path):

…

return walls_with_windows

The input should be the path to your IFC file, and the output should be a list including all walls with windows with the required info. Walls without windows cannot be in the list.

#### The format of the output should be like:
[{'Dimensions': #dimensions from propertyset of the wall,

'GlobalId': #GUID of the wall,

'WindowsArea': #the total window area of the wall },

{'Dimensions': {'Height': #height, 'Length': #length , 'Width': #witdth }

#dimensions from propertyset of the wall,

'GlobalId': #GUID of the wall,

'WindowsArea': #the total window area of the wall },

…]


#### Abstract

The goal of this assignment was to identify walls in an IFC model that have windows attached to them and to retrieve important information such as the dimensions, GUID of the walls and the total window area associated with each wall. I achieved this using IfcOpenShell with Python to analyze the IFC file.

#### Approach

![image](https://github.com/user-attachments/assets/a08687a2-c11e-471b-a0d3-52a5af03adb0)

#### 1. Opening the IFC model:

* First, I opened the IFC model file using IfcOpenShell. I used the by_type('IfcWallStandardCase') method to extract all instances of IfcWallStandardCase from the model, which represent the walls I wanted to analyze.

#### 2. Identifying walls with windows:
I wrote the function get_walls_have_windows() to loop through each wall and check for any windows associated with it. The process was as follows:
* I checked if each wall has an a􀆩ribute called “HasOpenings”. This indicates if the wall contains or voids an opening.
* Through the “HasOpenings” relationship, I retrieved the IfcOpeningElement, which represents an opening in the wall (like a hole or void for a window).
* If this opening had fillings, I then looked for the “HasFillings” relationship, which pointed to elements like windows. When I found an IfcWindow, I knew that this wall had windows attached to it.

#### 3. Extracting wall dimensions:
* For each wall that I found with windows, I retrieved its dimensions: height, length, and width by accessing the BaseQuantities property set. If the wall had these properties, I extracted the values and stored them for reporting.

#### 4. Calculating window area:
* For each window associated with a wall, I extracted the area from the Dimensions property set. I summed up the areas of all windows attached to each wall and stored this total window area for later use.
#### 5. Storing and presenting the results:
* After processing all the walls and their related windows, I forma􀆩ed the information (GlobalId, dimensions, and total window area) into a structured dictionary for each wall. Finally, I printed the results for review.

#### The Relationships Between Walls and Windows:
* Walls (IfcWallStandardCase): I connected walls to windows through openings (IfcOpeningElement).
* Openings (IfcOpeningElement): These openings in the wall are typically voids where windows or doors can be placed.
* Windows (IfcWindow): Windows are linked to walls through the HasFillings relationship, which associates the opening in the wall with the window.

#### Wall and Window Relationship Diagram: 

![image](https://github.com/user-attachments/assets/823eaf90-f16e-424a-92c5-999d6bad49c5)

##### References:
IFC2x Edi􀆟on 3 Technical Corrigendum 1
https://standards.buildingsmart.org/IFC/RELEASE/IFC2x3/TC1/HTML/


  
