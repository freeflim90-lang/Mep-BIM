# Thermal Transmittance Workflows

This repository contains proprietary and open-source workflows developed as part of a PhD research project on the use of BIM, openBIM standards and digital procedures for the analysis of building thermal performance.

The repository focuses on workflows for structuring, checking and visualizing thermal transmittance requirements in BIM/openBIM processes.

Two alternative approaches are documented:

1. a proprietary workflow based on Revit and Dynamo;
2. an open-source workflow based on IDS, Python and JSON.

## Research context

This repository is part of the digital companion material of the PhD thesis:

**Utilizzo della metodologia BIM (Building Information Modeling) e degli standard openBIM per le analisi e il monitoraggio delle prestazioni termiche di edifici storici**

The research investigates how BIM, HBIM, openBIM standards and computational workflows can support:

- building performance analysis;
- thermal transmittance checks;
- structured management of regulatory requirements;
- comparison between proprietary and open-source workflows;
- interoperability-oriented procedures for building analysis;
- decision support in design, assessment and heritage-related contexts.

## Repository structure

```text
thermal-transmittance-workflows/
│
├── README.md
├── CITATION.cff
├── LICENSE
├── .gitignore
│
├── 01_Proprietary workflow/
│   ├── README.md
│   ├── dynamo/
│   └── images/
│
└── 02_Open source workflow/
    ├── README.md
    ├── ids/
    ├── python/
    ├── json/
    └── images/
```

## Workflow overview

The repository documents two complementary ways of approaching thermal transmittance and regulatory requirement analysis in BIM/openBIM environments.

### 1. Proprietary workflow

The proprietary workflow is based on:

```text
Revit model
        ↓
Dynamo workflow
        ↓
thermal transmittance-related data extraction
        ↓
thermal requirement processing
        ↓
visualization or interpretation of results
```

This part of the repository documents how thermal transmittance-related information and requirement checks can be managed through Autodesk-based tools.

The related files are stored in:

```text
01_Proprietary workflow/
```

This folder includes Dynamo files and images documenting the proprietary workflow.

### 2. Open-source workflow

The open-source workflow is based on:

```text
IFC / openBIM data
        ↓
IDS information requirements
        ↓
JSON file containing thermal transmittance limits
        ↓
Python-based checking procedure
        ↓
output / result interpretation
```

This part of the repository documents how thermal transmittance requirements can be structured and checked using openBIM-oriented tools and open data structures.

The related files are stored in:

```text
02_Open source workflow/
```

This folder includes IDS files, Python scripts, JSON files and images documenting the open-source workflow.

## Main components

### Revit and Dynamo

The proprietary workflow explores how building elements and related parameters can be processed through Dynamo scripts in a Revit-based environment.

The workflow is used to support the extraction, organization and interpretation of information related to thermal transmittance requirements.

### IDS files

The open-source workflow uses IDS files to represent structured information requirements.

IDS is used here as part of an openBIM-oriented strategy to formalize the information needed for checking thermal transmittance-related requirements.

### JSON transmittance limits

The open-source workflow uses JSON files to structure thermal transmittance limits and related requirement values.

The JSON file organizes reference values according to:

- type of intervention;
- building envelope category;
- climate zone;
- building element type.

These values are included for research and methodological purposes.

They should always be checked against the current applicable legislation, standards or official documents before any professional or operational use.

### Python scripts

Python scripts are used to read structured information, process thermal requirement data and support comparison or checking procedures.

The open-source script is based on the extraction of IFC information, including wall-space relationships, material layers and thermal conductivity values, followed by the calculation and comparison of wall thermal transmittance values.

The scripts are research prototypes and are not intended as certified regulatory compliance tools.

## Role in the research workflow

This repository supports the part of the research related to the analysis of building thermal performance and the management of thermal transmittance requirements.

It documents how similar analytical objectives can be approached through:

- proprietary BIM tools;
- open-source and openBIM-oriented tools;
- structured information requirements;
- external data files;
- computational checking procedures.

The aim is not only to perform a specific calculation, but to demonstrate how information can be structured, exchanged and checked across different BIM/openBIM workflows.

## Data and privacy note

This repository is intended to publish research workflows, scripts, templates and documentation.

The repository should not include:

- confidential building models;
- private Revit files;
- sensitive IFC models;
- real project data not intended for publication;
- private paths;
- credentials;
- personal data;
- unpublished or restricted case-study information.

Where needed, example files, templates or anonymized material should be used instead of real project files.

## Limitations

The materials in this repository are research prototypes and methodological workflows.

They are not intended as:

- certified regulatory compliance tools;
- official legal verification systems;
- production-ready software;
- substitutes for professional technical assessment;
- substitutes for official standards, laws or regulatory documents.

Thermal transmittance limits and regulatory values must always be verified against the official applicable sources before any professional use.

## Citation

If you use or refer to this repository, please cite the related PhD thesis and this repository.

Suggested citation:

Fontanella, L. (2026). *Thermal Transmittance Workflows: proprietary and open-source procedures for BIM/openBIM-based thermal requirement analysis*. GitHub repository.

## Author

Luca Fontanella  
Università Iuav di Venezia  
PhD programme: Culture del progetto
