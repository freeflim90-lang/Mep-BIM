# Starter — Track 5~8 Complete Lessons + BIM Check Friday

All lessons follow the standard LUA BIM LABS format.
Language: English
Status: Production-ready

---

## Track 5 — Clash Coordination Basics (Days 31–38)

---

### Day 31 — Navisworks Basics

**1. Why This Matters**
Navisworks is the industry-standard tool for clash detection and coordination review — knowing how to navigate it is a baseline skill expected on any BIM coordination project.

**2. Core Concept**
Navisworks is a model aggregation and review tool. It lets you combine models from multiple disciplines (HVAC, plumbing, structure, architecture) into one federated model for clash checking and visual review.

Key elements:
- **Append vs. Merge**: Append adds models as separate items; Merge combines them into one file
- **NWC files**: Navisworks Cache files exported from Revit — lightweight and fast to load
- **NWD files**: Packaged project files that bundle all appended models
- **Selection Tree**: Left-side panel showing the file/model hierarchy
- **Clash Detective**: The module where clash tests are run and results are reviewed
- **Viewpoint**: A saved camera position used to document and revisit specific clash locations

**3. Real Project Lens**
On a mid-size commercial project, the MEP coordinator receives NWC exports from the mechanical, electrical, and plumbing modelers every Friday. These are appended into a single NWD file in Navisworks, and the Clash Detective test is re-run to capture new conflicts introduced that week.

**4. BIM Check**
- Check: Can you open a NWC file in Navisworks and see the model geometry?
- Check: Can you identify the Selection Tree panel and expand it to see individual model files?
- Check: Can you locate the Clash Detective module in the Home tab ribbon?

**5. Common Mistake**
Beginners often open only one discipline's model and run clashes against itself. Clash detection is only useful when two or more models from different disciplines are appended together.

**6. Today's Action**
Open Navisworks (or Navisworks Freedom if you don't have a license), load a sample NWC file, and practice saving a viewpoint at one location in the model.

---

### Day 32 — Clash Grouping and Prioritization

**1. Why This Matters**
A single clash test can return hundreds or thousands of results — without grouping and prioritization, the coordination team wastes time reviewing the same clash multiple times or fixing low-priority items first.

**2. Core Concept**
After running a clash test, results must be organized before the coordination meeting. Grouping and prioritization reduce noise and focus effort where it matters most.

Key approaches:
- **Group by Grid**: Clusters clashes in the same structural bay together — useful for large floor plates
- **Group by Level**: Separates clashes by floor, so each trade knows which level to address
- **Group by Assigned**: Lets you assign clashes to specific people or companies for resolution
- **Status tags**: New, Active, Reviewed, Approved, Resolved — each clash moves through these states
- **Priority tiers**: Critical (blocks structure or ceiling install), Major (requires rerouting), Minor (can be resolved with small adjustment)

**3. Real Project Lens**
A plumbing coordinator running a test against structural steel might see 420 raw clashes. After grouping by level and filtering out "Reviewed" items from last week, the active list drops to 38 clashes — all on Level 3, all involving the same beam run. This focused list drives the agenda for the Thursday coordination meeting.

**4. BIM Check**
- Check: Can you group clashes in Clash Detective by Grid or Level using the "Group" dropdown?
- Check: Can you change the status of a clash from "New" to "Active"?
- Check: Can you assign a clash to a specific model file or discipline?

**5. Common Mistake**
Teams that skip grouping tend to fix clashes in random order. This leads to trades rerouting pipes around a beam that will itself be modified next week — wasted effort that proper prioritization would have prevented.

**6. Today's Action**
In a Navisworks file with at least two models appended, run a clash test and manually tag three clashes as Critical, Major, and Minor based on what you observe at each location.

---

### Day 33 — Clash Report Reading

**1. Why This Matters**
The clash report is the official output of coordination — every stakeholder, from the project manager to the subcontractor, uses it to understand what needs to be fixed and by whom.

**2. Core Concept**
Navisworks can export clash reports in multiple formats. Understanding what each field means lets you use the report as a working document, not just a printout.

Key fields in a clash report:
- **Clash Name/ID**: Unique identifier (e.g., MEP-STRUCT-0045) used to track the item across meetings
- **Status**: Current state — New, Active, Reviewed, or Resolved
- **Distance**: The depth of penetration for a hard clash (negative = overlap in mm)
- **Element 1 / Element 2**: The two objects in conflict — includes Element ID, file source, and category
- **Assigned To**: Responsible party for resolution
- **Image**: Viewpoint screenshot embedded in the report showing the clash location
- **Found / Approved Date**: Timeline markers for coordination tracking

**3. Real Project Lens**
A junior BIM coordinator receives a clash report PDF before a meeting. By scanning the "Element 1 / Element 2" columns, they can quickly identify that most conflicts are between the HVAC ductwork (from the mechanical model) and the structural steel (from the structural model) — and that the structural engineer has already marked seven of those as "Approved" because the duct can pass through a web penetration.

**4. BIM Check**
- Check: Can you identify the Element ID for both elements in a clash from the report?
- Check: Can you find which model file (NWC) each clashing element came from?
- Check: Can you read the distance value and understand whether it represents a gap or an overlap?

**5. Common Mistake**
Beginners often confuse "Reviewed" with "Resolved." Reviewed means someone has looked at the clash; Resolved means the physical conflict has been eliminated in the model. Treating them as the same leads to false close-outs.

**6. Today's Action**
Find a sample Navisworks clash report (Autodesk provides examples online) and locate five clashes. For each one, write down the two elements involved and the current status.

---

### Day 34 — Coordination Meetings Basics

**1. Why This Matters**
The coordination meeting is where clashes get resolved — or get delayed. Knowing how these meetings work helps you contribute effectively rather than sit silently through them.

**2. Core Concept**
MEP coordination meetings bring together representatives from each trade and discipline to review clash results, assign responsibility, and agree on resolution paths. They follow a predictable structure.

Typical meeting flow:
- **Pre-meeting prep**: Coordinator filters clash list to only open/active items for that week's zone
- **Screen share**: Clash Detective or a pre-exported report is displayed for the group
- **Clash-by-clash review**: Each open item is shown in 3D; trades discuss root cause
- **Resolution decision**: One of three outcomes — Fix (trade commits to reroute), Hold (pending design info), or Accept (no physical change needed, but documented)
- **Action assignment**: Name + deadline added to each item in the issue tracker
- **Meeting minutes**: Written record sent within 24 hours listing all decisions

**3. Real Project Lens**
On a hospital MEP package, the weekly coordination meeting covers Level 5 only. The mechanical sub commits to dropping a 600mm duct by 150mm to clear a structural beam. The plumbing sub agrees to shift a waste stack 200mm east. Both decisions are logged in the issue tracker with a two-week resolution deadline before the next review.

**4. BIM Check**
- Check: Can you describe the difference between a "Fix," "Hold," and "Accept" resolution outcome?
- Check: Can you identify who typically chairs an MEP coordination meeting on a large project?
- Check: Can you explain why meeting minutes matter beyond just documentation?

**5. Common Mistake**
Attending coordination meetings without a prepared clash list for your discipline means you cannot speak to your own items. Always know which clashes belong to your trade before entering the room.

**6. Today's Action**
Write a short outline (5–6 bullet points) of how you would prepare for your first coordination meeting as a junior MEP BIM modeler — what would you check and bring?

---

### Day 35 — Issue Tracking in BIM Projects

**1. Why This Matters**
Verbal agreements in meetings disappear — a formal issue tracker turns coordination decisions into documented, assignable, auditable records that protect all parties.

**2. Core Concept**
Issue tracking is the process of logging, assigning, and closing coordination problems through a structured system. It is distinct from the clash report — the tracker is a live working document.

Common tools and methods:
- **BIM 360 / ACC Issues**: Cloud-based, linked to model elements, visible to all project team members
- **Revit Worksharing Monitor + Comments**: Simple in-model notes for small teams
- **Excel-based trackers**: Still widely used on projects without a cloud platform
- **Key fields in any tracker**: Issue ID, Description, Location (grid/level), Assigned To, Due Date, Status, Resolution Notes, Closed By, Closed Date
- **Status lifecycle**: Open → In Progress → Resolved → Verified → Closed

**3. Real Project Lens**
On a data center project, the MEP coordinator uses Autodesk Construction Cloud (ACC) Issues. Each clash that requires a trade response is logged as an Issue pinned to the 3D model. The mechanical subcontractor receives an email notification and can mark it "In Progress" from their mobile app on site. The coordinator verifies the fix in the updated model before closing the issue.

**4. BIM Check**
- Check: Can you describe the minimum five fields an issue tracker entry should contain?
- Check: Can you explain the difference between "Resolved" (trade says it's fixed) and "Verified" (coordinator confirmed in model)?
- Check: Can you identify which issue tracking tool your current project or employer uses?

**5. Common Mistake**
Logging issues without assigning a clear owner and due date makes the tracker useless. Every open issue must have a name and a deadline — without both, nothing gets resolved.

**6. Today's Action**
Create a simple 6-column issue tracker template in Excel or Google Sheets: Issue ID, Description, Location, Assigned To, Due Date, Status. Add three fictional issues and practice filling out each field.

---

### Day 36 — Common Clash Resolution Patterns

**1. Why This Matters**
Most MEP clashes are resolved using one of a small set of standard approaches — recognizing these patterns lets you contribute to resolution discussions even as a junior team member.

**2. Core Concept**
Rather than treating each clash as a unique problem, experienced coordinators recognize resolution patterns that apply repeatedly across projects.

The most common patterns:
- **Elevation drop/raise**: Duct or pipe shifts up or down to clear a beam or other system — most frequent resolution
- **Horizontal offset**: Pipe or conduit moves left or right within tolerance to clear a parallel run
- **Size reduction with velocity check**: Duct is reduced in size (and velocity re-checked by engineer) to fit within the available zone
- **Penetration through structure**: A sleeve or core is added to structural element — requires structural engineer approval
- **System re-routing**: An entire run is redesigned along a different path — used when no small adjustment is possible
- **Accept with clearance note**: The clash is accepted as-is because the elements are flexible (e.g., a cable tray with a pipe that has documented clearance)

**3. Real Project Lens**
In a corridor ceiling space with 350mm clearance, a 400mm HVAC duct clashes with a structural beam. The resolution is to offset the duct horizontally by 600mm around the beam end, reconnect it with two 45-degree elbows, and maintain the same invert elevation. This is a horizontal offset combined with elevation preservation — a pattern the team has used on every floor of the same building.

**4. BIM Check**
- Check: Can you name three resolution patterns and describe when each one is appropriate?
- Check: Can you explain why a size reduction on a duct requires engineer confirmation before the model is updated?
- Check: Can you identify which pattern requires approval from a structural engineer before implementation?

**5. Common Mistake**
Junior modelers sometimes fix a clash by moving an element without checking whether the new position creates a new clash with a third system. Always re-run the test after making a resolution change.

**6. Today's Action**
Pick one clash resolution pattern and sketch (on paper or digitally) what it looks like in section view — show the original position, the conflict, and the resolved position.

---

### Day 37 — Coordination Drawing Check

**1. Why This Matters**
A coordination drawing is only useful if it accurately reflects the agreed resolutions — checking it before issue means catching errors before they reach the construction team.

**2. Core Concept**
A coordination drawing (also called a coordination sheet or MEP coordination plan) is a 2D drawing produced from the federated model that shows all MEP systems in a defined zone, used by site teams to install work without conflicts.

What to check before issuing a coordination drawing:
- **Model status**: Is the drawing exported from the latest clash-resolved model — not a two-week-old version?
- **Elevation annotations**: Are pipe/duct inverts clearly labeled at changes in direction or crossings?
- **Clearance zones**: Is maintenance access space shown for major equipment?
- **Grid references**: Are structural grid lines shown as reference so site can orient the drawing?
- **Revision cloud**: If this is an updated issue, is the change area marked with a revision cloud?
- **Title block data**: Is the issue date, revision number, and zone name correct?
- **Clash status**: Have all Critical and Major clashes in this zone been resolved before issue?

**3. Real Project Lens**
A BIM coordinator issues a Level 2 plant room coordination drawing without checking the model version. The drawing shows a chilled water pipe at 2800mm FFL, but that pipe was lowered to 2650mm FFL in the model two days ago to resolve a beam clash. The mechanical installer sets out to the old elevation and drills brackets in the wrong position — a rework event that costs half a day.

**4. BIM Check**
- Check: Can you verify which model version a coordination drawing was generated from by checking the title block or issue log?
- Check: Can you identify whether all Major clashes in a zone have been resolved before a drawing is issued?
- Check: Can you confirm that all pipe and duct elevations are annotated at key change points in the drawing?

**5. Common Mistake**
Issuing a coordination drawing with unresolved Major clashes marked as "TBC" on site. If a clash is not resolved in the model, it is not resolved — site will have to improvise, and the result will not match the BIM.

**6. Today's Action**
Find a sample MEP coordination drawing (search "MEP coordination drawing example" online). Identify three pieces of annotation information and check whether each one is clearly readable at a standard print scale.

---

### Day 38 — Track 5 Review — Clash Coordination Basics

**1. Why This Matters**
Clash coordination is the activity that connects BIM modeling to real construction — reviewing the core concepts ensures you can participate in the process, not just observe it.

**2. Core Concept**
Track 5 covered the full clash coordination workflow from tool setup to drawing issue. Here is a structured recap:

| Day | Topic | Key Takeaway |
|-----|-------|--------------|
| 31 | Navisworks Basics | Append NWC files; use Clash Detective; save viewpoints |
| 32 | Grouping & Prioritization | Group by level/grid; assign Critical/Major/Minor |
| 33 | Clash Report Reading | Read Element IDs, status, distance; know Reviewed vs. Resolved |
| 34 | Coordination Meetings | Prepare your discipline's open clashes; Fix / Hold / Accept |
| 35 | Issue Tracking | Log with owner and due date; track Open → Closed lifecycle |
| 36 | Resolution Patterns | Elevation shift, offset, re-route, penetration, accept |
| 37 | Coordination Drawing Check | Verify model version, elevations, grid refs, revision cloud |

**3. Real Project Lens**
A junior MEP BIM coordinator on a commercial office project uses every skill from this track in a single week: they export NWC files, run the clash test, group results by level, attend the coordination meeting, log new issues in the tracker, update the model with resolutions, and issue an updated coordination drawing for Level 4 by Friday.

**4. BIM Check**
- Check: Can you explain the difference between a hard clash and a soft clash without notes?
- Check: Can you describe the five status stages of an issue tracker entry?
- Check: Can you name three clash resolution patterns and give a one-sentence use case for each?

**5. Common Mistake**
Treating clash coordination as a software task rather than a communication task. The tools (Navisworks, issue tracker, coordination drawings) are only as effective as the communication and agreements that happen around them.

**6. Today's Action**
Write a one-paragraph summary of the clash coordination workflow — from model export to coordination drawing issue — as if explaining it to someone joining the project next week.

---

## Track 6 — Data and Schedule Basics (Days 39–47)

---

### Day 39 — What Is a Revit Schedule?

**1. Why This Matters**
Revit schedules turn model elements into structured data tables — they are how engineers, contractors, and project managers extract real information from a BIM model without manually counting or measuring.

**2. Core Concept**
A Revit schedule is a view type that reads parameter values from model elements and displays them as a table. It is live — when the model changes, the schedule updates automatically.

Key concepts:
- **Schedule View**: Found in the Project Browser under Views > Schedules
- **Fields**: The columns in your schedule, each mapped to an element parameter (e.g., Family, Type, Level, Mark, System Classification)
- **Filter**: Limits rows to a subset of elements (e.g., only Level 3, only HVAC supply air)
- **Sorting/Grouping**: Organizes rows by a field value — commonly by Level or System
- **Calculated Value**: A custom column that performs a formula (e.g., total duct length = quantity × length)
- **Totals**: Footers that sum numeric fields for a group or the entire schedule

**3. Real Project Lens**
An MEP BIM coordinator creates a Mechanical Equipment Schedule in Revit by adding fields for Mark, Family, Type, Level, System Type, and Flow Rate. After filtering to Level 5 only, the schedule shows 12 fan coil units with their flow parameters — exactly what the mechanical engineer needs to cross-check against the design specification.

**4. BIM Check**
- Check: Can you locate the Schedule view type in the Revit View tab and create a new schedule from scratch?
- Check: Can you add and remove fields (columns) in a schedule using the Schedule Properties dialog?
- Check: Can you apply a filter to show only elements on a specific level?

**5. Common Mistake**
Creating a schedule without setting a filter and including elements from all levels — the resulting table mixes data from every floor, making it unreadable and unreliable for any specific use.

**6. Today's Action**
In Revit, create a new Mechanical Equipment Schedule with at least four fields: Mark, Family Name, Type Name, and Level. Apply a filter to show only one level and count the results.

---

### Day 40 — MEP Equipment Schedule Basics

**1. Why This Matters**
MEP equipment schedules are a standard project deliverable — they link the BIM model to specifications, procurement lists, and commissioning records, and they are reviewed by engineers and clients alike.

**2. Core Concept**
An MEP equipment schedule documents the key parameters of each piece of mechanical, electrical, or plumbing equipment in the model. It is often contractually required as part of the BIM deliverable.

Typical fields for an MEP equipment schedule:
- **Mark**: Unique equipment tag (e.g., AHU-01, FCU-L3-04) — must be set per element
- **Family and Type**: The Revit family name and type (describes the equipment category and size)
- **Level**: Which floor the equipment is located on
- **System Classification / System Name**: The HVAC or plumbing system the equipment belongs to
- **Flow Rate / Capacity**: Design parameter values — must be filled in manually or from the design spec
- **Manufacturer / Model**: Often left blank in early BIM but required for procurement and commissioning
- **Comments**: Free-text field for coordination notes or status flags

**3. Real Project Lens**
On a hotel project, the BIM coordinator produces a Fan Coil Unit Schedule filtered by floor. The schedule shows 48 FCUs across Levels 3–8, but 11 of them have no Mark value set, and 6 have no flow rate entered. The coordinator flags this to the mechanical modeler before the schedule is submitted to the engineer — preventing an incomplete deliverable from leaving the project team.

**4. BIM Check**
- Check: Can you verify that every piece of equipment in a schedule has a unique Mark value?
- Check: Can you identify which fields in an equipment schedule are model-driven vs. manually entered?
- Check: Can you filter the schedule to show only equipment with missing or blank parameter values?

**5. Common Mistake**
Submitting an equipment schedule with blank Mark fields. Unmarked equipment cannot be tracked, purchased, or commissioned — every item must have a unique, readable tag before the schedule leaves the model.

**6. Today's Action**
Open an existing Revit project (or a sample model) and find the equipment schedule. Identify three elements where a required field is blank, and manually enter placeholder values to test how the schedule updates live.

---

### Day 41 — Duct and Pipe Schedule Configuration

**1. Why This Matters**
Duct and pipe schedules are used to verify that system sizes match the design specification and to generate material takeoff quantities — both are essential for procurement and QA.

**2. Core Concept**
Unlike equipment schedules (which list individual pieces), duct and pipe schedules typically aggregate by type and size. Configuration choices directly affect whether the output is useful or misleading.

Key configuration steps:
- **Category selection**: Choose Ducts or Pipes as the schedule category — do not mix them
- **Fields to include**: Size (Width × Height or Diameter), Length, Level, System Name, Insulation Thickness, Material/Specification
- **Itemize Every Instance vs. Group**: "Group by" similar elements to get total lengths by size; ungroup to see every segment individually
- **Calculated Length column**: Revit reports duct/pipe length in the model unit — verify it matches your project units (mm or m)
- **Sorting by size**: Sort by Width then Height (for rectangular duct) to create a readable size-ordered table
- **Phase filter**: Make sure the schedule phase matches the construction phase of the model

**3. Real Project Lens**
A mechanical coordinator configures a Duct Schedule grouped by size and system. After grouping, the schedule shows 85 meters of 600×300mm supply air ductwork on Level 2. The mechanical engineer cross-checks this against the design calculation sheet, which shows 88 meters — a 3-meter discrepancy that leads to discovering one run was modeled at an incorrect size.

**4. BIM Check**
- Check: Can you create a Duct Schedule that groups elements by size and shows total length per size?
- Check: Can you verify the unit of the Length field matches your project's unit setting?
- Check: Can you filter the schedule to show only ducts within a specific system (e.g., supply air only)?

**5. Common Mistake**
Using the default "itemize every instance" setting for a duct schedule on a large model — this produces thousands of rows of individual duct segments and is unreadable for any practical use. Always group by size when producing a takeoff schedule.

**6. Today's Action**
In Revit, create a Duct Schedule with at minimum these fields: Size, Length, Level, System Name. Group the rows by Size and confirm that the Length column shows a summed total for each size group.

---

### Day 42 — Parameter Completeness Check

**1. Why This Matters**
A model with missing parameter values fails BIM LOD requirements and produces unreliable schedules and reports — checking completeness before submission is a professional responsibility.

**2. Core Concept**
Parameter completeness means every required field for every element contains a valid, non-blank value. It is one of the most common BIM quality check items.

How to check parameter completeness in Revit:
- **Schedule-based check**: Create a schedule for the target category, add all required fields, then sort by the field you want to check — blank values appear first or last
- **Filter trick**: Add a filter where a field "does not equal" a known valid value — any blank entries will appear in the filtered view
- **Dynamo**: Write a simple script that flags elements with empty required parameters and outputs a list with Element IDs
- **BIM Collab / Solibri**: Model checker tools can run automated parameter completeness rules across an entire federated model
- **Project parameters vs. shared parameters**: If a parameter isn't showing values, verify it was added as a shared parameter, not a project parameter — shared parameters can be scheduled and exported; project parameters cannot always be shared across files

**3. Real Project Lens**
Before submitting the MEP model for a BIM Level 2 milestone review, the BIM coordinator runs a parameter completeness check across all mechanical equipment. The schedule reveals that 23 out of 140 elements have no "Mark" value and 11 have no "System Name" assigned. These are fixed before submission, preventing the model from failing the client's BIM checker tool.

**4. BIM Check**
- Check: Can you create a Revit schedule that clearly shows which elements have a blank value in a required field?
- Check: Can you explain the difference between a shared parameter and a project parameter in terms of schedule availability?
- Check: Can you name two tools (beyond Revit schedules) that can automate parameter completeness checking?

**5. Common Mistake**
Assuming that if a field shows a value in the Properties panel for one element, all similar elements also have that value. Parameter completeness must be checked across the entire category, not element by element.

**6. Today's Action**
Pick one element category in your Revit model (e.g., Mechanical Equipment or Pipes). Create a schedule with four key fields and sort by each field to identify any blank values. Write down how many elements are incomplete.

---

### Day 43 — Exporting Data from Revit

**1. Why This Matters**
BIM data is only useful if it can reach the people who need it — engineers, contractors, facility managers. Knowing how to export data correctly prevents information getting lost in translation.

**2. Core Concept**
Revit offers multiple data export paths depending on the target audience and use case.

Common export methods:
- **Export Schedule to .txt or .csv**: In any schedule view, go to File > Export > Reports > Schedule — produces a tab-delimited or comma-separated file readable in Excel
- **Export to IFC**: File > Export > IFC — the universal open format for sharing BIM data with non-Revit tools; preserves element parameters and geometry
- **Export to CAD (DWG/DXF)**: File > Export > CAD Formats — for teams working in 2D CAD; loses most BIM parameter data
- **Dynamo to Excel**: A Dynamo script can write parameter values directly to an Excel file with precise column mapping — preferred for complex data exports
- **Navisworks (NWC)**: Export via the Navisworks plugin from Revit — carries parameter data into Navisworks for clash detection and model review
- **ODBC/Linked database**: Advanced — links Revit to an external database; rarely used on standard projects

**3. Real Project Lens**
The project manager on a healthcare project needs an equipment list for procurement. The BIM coordinator exports the Mechanical Equipment Schedule as a CSV from Revit, opens it in Excel, formats it with the project's procurement template headers, and sends it to the purchasing team — a 10-minute task that replaces what used to be a full day of manual counting.

**4. BIM Check**
- Check: Can you export a Revit schedule as a .csv file and open it successfully in Excel?
- Check: Can you explain what data is preserved and what is lost when exporting from Revit to DWG?
- Check: Can you name the Revit export format used when sharing the model with teams using non-Autodesk software?

**5. Common Mistake**
Exporting a schedule without checking the unit settings first. If the Revit file uses millimeters but the export is read by a team expecting meters, every length value will appear 1,000 times larger than reality — a procurement error waiting to happen.

**6. Today's Action**
Export any schedule from Revit (or a sample model) as a .csv file. Open it in Excel or Google Sheets and verify that the column headers, values, and units appear as expected.

---

### Day 44 — Tracking Model Changes

**1. Why This Matters**
On live projects, the model is modified daily — without change tracking, coordination decisions made last week may be unknowingly overwritten, creating conflicts that were supposed to be resolved.

**2. Core Concept**
Model change tracking records what changed in the model, when, and by whom. It supports accountability, coordination integrity, and audit trails.

Methods and tools:
- **Revit Worksharing / Central Model history**: In a workshared project, the server log records which user synced changes and when — accessible through Manage > Worksharing Monitor
- **Model Version naming**: A discipline-standard naming convention (e.g., MEP_L2_COORD_v03_2026-05-29.rvt) lets teams track model states without in-software tools
- **BIM 360 / ACC Model Versioning**: Cloud-hosted Revit files record every publish event with a timestamp and user — accessible from the project's Files dashboard
- **Revision table in drawings**: Formal issued drawings carry a revision block tracking drawing-level changes, not model-level
- **Change log (manual)**: A shared document (often Excel) where modelers record what they changed, why, and which coordination item it relates to

**3. Real Project Lens**
A mechanical modeler makes 14 duct routing changes to resolve coordination items but does not sync the central file until end of day Friday. A clash test run by the coordinator on Thursday afternoon reflects the old model state. The Friday sync updates the model, but the Thursday clash report was already sent to the site team — causing confusion about which routes are current.

**4. BIM Check**
- Check: Can you view the worksharing history of a Revit central file to see recent sync events?
- Check: Can you describe a model file naming convention that makes version history readable without opening the file?
- Check: Can you explain why running a clash test on an out-of-date NWC file produces unreliable results?

**5. Common Mistake**
Saving the Revit file locally and not syncing to the central model. Local changes are invisible to everyone else on the project until synced — always sync after completing coordination-related edits.

**6. Today's Action**
Write a short model version naming convention for a fictional project — include project code, discipline code, zone, version number, and date. Test it by writing three "version" names that show progression over two weeks.

---

### Day 45 — Revision and Change Management in BIM

**1. Why This Matters**
Design changes after coordination is underway are one of the biggest sources of rework — having a clear change management process protects both the BIM team and the construction team from avoidable errors.

**2. Core Concept**
Change management in BIM covers how design changes are communicated, incorporated into the model, and propagated to all affected coordination documents.

Key elements of a BIM change management process:
- **Change Notification**: The design team issues a formal notice (email, RFI response, or design bulletin) describing the change — this triggers the BIM update
- **Impact Assessment**: Before updating the model, the BIM coordinator assesses which elements are affected and whether the change reopens previously resolved clashes
- **Model Update**: The modeler makes the change in the model with a notation in the element's Comments field or a Revit workset named for the change event
- **Re-clash**: After the model update, a targeted clash test is re-run for the affected zone
- **Drawing Reissue**: Any coordination drawings or equipment schedules affected by the change are updated and reissued with a new revision number
- **Stakeholder Notification**: The updated model/drawings are distributed to all parties who received the previous version

**3. Real Project Lens**
The structural engineer issues a design bulletin moving a major beam 400mm lower on Level 6. The BIM coordinator identifies that this reopens 12 previously resolved HVAC clashes and affects three issued coordination drawings. The mechanical modeler updates the model, the clashes are re-run, six new resolution decisions are made, and the three drawings are reissued at Revision B — all within five working days of the bulletin.

**4. BIM Check**
- Check: Can you describe what happens to previously resolved clashes when a structural element changes position?
- Check: Can you explain what a "design bulletin" is and how it triggers a BIM update workflow?
- Check: Can you list three document types that may need reissuing after a significant model change?

**5. Common Mistake**
Making the model change without notifying the site team that previously issued coordination drawings are now superseded. Construction crews may continue working from the old drawings if they are not formally notified of the reissue.

**6. Today's Action**
Write a four-step change management checklist that a junior BIM modeler should follow when they receive notification of a design change that affects their model.

---

### Day 46 — Model-Based Quantity Basics

**1. Why This Matters**
One of BIM's clearest commercial benefits is the ability to extract quantities directly from the model — reducing estimation time and improving the accuracy of material procurement.

**2. Core Concept**
Model-based quantity takeoff uses Revit schedules and parameters to count and measure elements without manual calculation. The accuracy of the output depends entirely on the completeness and accuracy of the model.

Key concepts:
- **Quantity fields**: Length (pipes/ducts), Area (ductwork lining/insulation), Count (fittings, equipment), Volume (insulation)
- **Itemize vs. Group**: Grouped schedules show total quantity per type; itemized schedules show every single element
- **Nested families**: Equipment like AHUs may contain sub-components — understand whether the schedule is counting the host family or the nested parts
- **Unhosted elements**: Elements placed without a host (e.g., pipe fittings placed manually) may have different quantity behavior than system-generated fittings
- **LOD limitation**: Quantities from an LOD 200 model are indicative only; LOD 350 quantities are suitable for procurement
- **Cross-reference**: Always cross-reference model quantities against engineering calculations — BIM quantities are a check, not a replacement for the design calculation

**3. Real Project Lens**
On a hospital fitout, the procurement manager requests a pipe quantity takeoff by size and material for Level 4. The BIM coordinator produces a Pipe Schedule grouped by Diameter and Material, showing total lengths by size. The 100mm copper domestic hot water pipe quantity from the model shows 87 meters — close to the engineer's 90-meter estimate, providing confidence that the model geometry is substantially complete.

**4. BIM Check**
- Check: Can you create a Revit schedule that shows total pipe length grouped by nominal diameter?
- Check: Can you explain why quantity takeoffs from an early-stage (LOD 200) model should not be used for procurement?
- Check: Can you identify at least two element types where the "Count" field in a schedule gives useful procurement data?

**5. Common Mistake**
Using model quantities for procurement without verifying the model LOD. An LOD 200 duct length schedule may exclude all branch connections and transitions — the delivered quantity could be 20-30% higher than the schedule shows.

**6. Today's Action**
In Revit, create a schedule for Pipe Fittings or Duct Fittings that includes a Count field. Group by Type to see how many of each fitting type the model contains. Note the top three most-used types.

---

### Day 47 — Track 6 Review — Data and Schedule Basics

**1. Why This Matters**
The ability to extract reliable data from a BIM model is what separates a model used for reference from a model used for decision-making — this track built the foundation for that capability.

**2. Core Concept**
Track 6 covered how Revit stores, organizes, and exports data, and how change events affect that data. Here is the structured recap:

| Day | Topic | Key Takeaway |
|-----|-------|--------------|
| 39 | What Is a Revit Schedule? | Live table linked to model parameters; filter and group for useful output |
| 40 | MEP Equipment Schedule | Every item needs Mark, Level, System — check for blanks before submission |
| 41 | Duct and Pipe Schedules | Group by size for takeoff; verify unit settings match project standard |
| 42 | Parameter Completeness | Schedule-based check; shared vs. project parameters; use BIM checker tools |
| 43 | Exporting Data | CSV for Excel; IFC for open exchange; NWC for Navisworks; DWG loses data |
| 44 | Tracking Model Changes | Sync discipline; version naming convention; central model history |
| 45 | Revision and Change Mgmt | Notify → assess → update → re-clash → reissue → distribute |
| 46 | Model-Based Quantities | LOD matters; group by type; cross-reference against design calculations |

**3. Real Project Lens**
A BIM coordinator on a commercial tower uses every skill from this track in the same week: creates equipment schedules for the weekly report, checks parameter completeness before a milestone submission, exports a pipe quantity CSV for procurement, tracks a mid-week structural change through the revision process, and issues updated coordination drawings at Revision C by end of week.

**4. BIM Check**
- Check: Can you explain the difference between a schedule filter and a schedule grouping?
- Check: Can you describe the correct export format for sharing Revit data with a non-Revit team?
- Check: Can you outline the five steps you would take when a design change arrives mid-coordination?

**5. Common Mistake**
Treating schedules as final outputs without checking the underlying model data quality. A schedule is only as accurate as the parameters it reads — garbage parameters produce garbage schedules.

**6. Today's Action**
Create a one-page "data checklist" for your own use — listing five parameter fields you would check before submitting any MEP model or schedule to an engineer or client.

---

## Track 7 — Site-Readiness Thinking (Days 48–54)

---

### Day 48 — What Happens When BIM Goes to Site?

**1. Why This Matters**
BIM models created in the office eventually drive physical installation on site — understanding how that transition works prevents you from producing models that cannot be built.

**2. Core Concept**
"BIM goes to site" describes the process by which the coordinated digital model is translated into information that construction workers can actually use. This is not automatic — it requires deliberate preparation.

What the transition involves:
- **Coordination drawings issued**: 2D plans and sections extracted from the model and formally issued to the installation teams
- **Setting-out information**: Grid-referenced dimensions derived from the model used to mark hole positions, hanger locations, and equipment bases on the slab or wall
- **Model access on site**: Tablets or laptops with BIM viewer apps (e.g., Navisworks Freedom, BIM 360 Docs, Autodesk Viewer) give site supervisors direct model access
- **Spool drawings**: Pre-fabricated pipe or duct assemblies are produced from model segments — these are manufactured off-site and delivered for installation
- **RFI (Request for Information)**: When site conditions differ from the model, a formal RFI is raised back to the design team
- **As-built updates**: Deviations from the model on site are recorded and fed back to the BIM coordinator for as-built documentation

**3. Real Project Lens**
On a laboratory fitout project, the MEP BIM coordinator packages the Level 3 coordination drawings, a set of pipe spool drawings, and a Navisworks NWD file onto a project tablet. The site supervisor uses the NWD file to verify pipe hanger spacing during installation, raising two RFIs where the ceiling void was tighter than the model showed due to an unreported slab deviation.

**4. BIM Check**
- Check: Can you name three information outputs that a site team needs to install MEP systems from a BIM model?
- Check: Can you explain what an RFI is and what triggers one during MEP installation?
- Check: Can you describe the purpose of an as-built update in the BIM workflow?

**5. Common Mistake**
Assuming that issuing a coordination drawing is the end of the BIM team's involvement. Site conditions rarely match the model exactly — the BIM team must remain available to respond to RFIs and capture deviations as the build progresses.

**6. Today's Action**
Write a list of five questions a site supervisor might ask a BIM coordinator on their first day using a federated model on site — then write a one-sentence answer for each.

---

### Day 49 — Reading a Coordination Drawing on Site

**1. Why This Matters**
A coordination drawing is the most common BIM output that site installers use — being able to read one confidently is a practical skill that makes you directly useful on site.

**2. Core Concept**
An MEP coordination drawing is a plan-view (or section-view) drawing extracted from the federated model. It shows all MEP systems within a defined zone at a defined level, overlaid on structural grid references.

Key elements to read:
- **Title block**: Project name, drawing number, revision, zone, level, issue date — always check these first to confirm you have the right drawing
- **Grid lines**: Alphanumeric grid (e.g., A–H, 1–10) from the structural model — used to locate elements in the building
- **System color code**: Each MEP system is represented by a different color or line weight — the legend is in the drawing margin
- **Elevation annotations**: Numbers such as "IL 2750 FFL" mean invert level 2750mm above finished floor level — critical for setting out pipes
- **Service identification tags**: Labels like "HWS-D150" mean Heating Hot Water Supply, Diameter 150mm
- **Section reference markers**: Arrows or cut lines pointing to a section drawing that shows vertical relationships between services

**3. Real Project Lens**
A plumbing site supervisor reads a Level 4 coordination drawing and identifies that a 100mm soil stack is annotated at "CL 2900 FFL" — centerline 2900mm above finished floor. They mark the wall bracket position accordingly. The section reference on the drawing shows a second drawing that reveals the stack must drop 200mm to clear a structural tie at Grid D3.

**4. BIM Check**
- Check: Can you find the revision number and issue date on a coordination drawing before using it on site?
- Check: Can you read an elevation annotation (e.g., "IL 2650 FFL") and explain what it means in physical terms?
- Check: Can you use the grid reference system to locate a specific element on site from the drawing?

**5. Common Mistake**
Working from a coordination drawing without checking the revision. An earlier revision may show routing that was later changed — always confirm you have the current issue before committing to installation.

**6. Today's Action**
Find a sample MEP coordination drawing online and identify: (1) the title block revision, (2) one elevation annotation, (3) one system tag and what it likely means, and (4) one grid intersection referenced in the drawing.

---

### Day 50 — MEP Installation Sequence Basics

**1. Why This Matters**
MEP trades must install in a defined sequence to avoid blocking each other's work — understanding installation sequence helps you model and coordinate in the right order.

**2. Core Concept**
MEP installation is not random — it follows a sequence driven by physical access, structural completion, and ceiling void priorities.

Typical MEP installation sequence (simplified):
1. **Structural frame complete** — prerequisite for all MEP work in a zone
2. **Primary containment**: Large cable trays and major duct trunks installed first — they occupy the highest and most space-constrained positions
3. **Mechanical ductwork**: Main runs then branches; larger sections before smaller sections
4. **Sprinkler mains**: Typically follow immediately after major duct runs
5. **Domestic plumbing mains**: Cold and hot water mains along service routes
6. **Electrical conduit and secondary containment**: Runs alongside plumbing before ceiling void closes
7. **Small bore pipework and flex connections**: Last in the void before ceiling grid
8. **Ceiling grid and tiles**: Installed only after all services are complete, tested, and signed off

**3. Real Project Lens**
On a hotel corridor project, the electrical contractor starts running conduit before the HVAC duct is installed. When the 600×300mm supply duct is installed the following week, the conduit runs are in the way and must be relocated — a delay and cost event that correct sequencing would have prevented. The BIM coordinator flags this in the coordination meeting as a sequencing conflict, not just a spatial clash.

**4. BIM Check**
- Check: Can you list the first three MEP systems typically installed in a ceiling void and explain why they come first?
- Check: Can you explain why sprinkler mains are generally installed before small-bore pipework?
- Check: Can you describe what "primary containment" means and give an example?

**5. Common Mistake**
Treating installation sequence as the contractor's problem alone. BIM coordinators who understand sequence can flag sequencing conflicts during coordination review — these are as costly as spatial clashes.

**6. Today's Action**
Draw a simple timeline (or numbered list) showing the MEP installation sequence for a typical office floor ceiling void — include at least six steps in order.

---

### Day 51 — Prefabrication and Spool Drawings

**1. Why This Matters**
Prefabrication is growing rapidly in MEP construction — BIM models are the source data for spool drawings, making model accuracy a direct driver of fabrication quality.

**2. Core Concept**
Prefabrication (or offsite manufacturing) involves building sections of pipework or ductwork in a factory, then delivering them to site for final connection. This requires highly accurate model data to produce correct spool drawings.

Key terms:
- **Spool**: A pre-built section of pipework including fittings, flanges, and supports — manufactured to exact dimensions
- **Spool drawing**: A 2D fabrication drawing showing each segment, fitting, and connection point with precise dimensions — produced from the BIM model
- **ISO drawing (isometric)**: A spool drawing shown in isometric view to clearly display the 3D routing and all connections
- **Cut length**: The exact length of each straight pipe segment, accounting for fitting allowances — derived from the model
- **End preparation**: The type of joint at each spool end (flanged, grooved, butt-welded) specified in the spool drawing
- **BIM-to-fabrication tolerance**: The model must be accurate to ±3mm at LOD 350 for fabrication drawings to be reliable

**3. Real Project Lens**
A mechanical contractor on a pharmaceutical project uses the BIM model to generate spool drawings for the process pipework on Level 2. The pipework is fabricated in a workshop in segments no longer than 6 meters (for transport). Each spool is tagged with a unique ID matching the spool drawing — site crews install by matching the tag to the drawing, significantly reducing on-site cutting and fitting time.

**4. BIM Check**
- Check: Can you explain the difference between a spool drawing and a coordination drawing?
- Check: Can you describe why a BIM model must be at LOD 350 (not LOD 200) before spool drawings are produced?
- Check: Can you identify what "cut length" means on a spool drawing and how it is derived from the model?

**5. Common Mistake**
Generating spool drawings from a model that has not been clash-resolved. If the coordinated routing changes after spools are fabricated, the pre-built sections may not fit on site — extremely costly rework.

**6. Today's Action**
Search for a sample pipe isometric (ISO) spool drawing online. Identify three pieces of information shown on it (dimensions, fitting types, end connections, etc.) and note which ones would come directly from a BIM model.

---

### Day 52 — Site Conflict vs. Model Conflict

**1. Why This Matters**
Not every problem on site is a model error — and not every model error causes a site problem. Understanding the difference prevents unnecessary blame and leads to faster resolution.

**2. Core Concept**
A model conflict is a spatial clash identified in the digital model. A site conflict is a physical installation problem encountered during construction. These are related but distinct.

Key differences:

| | Model Conflict | Site Conflict |
|---|---|---|
| **Where found** | Navisworks / BIM checker | On site during installation |
| **When found** | Pre-construction coordination | During construction |
| **Root cause** | Modeling error, design clash, or coordination gap | Model vs. reality deviation, trade sequencing, or unrecorded design change |
| **Resolution path** | Coordination meeting + model update | RFI + site instruction + as-built capture |
| **Cost impact** | Low (if found pre-construction) | High (rework, delay) |

Common causes of site conflicts that do not appear in the model:
- Slab deviation (floor level is not exactly as modeled)
- Structural elements installed out of position
- Design change issued to site but not updated in model
- Trade working from superseded drawing

**3. Real Project Lens**
A piping contractor raises a site conflict on Level 7: a structural column appears 50mm south of its modeled position, causing the piping run to clash with the column flange. The model showed no clash. Investigation reveals the column was installed out of position by the structural contractor — the model was correct, but reality was not. An RFI documents the deviation and a minor pipe offset is approved on site.

**4. BIM Check**
- Check: Can you describe two causes of site conflicts that would not appear in a clash detection test?
- Check: Can you explain what an RFI is and how it resolves a site conflict formally?
- Check: Can you describe how a site conflict deviation should be captured back into the BIM model?

**5. Common Mistake**
Assuming that a zero-clash model means zero problems on site. Clash detection eliminates model conflicts — it cannot account for construction tolerances, installation deviations, or undocumented design changes.

**6. Today's Action**
Write two short scenario descriptions: one where a site conflict is caused by a model error, and one where it is caused by a site condition the model could not predict. Describe how each one would be resolved.

---

### Day 53 — What a Site Supervisor Needs from BIM

**1. Why This Matters**
BIM outputs are only valuable if the site team can actually use them — designing your outputs for the end user (the site supervisor) makes the BIM model a real construction tool, not just a documentation exercise.

**2. Core Concept**
Site supervisors have different needs from BIM coordinators and engineers. Understanding those needs shapes what you produce and how you present it.

What a site supervisor typically needs from BIM:

- **Clear, printed coordination drawings**: A3 or A1 format, clearly dimensioned from grid lines, showing the zone they are installing today — not the whole building
- **Simple elevation data**: Pipe inverts and duct soffit levels relative to the finished floor — not complex model coordinates
- **Model access for visual reference**: A lightweight NWD or Revit-to-viewer file they can rotate in 3D to understand spatial relationships
- **Clash status**: Confirmation that the zone is clear of unresolved Major clashes before they start work
- **Spool delivery schedule**: If prefabricated spools are being used, they need to know which spools arrive when so they can sequence the install
- **Quick RFI response**: When something on site doesn't match the drawing, they need an answer within 24 hours — delays cascade

**3. Real Project Lens**
A mechanical site supervisor on a data center project asks the BIM coordinator for a "one-page cheat sheet" for the Level 2 comms room — a plan with duct sizes, elevations, and critical dimensions, printed large enough to read in low light with gloves on. The coordinator exports a cropped coordination drawing at 1:20 scale with annotation enlarged. The supervisor uses this drawing for three days of installation without a single RFI.

**4. BIM Check**
- Check: Can you name three specific outputs a site supervisor needs from the BIM team during active MEP installation?
- Check: Can you explain why a site supervisor's needs differ from an engineer's needs when accessing BIM data?
- Check: Can you describe what information should be on a zone-specific coordination drawing prepared specifically for site use?

**5. Common Mistake**
Sending the full federated NWD file to the site supervisor and expecting them to navigate it independently. Site teams need curated, simplified outputs — not raw model access that requires BIM software training to use effectively.

**6. Today's Action**
Design the content of a one-page "site information sheet" for a single zone (one floor, one area). List exactly what information it would contain, in what format, and at what scale — as if you were handing it to a site supervisor tomorrow.

---

### Day 54 — Track 7 Review — Site-Readiness Thinking

**1. Why This Matters**
A BIM model that cannot be built from is incomplete — site-readiness thinking means designing your coordination process with the construction team's needs as the primary output standard.

**2. Core Concept**
Track 7 covered how BIM transitions from the office model to active construction. Here is the structured recap:

| Day | Topic | Key Takeaway |
|-----|-------|--------------|
| 48 | BIM Goes to Site | Coordination drawings, setting-out, spool drawings, RFIs, as-built |
| 49 | Reading Coordination Drawings | Title block, grid refs, elevation annotations, system tags, section refs |
| 50 | Installation Sequence | Primary containment first; ceiling grid last; sequence = spatial + time |
| 51 | Prefabrication and Spools | LOD 350 required; spool IDs; cut lengths from model; clash-resolve first |
| 52 | Site vs. Model Conflict | Model conflict = digital; site conflict = physical; different resolution paths |
| 53 | What Site Supervisors Need | Curated zone drawings; simple elevation data; fast RFI response |

**3. Real Project Lens**
The BIM coordinator for a Level 3 fitout zone prepares a site-readiness package: a zone coordination drawing, a pipe spool delivery schedule, a simplified 3D viewer link, and a clash clearance sign-off memo. The mechanical contractor installs the full zone in four days with only one RFI — the lowest RFI rate of any zone on the project.

**4. BIM Check**
- Check: Can you describe the difference between a spool drawing and a coordination drawing in terms of their purpose and audience?
- Check: Can you explain why installation sequence matters during BIM coordination — not just during construction?
- Check: Can you list three things a site supervisor needs that a design engineer does not need?

**5. Common Mistake**
Completing Track 7 thinking that "site-readiness" is someone else's job. Whether you are a modeler, coordinator, or junior BIM technician, producing model outputs that can actually be used on site is part of your professional responsibility.

**6. Today's Action**
Write a short "site-readiness checklist" for a single zone — at least six items that must be confirmed before a coordination package is handed to a site supervisor. Make each item a yes/no check.

---

## Track 8 — Career and Professional Basics (Selected Lessons)

---

### Day 56 — Using BIM References and Standards

**1. Why This Matters**
BIM work does not happen in a vacuum — industry standards define what is expected at each project stage, and knowing how to find and use those references makes your work defensible and professional.

**2. Core Concept**
BIM standards provide documented frameworks for how models should be created, shared, and verified. Understanding the key references helps you answer questions like "How detailed should this model be?" and "What parameters are required at this stage?"

Key BIM references and standards:
- **ISO 19650 (Parts 1 & 2)**: International standard for information management using BIM — defines how information is produced, shared, and archived across a project lifecycle
- **LOD Specification (BIMForum)**: Defines Level of Development (LOD 100–500) for each element type — the most widely referenced guide for model content requirements
- **National BIM Standards (country-specific)**: UK has PAS 1192 (now superseded by UK BIM Framework/ISO 19650); Singapore has BCA BIM guidelines; US has NBIMS-US
- **EIR (Employer's Information Requirements)**: A project-specific document written by the client defining what BIM information they require and when
- **BEP (BIM Execution Plan)**: Written by the project team in response to the EIR — defines who delivers what model content, in what format, at what stage
- **Revit MEP Content Standards**: Many firms maintain internal standards for family naming, parameter naming, and system naming conventions

**3. Real Project Lens**
A junior BIM coordinator is asked what parameters should be in the mechanical equipment model at RIBA Stage 4 (Technical Design). Rather than guessing, they consult the project's BEP, which references the LOD Specification and lists the required fields: Mark, System Name, Flow Rate, Manufacturer, and Model Number. This directly answers the question without needing to involve senior staff.

**4. BIM Check**
- Check: Can you name the international standard that governs information management in BIM projects?
- Check: Can you explain the difference between an EIR and a BEP in terms of who writes each and what it contains?
- Check: Can you find the LOD Specification online and identify what LOD 350 requires for a mechanical duct?

**5. Common Mistake**
Modeling to a self-determined standard without consulting the project EIR or BEP. Every project has specific information requirements — assuming you know what is needed without checking the contract documents leads to rework or non-compliant deliverables.

**6. Today's Action**
Download or find the BIMForum LOD Specification (free PDF online). Look up one MEP element (e.g., Pipe or HVAC Duct) and read what is required at LOD 300 vs. LOD 350. Write down the difference in two sentences.

---

### Day 58 — MEP BIM Portfolio Building for Beginners

**1. Why This Matters**
In MEP BIM, portfolios are sparse — most beginners skip them and then struggle to demonstrate capability in job applications. A focused, honest portfolio gets you past the first round of hiring review.

**2. Core Concept**
An MEP BIM portfolio shows what you can do with real examples. It does not need to be from paid work — training exercises, self-study projects, and academic work are all valid starting points.

What to include in a beginner MEP BIM portfolio:

- **Project snapshots**: 3D model views or coordination drawings from Revit or Navisworks — even if from a training project, clearly labeled as such
- **Clash detection examples**: A clash report screenshot with a brief explanation of what you found and how it would be resolved
- **Schedule examples**: A screenshot of a Revit equipment or pipe schedule with a note about what it shows
- **Workflow descriptions**: A short written paragraph (3–5 sentences) explaining your process for one task — employers value people who can explain what they did and why
- **Tools used**: A clear list — Revit version, Navisworks version, Dynamo (if used), BIM 360 / ACC
- **Project types you have worked on or studied**: Residential, commercial, healthcare — even if from a training module

What to avoid:
- Images with confidential project data or client names
- Claims of LOD or deliverable compliance without evidence
- Long paragraphs of text — use visuals with captions

**3. Real Project Lens**
A beginner BIM technician applies for a junior coordinator role with a portfolio showing three items: a Revit pipe model screenshot with a schedule, a Navisworks clash report from a training exercise (labeled "training"), and a written workflow summary of how they ran a clash test and grouped results. The hiring manager notes the portfolio as a positive differentiator — most applicants at that level submit nothing.

**4. BIM Check**
- Check: Can you name three types of content a beginner can include in an MEP BIM portfolio without having professional project experience?
- Check: Can you explain why labeling training or self-study work as such is better than omitting it or misrepresenting it?
- Check: Can you identify which tool versions you currently use and write a clear tools list for a portfolio page?

**5. Common Mistake**
Waiting until you have professional project experience to start a portfolio. Training work, sample models, and study exercises are legitimate portfolio content — the habit of documenting your work should start now.

**6. Today's Action**
Create a simple portfolio entry for one thing you have done in this 90-day course. Include: a screenshot or description, the tool used, what you did, and what you learned. This is the first item in your MEP BIM portfolio.

---

### Day 59 — Common Career Questions in MEP BIM

**1. Why This Matters**
Knowing how to answer common interview and career questions in MEP BIM — with specific, honest answers — directly improves your chances of landing your first role or moving into a coordination position.

**2. Core Concept**
MEP BIM hiring conversations follow predictable patterns. Preparing clear, honest answers to the most common questions saves anxiety and projects professionalism.

The most common career questions and how to approach them:

- **"What MEP BIM tools do you know?"** — Be specific: name the tools, versions, and what tasks you have used them for. Do not claim tools you have only read about.
- **"What is your coordination experience?"** — Be honest about level. If your experience is training-based, say so clearly and describe the process you followed.
- **"What does LOD mean?"** — Explain Level of Development: the amount of geometric and parameter detail required in a model element at a given project stage (LOD 100–500). Give one example.
- **"Can you run a clash test?"** — If yes, describe the steps: export NWC → append in Navisworks → set up Clash Detective test → run → review → group → report.
- **"What discipline do you want to specialize in?"** — Have an opinion: mechanical, electrical, or plumbing. Generalists are fine early in a career, but directional thinking signals maturity.
- **"Where do you see yourself in three years?"** — Aim for a specific BIM role: junior coordinator → coordinator → BIM manager. Show you understand the career path.

**3. Real Project Lens**
A junior BIM technician is asked in an interview: "Tell me about a coordination challenge you solved." They describe a training scenario: running a clash test, finding 40 conflicts between HVAC ductwork and the structural model, grouping them by level, and prioritizing the six that were Critical. The interviewer is satisfied — the answer demonstrates process knowledge even without professional project experience.

**4. BIM Check**
- Check: Can you answer "What MEP BIM tools do you know?" in two sentences, naming tools and specific tasks?
- Check: Can you describe the clash detection process in five steps without notes?
- Check: Can you explain LOD clearly to someone who has never heard the term?

**5. Common Mistake**
Overclaiming in interviews — saying you have "extensive coordination experience" when you have completed training exercises. Interviewers with BIM backgrounds ask follow-up questions that quickly expose overstatement. Honest, specific answers build more trust than inflated ones.

**6. Today's Action**
Write out answers to three questions from the list above. Keep each answer under 60 words. Read them aloud — if they sound unnatural, rewrite them until they do not.

---

## BIM Check Friday — All 13 Weeks

---

### Week 1 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 1 | MEP BIM Orientation

Q1. What does MEP stand for, and what does each letter represent on a building project?
Q2. What is the difference between a BIM model and a 2D CAD drawing in terms of the information they contain?
Q3. What is LOD, and what does LOD 300 generally mean for a mechanical duct?
Q4. What is the purpose of a BIM Execution Plan (BEP) on a construction project?
Q5. Name two MEP systems that would typically be coordinated against each other in a BIM clash test.

Think through each one.
No grades — this tests your own understanding.

Next week: Revit MEP Basics check.
```

---

### Week 2 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 2 | Revit MEP Basics

Q1. What is the difference between a Revit System and a Revit Family in the context of MEP modeling?
Q2. How does a Workshared (central) Revit file differ from a standard local Revit file on a team project?
Q3. What is a Revit Workset, and why are they used in MEP projects?
Q4. If a pipe appears in the wrong color in a Revit view, what is the most likely cause?
Q5. What does "Sync to Central" do, and why is it important to do it regularly?

Think through each one.
No grades — this tests your own understanding.

Next week: Drawing and System Reading check.
```

---

### Week 3 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 3 | Drawing and System Reading

Q1. What is the difference between a plan view and a section view on an MEP drawing?
Q2. What does "IL 2750 FFL" mean on a plumbing drawing?
Q3. On a duct drawing, what does the annotation "600×300 SA" typically represent?
Q4. What is a P&ID, and which MEP discipline uses it most commonly?
Q5. Why is it important to check a drawing's revision block before using it for installation?

Think through each one.
No grades — this tests your own understanding.

Next week: Model Quality Basics check.
```

---

### Week 4 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 4 | Model Quality Basics

Q1. What is the difference between LOD 200 and LOD 350 in terms of what a model element contains?
Q2. Name two types of model quality checks that should be performed before a BIM model is submitted to a client.
Q3. What does it mean when a Revit element has no "Mark" value assigned?
Q4. What is a shared parameter in Revit, and why does it matter for BIM deliverables?
Q5. If a model quality checker tool flags 120 elements as failing, what should you do before fixing them all?

Think through each one.
No grades — this tests your own understanding.

Next week: Clash Coordination Basics check (Part 1).
```

---

### Week 5 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 5 | Clash Coordination Basics — Part 1

Q1. What is the difference between a hard clash and a soft clash in Navisworks?
Q2. What file format does Revit export for use in Navisworks, and what does that format contain?
Q3. In Navisworks Clash Detective, what does the status "Reviewed" mean — and how is it different from "Resolved"?
Q4. Why is it important to group clash results before attending a coordination meeting?
Q5. What are the three typical resolution outcomes for a clash in a coordination meeting?

Think through each one.
No grades — this tests your own understanding.

Next week: Clash Coordination Basics check (Part 2).
```

---

### Week 6 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 6 | Clash Coordination Basics — Part 2

Q1. Name three common clash resolution patterns used in MEP coordination and describe when each is appropriate.
Q2. What is an issue tracker, and what five fields should every issue tracker entry contain?
Q3. What should you check before issuing a coordination drawing to a site team?
Q4. If you fix a clash by moving a pipe, what should you always do immediately afterward in Navisworks?
Q5. Which clash resolution pattern requires a structural engineer's approval before the model is updated?

Think through each one.
No grades — this tests your own understanding.

Next week: Data and Schedule Basics check (Part 1).
```

---

### Week 7 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 7 | Data and Schedule Basics — Part 1

Q1. What is a Revit schedule, and how is it different from a manually created Excel table?
Q2. In an MEP equipment schedule, what three fields are most important to verify before submitting to a client?
Q3. What does "grouping" a duct schedule by size achieve, compared to listing every instance individually?
Q4. What is a shared parameter, and why does it matter for MEP schedules?
Q5. If a schedule shows blank values for 15 elements in the "Mark" column, what is the correct next step?

Think through each one.
No grades — this tests your own understanding.

Next week: Data and Schedule Basics check (Part 2).
```

---

### Week 8 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 8 | Data and Schedule Basics — Part 2

Q1. What Revit export format should you use when sharing model data with a team that does not use Autodesk software?
Q2. A design change arrives mid-coordination. Name the five steps you should follow to manage it correctly.
Q3. What LOD level is typically required before model quantities can be used for material procurement?
Q4. Why is it risky to use an LOD 200 duct quantity schedule for procurement purposes?
Q5. What does "Sync to Central" have to do with model change tracking on a workshared project?

Think through each one.
No grades — this tests your own understanding.

Next week: Site-Readiness Thinking check (Part 1).
```

---

### Week 9 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 9 | Site-Readiness Thinking — Part 1

Q1. What does "BIM goes to site" mean, and name three outputs the construction team needs from the BIM model?
Q2. On a coordination drawing, what does "IL 2650 FFL" mean and why does it matter for installation?
Q3. What is the typical MEP installation sequence in a ceiling void — name at least five steps in order?
Q4. What is an RFI, and what triggers one during MEP installation?
Q5. Why should clash detection be completed before spool drawings are produced from a BIM model?

Think through each one.
No grades — this tests your own understanding.

Next week: Site-Readiness Thinking check (Part 2).
```

---

### Week 10 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 10 | Site-Readiness Thinking — Part 2

Q1. What is the difference between a model conflict and a site conflict — and give one example of each?
Q2. Name three things a site supervisor needs from the BIM team that a design engineer typically does not need.
Q3. What is a spool drawing, and at what LOD should the BIM model be before spool drawings are produced?
Q4. A structural column was installed 50mm out of position. The model shows no clash. How should this be resolved?
Q5. What does "as-built capture" mean in the BIM workflow, and why does it matter after construction?

Think through each one.
No grades — this tests your own understanding.

Next week: BIM Standards and Career check (Part 1).
```

---

### Week 11 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 11 | BIM Standards and References

Q1. What is ISO 19650, and which two project documents does it influence most directly?
Q2. What is the difference between an EIR and a BEP — who writes each, and what does each contain?
Q3. In the LOD Specification, what is the key difference between LOD 300 and LOD 350 for a pipe?
Q4. If you are unsure what parameters to include in your MEP model at a given project stage, where should you look first?
Q5. Name one national BIM standard (other than ISO 19650) and the country it applies to.

Think through each one.
No grades — this tests your own understanding.

Next week: Portfolio and Career Questions check.
```

---

### Week 12 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 12 | Portfolio and Career Basics

Q1. Name three types of content a beginner can include in an MEP BIM portfolio without professional project experience.
Q2. If an interviewer asks "Can you run a clash test?" — describe the process in five steps without notes.
Q3. What is the most common mistake beginners make in BIM job interviews, and how do you avoid it?
Q4. How would you honestly describe your coordination experience if it comes only from training exercises?
Q5. What MEP discipline do you want to specialize in, and give one reason why?

Think through each one.
No grades — this tests your own understanding.

Next week: Final Review — 90-Day Course Wrap.
```

---

### Week 13 — BIM Check Friday

```
LUA BIM LABS — BIM Check Friday ✓
Week 13 | Final Review — 90-Day Course Wrap

Q1. You are asked to produce a site-readiness package for a Level 3 MEP zone. List five items you would include.
Q2. A design change arrives and reopens 12 previously resolved clashes. Describe the steps you take from notification to reissue.
Q3. An equipment schedule has 20 blank "Mark" fields out of 140 elements. What do you do before submitting it?
Q4. Explain the difference between a coordination drawing and a spool drawing — who uses each, and for what purpose?
Q5. In one sentence each: define LOD, EIR, BEP, and IFC.

Think through each one.
No grades — this tests your own understanding.

You have completed the 90-day Starter curriculum. Apply what you know — the next step is practice on real projects.
```
