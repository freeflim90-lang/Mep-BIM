# Open Source Workflow

This folder documents an open-source workflow for thermal transmittance requirement analysis using IDS, Python and JSON.

The workflow was developed as part of a PhD research project focused on BIM, openBIM standards and digital procedures for the analysis of building thermal performance.

## Workflow overview

The open-source workflow is based on the following logic:

```text
IFC / openBIM model
        ↓
IDS information requirements
        ↓
Python-based data extraction and processing
        ↓
JSON file containing thermal transmittance limits
        ↓
comparison between calculated and reference values
        ↓
result interpretation
```

The objective is to test how thermal transmittance-related requirements can be structured and checked through openBIM-oriented and open-source tools.

## Folder structure

```text
02_Open source workflow/
│
├── README.md
│
├── ids/
│   └── Requisiti_informativi_An.En_V03.ids
│
├── python/
│   └── wall_thermal_transmittance_check.py
│
├── json/
│   └── ThermalTransmittanceLimits.json
│
└── images/
    ├── ids-editor-requirements.jpg
    ├── ids-validation-report.jpg
    ├── json-thermal-transmittance-limits.jpg
    └── python-transmittance-check-output.jpg
```

## Main components

### IDS information requirements

The IDS file is used to represent structured information requirements related to thermal transmittance analysis.

In the workflow, IDS supports the definition and checking of the information that must be available in the IFC/openBIM model before running the thermal transmittance analysis.

The IDS-related material is stored in:

```text
ids/
```

The images documenting the IDS workflow are:

```text
images/ids-editor-requirements.jpg
images/ids-validation-report.jpg
```

### Python script

The Python script is stored in:

```text
python/wall_thermal_transmittance_check.py
```

The script documents a prototype workflow based on `ifcopenshell`.

Its role is to:

1. open an IFC model;
2. identify `IfcWall` elements;
3. identify the `IfcSpace` entities related to each wall through space-boundary relationships;
4. extract wall material layers;
5. read layer thickness and thermal conductivity values;
6. identify walls separating heated and non-heated spaces;
7. calculate thermal resistance and wall thermal transmittance;
8. compare the calculated U-value with the reference value stored in the JSON file.

The script is a research prototype and must be adapted to the structure of the IFC model used in each application.

### JSON thermal transmittance limits

The JSON file is stored in:

```text
json/ThermalTransmittanceLimits.json
```

The file structures thermal transmittance limits according to:

- type of intervention;
- building envelope category;
- climate zone;
- building element type.

The JSON file is used by the Python script to compare calculated U-values with reference limits.

The values are included for research and methodological purposes. They must always be checked against the current applicable legislation, standards or official documents before any professional or operational use.

The related image is:

```text
images/json-thermal-transmittance-limits.jpg
```

## Python output

The workflow produces a textual output showing calculated thermal transmittance values and whether the checked elements satisfy the selected reference limit.

The related image is:

```text
images/python-transmittance-check-output.jpg
```

## Role in the research workflow

This open-source workflow represents an alternative to the proprietary Revit/Dynamo workflow documented in the other folder of the repository.

It demonstrates how openBIM-oriented information requirements and open-source tools can be combined to support thermal performance analysis.

The workflow connects:

- IFC data;
- IDS requirements;
- material layer information;
- thermal conductivity values;
- JSON-structured reference limits;
- Python-based checking procedures.

## Data and privacy note

This folder is intended to publish research scripts, IDS files, JSON files and documentation images.

The folder does not include:

- confidential IFC models;
- private project data;
- local file paths;
- credentials;
- non-public case-study material.

The Python script contains placeholder paths and must be adapted locally before execution.

## Limitations

This folder documents a research prototype.

It is not intended as:

- a certified regulatory compliance tool;
- an official legal verification system;
- production-ready software;
- a substitute for professional technical assessment;
- a substitute for official standards, laws or regulatory documents.

The workflow should be interpreted as a methodological prototype for structuring and checking thermal transmittance-related information in BIM/openBIM contexts.
