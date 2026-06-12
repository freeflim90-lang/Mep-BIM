## Understanding and Extracting data from an IFC File

In this project we will extract all the relevant information from the <a href="IFC Files\MAD_SCIENTIST_21.ifc">IFC File</a>

<img src="gifs\3d Blender view.gif" height=400>

Before that we will try understand what is IFC file and its basic data structure.

The code used to extract the data can be found this <a href="ifcopenshell_basics.ipynb">Notebook</a>

## Industry Foundation Classes (IFC)

IFC or Industry Foundation Classes is a global standard for describing, sharing and exchanging information on building and facility management.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/9YgXXbdohOQ/0.jpg)](https://www.youtube.com/watch?v=9YgXXbdohOQ)

IFC was created to facilitate interoperability and standardized data exchange between different software applications in the architecture, engineering, and construction (AEC) industry to improve collaboration and efficiency in building projects.

<img src="https://bimcorner.com/wp-content/uploads/2019/12/buildingSmartLOGO.jpg" height=100/>

The organization is constantly improving the data exchange between applications employed in the construction industry. They develop standards, norms, and tools supporting the flow of information among different platforms. The main values of the organization are openness, neutrality, not-for-profit as well as internationalization.

It is a non-proprietary, neutral data format. IFC provides a set of definitions for all types of object elements encountered in the construction industry and a text structure to store such definitions in a data file.

<img src="https://bimcorner.com/wp-content/uploads/2019/12/GEOMETRYDATA-IFC-STRUCTURE-1.jpg" height=400/>

## IFC Version and evolution

<img src="https://bimcorner.com/wp-content/uploads/2019/12/IFC-EVOLUTION-1-1-614x1536.jpg" height=400/>

The IFC 5 version is still in preparation with further parametric capabilities and the activation of the infrastructure domain.
BuildingSMART International has defined a certification process to guarantee that the correct processes for importing and exporting IFC data are followed, ensuring compliance with the standards. All IFC certified programs are capable of reading, writing and exchanging information with other software solutions according to data provided by buildingSMART. IFC files may be exported and exchanged between software products using .ifc, .ifcXML and .ifcZIP file formats

## The best way to use IFC

What is the best workflow during the application of the IFC files? It is quite often said that you can start creating a 3D model in one software, export IFC to another program, and continue working on that model. Some programs have the ability to convert IFC to their native objects (Tekla Structures), however, it is not the best solution. In a general process, you should treat the IFC as a reference or performing another scope of work on the project.

As an example, we could imagine an architect working in their native software to create an architectural model of a building. Then the model is exported to the IFC and passed it on to HVAC designers and used there as a reference to run the ducts. If there is a problem or a change is required (e.g. moving a wall or making a hole in a duct), they do not alter the IFC model themselves but send a request to the architect with the specified changes. This one makes the necessary modifications and exports the updated IFC model.

<img src="https://bimcorner.com/wp-content/uploads/2019/12/Workflow.jpg" height=400/>

## IFC Spatial Hierarchy

The Industry Foundation Classes (IFC) hierarchy is a fundamental aspect of the IFC data model, which is used in Building Information Modeling (BIM) to represent and exchange information about building and construction projects. The IFC hierarchy organizes building elements and their associated data in a structured and standardized manner. It is crucial for maintaining consistency and interoperability between different BIM software applications and for effectively managing building project information. The IFC hierarchy consists of several levels, with each level representing a different aspect of the building project:

1. Project: At the top of the hierarchy is the "Project." The project represents the entire building or construction project and serves as the container for all other elements and information related to the project. It includes high-level information such as project name, location, and participants.

2. Site: Within the project, there can be one or more "Site" elements. A site represents the physical location of the building project, including its boundaries, terrain, and contextual information. It may contain information about land use, topography, and other site-specific details.

3. Building: A "Building" is a major physical structure within the project. It represents the main building or structure and contains information about its architectural design, structural elements, and other building-specific attributes. A project can have multiple buildings if it consists of several distinct structures.

4. Building Storey (Story): Within a building, you have "Building Storey" elements, often referred to as "Stories" in some regions. These represent the different levels or floors of the building. Each story contains information about the spaces, walls, ceilings, and other elements that make up that specific level.

5. Space: A "Space" represents a defined area within a building storey. Spaces can be rooms, corridors, open areas, or any other distinguishable spaces within a building. Information about spatial characteristics, usage, and attributes are stored within space elements.

6. Building Element: Building elements represent the physical components of the building, such as walls, floors, roofs, doors, windows, and structural components like beams and columns. Each building element contains detailed information about its geometry, material properties, and other relevant attributes.

7. Component: Some building elements can be further broken down into components. For example, a door (building element) may have components like handles, locks, and hinges. Components allow for more granular representation and management of elements within the building.

8. Materials and Assemblies: Materials and assemblies are used to define the composition of building elements. They specify the types of materials used in construction and how they are assembled. This information is essential for accurately representing the physical properties and behavior of building elements.

9. Types and Classes: Within the hierarchy, types and classes are used to categorize and standardize building elements. Types define common characteristics and behaviors shared by multiple instances of an element (e.g., a standard door type), while classes provide a broader categorization (e.g., doors, windows, walls).

10. Attributes and Properties: At each level of the hierarchy, elements and objects have associated attributes and properties that describe their characteristics and behavior. These attributes can include information like dimensions, materials, cost, and performance data.

The IFC hierarchy provides a structured framework for organizing and representing all the information needed for the design, construction, and management of a building project. It allows stakeholders to access and exchange data consistently, regardless of the software tools they use, promoting interoperability and collaboration throughout the project lifecycle

<img src="https://wiki.osarch.org/images/e/e1/Ifc-spatial-tree.png" height=400/>

## IFC Class Hierarchy

IFC Class Hierarchy. You can find more information on this [page](https://standards.buildingsmart.org/IFC/RELEASE/IFC4/FINAL/HTML/)

<img src="https://standards.buildingsmart.org/IFC/DEV/IFC4_2/FINAL/HTML/diagrams/ifcbuildingelement.png" height=400/>

## Property Sets

Property sets in IFC files are essential for accurately representing and exchanging detailed information about building elements, enabling better collaboration and data-driven decision-making throughout the building's lifecycle, from design and construction to operation and maintenance.

<img src="https://biblus.accasoftware.com/en/wp-content/uploads/sites/2/2020/02/Ifc-Property-Definition.jpg" height=400/>

Property sets in IFC are typically organized hierarchically, with the following key components:

- Property Set: This is the highest level of organization and represents a set of related properties. For example, you might have a "Wall Properties" property set that includes attributes like thickness, height, and material.

- Property: Properties are individual pieces of information within a property set. Each property has a name, a data type (e.g., text, number, date), and a value. In the "Wall Properties" set, "Thickness" could be a property with a numerical value.

- Property Single Value: Some properties may have a single value, while others can have multiple values. For example, a wall's material might have a single value (e.g., "Brick") or multiple values to represent complex materials.

- Property Enumeration Value: Some properties use predefined lists of values, known as enumeration values, to ensure consistency. For example, a property for a door's swing direction might have enumeration values like "Inward," "Outward," or "Swing Both Ways."

## References:

1. [IFC4 Documentation](https://standards.buildingsmart.org/IFC/RELEASE/IFC4/FINAL/HTML/)
2. [ifcopenshell.util.element](https://blenderbim.org/docs-python/autoapi/ifcopenshell/util/element/index.html#module-ifcopenshell.util.element)
3. [Youtube video on Export IFC to JSON, Pandas, CSV, Excel (IFC 101 - E.08)](https://youtu.be/RjG_AFiTedE?si=OHe8TauB1foHsSQl)
