# Tool architecture


  



  

  

  

  

1. Large Coordinate Protection (Critical for Revit)

  

  

One of the biggest problems with survey coordinates is floating point precision errors in Revit when coordinates are very large.

  

Typical survey coordinates:

Easting: 748221.40

Northing: 2134556.20

Revit geometry becomes unstable beyond roughly:

20 miles from origin

≈ 105,600 ft

Your tool should automatically calculate:

Distance from internal origin

Then warn the user if the building is too far away.

  

  

Add this feature

  

  

The tool should automatically recommend a coordinate shift:

Survey = real world

Revit = local working coordinates

Example output:

Recommended Revit Origin Shift

X = -748000

Y = -2134000

This keeps geometry close to the origin while preserving survey coordinates.

  

  

  

  

2. Unit Conversion Engine

  

  

Your system must support all major BIM units.

  

Inputs may arrive as:

US survey feet

International feet

meters

millimeters

Many surveyors still use US Survey Foot, which differs from International Foot.

  

Conversion difference:

1 US survey foot = 1200/3937 m

1 international foot = 0.3048 m

Your tool should include:

Survey Foot → Revit Foot conversion

Meters → Feet conversion

  

  

  

  

3. Grid Intersection Solver

  

  

Right now you allow a grid intersection input.

  

But you should also allow two grid intersections.

  

Why this matters:

  

Two points define project orientation.

  

Example:

Grid A1 = known coordinate

Grid B1 = known coordinate

From this the tool can calculate:

True project rotation

Formula:

rotation = atan2(ΔEasting , ΔNorthing)

This removes human error in rotation entry.

  

  

  

  

4. Model Alignment Validator

  

  

After setup, the tool should scan the model and verify:

Are linked models aligned?

Are coordinates consistent?

Is project north correct?

Checks include:

Revit internal origin

Survey point

PBP position

True north rotation

Output:

COORDINATE VALIDATION

  

Revit Model: OK

Linked Structural Model: ROTATION MISMATCH

Civil Model: OFFSET ERROR

This becomes extremely valuable in large projects.

  

  

  

  

5. CAD Export Script Generator

  

  

Instead of just showing CAD coordinates, your tool should generate AutoCAD scripts.

  

Output file:

setup_ucs.scr

Example contents:

UCS

W

UCS

Origin

748221.4,2134556.2,100

UCS

Z

12.5

PLAN

C

Users simply run:

SCRIPT

setup_ucs.scr

This automatically sets coordinates in:

  

- AutoCAD
- Plant3D
- CADWorx

  

  

  

  

  

6. Civil 3D Integration

  

  

Civil files typically define:

State Plane Coordinate System

Your tool should store:

Coordinate system name

Datum

Zone

Example:

NAD83 Indiana West

EPSG:2965

This becomes part of the project coordinate report.

  

  

  

  

7. BIM Execution Plan Generator

  

  

Your tool should automatically generate the project coordinate specification.

  

Example output:

PROJECT COORDINATE STANDARD

  

Survey Datum: NAD83

Units: US Survey Feet

  

Revit Setup

Survey Point = 748221.40 , 2134556.20 , 100

  

AutoCAD Setup

UCS Origin = 748221.40 , 2134556.20 , 100

  

Rotation

True North = 12.5°

This becomes the coordination standard document.

  

  

  

  

8. Linked Model Coordinate Push

  

  

The tool should optionally push coordinates into linked models.

  

For example:

Mechanical model

Structural model

Electrical model

Function:

Publish Shared Coordinates

This ensures all teams share the same coordinate system.

  

  

  

  

9. Grid Coordinate Calculator

  

  

Another extremely useful feature:

  

Select any grid intersection and the tool reports:

Northing

Easting

Elevation

This helps during field coordination.

  

Example output:

Grid C4

  

Easting: 748350.12

Northing: 2134677.90

Elevation: 100'

  

  

  

  

10. Model Origin Diagnostic

  

  

Many BIM models already contain bad coordinate setups.

  

Your tool should detect:

Survey point clipped/unclipped

PBP moved incorrectly

model 10 miles from origin

rotation mismatches

Output example:

COORDINATE DIAGNOSTIC

  

Survey Point: Unclipped

PBP Offset: 120000 ft

Rotation Error: 1.5°

  

  

  

  

11. Multi-Software Output Package

  

  

Your tool should produce a coordination package:

/Coordinates

  

Revit_setup.txt

Autocad_ucs.scr

Plant3D_origin.txt

Civil3D_reference.txt

Coordinate_Report.pdf

This becomes the official coordinate setup package for the project.

  

  

  

  

12. Visualization Tool (Very Helpful)

  

  

Your tool could also generate a coordinate diagram.

  

Example:

Internal Origin

Project Base Point

Survey Point

Grid A1

True North

Project North

This helps coordinators visually understand the setup.

  

  

  

  

The Final Tool Architecture

  

  

Your tool would consist of five engines.

Input Engine

Coordinate Math Engine

Software Output Engine

Validation Engine

Documentation Engine

  

  

  

  

If you build all of this…

  

  

You will essentially have created a Universal BIM Coordinate System Engine.

  

Very few companies have something like this internally.

  

It would solve problems across:

  

- Revit
- AutoCAD
- Plant3D
- CADWorx
- Civil3D
- ACC coordination

  

  

  

  

If you’d like, I can also help you design something extremely valuable for this tool:

  

A full mathematical model for coordinate transformations used in survey engineering (translation + rotation matrices).

  

That is the core math behind professional survey software, and implementing it will make your tool extremely accurate.