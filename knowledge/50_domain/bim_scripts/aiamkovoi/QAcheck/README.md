# SmartCheck — Rule-Based Model Checking in Revit

A pyRevit extension that brings Smart Views-style QA checks into the Revit authoring environment. Define rules in JSON, color-code elements by pass/fail, auto-color by any parameter — all before IFC export.

## What It Does

**RunChecks** — Reads rules from `rules.json`, checks elements across categories, applies color overrides (red/orange/green), prints a report with clickable element IDs and a visual pass/fail summary bar.

**AutoColor** — Pick one or more categories, pick a parameter from a dropdown (populated from the model), and the script colors all elements by distinct values with an auto-generated legend. Option to fade unselected elements to 50% transparency.

**ClearChecks** — Resets all overrides in one click. Silent, no output.

## Included Rules (10)

All based on common openBIM / IDM checks:

| Check | Category | What it catches |
|-------|----------|-----------------|
| Classification missing | Walls, Floors | No Uniformat/OmniClass/NL-SfB code |
| Fire Rating empty | Doors, Windows | Missing fire safety data |
| Room Name not set | Rooms | Unnamed rooms (breaks IFC space validation) |
| Room Number not set | Rooms | No number (COBie/FM handover) |
| Mark empty | Columns, Beams | Missing element identification |
| Material not assigned | Walls | No material for quantity takeoff |
| Type Name not defined | Walls | Elements without a type name |

Adding a new check = adding one JSON object to `rules.json`. No Python changes needed.

## Installation

1. Clone or download this repo
2. Copy `SmartCheck.extension` to your pyRevit extensions folder
   - Default: `%appdata%\pyRevit\Extensions\`
   - Or your custom extensions path
3. Reload pyRevit (pyRevit tab → Reload)
4. SmartCheck tab appears in Revit ribbon

## Requirements

- Revit 2019+
- pyRevit installed

## How Rules Work

```json
{
  "name": "Doors: Fire Rating missing",
  "category": "OST_Doors",
  "parameter": "Fire Rating",
  "condition": "is_empty",
  "color": [255, 0, 0],
  "description": "Fire rating is a common BEP deliverable for doors"
}
```

Supported conditions: `is_empty`, `is_not_empty`, `equals`, `not_equals`, `contains`, `not_contains`, `greater_than`, `less_than`

Parameters are checked on instance first, then type (fallback).

## How It Compares

| | SmartCheck | BIMcollab Zoom Smart Views | Solibri |
|---|---|---|---|
| Runs on | Live Revit model | IFC (post-export) | IFC (post-export) |
| Rules format | JSON | .bcsv | Built-in UI |
| Auto-color | Yes | Yes | Yes |
| Sharing | Git / copy file | BIMcollab cloud | Solibri project |
| Issue tracking | No | Yes | Yes |
| Cost | Free | Licensed | Licensed |


## Built With

pyRevit + Revit API + Claude AI

## License

MIT
