# Revit Assembly Navigator

A **PyRevit + C# DLL-based automation tool** for Autodesk Revit that enables **fast, context-aware selection and navigation of Assemblies** within a BIM model.

Built with a **Python UI layer (PyRevit)** and a **C# backend (Revit API)**, the tool provides a responsive and scalable way to interact with assembly data.

---

## Features

- **List all assemblies** in the active Revit model  
- **Context-aware preselection**  
  - Detects currently selected elements  
  - Automatically resolves and highlights their parent assemblies  
- **Live search & filtering**  
  - Instantly filter assemblies by name  
- **Multi-select with “Select All” (visibility-aware)**  
  - Select only filtered/visible items  
- **Bidirectional sync**  
  - UI → Revit selection  
  - Revit selection → UI state  
- **Auto-zoom to selected assemblies** in the model  
- **Lightweight and modular architecture** (Python + C# DLL)

---

## Tech Stack

- Autodesk Revit API  
- PyRevit (Python)  
- C# (.NET Framework DLL)  

---

## Architecture

```
PyRevit (Python UI Layer)
↓
C# DLL (AssemblyService - Revit API Logic)
↓
Revit Model (Assembly Query, Selection & Navigation)
```

---

## Installation

### 1. Install PyRevit

Download and install PyRevit:  
https://github.com/eirannejad/pyRevit  

Attach it to your installed Revit version.

---

### 2. Add Extension

Copy the extension folder to:

%APPDATA%\pyRevit\Extensions\

---

### 3. Reload

- Open Revit  
- Go to **PyRevit tab**  
- Click **Reload**

---

## Usage

1. Open Revit  
2. Go to **Workshop → BIM Tools**  
3. Click **Assembly Navigator**  
4. Use search to filter assemblies  
5. Select one or multiple assemblies  
6. Click **Select**  
7. Selected assemblies will be highlighted and zoomed in the model  

---

## Project Structure

```
Workshop.extension/
│
├── Workshop.tab/
│   └── BIM Tools.panel/
│       └── Assembly Navigator.pushbutton/
│           ├── script.py
│           └── lib/
│               ├── AssemblyHelper.cs
│               └── AssemblyHelper.dll
│
└── extension.yaml
```

---

## What This Demonstrates

- Revit API integration using C#  
- PyRevit-based UI development  
- Cross-language architecture (Python + C#)  
- Clean separation of UI and logic layers  
- Scalable BIM automation design  

---

## Screenshots

### Revit Ribbon - BIM Tools Tab
![Ribbon](assets/panel.png)

### Assembly Navigator UI
![Assembly Navigator](assets/UI.png)

### Assembly Selection in Model
![Model Selection](assets/model.png)


---

## Author

**Sangeeta Achari**