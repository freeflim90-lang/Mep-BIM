# Proprietary Workflow

This folder documents a proprietary workflow for thermal transmittance analysis developed in a BIM environment using Autodesk Revit and Dynamo.

The workflow was developed as part of a PhD research project focused on BIM, openBIM standards and digital procedures for the analysis of building thermal performance.

## Workflow overview

The proprietary workflow is based on the following logic:

```text
Revit model
        ↓
identification of building spaces and building envelope elements
        ↓
Dynamo-based extraction and processing of data
        ↓
thermal transmittance-related analysis
        ↓
result interpretation
```

The workflow explores how thermal transmittance-related information can be managed through Autodesk-based tools in a BIM process.

## Folder structure

```text
01_Proprietary workflow/
│
├── README.md
├── dynamo/
│   └── WallThermalTransmittance.dyn
└── images/
    ├── revit-heated-room-and-wall-layers.jpg
    └── dynamo-wall-thermal-transmittance.jpg
```

## Main components

### Revit model environment

The workflow is based on a Revit model in which building elements and spaces are organized and parameterized for thermal analysis purposes.

A relevant aspect of the workflow is the identification of heated spaces and the definition of the building envelope elements associated with them.

For example, the workflow considers the distinction between heated and non-heated rooms, which affects the interpretation of thermal transmittance requirements.

The repository does not include the original Revit model.

### Dynamo script

The Dynamo script included in this folder is:

```text
dynamo/WallThermalTransmittance.dyn
```

The script documents a proprietary workflow developed to support the extraction and organization of thermal transmittance-related information from the BIM model.

The exact behavior of the script depends on the structure of the Revit model, the available parameters and the logic implemented in the Dynamo graph.

The script should therefore be interpreted as a research workflow and may require adaptation before reuse in other models.

## Images

The `images` folder includes screenshots documenting the proprietary workflow.

### 1. Revit space and wall information

```text
images/revit-heated-room-and-wall-layers.jpg
```

This image shows an example of the Revit model environment used in the workflow.

The screenshot documents two relevant aspects:

- the use of a room parameter such as **"Heated room"** to identify thermally relevant spaces;
- the layered composition of a wall assembly, including thickness and material-related information.

These data are important for thermal transmittance analysis because they help define the thermal role of spaces and envelope elements.

### 2. Dynamo-based thermal workflow

```text
images/dynamo-wall-thermal-transmittance.jpg
```

This image shows the Dynamo environment used to process wall-related information extracted from the Revit model.

The screenshot illustrates the use of a Dynamo graph for organizing and interpreting data connected to thermal transmittance analysis.

## Role in the research workflow

This proprietary workflow represents one of the methodological approaches explored in the research.

Its role is to test how BIM-based thermal information can be managed through commercial software tools, in parallel with the open-source/openBIM workflow documented in the other section of the repository.

The workflow contributes to:

- extracting information from BIM models;
- organizing thermal analysis inputs;
- supporting thermal transmittance-related reasoning;
- comparing proprietary and open-source approaches.

## Data and publication note

This folder is intended to document the workflow structure and the research logic.

It does not include:

- the original Revit model;
- confidential project data;
- private local paths;
- restricted files not intended for publication.

Only the Dynamo script and selected screenshots are published here for research documentation purposes.

## Limitations

This folder documents a research workflow and should not be interpreted as:

- a complete commercial software package;
- a certified thermal verification tool;
- a substitute for official regulatory assessment;
- a ready-to-use workflow applicable without adaptation.

The script and the illustrated procedure may require model-specific customization depending on the BIM structure, parameters and intended use.
