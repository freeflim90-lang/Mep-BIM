# Starter Plan — Support Materials Pack

> LUA BIM LABS Starter Plan | USD 39/month | 90-Day MEP BIM Education via Telegram
> Last updated: 2026-05-29

---

## Part 1: Quick Reference Cards (8 Cards)

---

### Card 1: MEP BIM Key Roles & LOD Reference
Send on: Day 7

---

**MEP BIM Key Roles**

| Role | Primary Responsibility | Main Deliverable |
|---|---|---|
| BIM Manager | Standards, protocol, coordination | BEP, BIM Execution Plan |
| MEP Modeler | 3D model creation per discipline | Federated MEP model |
| MEP Coordinator | Clash detection, resolution | Clash reports, RFIs |
| MEP Engineer | Design intent, system sizing | Engineering drawings |
| BIM Coordinator | Cross-discipline federated model | Coordination model |
| Project Manager | Schedule, resources, client | Project reports |

**LOD Reference Table (MEP)**

| LOD | Name | What Is Modeled | Used For |
|---|---|---|---|
| LOD 100 | Conceptual | Zones, rough equipment areas | Early massing |
| LOD 200 | Schematic | Approximate size, shape, location | Design coordination |
| LOD 300 | Detailed | Exact geometry, connections | Construction documentation |
| LOD 350 | Coord-Ready | Connectors, interface detail | Clash coordination |
| LOD 400 | Fabrication | Fabrication-ready geometry | Shop drawings |
| LOD 500 | As-Built | Verified field conditions | O&M handover |

**Practical Rule of Thumb**

- Day 1–Design Development: LOD 200–300
- Clash Coordination Submission: LOD 350 minimum
- Construction Issue: LOD 350–400
- Handover: LOD 500

**Key Abbreviations**

| Term | Meaning |
|---|---|
| BEP | BIM Execution Plan |
| MEP | Mechanical, Electrical, Plumbing |
| RFI | Request for Information |
| IFC | Industry Foundation Classes |
| BCF | BIM Collaboration Format |
| CDE | Common Data Environment |

---

---

### Card 2: Revit MEP Setup Checklist
Send on: Day 14

---

**Project File Setup**

- [ ] Use the correct project template (MEP discipline-specific)
- [ ] Confirm units: millimeters (metric) or feet/inches (imperial)
- [ ] Set project base point and survey point — match architectural model
- [ ] Link architectural model using "Origin to Origin" or "Shared Coordinates"
- [ ] Link structural model — same method as architectural

**Workset / Worksharing Setup**

- [ ] Enable worksharing before inviting team
- [ ] Create worksets: MEP-HVAC, MEP-Piping, MEP-Electrical, MEP-Plumbing
- [ ] Assign each team member to their workset
- [ ] Set up central model location on CDE or shared drive
- [ ] Never save central model locally — always to shared path

**System and Connector Settings**

- [ ] Mechanical systems defined: Supply Air, Return Air, Exhaust Air
- [ ] Piping systems defined: CHW Supply, CHW Return, HHW Supply, HHW Return, Domestic Cold, Domestic Hot
- [ ] Electrical systems: Power, Lighting, Data, Fire Alarm
- [ ] Confirm pipe and duct material parameters match project spec
- [ ] Check insulation types are loaded in the project

**View Setup**

- [ ] Create discipline views: HVAC Plan, Piping Plan, Electrical Plan, Plumbing Plan
- [ ] Set view range for each plan view (confirm slab-to-slab heights)
- [ ] Create section views for riser locations
- [ ] Apply view templates consistently across team

**Quick Checks Before Modeling**

- [ ] Levels match architectural floor-to-floor heights
- [ ] Grid lines imported and locked
- [ ] Room/space elements placed for load calculations
- [ ] Project information filled in (Project Number, Client, Address)

---

---

### Card 3: MEP Drawing Reading Guide
Send on: Day 21

---

**Drawing Types and What to Look For**

| Drawing Type | Key Information to Extract |
|---|---|
| Floor Plan (MEP) | Equipment location, duct/pipe routes, room designations |
| Riser Diagram | Vertical system flow, pipe sizes per floor |
| Schematic Diagram | System logic, valve positions, flow direction |
| Detail Drawing | Specific connection method, clearance dimensions |
| Coordination Drawing | Cross-discipline overlay, clash zones |
| Legend / Symbol Sheet | Symbol meanings, line types, abbreviations |

**Reading a Duct Plan — Step by Step**

1. Identify AHU or FCU — the air source
2. Trace supply ducts (solid line) from source to diffusers
3. Trace return ducts (dashed line) back to AHU
4. Note duct sizes — Width x Height in mm (e.g., 600x300)
5. Note elevation callouts — duct invert or centerline
6. Locate dampers, fire dampers, VAV boxes

**Reading a Piping Plan — Step by Step**

1. Find the pipe source — pump, riser connection, or entry point
2. Identify pipe type by line style or color code
3. Note pipe diameter (DN or NPS) at each branch
4. Check flow direction arrows
5. Locate valves, strainers, and isolation points
6. Cross-reference with riser diagram for vertical routing

**Common Line Types**

| Line | Meaning |
|---|---|
| Solid thick | Supply duct or pipe |
| Dashed | Return duct or concealed pipe |
| Dash-dot | Centerline / system boundary |
| Double solid | Cable tray or conduit |

**Common MEP Symbols**

| Symbol | Meaning |
|---|---|
| Circle with X | Diffuser or grille |
| Circle with dot | Sprinkler head |
| Rectangle with tag | Equipment (AHU, FCU, Pump) |
| Valve shape | Isolation/gate/ball valve |
| Triangle on pipe | Check valve (flow direction) |

---

---

### Card 4: Model Quality Self-Review Checklist
Send on: Day 28

---

**Before Submitting Any MEP Model — Run This Checklist**

**Geometry Checks**

- [ ] No elements modeled below the lowest floor level or above the roof slab
- [ ] No duplicate elements in the same location (check with Select All Instances)
- [ ] All ducts and pipes are connected — no open ends (use system inspector)
- [ ] No crossing pipes/ducts that are not physically connected or are unintentional
- [ ] Equipment is placed on correct level (not floating or below floor)

**System Connectivity Checks**

- [ ] All duct segments belong to a named mechanical system
- [ ] All pipe segments belong to a named piping system
- [ ] Electrical circuits are assigned to a panel
- [ ] No orphaned connectors (unconnected fittings or stubs)

**Parameter / Data Checks**

- [ ] All equipment has: Mark, Type Comments, System Classification filled in
- [ ] Pipe sizes match the engineer's design schedule
- [ ] Duct sizes match the engineer's schedule or design intent
- [ ] Material and insulation parameters are assigned

**Coordination Checks**

- [ ] Model is linked to current version of architectural and structural models
- [ ] No MEP element passes through a structural column or beam without a sleeve
- [ ] Ceiling clearance maintained — MEP bottom of element is above ceiling level
- [ ] Service access maintained for all equipment (minimum 600mm recommended)

**File Housekeeping**

- [ ] File saved to CDE — not local desktop
- [ ] File named per project naming convention
- [ ] Revision number or date in file name updated
- [ ] Workset ownership released before saving to central

**Red Flags — Stop and Fix These**

- Pipe or duct passing through floor slab with no sleeve modeled
- Equipment mark left blank
- Model linked from a personal desktop path

---

---

### Card 5: Clash Types & Priority Matrix
Send on: Day 38

---

**The 3 Clash Types**

| Type | Definition | Example |
|---|---|---|
| Hard Clash | Two elements occupy the same physical space | HVAC duct intersects structural beam |
| Soft Clash | Two elements violate required clearance buffer | Pipe too close to electrical cable tray (< 150mm) |
| Workflow / 4D Clash | Construction sequence conflict (time-based) | Ductwork scheduled before slab pour is complete |

**Clash Priority Matrix**

| Priority | Clash Type | Criteria | Action Required |
|---|---|---|---|
| P1 — Critical | Hard clash: MEP vs. Structure | Beam, slab, column penetrated | Stop — resolve before issue |
| P1 — Critical | Hard clash: MEP vs. MEP | Two systems occupy same space | Stop — resolve before issue |
| P2 — High | Soft clash: Clearance violation | Access or code-required clearance missing | Resolve before construction |
| P2 — High | Hard clash: MEP vs. Architecture | Wall penetration not coordinated | Resolve before construction |
| P3 — Medium | Soft clash: Aesthetic or maintenance | Equipment access tight but passable | Schedule resolution |
| P4 — Low | Minor overlap of non-critical elements | Annotation or non-physical element | Log and monitor |

**Clash Reporting Checklist**

- [ ] Clash exported from Navisworks with BCF or clash report
- [ ] Each clash tagged with: Discipline, Priority, Description, Owner
- [ ] Clashes assigned to responsible party (not left unassigned)
- [ ] Screenshot or viewpoint attached to each P1/P2 clash
- [ ] Clash log shared to all disciplines before coordination meeting

**Resolution Priority Rule**

Structure wins > Architecture wins > HVAC > Piping > Plumbing > Electrical > Fire Protection

*If in doubt, refer to the project BIM coordinator — do not resolve P1 unilaterally.*

---

---

### Card 6: MEP Data & Schedule Reference
Send on: Day 47

---

**Equipment Schedules — Required Fields**

| Schedule Type | Required Fields |
|---|---|
| AHU Schedule | Mark, CFM (supply/return/OA), kW, dimensions, weight |
| FCU Schedule | Mark, CFM, cooling kW, heating kW, static pressure |
| Pump Schedule | Mark, flow rate (L/s or GPM), head (kPa or ft), kW |
| Chiller Schedule | Mark, cooling kW, COP, refrigerant type |
| Panel Schedule | Panel ID, voltage, phase, total load (kVA) |
| Sprinkler Schedule | Head type, K-factor, minimum pressure, coverage area |

**Key MEP Data Parameters in Revit**

| Parameter | Used For | Where to Set |
|---|---|---|
| Mark | Equipment identification | Instance Properties |
| System Classification | Duct/pipe system type | System Properties |
| Flow | Design airflow or fluid flow | Duct/Pipe Properties |
| Size | Duct width/height or pipe diameter | Duct/Pipe Properties |
| Insulation Type | Thermal or acoustic insulation | Type Properties |
| Level | Floor assignment | Instance Properties |
| Phase | Construction phase | Instance Properties |

**Reading a Mechanical Schedule**

1. Check Mark number — cross-reference to drawing and model
2. Verify CFM or flow rate — should match design intent
3. Check static pressure — used for duct sizing
4. Note electrical supply (kW, voltage, phase) — link to electrical team
5. Check weight — structural team needs this for equipment pads

**Piping Data Quick Reference**

| Parameter | Typical Metric Value |
|---|---|
| Chilled Water Supply Temp | 6–7°C |
| Chilled Water Return Temp | 12–13°C |
| Heating Hot Water Supply | 60–80°C |
| Domestic Cold Water | 15–20°C |
| Max Pipe Velocity (chilled water) | 1.5–2.5 m/s |

---

---

### Card 7: Site-Readiness Check Guide
Send on: Day 54

---

**What Is Site Readiness in MEP BIM?**

Site readiness means the BIM model and documents are complete enough that site installation can begin without coordination failures. This card is your pre-construction checklist.

**Model Readiness — Before Site**

- [ ] All clashes resolved or formally accepted (signed clash log)
- [ ] Penetrations through slabs and walls coordinated and approved
- [ ] Sleeve drawings issued to structural team
- [ ] Shop drawings generated and reviewed for prefabricated elements
- [ ] LOD 350 confirmed for all installation zones

**Document Readiness**

- [ ] Coordination drawings issued for each floor (IFC or PDF)
- [ ] Equipment data sheets submitted to procurement team
- [ ] Pipe and duct material specifications confirmed
- [ ] Valve and damper schedule issued
- [ ] Fire protection hydraulic calculations submitted to authority (if required)

**Spatial Readiness Checks**

| Zone | Check |
|---|---|
| Mechanical room | All equipment fits with maintenance access |
| Riser shafts | All ducts, pipes, and cables fit within shaft boundaries |
| Ceiling plenum | MEP fits within coordinated ceiling zone |
| Roof | Equipment weight distributed, screen locations confirmed |
| Electrical room | Clearance in front of panels meets local code |

**Coordination Meetings — Before Site**

- [ ] Final coordination meeting held — all disciplines present
- [ ] Outstanding RFIs logged and responded to
- [ ] Construction sequence agreed (which system installs first per zone)
- [ ] Site engineer briefed on BIM model viewing tool (BIM 360, Navisworks, etc.)

**Warning Signs — Not Site Ready**

- Open P1/P2 clashes unresolved
- Sleeve drawings not issued
- Equipment mark numbers missing from procurement list
- Model not updated after last design change

---

---

### Card 8: BIM Learning Path & Next Steps
Send on: Day 60

---

**You Have Completed 60 Days of MEP BIM Foundation**

**What You Now Know**

| Track | Core Skill Gained |
|---|---|
| Track 1 | MEP BIM roles, LOD, industry context |
| Track 2 | Revit MEP project setup and modeling basics |
| Track 3 | Reading and interpreting MEP drawings |
| Track 4 | Model quality review and self-check |
| Track 5 | Clash detection, classification, priority |
| Track 6 | MEP data, schedules, parameters |
| Track 7 | Site-readiness thinking and pre-construction BIM |
| Track 8 | BIM career habits and continuous improvement |

**Your Discipline Track Options (Day 61–90)**

| Track | Focus | Best For |
|---|---|---|
| 9A — HVAC | Duct systems, AHU, VAV, cooling | Mechanical/HVAC modelers |
| 9B — Piping | Chilled/hot water, pumps, mechanical rooms | Piping/mechanical modelers |
| 9C — Plumbing | Sanitary, drainage, water supply | Plumbing modelers |
| 9D — Fire Protection | Sprinklers, standpipes, hydraulics | Fire protection modelers |
| 9E — Electrical | Power distribution, cable tray, conduit | Electrical modelers |

**BIM Career Growth Roadmap**

- Level 1 (Now): MEP Modeler — execute to LOD 300/350
- Level 2 (6–12 months): MEP Coordinator — lead clash resolution
- Level 3 (1–2 years): BIM Coordinator — manage federated model
- Level 4 (2–4 years): BIM Manager — write BEP, lead standards
- Advanced: BIM Consultant / Automation Specialist

**Daily BIM Habit — Keep These After Day 60**

- [ ] Open your model — check it daily even on non-modeling days
- [ ] Log one lesson learned each week
- [ ] Read one project RFI or coordination issue per week
- [ ] Stay updated on Revit release notes (annual updates)

---

---

## Part 2: Completion Certificate Templates

---

### Certificate 1: 60-Day MEP BIM Foundation Certificate

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    LUA BIM LABS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

             MEP BIM FOUNDATION CERTIFICATE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This certifies that

     _____________________________________________
                      [Client Name]

has successfully completed the

     LUA BIM LABS 60-Day MEP BIM Foundation Program

Delivered via the LUA BIM LABS Starter Plan
(Telegram-based daily learning program)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROGRAM COVERAGE

  ✓  Track 1:  MEP BIM Orientation
  ✓  Track 2:  Revit MEP Basics
  ✓  Track 3:  Drawing and System Reading
  ✓  Track 4:  Model Quality Basics
  ✓  Track 5:  Clash Coordination Basics
  ✓  Track 6:  Data and Schedule Basics
  ✓  Track 7:  Site-Readiness Thinking
  ✓  Track 8:  BIM Career Habit Building

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Duration:      60 Days
Format:        Daily Telegram Lessons
Standard:      LOD 100–350 MEP Foundation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Date of Issue: _____________________________________

Authorized by: LUA BIM LABS Education Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                      LUA BIM LABS
            Practical BIM Education for MEP
                  www.luabimlabs.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Certificate 2: 90-Day MEP BIM Discipline Certificate

---

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    LUA BIM LABS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

          MEP BIM DISCIPLINE SPECIALIST CERTIFICATE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This certifies that

     _____________________________________________
                      [Client Name]

has successfully completed the full

    LUA BIM LABS 90-Day MEP BIM Starter Plan Program

including the 60-Day Foundation Program and the
30-Day Discipline Deep-Dive Track:

     ✦  Track 9[X]: [DISCIPLINE]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FULL PROGRAM COVERAGE

  ✓  Track 1:  MEP BIM Orientation
  ✓  Track 2:  Revit MEP Basics
  ✓  Track 3:  Drawing and System Reading
  ✓  Track 4:  Model Quality Basics
  ✓  Track 5:  Clash Coordination Basics
  ✓  Track 6:  Data and Schedule Basics
  ✓  Track 7:  Site-Readiness Thinking
  ✓  Track 8:  BIM Career Habit Building
  ✓  Track 9:  [DISCIPLINE] — Discipline Deep-Dive
               (Day 61 to Day 90)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[DISCIPLINE] Competencies Demonstrated:

  •  [Discipline-specific system understanding]
  •  [Revit modeling for the discipline]
  •  [Clash coordination in the discipline]
  •  [Site-readiness and handover for the discipline]

  [Fill these 4 bullets per discipline as follows:]

  For HVAC:
  •  HVAC system flow from AHU to terminal devices
  •  Duct sizing, VAV connections, and Revit modeling
  •  HVAC clash detection with structure and MEP
  •  HVAC site-readiness and as-built awareness

  For Piping / Mechanical:
  •  Chilled and hot water system design logic
  •  Pump configuration and piping layout in Revit
  •  Piping clash coordination with structure and MEP
  •  Mechanical room readiness and commissioning basics

  For Plumbing / Sanitary:
  •  Sanitary, vent, and domestic water system classification
  •  Gravity drainage modeling and slope in Revit
  •  Sanitary clash patterns with slab and structure
  •  Fixture connections and riser sleeve coordination

  For Fire Protection:
  •  Wet, dry, and pre-action system types
  •  Sprinkler head placement and branch pipe routing
  •  Fire protection clash with HVAC and ceiling
  •  Hydraulic calculation awareness for modelers

  For Electrical:
  •  Power distribution from MSB to DB to circuits
  •  Cable tray, conduit, and distribution board modeling
  •  Electrical separation — HV, LV, data
  •  Electrical clash with HVAC and structure

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Duration:      90 Days (60-Day Foundation + 30-Day Discipline)
Format:        Daily Telegram Lessons
Discipline:    [DISCIPLINE]
Standard:      LOD 100–400 MEP Specialist Level

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Date of Issue: _____________________________________

Authorized by: LUA BIM LABS Education Team

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                      LUA BIM LABS
            Practical BIM Education for MEP
                  www.luabimlabs.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

*Discipline Placeholder Values:*
- Track 9A: HVAC Specialist
- Track 9B: Piping & Mechanical Specialist
- Track 9C: Plumbing & Sanitary Specialist
- Track 9D: Fire Protection Specialist
- Track 9E: Electrical Specialist

---

---

## Part 3: Track 9 Discipline Lessons — Day 61 to 67

---

### Track 9A: HVAC

---

### Day 61 — HVAC System Flow Overview (AHU to Diffuser)

**1. Why This Matters**
If you cannot trace the full air path from the AHU to the last diffuser in the space, you will model disconnected systems that fail system checks, produce incorrect schedules, and cause clash issues that cannot be traced back to a source.

**2. Core Concept**
- The Air Handling Unit (AHU) conditions air: filters, cools or heats, and fans it out
- Supply air travels from the AHU through main supply ducts to branch ducts to VAV boxes or directly to supply diffusers
- Return air travels from return grilles in the space back to the AHU via return ducts
- Exhaust air (from toilets, kitchens, carparks) is pulled out by exhaust fans and discharged outside — it does not return to the AHU
- Outside Air (OA) is introduced at the AHU for ventilation — percentage defined by ventilation code
- The full air loop: AHU → Main Supply Duct → Branch Duct → VAV Box (if VAV system) → Flexible Duct → Diffuser → Return Grille → Return Duct → AHU

**3. Real Project Lens**
On a commercial office floor, one AHU on Level 12 serves the entire floor via a central supply duct running along the corridor. Branch ducts split left and right into office bays. Each bay has 4–6 supply diffusers and a VAV box controlling airflow based on thermostat. Return grilles near the corridor feed a return plenum above the ceiling tiles, which connects back to the AHU return inlet.

**4. BIM Check**
- Check: Open Revit's Mechanical Systems Browser — confirm every duct segment is assigned to a named supply or return air system
- Check: Trace from AHU connector to last diffuser — confirm no open ends (gaps in the duct run)
- Check: Confirm return ducts are assigned "Return Air" system — not accidentally labeled "Supply Air"

**5. Common Mistake**
Modeling supply and return ducts in the correct physical location but failing to connect them to the AHU connector in Revit — causing the system browser to show them as "unassigned" and breaking all flow calculations.

**6. Today's Action**
Open a Revit MEP model (your own or a sample file). Navigate to Systems Browser. Find any duct tagged as "Unassigned" and trace why it is not connected to a system. Fix one connection.

---

### Day 62 — Duct Sizing Logic — CFM and Velocity

**1. Why This Matters**
Duct sizes are not guesses. If you model a duct that is too small, the system will not deliver the required airflow — and you will be asked to change it during construction, causing major coordination rework. If too large, it wastes ceiling space and causes unnecessary clashes.

**2. Core Concept**
- CFM (Cubic Feet per Minute) or L/s is the volume of air that must pass through the duct
- Velocity is how fast the air moves through the duct (in m/s or fpm)
- Duct area = Airflow ÷ Velocity
- Target velocities by application:
  - Main supply duct in office: 5–8 m/s
  - Branch duct to VAV: 3–5 m/s
  - Final branch to diffuser: 2–3 m/s
  - Return duct: 3–5 m/s
- Duct shape: Rectangular is most common for large spaces (easier to coordinate with flat ceilings). Round ducts are used for smaller branches
- After sizing: check that the duct fits within the ceiling zone (confirm available space with structural beam depth and ceiling height)

**Duct Size Quick Reference (Rectangular, Supply Air)**

| Airflow (L/s) | Suggested Size (mm) |
|---|---|
| 100–200 | 300 x 150 |
| 200–400 | 400 x 200 |
| 400–700 | 600 x 250 |
| 700–1200 | 800 x 300 |
| 1200–2000 | 1000 x 400 |

**3. Real Project Lens**
The engineer's design schedule specifies 850 L/s for the main supply duct on Level 5. At a velocity of 6 m/s, the duct area required is 850/1000 ÷ 6 = 0.142 m². A 600 x 250mm duct gives 0.15 m² — acceptable. The modeler enters 600 x 250 as the duct width and height in Revit.

**4. BIM Check**
- Check: Open the engineer's duct schedule — compare each duct size on the schedule to the size modeled in Revit
- Check: For any duct modeled at a size not on the schedule, log it as a discrepancy and raise with the engineer
- Check: Confirm the duct invert elevation fits within the ceiling zone (bottom of duct = ceiling level + clearance)

**5. Common Mistake**
Modelers sometimes scale duct sizes visually from the 2D drawing without reading the size tag — resulting in a duct that looks right on plan but is 200mm too wide, causing a clash with the sprinkler main.

**6. Today's Action**
Find a duct size schedule from a real project or sample drawing. Pick one duct entry. Calculate the duct area (flow ÷ velocity). Confirm the size in the schedule gives adequate area.

---

### Day 63 — Supply vs. Return vs. Exhaust System Assignment

**1. Why This Matters**
Assigning a duct to the wrong system type — supply labeled as return, or exhaust misassigned — corrupts airflow calculations, makes schedules wrong, and creates commissioning failures that are traced back to the BIM model.

**2. Core Concept**
- Three main air system types in HVAC BIM:
  - **Supply Air**: Conditioned air from AHU to space. Flows toward the occupied area. Duct assigned as "Supply Air" in Revit
  - **Return Air**: Air from occupied space back to AHU. Separate duct or plenum. Assigned "Return Air"
  - **Exhaust Air**: Air expelled outside. Toilets, kitchens, carparks, server rooms. Assigned "Exhaust Air" — never recirculated
- In Revit, system type is set at the mechanical system level — not just at the duct level
- Connector polarity matters: AHU supply outlet connector links to supply system; AHU return inlet connector links to return system
- Mixed-mode error: if return ducts are accidentally connected to the supply system, Revit's system analysis will show reversed flow or incorrect pressures

**3. Real Project Lens**
On a hospital project, the operating theatre has three separate duct systems: HEPA-filtered supply air (positive pressure), exhaust air (negative pressure, expelled outside), and a corridor return air system. The BIM modeler must create three separate mechanical systems in Revit — one per type — and connect each duct run to the correct system. Mixing them triggers infection control failures.

**4. BIM Check**
- Check: In Mechanical Systems Browser, expand each system — confirm all ducts inside are the correct type (no supply duct inside a return system)
- Check: Verify exhaust ducts do not connect back to any AHU return inlet — trace each exhaust duct to an exhaust fan or louver termination point
- Check: Confirm fresh air intake duct at AHU is separate from the exhaust discharge — no short-circuiting

**5. Common Mistake**
Copying a supply duct and changing its physical routing without changing the system assignment — the new duct remains on the supply system even though it is now feeding a return grille. This is invisible on plan but breaks system analysis.

**6. Today's Action**
In Revit, open the Mechanical Systems dialog. Find a project or sample model with at least two mechanical systems. Check whether each duct in the model belongs to the correct system. Rename any system that has an unclear name (e.g., "Mechanical System 1" should be "L3-AHU01-Supply").

---

### Day 64 — VAV Box Connections in Revit

**1. Why This Matters**
VAV (Variable Air Volume) boxes are the key flow control device on VAV systems. If VAV boxes are not properly connected in Revit — both to the upstream supply duct and the downstream flexible duct to diffusers — the system cannot calculate airflow correctly and coordination with controls contractors is compromised.

**2. Core Concept**
- A VAV box sits between the main supply branch duct and the final flex duct to diffusers
- It has: one supply air inlet connector (connected to branch duct from AHU) and one or more discharge connectors (connected to flex duct to diffusers)
- Some VAV boxes include a reheat coil (hot water or electric) — these have additional pipe connectors
- In Revit: load the correct VAV box family, place it at the correct elevation (above ceiling, upstream of diffusers), and connect branch duct to inlet, flex duct to outlet
- Mark parameter: set the VAV box mark to match the engineer's schedule (e.g., VAV-B05-01)
- Set maximum and minimum CFM in the instance parameters to match the design schedule

**Typical VAV Box Connection Sequence in Revit**
1. Place VAV box family at correct elevation
2. Draw branch duct from main supply to VAV inlet connector
3. Draw flex duct from VAV discharge connector to first diffuser
4. Set Mark, Max Flow, Min Flow in instance properties
5. Verify VAV is on Supply Air system

**3. Real Project Lens**
An office floor has 12 VAV boxes — one per zone. Each is tagged VAV-L6-01 through VAV-L6-12. The controls contractor needs the Revit model to show the exact location and connectivity of each box, because they will install the DDC controller wiring based on the BIM model.

**4. BIM Check**
- Check: Each VAV box has a unique Mark matching the engineering schedule
- Check: Inlet connector shows flow in the correct direction (supply from branch duct)
- Check: Discharge connector is connected — no unconnected stub
- Check: For reheat VAV boxes, hot water pipe connectors are connected to the piping model

**5. Common Mistake**
Placing the VAV box family as a non-hosted element at the wrong elevation — it appears correct on plan but is 200mm too high in section, causing it to clash with a structural beam that the modeler did not check.

**6. Today's Action**
In Revit, place one VAV box family in a sample project. Connect a supply duct to the inlet. Connect a short flex duct to the discharge. Open Properties and set the Mark and Max Flow Rate. Verify it appears in the Mechanical Systems Browser.

---

### Day 65 — AHU Room Layout and Clearance

**1. Why This Matters**
An AHU that fits in a room on plan but has no maintenance access cannot be serviced after installation. MEP plants packed too tightly together cause failures during construction and long maintenance shutdowns during operation.

**2. Core Concept**
- AHU clearance requirements:
  - Filter access side: minimum 900mm–1200mm (for filter slide-out)
  - Coil access side: minimum 900mm (for coil pull-out or cleaning)
  - Fan motor side: minimum 600mm
  - General circulation: 1000mm between units
- Floor loading: AHUs are heavy — confirm floor slab load capacity with structural engineer
- Vibration isolation: AHUs must sit on spring isolators or pads — this adds 100–150mm to overall height
- Service routes: confirm ductwork connections at AHU do not block access panels
- AHU rooms need: floor drain, access door (large enough for unit entry during install), lighting, and ventilation

**AHU Room Layout Checklist**

| Item | Minimum Requirement |
|---|---|
| Filter access clearance | 900–1200mm |
| Coil pull clearance | 900mm |
| Motor/fan side clearance | 600mm |
| General circulation path | 1000mm clear |
| Door width for installation | Equipment width + 200mm min |
| Floor drain | Within 2m of AHU drain pan |
| Vibration isolation allowance | 100–150mm height addition |

**3. Real Project Lens**
On Level 14 of a hotel, the AHU room hosts three rooftop-type units. The first draft of the model shows 500mm between Unit 1 and the wall — insufficient for filter access. The BIM coordinator flags this in the clash report as a soft clash (clearance violation). The layout is revised to shift Unit 1 by 500mm, requiring the supply duct to be re-routed.

**4. BIM Check**
- Check: Model AHU with actual manufacturer dimensions (not a placeholder box)
- Check: Create clearance zones as Revit in-place families or reference planes — visually confirm access zones do not overlap
- Check: Confirm AHU top elevation + vibration pad height does not exceed ceiling or beam soffit

**5. Common Mistake**
Using a generic AHU family with default dimensions (1000 x 500 x 800mm) when the actual specified unit is 2400 x 1200 x 1600mm — causing the room layout to look fine in the model but failing completely when site installation begins.

**6. Today's Action**
Find one AHU on a sample or real project model. Open its properties and check the actual dimensions. Then measure the clearance between the AHU and the nearest wall in the model. Compare to the minimum 900mm requirement. Log whether it passes or fails.

---

### Day 66 — HVAC Clash with Structure — Finding and Fixing

**1. Why This Matters**
HVAC ducts are the largest MEP elements by cross-section. They clash with structure more frequently than any other MEP system. An unresolved duct-beam clash discovered on site means cutting, re-routing, or delaying the entire floor.

**2. Core Concept**
- Common HVAC-structure clash types:
  - Duct crossing a beam flange (most common)
  - Duct passing through a shear wall without a sleeve
  - AHU on roof penetrating the roof slab
  - Supply/return duct at corridor crossing a deep transfer beam
- Resolution strategies:
  - **Lower the duct**: Acceptable if ceiling clearance allows — check finished ceiling level
  - **Route around the beam**: Change duct path — may affect supply to a zone
  - **Structural penetration**: Engineer-approved opening through the beam web only (flanges cannot be cut)
  - **Raise the beam**: Structural design change — expensive and slow
- In Navisworks: run HVAC vs. Structure clash test. Set tolerance to 0mm for hard clashes, 50mm for soft clearance clashes

**Clash Resolution Workflow**

1. Export HVAC model + Structural model to Navisworks
2. Run Clash Detective: HVAC vs. Structure, hard clash
3. Group clashes by floor and by duct size
4. Prioritize P1 clashes (main ducts crossing primary beams)
5. For each clash: screenshot viewpoint, assign to HVAC modeler, set deadline
6. Resolve in Revit — update in Navisworks on next coordination cycle

**3. Real Project Lens**
On Level 3 of an office building, the main 1000x400mm supply duct runs east-west along the corridor. At Grid C, a 600mm deep secondary beam crosses the path. The duct invert is at 2800mm, the beam soffit is at 2750mm — a 50mm hard clash. Resolution: reroute the duct 1m north through a beam web opening (structural approval required).

**4. BIM Check**
- Check: All P1 duct-beam clashes are logged in the clash tracker with a unique ID
- Check: Structural penetrations (beam web openings) have written confirmation from the structural engineer before modeling
- Check: After re-route, re-run clash test to confirm zero remaining hard clashes on that duct run

**5. Common Mistake**
Resolving a duct-beam clash by lowering the duct 100mm without checking the finished ceiling level — the duct now passes below the false ceiling and is exposed in the occupied space.

**6. Today's Action**
Open Navisworks (or a sample clash report). Find one HVAC vs. Structure clash. Determine from the report whether it is a main duct or branch duct. Write a one-sentence proposed resolution based on today's strategies.

---

### Day 67 — Week 1 HVAC Review

**1. Why This Matters**
Without reviewing what you learned, information fades. This review session consolidates Days 61–66 into a usable reference and identifies any gaps before you move to more advanced HVAC topics.

**2. Core Concept**
**Week 1 HVAC Summary**

| Day | Topic | Key Point |
|---|---|---|
| 61 | System Flow | AHU → Supply Duct → VAV → Diffuser → Return → AHU |
| 62 | Duct Sizing | Airflow ÷ Velocity = Duct Area. Match engineer's schedule |
| 63 | System Assignment | Supply / Return / Exhaust — never mix in Revit systems browser |
| 64 | VAV Connections | Connect inlet to supply branch, outlet to flex duct, set Mark and flow |
| 65 | AHU Room Layout | 900mm filter access, 1000mm circulation, actual unit dimensions |
| 66 | HVAC-Structure Clash | Duct vs. beam most common. Route around or get approved penetration |

**Key Rules to Remember**
- Duct size comes from the engineer's schedule — never guess
- System assignment in Revit is set at the system level, not just the duct
- VAV marks must match the engineering schedule exactly
- AHU clearance zones must be modeled — not assumed
- All P1 clashes must be resolved before coordination model submission

**3. Real Project Lens**
A junior HVAC modeler is handed a Level 7 HVAC model on Day 1 of a project. Using the skills from Days 61–66, they: (1) check the systems browser for unassigned ducts, (2) cross-reference duct sizes with the engineer's schedule, (3) verify VAV marks, (4) model AHU clearance zones, (5) run a clash test against structural model, and (6) issue a clash report before the coordination meeting — completing the work in one day.

**4. BIM Check**
- Check: Can you trace air flow from AHU to diffuser and back in the model without breaking the connection?
- Check: Are all VAV boxes marked and connected correctly?
- Check: Is the AHU clearance zone modeled and clear of obstructions?

**5. Common Mistake**
Treating the Week 1 review as optional. The most frequent cause of errors in Month 2 HVAC work is skipping the basics covered in Days 61–66 and advancing without fixing foundational gaps.

**6. Today's Action**
Write a personal checklist of 5 things you would check first if you were handed a new HVAC Revit model today. Save it — you will expand this list through Day 90.

---

---

### Track 9B: Piping / Mechanical

---

### Day 61 — Chilled Water System Overview — Supply and Return

**1. Why This Matters**
Chilled water systems carry cold water from chillers to air handling units and fan coil units throughout a building. A modeler who does not understand the supply-and-return loop will route pipes in the wrong direction, assign the wrong system type, and produce a model that confuses the mechanical engineer and the piping contractor.

**2. Core Concept**
- Chilled water is produced at the chiller plant (typically basement or roof)
- Chilled Water Supply (CHWS): Cold water (typically 6–7°C) flows from the chiller to cooling coils in AHUs and FCUs
- Chilled Water Return (CHWR): Warm water (typically 12–13°C) flows from the coils back to the chiller
- The temperature difference (Delta T) is 5–6°C — this is the system's heat exchange target
- Primary-secondary systems: primary pumps move water around the chiller; secondary pumps push water to the building loads
- In Revit: create two piping systems — "Chilled Water Supply" and "Chilled Water Return" — never mix them
- Flow direction: always model flow arrows from chiller to load for supply, load to chiller for return

**Chilled Water System Key Parameters**

| Parameter | Typical Value |
|---|---|
| Supply temperature | 6–7°C |
| Return temperature | 12–13°C |
| Design Delta T | 5–6°C |
| Max pipe velocity | 1.5–2.5 m/s |
| Design pressure | 600–1000 kPa |

**3. Real Project Lens**
A commercial building has two chillers in the basement. From the chiller room, 200mm CHWS and CHWR pipes rise through a riser shaft to each floor. On each floor, branch pipes feed FCUs in the office zones. The BIM modeler creates the riser first — confirming pipe sizes match the engineer's schedule — then branches to each FCU.

**4. BIM Check**
- Check: Supply and return pipes are assigned separate piping systems in Revit — no pipe on both systems
- Check: Flow direction arrows (if modeled) point from chiller toward load on supply, and from load toward chiller on return
- Check: Pipe sizes at each branch match the schedule — larger at riser, smaller at each successive branch

**5. Common Mistake**
Placing supply and return pipes at the same elevation and same location — visually correct on plan but creating a hard clash with each other in the model, indicating they were placed as copies rather than independently routed.

**6. Today's Action**
Sketch (on paper or screen) the basic chilled water loop from chiller to one AHU and back. Label: CHWS, CHWR, primary pump, secondary pump, AHU coil. This diagram is your reference for the next 6 days.

---

### Day 62 — Pump Configuration and Piping Layout

**1. Why This Matters**
Pumps are the heart of any piping system. If the pump suction and discharge are piped incorrectly in the model, the installation will fail commissioning — and the piping contractor will have to re-route in the field.

**2. Core Concept**
- Each pump has two connectors: Suction (inlet) and Discharge (outlet)
- Straight pipe before suction: minimum 5 × pipe diameter (to prevent turbulence at the impeller)
- Straight pipe after discharge: minimum 2 × pipe diameter before the first fitting
- Pump configuration types:
  - **Inline pump**: installed directly in the pipe run — used for smaller systems
  - **End suction pump**: floor-mounted, horizontal suction, vertical or horizontal discharge
  - **Double suction pump**: large flow applications, balanced impeller
- Accessories required at each pump: isolation valve (suction and discharge), check valve (discharge), flexible connector (both sides), pressure gauge (both sides), strainer (suction side)
- In Revit: use correct pump family with accurate dimensions; connect all accessories before connecting to the main pipe

**Pump Piping Accessories Sequence (Suction to Discharge)**
Strainer → Flexible Connector → Isolation Valve → [PUMP] → Isolation Valve → Flexible Connector → Check Valve → Main Pipe

**3. Real Project Lens**
In the chiller room, two secondary chilled water pumps (duty/standby) are installed in parallel. Each pump has 150mm suction and discharge connections. The modeler connects the common suction header to each pump, ensures 750mm (5×DN150) of straight pipe before each pump, and connects the discharge to the common discharge header via check valves.

**4. BIM Check**
- Check: Straight pipe before suction meets minimum 5× diameter requirement
- Check: All pump accessories (strainer, check valve, isolation valves, flexible connectors) are modeled
- Check: Pump Mark matches the engineering schedule (e.g., P-CHW-01, P-CHW-02)

**5. Common Mistake**
Modeling an isolation valve on the suction side but forgetting the strainer — the commissioning team will install the strainer on site but its location will clash with a wall bracket that was never coordinated.

**6. Today's Action**
In Revit, place one pump family. Add an isolation valve on each side. Add a check valve on the discharge side. Add a flexible connector on each side. Measure the total length of the pump assembly and confirm it fits in the allocated plant room space.

---

### Day 63 — Isolation Valves and Accessories in Revit

**1. Why This Matters**
Isolation valves and pipe accessories are not decorative — they control which sections of pipe can be shut down for maintenance. A missing isolation valve in the model means a missing valve on site, which means the entire system must be shut down to service a single FCU.

**2. Core Concept**
- Key pipe accessories and their function:
  - **Gate Valve / Ball Valve**: Full isolation (open or closed). Used at equipment connections and branch takeoffs
  - **Globe Valve**: Flow control (throttling). Used where fine flow adjustment is needed
  - **Check Valve**: Allows flow in one direction only. Used on pump discharge, bypass lines
  - **Strainer (Y-type)**: Removes debris from fluid. Always installed on suction side of pumps and before control valves
  - **Balancing Valve**: Manual or automatic flow balancing. Used at each FCU or AHU coil connection
  - **Pressure Reducing Valve (PRV)**: Reduces high pressure to a set value at system zones
  - **Flexible Connector**: Vibration isolation at pumps and equipment
- In Revit: use pipe accessory families — not just a pipe fitting. Each accessory has a unique family with a connector and a Mark parameter

**Valve Placement Rule of Thumb**

| Location | Valve Type |
|---|---|
| Equipment inlet/outlet | Isolation (ball or gate) valve |
| Branch takeoff from riser | Isolation valve |
| Pump suction | Strainer + Isolation valve |
| Pump discharge | Isolation valve + Check valve |
| FCU coil connection | 2-way or 3-way control valve + balancing valve |
| Zone isolation | Ball valve both sides of each floor branch |

**3. Real Project Lens**
An FCU on Level 4 requires: CHWS: ball valve → 2-way control valve → coil → ball valve → CHWR. The modeler places these accessories in sequence, sets the Mark for each valve (e.g., V-CHW-L4-FCU07-IN), and confirms the pipe sizes match the FCU connection size (typically DN20–DN25 for fan coils).

**4. BIM Check**
- Check: Every equipment connection point has an isolation valve modeled on both supply and return sides
- Check: Every pump has a strainer on the suction side
- Check: Control valves (2-way, 3-way) are placed on the correct side of the FCU coil (supply side for 2-way)

**5. Common Mistake**
Placing valve families that are too large — a DN50 ball valve placed on a DN25 branch creates a Revit connector mismatch error and prints incorrectly on the drawing.

**6. Today's Action**
In Revit (or a sample file), place one ball valve on a pipe branch. Confirm its size matches the pipe. Set the Mark parameter. Verify it appears in the pipe accessory schedule.

---

### Day 64 — Pipe Sizing Parameters

**1. Why This Matters**
Pipe sizing is engineering work — but the modeler must verify that the sizes in the Revit model match the engineer's design. Wrong pipe sizes in the model produce wrong material take-offs, wrong clash checks, and wrong shop drawings.

**2. Core Concept**
- Pipe size is defined by **Nominal Pipe Size (NPS)** in imperial or **DN (Diameter Nominal)** in metric
  - DN50 = NPS 2 inch (approximately)
  - DN100 = NPS 4 inch
  - DN150 = NPS 6 inch
  - DN200 = NPS 8 inch
- Pipe sizing is driven by:
  - **Flow rate** (L/s or GPM)
  - **Velocity limit** (typically 1.5–2.5 m/s for chilled water)
  - **Pressure drop limit** (typically 100–300 Pa/m)
- As flow branches out, pipe size reduces at each takeoff — the riser is the largest, the FCU connection is the smallest
- Wall thickness matters: pipe schedule (Schedule 40, Schedule 80) affects outer diameter — relevant for clash checking
- In Revit: pipe type (material + schedule) and size are set in type properties and instance properties

**Chilled Water Pipe Size Quick Reference**

| Flow Rate (L/s) | Suggested DN |
|---|---|
| 0.1–0.5 | DN20–DN25 |
| 0.5–2.0 | DN32–DN50 |
| 2.0–6.0 | DN65–DN100 |
| 6.0–15.0 | DN125–DN150 |
| 15.0–35.0 | DN200–DN250 |

**3. Real Project Lens**
The engineer's pipe schedule shows the Level 7 main branch at DN100 CHWS and CHWR. A junior modeler has drawn DN80 based on a misread drawing. The discrepancy is caught when the pipe schedule exported from Revit does not match the engineer's Excel schedule — saving a costly site change.

**4. BIM Check**
- Check: Export the pipe schedule from Revit (Mark, Size, System, Flow). Compare row by row to the engineer's schedule
- Check: Verify that pipe type (material) matches spec — carbon steel, CPVC, copper, or stainless steel per system type
- Check: Confirm pipe sizes reduce at every branch takeoff — no section that is larger downstream than upstream

**5. Common Mistake**
Changing a pipe size in the model without updating the pipe type — Revit may accept the size input but the pipe family has no corresponding size in its size table, resulting in a "pipe size not in type" warning that is often ignored.

**6. Today's Action**
Open the engineer's piping schedule (or a sample). Pick one pipe run. Calculate whether the velocity is within 1.5–2.5 m/s using: Velocity = Flow (L/s) ÷ Pipe Area (m²). Confirm the selected DN is appropriate.

---

### Day 65 — Mechanical Room Equipment Arrangement

**1. Why This Matters**
A mechanical room that looks tidy on plan but has no logical installation sequence or maintenance access will fail during both construction and operation. Equipment arrangement is a BIM coordination deliverable, not just an aesthetic choice.

**2. Core Concept**
- Mechanical room layout priorities:
  1. **Access for installation**: Can the largest equipment (chiller, pump skid) physically enter the room and be installed? Check door and corridor widths
  2. **Maintenance access**: Filters, strainers, and coils need clear front access — minimum 900mm
  3. **Pipe connection logic**: Equipment connections should align logically — inlet on one side, outlet on the other, in the direction of flow
  4. **Electrical clearance**: MCC panels, VFDs, and starters must have 1000mm front clearance (most electrical codes)
  5. **Floor drains**: All equipment with drain pans must be within 2m of a floor drain
  6. **Vibration and noise**: Pumps and air handling units need vibration isolators — model these as part of the equipment height
- Arrangement sequence: Place large equipment first (chillers, AHUs, cooling towers), then pumps, then headers, then accessories, then smaller equipment

**Mechanical Room Quick Check Table**

| Item | Minimum |
|---|---|
| Pump maintenance clearance | 600mm sides, 900mm front |
| Chiller maintenance | 1000mm tube pull clearance |
| Pipe header spacing | 150mm between pipe centerlines (minimum) |
| MCC front clearance | 1000mm |
| Aisle width | 1200mm minimum |
| Ceiling clearance above piping | 300mm minimum |

**3. Real Project Lens**
A chiller room on Level B2 contains two 500kW chillers, four primary pumps, and associated piping. The initial layout shows chillers side by side with pumps in front — but the chiller tube pull direction is toward the wall. A BIM review catches this and the chillers are rotated 90°, adding 2m to the room footprint. The structural team is informed early enough to revise the slab layout.

**4. BIM Check**
- Check: Model the tube pull direction for chillers as a reference plane or clearance volume — confirm it is unobstructed
- Check: All pump accessories (strainer, valves, gauges) are modeled and fit within the room without overlapping
- Check: Confirm the equipment installation path from the access door to final position — no width constraint larger than 100mm tighter than equipment dimension

**5. Common Mistake**
Modeling equipment at vendor-provided clearance minimums while forgetting that piping headers above the equipment also need space — resulting in a room where the ceiling is 200mm above the top of the pipe header with no room for insulation.

**6. Today's Action**
Sketch a simple mechanical room layout for a 3-pump arrangement (duty/standby/standby) with a common suction header and discharge header. Show the isolation valves, strainer, check valves, and where the floor drain should be located.

---

### Day 66 — Piping Clash with Structure and MEP

**1. Why This Matters**
Piping clashes — especially large-bore chilled water mains passing through structural beams or crossing other MEP systems — are among the most expensive to resolve on site. Each coordination failure can stop an entire floor of work while the clash is resolved.

**2. Core Concept**
- Most common piping clashes:
  - **Pipe through structural beam** (most critical — never cut flanges)
  - **Pipe through shear wall** (needs structural sleeve and fire stopping)
  - **CHW supply and return too close** (violates insulation clearance — typically need 50mm between insulated pipe surfaces)
  - **Piping crossing cable tray** (electrical separation and clearance conflict)
  - **Piping at riser shaft boundary** (pipe too large for the shaft opening)
- Clash resolution strategies:
  - Reroute the pipe to avoid the structural element
  - Use a structural penetration (beam web only — approved by structural engineer)
  - Negotiate with other MEP trades for vertical stacking (pipe below duct, tray above)
- In Navisworks: run Piping vs. Structure and Piping vs. All MEP tests separately — this gives cleaner clash grouping

**Piping Clash Priority**

| Clash | Priority | Resolution |
|---|---|---|
| Pipe through beam flange | P1 | Reroute — never cut |
| Pipe through shear wall no sleeve | P1 | Model sleeve, coordinate |
| CHW pipe insulation touching | P2 | Increase spacing |
| Pipe crossing cable tray < 100mm | P2 | Re-elevate one system |
| Pipe in shaft too wide | P1 | Revise shaft size or pipe path |

**3. Real Project Lens**
The 200mm CHWS riser passes through Level 3 floor slab. A 100mm diameter core is modeled — but the pipe insulation is 50mm thick, making the insulated OD 300mm. The core is too small. The BIM team catches this in the coordination model and requests a 350mm core to allow insulation and clearance.

**4. BIM Check**
- Check: All pipe penetrations through slabs and walls include modeled sleeve (or at minimum a penetration request submitted)
- Check: Insulated pipe sizes — add insulation thickness to OD before checking clearance (e.g., DN100 pipe + 50mm insulation = 214mm insulated OD)
- Check: Re-run clash test after all pipe re-routes — confirm zero remaining P1 clashes

**5. Common Mistake**
Running clash tests with bare pipe geometry only — the insulation adds 50–100mm to each side, which turns a "near miss" into a hard clash once insulation is installed on site.

**6. Today's Action**
For any pipe in your model (or a sample), calculate the insulated outside diameter using: Insulated OD = Pipe OD + (2 × insulation thickness). Compare to the available gap between the pipe and the nearest structural element. Does it pass?

---

### Day 67 — Week 1 Piping Review

**1. Why This Matters**
The fundamentals of piping BIM — system logic, pump configuration, valve placement, pipe sizing, room layout, and clash management — form the foundation for all piping work in Month 3. Gaps here will slow down every lesson from Day 68 onward.

**2. Core Concept**
**Week 1 Piping Summary**

| Day | Topic | Key Point |
|---|---|---|
| 61 | CHW System Overview | CHWS at 6–7°C, CHWR at 12–13°C. Separate piping systems in Revit |
| 62 | Pump Configuration | Straight pipe before suction. All accessories modeled |
| 63 | Valves and Accessories | Isolation, check, strainer, balancing — all at specific locations |
| 64 | Pipe Sizing | Match engineer's schedule. Velocity 1.5–2.5 m/s for chilled water |
| 65 | Mechanical Room Layout | Clearances, installation path, equipment sequencing |
| 66 | Piping Clashes | Include insulation OD in clash checks. Reroute before cutting structure |

**Critical Rules — Piping BIM**
- Supply and return are always separate piping systems — never combine
- Every pump needs: strainer, flexible connectors, isolation valves, check valve on discharge
- Model insulation thickness before running clearance checks
- Pipe sizes in Revit must match the engineer's schedule exactly
- Mechanical rooms need installation access paths — model them, do not assume

**3. Real Project Lens**
A piping BIM modeler given a new Level 2 mechanical room task uses the Week 1 checklist: (1) assign pipe systems correctly, (2) model pump accessories in sequence, (3) check sizes against schedule, (4) model clearance zones, (5) run clash check, (6) submit clash report. Total time from model open to clash report submission: 4 hours for an experienced modeler — 8 hours for a beginner still consolidating these skills.

**4. BIM Check**
- Check: Are all piping systems named correctly and assigned to every pipe in the model?
- Check: Is the mechanical room layout reviewed for installation sequence and clearance?
- Check: Has the insulated pipe OD been used in all clash checks?

**5. Common Mistake**
Rushing to Day 68 content without reviewing the six fundamentals from this week — the most common outcome is a piping model that looks complete but fails the coordination model review because of system naming errors and missing accessories.

**6. Today's Action**
Review your own pipe model (or a sample). Run a quick self-check against the six topics above. Write down the one area where you feel least confident. Focus next week's practice on that area.

---

---

### Track 9C: Plumbing / Sanitary

---

### Day 61 — Sanitary System Classification — Waste, Vent, Water

**1. Why This Matters**
Plumbing is divided into distinct systems that must never be connected to each other. Confusing a waste pipe with a vent pipe — or connecting a cold water supply to a sanitary line — creates health hazards and fails inspection. Correct system classification in the BIM model is the foundation of all plumbing coordination.

**2. Core Concept**
- Three primary plumbing system categories:
  - **Sanitary Waste**: Carries used water and sewage from fixtures (WC, basin, floor drain) to the building drain and public sewer. Flows by gravity. System type: "Sanitary"
  - **Vent**: Allows air into the drain system to maintain correct pressure (prevents siphoning of traps). Does not carry sewage. Connects to waste pipes but terminates above roof. System type: "Vent"
  - **Domestic Water**: Pressurized clean water supply — Cold Water Supply (CWS) and Hot Water Supply (HWS). Completely separate from sanitary. System types: "Domestic Cold Water", "Domestic Hot Water"
- In Revit: each pipe must be assigned to a named piping system that matches its actual function
- Visual color coding helps: sanitary typically shown in gray/brown; vent in yellow/green; cold water in blue; hot water in red

**System Classification Table**

| System | Flow Type | Direction | In Revit |
|---|---|---|---|
| Sanitary Waste | Gravity | Downward to sewer | "Sanitary" system |
| Vent | Air pressure relief | Upward to atmosphere | "Vent" system |
| Cold Water Supply | Pressurized | Distributed to fixtures | "Domestic Cold Water" |
| Hot Water Supply | Pressurized | Distributed to fixtures | "Domestic Hot Water" |
| Storm / Rainwater | Gravity | Downward to storm drain | "Storm" system |

**3. Real Project Lens**
On a hotel floor with 20 bathrooms, the BIM modeler creates four separate piping systems: Sanitary, Vent, CWS, HWS. Each WC connects to the Sanitary system. The vent pipe rises from each WC trap to a vent stack. CWS and HWS serve each basin and shower. The systems never cross-connect.

**4. BIM Check**
- Check: Every sanitary pipe is assigned to the Sanitary piping system — not "Unassigned"
- Check: Vent pipes connect to the tops of sanitary pipes (never to water supply)
- Check: Cold water and hot water are in separate, named systems — no pipe shared between them

**5. Common Mistake**
Assigning vent pipes to the sanitary system in Revit (because they appear to connect to sanitary lines) — this merges the two systems in schedules and makes it impossible to generate a separate vent riser diagram.

**6. Today's Action**
In Revit, create three piping systems: Sanitary, Vent, and Domestic Cold Water. Place one pipe in each system. Verify in the Mechanical Systems Browser that each pipe appears under its correct system.

---

### Day 62 — Gravity Drainage and Slope Modeling in Revit

**1. Why This Matters**
Sanitary drainage works by gravity — the pipe must slope downward continuously from the fixture to the drain point. A flat sanitary pipe will block. A pipe with back-fall will cause sewage to pool and back up into fixtures. Slope modeling in Revit is a specific technical skill that must be learned correctly.

**2. Core Concept**
- Standard slope requirements:
  - DN50–DN75 waste pipes: minimum 1:40 (25mm fall per 1000mm run)
  - DN100 (WC waste): minimum 1:80 (12.5mm fall per 1000mm run)
  - DN150 and larger: minimum 1:150 (6.7mm fall per 1000mm run)
- How to set slope in Revit:
  - Select a pipe → Properties → Slope parameter (set as percentage or ratio)
  - Or use the "Slope" tool in the Pipe tab for pitched pipes
  - Always set the high end first (at the fixture) and slope toward the branch collector or stack
- Slope direction: flow arrow must point downward in elevation — from fixture to drain
- Slope accumulates: if two branches join, the combined slope continues to the stack
- Stack (vertical pipe): carries drainage from all floors vertically — no slope needed, it is vertical

**Slope Reference Table**

| Pipe Size | Minimum Slope | Fall per Metre |
|---|---|---|
| DN50 | 1:40 | 25mm |
| DN75 | 1:40 | 25mm |
| DN100 | 1:80 | 12.5mm |
| DN150 | 1:100 | 10mm |

**3. Real Project Lens**
A bathroom on Level 5 has a WC at one end and a floor drain at the other — a run of 4.5 metres. The WC waste (DN100) must slope at 1:80 — a total fall of 56mm over 4.5m. The pipe start elevation is set at 400mm below finished floor level. The pipe end elevation at the stack connection is 400 + 56 = 456mm below finished floor. The modeler inputs these elevations and confirms the slope with Revit's slope indicator.

**4. BIM Check**
- Check: All sanitary branch pipes have a slope parameter — no horizontal sanitary pipes
- Check: Slope direction is toward the stack or collector — not back toward the fixture
- Check: Calculate total fall for the longest branch — confirm it fits within the floor zone (does not drop below the slab soffit below)

**5. Common Mistake**
Setting a slope on a pipe that was originally placed horizontally — Revit adjusts the pipe in one direction but the fitting connections at each end may not update correctly, creating a geometric gap in the pipe run.

**6. Today's Action**
In Revit, draw a 3-metre horizontal sanitary pipe. Set a slope of 1:80 from one end. Check the elevation difference between the start and end of the pipe. Confirm it shows approximately 37.5mm fall.

---

### Day 63 — Vertical Riser Planning and Sleeve Requests

**1. Why This Matters**
Plumbing risers — the vertical stacks that carry drainage and water supply between floors — must pass through floor slabs. Every penetration must be planned, sized, and approved before concrete is poured. A missed sleeve means core-drilling after construction — which is expensive and may cut through rebar.

**2. Core Concept**
- Plumbing riser types:
  - **Soil Stack**: Carries WC waste (black water) vertically — minimum DN100
  - **Waste Stack**: Carries waste from basins, showers (gray water) — typically DN75–DN100
  - **Vent Stack**: Carries air for the drainage system — typically DN50–DN75
  - **Cold and Hot Water Risers**: Pressurized supply — size varies by floor demand
- Sleeve sizing rule: Sleeve diameter = Pipe OD + Insulation (if any) + 25mm clearance
  - Example: DN100 soil stack OD = 114mm. No insulation. Sleeve = 114 + 25 = 139mm → use 150mm sleeve
- Sleeve location: must be coordinated with structural team — never through structural beams or within 300mm of a beam
- Sleeve request process:
  1. Finalize riser location in BIM model
  2. Export sleeve drawing (plan view with grid references and elevations)
  3. Submit to structural team with a written request before slab pour date
  4. Structural team confirms or revises location
  5. Contractor installs sleeve before concrete pour

**3. Real Project Lens**
A 20-floor residential tower has a wet wall with 6 plumbing stacks (2 soil, 2 waste, 1 vent, 1 CWS riser) on every floor. The BIM modeler creates a sleeve schedule from Revit — listing each sleeve: grid reference, floor level, pipe size, sleeve size, top of sleeve elevation. This schedule is submitted to the structural engineer 8 weeks before the first slab pour.

**4. BIM Check**
- Check: Every vertical pipe penetrating a slab has a sleeve modeled (or at minimum a penetration request logged)
- Check: Sleeve size = Pipe OD + clearance. Confirm no sleeve is undersized
- Check: Sleeve locations are at least 300mm from structural beams (check against structural model)

**5. Common Mistake**
Submitting a sleeve request with only pipe sizes listed — the structural engineer needs the sleeve centerline coordinates (X, Y from grids, Z elevation) to locate the sleeve in the formwork. Missing coordinates means the sleeve is placed in the wrong location.

**6. Today's Action**
Pick one sanitary riser in a model (or sketch). Calculate the required sleeve size (Pipe OD + 25mm clearance). Then write a one-line sleeve request entry: Grid reference, Level, Pipe size, Sleeve size, Top of slab elevation.

---

### Day 64 — Fixture Connections — WC, Basin, Sink

**1. Why This Matters**
Plumbing fixture connections are the final link between the designed plumbing system and the actual building function. Wrong connection sizes, wrong trap types, or missing vents cause blocked drains, odors, and code violations that require significant rework.

**2. Core Concept**
- Each fixture has specific connection requirements:

| Fixture | Waste Size | Trap Type | Water Supply |
|---|---|---|---|
| WC (toilet) | DN100 | Integral P-trap | CWS only (DN15) |
| Wash basin | DN32–DN40 | P-trap (external) | CWS + HWS (DN15) |
| Kitchen sink | DN40–DN50 | P-trap | CWS + HWS (DN15) |
| Urinal | DN50 | P-trap | CWS (DN15) |
| Floor drain | DN50–DN100 | Deep-seal trap | None (drain only) |
| Shower | DN50 | P-trap (internal) | CWS + HWS (DN20) |

- In Revit: plumbing fixtures are families with built-in connectors — a waste connector, and CWS and HWS connectors
- Connect waste connector to the sanitary branch pipe — match sizes
- Connect CWS and HWS connectors to the water supply pipes — match sizes
- Check trap-to-vent distance: P-trap must be within a maximum distance from the vent connection (typically 750mm for DN40, 1500mm for DN100 — check local code)

**3. Real Project Lens**
On a hotel floor, 20 bathrooms each have: 1 WC, 1 basin, 1 shower, 1 floor drain. The modeler places the fixture families, connects each waste to the horizontal branch, connects CWS and HWS to the supply branches. The vent pipes connect to the sanitary branches within code-required trap-to-vent distances. The system is fully connected with no open connectors.

**4. BIM Check**
- Check: Every fixture has both waste and water connections made — no open connectors
- Check: WC waste is DN100 — no WC connected to a DN50 waste branch
- Check: All P-traps are modeled (as part of fixture family or as separate fitting) — no untrapped drain connections

**5. Common Mistake**
Connecting a basin waste (DN32) to a WC soil branch (DN100) without a reducer fitting — Revit may allow the connection but the drawing will show a size mismatch that the plumbing inspector will reject.

**6. Today's Action**
In Revit, place one WC family and one basin family. Connect each to a sanitary branch pipe. Confirm the waste connector sizes match the pipe sizes. Check the Properties of each fixture and confirm CWS and HWS connectors show flow direction correctly.

---

### Day 65 — Domestic Water Supply Distribution

**1. Why This Matters**
The domestic water supply system delivers clean potable water to every fixture. Undersized pipes cause low pressure at outlets. Oversized pipes waste material. A poorly designed distribution layout causes cross-connections or dead legs that breed bacteria.

**2. Core Concept**
- Water supply distribution types:
  - **Direct system**: Mains pressure supplies all fixtures directly (low-rise buildings)
  - **Break tank and booster pump system**: Water stored in a tank, pumped up to high zones (high-rise or low mains pressure areas)
  - **Downfeed system**: Water pumped to a roof tank, gravity-feeds down to floors (some older or institutional buildings)
- Pipe sizing is based on **fixture units** (each fixture is rated a demand value):
  - WC: 8 fixture units
  - Basin tap: 1.5 fixture units
  - Shower: 3 fixture units
  - Sink: 3 fixture units
- As branch pipes move further from the riser, fewer fixtures are served and pipe size reduces
- Dead legs (a pipe that ends at one fixture with no circulation): maximum 3 litres of water in the pipe — beyond this, hot water cools and risks Legionella growth
- Insulation: hot water supply pipes must be insulated to retain heat. Cold water pipes in hot areas also insulated to prevent condensation

**CWS/HWS Branch Sizing Guide**

| Fixtures Served | Suggested CWS/HWS Pipe Size |
|---|---|
| 1–2 | DN15 |
| 3–6 | DN20 |
| 7–12 | DN25 |
| 12–20 | DN32 |
| 20–40 | DN40–DN50 |

**3. Real Project Lens**
A 15-storey apartment block has one cold water riser (DN65) and one hot water riser (DN50) rising from the basement plant room. On each floor, a DN25 branch serves 4 apartments. Each apartment has a local sub-distribution with DN15 and DN20 branches to each fixture. The BIM modeler sizes each segment from the riser outward, reducing size at each branch takeoff.

**4. BIM Check**
- Check: Pipe sizes reduce at every branch — no segment is larger downstream than upstream
- Check: Dead leg lengths are under code maximum (check local plumbing code — typically equivalent to 3 litres pipe volume)
- Check: CWS and HWS pipes are separate throughout — no common pipe carrying both temperatures

**5. Common Mistake**
Running the HWS distribution at the same elevation as the CWS pipe in the ceiling — the hot pipe raises the temperature of the cold pipe above it by convection, causing the cold water to warm above 20°C, which is a Legionella risk.

**6. Today's Action**
For a simple bathroom group (WC, basin, shower), calculate the total fixture units for CWS and HWS. Use the table above to select the branch pipe size. Draw the distribution from the riser to each fixture with correct sizes.

---

### Day 66 — Sanitary Clash Patterns — Slab and Structure

**1. Why This Matters**
Sanitary pipes are gravity-driven, which means they slope downward through the floor zone. This brings them into frequent conflict with structural beams, slabs, and other MEP services at low elevations. Sanitary clashes are often discovered too late — after slabs are poured or ceilings are installed.

**2. Core Concept**
- Most common sanitary clash patterns:
  - **Sloped pipe drops below slab soffit** (pipe falls too far along a long horizontal run)
  - **Sanitary branch crosses structural beam at the same elevation** (gravity slope means the pipe cannot easily route over or under)
  - **Soil stack core not large enough** (insulation and clearance not accounted for)
  - **Floor drain at slab level clashes with beam below** (drain body extends into the structural zone)
  - **Horizontal branch at ceiling conflicts with HVAC duct** (both systems competing for the narrow ceiling zone)
- Solutions:
  - For long horizontal runs that drop below the slab: use an additional stack closer to the fixtures to limit run length
  - For beam crossings: request a structural penetration in the beam web (with engineer approval)
  - For stack cores: verify insulated OD before requesting core size
  - For drain bodies: select slim-profile drain families or coordinate drain location with structural layout

**Sanitary Clash Priority Table**

| Clash | Priority | Resolution |
|---|---|---|
| Sanitary pipe below slab soffit | P1 | Add stack or reroute |
| Sanitary through beam flange | P1 | Reroute — structural approval needed |
| Stack core undersized | P1 | Revise sleeve request before pour |
| Sanitary vs. HVAC in ceiling | P2 | Re-elevate HVAC or add duct depth |
| Drain body in structural zone | P2 | Coordinate drain location |

**3. Real Project Lens**
On Level 3 of an office building with 4m floor-to-floor height, a 6m long DN100 WC waste branch must connect to the stack. At 1:80 slope, the pipe falls 75mm over 6m. Starting at 400mm below FFl, the pipe ends at 475mm below FFl — still within the 600mm structural zone. Acceptable — but if the run were 10m, the fall would be 125mm, potentially clashing with the beam zone. The BIM modeler checks this for every long branch.

**4. BIM Check**
- Check: For every horizontal sanitary run longer than 3m, calculate total fall and check it stays above beam soffit level
- Check: All floor drain bodies are checked against structural beam layout — drain centerlines should be between beams
- Check: Run a clash test in Navisworks — Sanitary Piping vs. Structure. Review all P1 results before submitting

**5. Common Mistake**
Not modeling the sloped pipe correctly in Revit (pipe placed flat, slope parameter set but not reflected in geometry) — the model appears fine but the 3D geometry shows a flat pipe, causing the clash report to miss the real clash that would occur in the field.

**6. Today's Action**
Find the longest horizontal sanitary run in a model (or estimate one on paper). Calculate the total fall using the appropriate slope. Check whether the pipe invert at the downstream end is above the beam soffit below.

---

### Day 67 — Week 1 Plumbing Review

**1. Why This Matters**
Plumbing BIM requires precision in system classification, slope geometry, sleeve coordination, fixture connectivity, and spatial clash management. A one-week review ensures these fundamentals are locked in before advancing to more complex plumbing scenarios.

**2. Core Concept**
**Week 1 Plumbing Summary**

| Day | Topic | Key Point |
|---|---|---|
| 61 | System Classification | Sanitary, Vent, CWS, HWS — four separate systems, never cross-connect |
| 62 | Gravity Drainage and Slope | DN100 = 1:80 min slope. Set slope in Revit. Check total fall fits in floor zone |
| 63 | Riser and Sleeve Planning | Sleeve = Pipe OD + clearance. Submit sleeve schedule before slab pour |
| 64 | Fixture Connections | Each fixture has specific waste size and water supply size. No open connectors |
| 65 | Water Supply Distribution | Pipe size reduces at each branch. Avoid dead legs > 3 litres |
| 66 | Sanitary Clashes | Long runs fall below slab. Stack core must include insulation OD |

**Critical Rules — Plumbing BIM**
- Sanitary and vent are separate systems — do not merge in Revit
- Every horizontal sanitary pipe must have a slope — never flat
- Sleeve requests must be submitted before slab pour with exact coordinates
- Model P-traps for every fixture — missing traps fail plumbing inspection
- Dead legs in HWS must be within code limit — Legionella risk

**3. Real Project Lens**
A plumbing BIM modeler joins a hotel project on Day 1 of a new floor. Using the Week 1 skills, they: assign system types to all pipes, set slopes on all branches, submit a sleeve schedule, connect all fixtures, check dead leg lengths, and run a sanitary clash test — before handing the model to the coordination team. This structured approach prevents the most common plumbing rework scenarios.

**4. BIM Check**
- Check: Systems Browser — no pipe showing as "Unassigned"
- Check: Every sanitary branch has a slope parameter and the slope direction is correct
- Check: Sleeve schedule drafted and ready for structural submission

**5. Common Mistake**
Believing plumbing BIM is simpler than HVAC or piping because the pipes are smaller — then missing the slope and clearance checks that are specific to sanitary systems and failing the coordination review.

**6. Today's Action**
Open any plumbing model (or create a simple test model). Verify: (1) system assignments, (2) slope on sanitary branches, (3) fixture connections. Write a short personal checklist you will use at the start of every plumbing model review.

---

---

### Track 9D: Fire Protection

---

### Day 61 — Fire Protection System Types — Wet, Dry, Pre-Action

**1. Why This Matters**
Fire protection systems are life safety systems. Modeling the wrong system type in the BIM model — for example, showing a wet system in a freezer room where a dry system is required — creates a non-compliant installation that will fail authority inspection and potentially endanger lives.

**2. Core Concept**
- Three primary automatic sprinkler system types:

| System Type | How It Works | Where Used |
|---|---|---|
| Wet Pipe | Pipes always filled with water under pressure. Sprinkler opens → water flows immediately | Offices, hotels, retail, most occupied spaces |
| Dry Pipe | Pipes filled with pressurized air/nitrogen. Water enters only after sprinkler opens and air releases | Freezer rooms, unheated carparks, loading docks |
| Pre-Action | Requires two events: detection AND sprinkler activation. Until both occur, no water | Data centers, museums, archive rooms |

- Additional system types:
  - **Deluge**: All sprinkler heads are open — no fusible element. Water covers entire area simultaneously. Used in high-hazard areas (aircraft hangars, chemical storage)
  - **Foam/Water**: Water mixed with foam concentrate. Aircraft hangars and fuel storage
- In Revit: pipe system type is set as "Fire Protection Wet", "Fire Protection Dry", or "Fire Protection Pre-Action" — this affects schedules and drawings
- Zone boundary: each system type occupies a separately valved zone — the BIM model must show zone valves (alarm check valve assembly, dry pipe valve, pre-action valve)

**3. Real Project Lens**
A mixed-use building has offices (wet system), a freezer room in the kitchen (dry system), and a server room (pre-action). The BIM modeler creates three separate fire protection systems in Revit — one per type. Zone valves are modeled at the riser for each system. Pipe color is coded per system type for clarity.

**4. BIM Check**
- Check: Each zone of the model is assigned the correct system type (wet, dry, pre-action)
- Check: Zone valve assemblies are modeled at the correct locations — one per zone
- Check: Dry pipe zones do not overlap with wet pipe zones — no shared pipe between the two

**5. Common Mistake**
Modeling a dry pipe zone as a wet pipe system because the pipes look identical on plan — this error is invisible until the hydraulic calculation is run or the authority inspector reviews the drawings.

**6. Today's Action**
Identify the fire protection system types required on a project you are working on or a sample project. List: (1) each zone, (2) system type for that zone, (3) the reason for that system type selection.

---

### Day 62 — Sprinkler Head Placement Rules

**1. Why This Matters**
Sprinkler heads that are placed incorrectly will not activate when needed or will activate and not cover the fire area. Both outcomes are life safety failures. Placement rules are defined by NFPA 13, EN 12845, or local standards — and the BIM model must reflect these rules.

**2. Core Concept**
- Key sprinkler placement rules (based on NFPA 13 as reference — verify local code):
  - **Maximum coverage area per head**: Depends on hazard classification
    - Light Hazard (offices, hotels): up to 20.9 m² per head
    - Ordinary Hazard Group 1 (retail, dining): up to 12.1 m²
    - Extra Hazard: up to 9.3 m²
  - **Maximum spacing between heads**: 4.6m (Light), 4.6m (Ordinary) — check local code
  - **Maximum distance from wall to first head**: half the maximum spacing (e.g., 2.3m for 4.6m max)
  - **Obstruction rule**: If an obstruction (beam, duct) is deeper than 150mm, add a sprinkler below the obstruction
  - **Ceiling type matters**: Flat ceiling = pendant heads. Exposed structure = upright heads. Concealed ceiling = concealed heads

**Sprinkler Layout Quick Reference**

| Space Type | Head Type | Max Area/Head | Max Spacing |
|---|---|---|---|
| Open office | Pendant (concealed) | 20.9 m² | 4.6m |
| Storage room | Upright | 9.3 m² | 3.7m |
| Carpark | Pendant (standard) | 12.1 m² | 4.6m |
| Corridor | Pendant | 20.9 m² | 4.6m |

**3. Real Project Lens**
An open-plan office floor plate of 800m² is served by pendant concealed sprinklers at light hazard classification. Maximum area per head = 20.9m². Minimum heads required = 800 ÷ 20.9 = 39 heads. The BIM modeler lays out heads in a regular grid, verifying maximum distance from walls and between heads, then checks for beams deeper than 150mm that require additional sub-beam heads.

**4. BIM Check**
- Check: Calculate area coverage per head — confirm no head exceeds the maximum for its hazard classification
- Check: Measure distance from each wall to the nearest head — confirm it is less than half the maximum spacing
- Check: Check all beams and ducts deeper than 150mm — confirm sub-obstruction heads are added

**5. Common Mistake**
Placing sprinkler heads at a regular grid without checking the maximum distance from the wall — the first row of heads ends up 3.5m from the wall in a light hazard zone, exceeding the 2.3m limit.

**6. Today's Action**
For a room 10m x 8m (80 m²) at Light Hazard classification, calculate the minimum number of heads required. Sketch a grid layout that satisfies both the maximum coverage area and the maximum distance-from-wall rule.

---

### Day 63 — Main and Branch Pipe Routing

**1. Why This Matters**
The routing of fire protection mains and branch lines determines how water reaches each sprinkler head. Poor routing creates hydraulic imbalance (some heads get too much flow, others too little), unnecessary clashes with other MEP systems, and maintenance access problems.

**2. Core Concept**
- Fire protection pipe hierarchy:
  - **Main (or Riser Main)**: The primary supply pipe from the pump room or riser — typically DN100–DN150
  - **Cross Main**: Horizontal pipe fed from the main, running the long axis of the floor — typically DN65–DN100
  - **Branch Line**: Pipes fed from the cross main, running perpendicular to it — typically DN25–DN50
  - **Sprinkler Drop**: Short pipe from the branch line to each sprinkler head — typically DN20–DN25
- Tree system vs. Loop system:
  - **Tree (dead-end)**: One flow path. Simpler. Used in smaller zones
  - **Loop (gridded)**: Water can reach a head from two directions. More resilient. Used in large open floors
- Routing rules:
  - Branch lines should be parallel and evenly spaced
  - Cross main should be centered on the floor plate for balanced pressure distribution
  - Avoid routing branch lines below air conditioning ducts without checking clearance

**3. Real Project Lens**
An office floor 50m × 25m uses a gridded system. A DN100 cross main runs north-south at mid-floor. DN50 branch lines run east-west at 3.6m centers. DN25 drops serve each pendant head. The grid pattern allows hydraulic balance and any single branch failure does not render a large area unprotected.

**4. BIM Check**
- Check: Cross main is connected to the riser with a zone control valve (alarm check valve assembly) — confirm it is modeled
- Check: Branch lines are evenly spaced — no branch spacing exceeds the maximum coverage distance
- Check: Sprinkler drops are modeled at the correct elevation — pendant head face is at the correct distance from the ceiling (typically 25–150mm below ceiling face)

**5. Common Mistake**
Routing branch lines over the top of air conditioning ducts, then adding sprinkler drops that must penetrate the duct insulation to reach the ceiling level — creating a clash that is impossible to resolve without rerouting the branch line.

**6. Today's Action**
For a floor plate 30m × 20m, sketch (on paper) a tree or gridded fire protection layout. Show: riser connection point, cross main, branch lines, and approximate head positions. Label approximate pipe sizes at each level of the hierarchy.

---

### Day 64 — Standpipe and Hose Reel Locations

**1. Why This Matters**
Standpipe systems and hose reels provide manual firefighting capability. Their location is governed by reach distance — if a hose reel is too far from any point in the building, fire cannot be fought manually with the installed equipment. BIM models must reflect code-compliant placement.

**2. Core Concept**
- **Standpipe**: A fixed pipe system with outlet connections for fire brigade hoses. Rises vertically through the building. Typically DN100–DN150
  - Class I: For fire brigade use only (2.5" outlets in stairwells)
  - Class II: For building occupant use (1.5" hose reels)
  - Class III: Both
- **Hose Reel**: A cabinet containing a flexible hose (25mm or 19mm diameter, 30m long) for occupant use in early-stage fires
- Coverage rule: every point in the building must be within 30m hose reach of a hose reel (accounting for walls and corridors — not straight-line distance)
- Placement: typically in corridors near stairwells and fire exits, at maximum 30m spacing
- In Revit: model the hose reel cabinet as an equipment family (wall-mounted or recessed). Connect to the domestic/fire water supply with an isolation valve
- Standpipe outlet elevation: 750mm–1000mm above finished floor level

**Hose Reel Placement Checklist**

| Requirement | Value |
|---|---|
| Maximum hose length | 30m (flexible hose) |
| Coverage radius | 30m from cabinet (path distance, not straight line) |
| Maximum spacing | 30–35m between hose reels |
| Height of outlet | 750–1000mm AFF |
| Supply pipe size | DN25 (hose reel) / DN100 (standpipe) |

**3. Real Project Lens**
A 60m long corridor with fire exit stairs at each end has two hose reel cabinets — one at 20m from each end. A path coverage check in the BIM model confirms that every office door in the corridor is within 30m path distance of at least one hose reel.

**4. BIM Check**
- Check: Model hose reels as placed families, not just symbols. Confirm wall recess depth is within the wall construction depth
- Check: Standpipe outlet heights are modeled at 750–1000mm AFF — not at floor level or ceiling level
- Check: For every hose reel, trace a 30m path (using a measurement tool) to the furthest point it must serve — confirm it reaches

**5. Common Mistake**
Measuring hose reel coverage using straight-line distance — a hose reel that covers 30m straight-line may only cover 18m of an L-shaped corridor because the hose must go around the corner.

**6. Today's Action**
On a floor plan (sketch or real), place one hose reel in a corridor. Trace the 30m path coverage along actual corridor routes (around corners and through doors). Identify any uncovered area. Add a second hose reel if needed.

---

### Day 65 — Hydraulic Calculation Basics for Modelers

**1. Why This Matters**
Hydraulic calculations determine the minimum pressure and flow required at the water supply to ensure the most remote sprinkler heads operate correctly. A BIM modeler does not perform engineering calculations — but must understand what the calculations require and ensure the model supports them.

**2. Core Concept**
- Hydraulic calculation determines:
  - **Design area**: The worst-case group of sprinkler heads that could activate simultaneously (typically a 139 m² area for Light Hazard per NFPA 13)
  - **Flow rate**: Total water demand from all heads in the design area
  - **Pressure**: Required pressure at the inlet to the design area
  - **Pipe sizes**: Must be sufficient to deliver the required flow at the required pressure
- Key parameters the modeler must get correct for calculations to work:
  - Pipe size and material (affects friction loss)
  - Pipe routing and length (affects friction loss calculation)
  - Fittings count (each elbow, tee adds equivalent pipe length for friction)
  - Head K-factor (a property of the sprinkler head — typically K=80 or K=115 in metric)
- Most remote area: hydraulic calculations focus on the area farthest from the water supply — ensure the model shows the most challenging routing accurately
- The modeler's role: ensure pipe sizes match the hydraulic calculation output; flag any field changes to the engineer for recalculation

**Key Terms for Modelers**

| Term | Meaning |
|---|---|
| K-factor | Sprinkler discharge coefficient (higher K = more flow per unit pressure) |
| Design density | L/min/m² required at the ceiling (e.g., 4 L/min/m² for Light Hazard) |
| Residual pressure | Pressure remaining after system losses — must meet minimum at remote head |
| Hazen-Williams C | Pipe material friction coefficient (e.g., steel = 120, CPVC = 150) |

**3. Real Project Lens**
The fire engineer calculates that the remote design area on Level 8 requires 750 L/min at 0.7 bar at the branch line inlet. They specify DN50 branch lines and a DN80 cross main. The modeler checks the Revit model — all branch lines are DN50, cross main is DN80, and pipe lengths match the engineer's routing assumption. No discrepancy. Calculation is valid.

**4. BIM Check**
- Check: Pipe sizes in the model match the hydraulic calculation output — do not change pipe sizes without informing the fire engineer
- Check: Pipe material in Revit matches the material used in the calculation (steel, CPVC, or stainless)
- Check: If any pipes were rerouted (longer path), notify the fire engineer — the recalculation may require larger pipes

**5. Common Mistake**
Re-routing a branch line 3m longer to avoid a clash — without telling the fire engineer. The longer route increases friction loss, which may drop pressure below the required minimum at the remote head, making the calculation invalid.

**6. Today's Action**
Find a fire protection hydraulic calculation sheet (or a sample online). Identify: (1) the design area, (2) the required flow rate, (3) the required pressure at the system inlet. Write these three numbers down — they are the key outputs the modeler must protect in the BIM model.

---

### Day 66 — Fire Protection Clash with HVAC and Ceiling

**1. Why This Matters**
Fire protection branch lines and sprinkler drops run at ceiling level — exactly where HVAC ducts, cable trays, and light fittings compete for space. Clashes in the ceiling zone are the most common fire protection coordination issue and must be resolved before ceiling installation.

**2. Core Concept**
- Common fire protection clash patterns:
  - **Sprinkler head conflicts with HVAC supply diffuser** (both at ceiling face level)
  - **Branch line behind HVAC duct** (blocks access to sprinkler head)
  - **Sprinkler drop passes through HVAC flexible duct**
  - **Head position obstructed by light fitting or ceiling grid**
  - **Branch line too close to cable tray** (minimum 150mm separation from electrical)
- Code requirement: sprinkler heads must be within a maximum distance from the ceiling face (NFPA 13: 25mm to 300mm below ceiling, depending on head type)
- Coordination priority: fire protection head positions are often fixed by coverage geometry — other trades must route around them
- Concealed ceiling: sprinkler heads must align with ceiling grid modules — coordinate with architect
- Obstruction rule: if an HVAC duct or beam is deeper than 150mm and the branch line is on one side, a separate head is needed on the other side of the obstruction

**Ceiling Zone Coordination Hierarchy**

| Priority | System |
|---|---|
| 1 (top) | Structural elements (beams, slab) |
| 2 | Large HVAC supply/return mains |
| 3 | Lighting (recessed) |
| 4 | Fire protection branch lines |
| 5 | Cable trays (small power/data) |
| 6 | Flexible ducts, small pipes |

**3. Real Project Lens**
On a Level 4 office floor, the HVAC coordination model shows 600×250mm supply ducts at 2700mm ceiling height, with the duct soffit at 2450mm. Fire protection branch lines need to be below the duct at 2300mm to serve concealed pendant heads at 2200mm (face of ceiling). The modeler adjusts branch line elevation to route under the ducts, adding elbows where needed. The fire engineer is notified to confirm the routing does not significantly increase friction loss.

**4. BIM Check**
- Check: All sprinkler heads are within code distance from ceiling face (25–300mm for pendant heads)
- Check: No sprinkler drop passes through an HVAC duct or flexible duct — check in 3D view
- Check: Branch lines maintain 150mm minimum clearance from cable trays and electrical conduits

**5. Common Mistake**
Routing the fire protection branch line above the HVAC duct to avoid clashing — then discovering the sprinkler drop cannot reach the ceiling face without passing through the duct, because the branch is now 600mm above the ceiling.

**6. Today's Action**
In a 3D BIM view (or Navisworks), navigate to the ceiling zone on one floor. Visually check: (1) Are any sprinkler heads behind or inside an HVAC duct? (2) Are any drops cutting through duct insulation? (3) Do all heads clear the ceiling grid modules?

---

### Day 67 — Week 1 Fire Protection Review

**1. Why This Matters**
Fire protection is a life safety system. Every lesson from Days 61–66 directly affects whether people in a building are protected or not. The Week 1 review reinforces the non-negotiable rules that separate compliant fire protection BIM from non-compliant modeling.

**2. Core Concept**
**Week 1 Fire Protection Summary**

| Day | Topic | Key Point |
|---|---|---|
| 61 | System Types | Wet, dry, pre-action — determined by environment, not preference |
| 62 | Head Placement | Coverage area per head must not exceed hazard classification limit |
| 63 | Pipe Routing | Main → cross main → branch → drop. Size reduces at each level |
| 64 | Standpipe and Hose Reel | 30m path coverage per hose reel. Not straight-line distance |
| 65 | Hydraulic Calculations | Modeler must preserve pipe sizes and routing that the engineer calculated |
| 66 | Ceiling Zone Clashes | Heads must be within code distance from ceiling. Route branches under ducts |

**Critical Rules — Fire Protection BIM**
- Never change fire protection pipe sizes without notifying the fire engineer
- Never place a wet pipe system in a space that requires dry (freezer room, unheated zone)
- Head coverage must be calculated — never guessed
- 30m hose reel coverage is path distance, not straight-line
- Sprinkler drops must reach the ceiling face — check elevation carefully
- Any pipe re-route must be flagged to the fire engineer for recalculation review

**3. Real Project Lens**
A fire protection modeler on Day 1 of a new floor uses the Week 1 framework: (1) confirm system type for each zone, (2) check head coverage calculations, (3) verify pipe hierarchy sizes match the engineer's output, (4) confirm hose reel locations by path coverage, (5) run a ceiling zone clash test. This structured approach prevents the three most common fire protection BIM failures: wrong system type, incorrect coverage, and ceiling zone clashes.

**4. BIM Check**
- Check: Every zone of the building has the correct fire protection system type assigned
- Check: Head coverage calculation is documented — maximum area per head does not exceed limit
- Check: All hose reel coverage has been verified by path distance measurement

**5. Common Mistake**
Treating fire protection BIM as the same as HVAC or piping BIM — it is not. The life safety consequences mean zero tolerance for missing heads, wrong system types, or pipe size errors. The bar is higher.

**6. Today's Action**
Write a personal fire protection BIM checklist — 5 items you will check on every fire protection model before submission. This list will grow as you advance through Day 90.

---

---

### Track 9E: Electrical

---

### Day 61 — Power Distribution Overview — MSB to DB to Circuits

**1. Why This Matters**
Understanding how electrical power flows from the incoming supply to the final outlet is the foundation of all electrical BIM work. Without this understanding, you cannot correctly model distribution boards, route cable trays, or coordinate with other MEP systems.

**2. Core Concept**
- Electrical power distribution hierarchy:

| Level | Equipment | Description |
|---|---|---|
| Incoming Supply | HV Switchgear / Transformer | High voltage from utility converted to LV |
| Main Distribution | MSB (Main Switchboard) | Central LV distribution point for the building |
| Sub-Distribution | DB (Distribution Board) | Serves one floor or zone |
| Final Circuit | MCB / Isolator | Individual circuit to a socket, lighting point, or equipment |

- MSB (Main Switchboard): located near the incoming supply (basement or ground floor), houses the main circuit breakers for each riser and major distribution circuit
- DB (Distribution Board): one per floor or per zone. Houses MCBs for all circuits on that floor. Fed from MSB or sub-MSB via a riser cable
- The riser: cables or busbar trunking rising from MSB to each floor DB — housed in an electrical riser shaft
- In Revit: MSB and DBs are modeled as equipment families placed in electrical rooms and within office floor areas respectively
- Electrical circuits: assigned in Revit from the DB to each connected device (light, socket, equipment)

**3. Real Project Lens**
A 10-floor office building has: one MSB in the basement electrical room, one sub-DB on Level 1 (for basement and Level 1), and one DB per floor on Levels 2–10. Each floor DB is fed by a cable rising in the dedicated electrical riser shaft. The floor DB feeds lighting circuits, power circuits, and a UPS circuit for IT equipment.

**4. BIM Check**
- Check: MSB is modeled in the electrical room with accurate dimensions from the vendor datasheet
- Check: Each floor has a DB modeled at the correct location (typically near the riser shaft or in the electrical cupboard)
- Check: Riser cables or busbar trunking are modeled in the riser shaft — confirm they fit within the shaft cross-section

**5. Common Mistake**
Modeling DBs as generic boxes without checking actual panel dimensions — on site, the DB may be 200mm deeper than the wall niche allows, requiring an expensive wall reconstruction.

**6. Today's Action**
Sketch the electrical distribution diagram for a 5-floor building: Incoming supply → Transformer → MSB → Sub-DB → DB per floor. Label each item. This diagram is your reference for the next 6 days.

---

### Day 62 — Cable Tray Sizing and Routing Basics

**1. Why This Matters**
Cable trays carry power, data, and control cables through the building. An undersized cable tray cannot accommodate all cables. An oversized tray wastes ceiling space and creates unnecessary clashes with HVAC. Incorrect routing creates safety hazards (power cables too close to data cables) and maintenance access problems.

**2. Core Concept**
- Cable tray types:
  - **Ladder Tray**: Open rung design for heavy power cables. Good airflow — preferred for HV and LV power
  - **Perforated Tray**: Perforated base for lighter cables. Used for data and control cables
  - **Solid Bottom Tray**: Used in hazardous environments or areas requiring cable protection
- Tray sizing: based on cable fill ratio
  - Power cables: maximum 40% of tray cross-section area
  - Data/control cables: maximum 50% of tray cross-section area
  - Rule: always allow room for future cables — size for current + 20% spare capacity
- Common tray widths: 100mm, 150mm, 200mm, 300mm, 450mm, 600mm
- Routing rules:
  - Power and data trays must be separated by minimum 300mm (reduces electromagnetic interference)
  - Tray must be continuous from source to destination — no gaps
  - Maintain minimum 300mm above finished floor level (for access panels) or route high in ceiling zone
  - Trays require support brackets every 1200–1500mm

**Cable Tray Selection Guide**

| Cable Type | Tray Type | Minimum Separation |
|---|---|---|
| HV Power | Ladder tray | Separate shaft or 600mm from LV |
| LV Power | Ladder tray | 300mm from data/control |
| Data (IT) | Perforated tray | 300mm from LV power |
| Fire Alarm / Control | Perforated tray | 300mm from power |

**3. Real Project Lens**
Level 4 of an office building requires: one 450mm wide ladder tray for LV power (fed from DB-L4) and one 300mm wide perforated tray for IT data cables (from the IT room to each workstation cluster). The two trays are routed at 2800mm and 2650mm ceiling height respectively — 150mm vertical separation — insufficient. The modeler re-routes the data tray to 2500mm, achieving 300mm separation.

**4. BIM Check**
- Check: Power and data trays maintain 300mm minimum separation throughout their parallel runs
- Check: Tray cross-section fill is below 40% (power) or 50% (data) — calculate from cable schedule
- Check: Tray supports (hangers or brackets) are modeled at maximum 1500mm centers

**5. Common Mistake**
Routing all cable trays in the same horizontal plane at the same elevation to simplify the model — this makes the model look clean but puts power and data trays at the same level, creating electromagnetic interference and a code violation.

**6. Today's Action**
For a DB supplying 12 circuits, estimate the total cable cross-section area (assume each circuit uses 4mm² × 3-core cable ≈ 28mm² per circuit). Calculate the total fill area. Select a tray width where 12 × 28mm² = 336mm² is less than 40% of the tray area.

---

### Day 63 — Distribution Board Modeling in Revit

**1. Why This Matters**
Distribution boards (DBs) are the local power distribution points on each floor. A DB modeled at the wrong location, wrong size, or wrong orientation cannot be installed as shown — and the electrical contractor will install it differently to what the BIM model shows, invalidating the coordination model.

**2. Core Concept**
- DB physical characteristics:
  - Typical depth: 150–200mm (surface mount) or 100–150mm (flush mount)
  - Typical width: 300–600mm depending on number of ways (circuits)
  - Typical height: 600mm–1200mm depending on circuit count
  - Front clearance required: minimum 600mm–1000mm (to open the door and work inside)
  - Top clearance: 300mm above DB for cable entry
- In Revit:
  - Use an electrical panel family (not a generic box)
  - Set the number of circuits/ways to match the engineer's panel schedule
  - Assign circuits from each load device to the DB
  - Set the installation height: typically 1500mm to the center of the DB (check local code)
- Panel schedule: generated from Revit — lists each circuit breaker, connected load, and load (W or A). Compare to the engineer's schedule
- Wall type matters: confirm the wall where the DB is located is thick enough for a flush mount, or confirm surface mount clearance in front

**DB Sizing Guide**

| Circuit Count | Typical Panel Width |
|---|---|
| Up to 12 | 250–300mm |
| 12–24 | 300–400mm |
| 24–48 | 400–600mm |
| 48+ | Multiple panels or a sub-MSB |

**3. Real Project Lens**
Level 7 of a hotel has a DB with 36 circuits. The modeler places a 36-way panel family (550mm W × 900mm H × 175mm D) in the electrical cupboard near the riser shaft. A reference plane is created 800mm in front of the panel face — confirmed clear of any obstruction for access. The panel schedule from Revit is exported and checked against the engineer's circuit schedule.

**4. BIM Check**
- Check: DB dimensions match the manufacturer's datasheet (not a generic placeholder)
- Check: 600mm minimum clearance in front of the DB is unobstructed — no pipe, duct, or fixture in this zone
- Check: Panel schedule from Revit matches the engineer's schedule — circuit by circuit

**5. Common Mistake**
Placing a DB in a wall alcove where the wall finish makes the panel flush with the wall face — but the panel body extends 150mm deeper than the wall, requiring wall modification that was never coordinated.

**6. Today's Action**
In Revit, place a distribution board family on a wall. Set the number of circuits to 24. Check that a 600mm clearance zone in front of the panel is clear of all other elements. Export the panel schedule and compare it to a blank engineer's schedule template.

---

### Day 64 — Conduit Routing and Pull Box Placement

**1. Why This Matters**
Conduits protect individual cables between the cable tray and the final device (socket, switch, light). Incorrectly routed conduits are the most common cause of cable installation failures on site — too many bends, too long a run, or a missing pull box means the cable cannot be pulled through.

**2. Core Concept**
- Conduit types:
  - **EMT (Electrical Metallic Tubing)**: Thin wall, easy to bend, used in dry indoor areas
  - **Rigid PVC**: Used in wet areas, concealed in walls or slabs
  - **GI Conduit**: Heavy-duty, used in industrial or exposed areas
- Conduit sizing: based on the number and size of cables inside
  - Maximum fill: 40% of conduit internal area for 3+ cables
  - Common sizes: 20mm, 25mm, 32mm, 50mm diameter
- Pull box requirement: required when:
  - Run exceeds 15m (check local code)
  - More than 2 × 90° bends in the run
  - Conduit changes direction more than 360° total
- Pull box sizing: must allow cables to make the bend inside — minimum internal dimension = 8 × conduit diameter
- In Revit: conduit is modeled using the Conduit tool. Pull boxes are modeled as junction box families

**Conduit Routing Rules**

| Rule | Limit |
|---|---|
| Maximum run before pull box | 15m (or 360° total bends) |
| Maximum bends between pull boxes | 2 × 90° bends (varies by code) |
| Minimum bend radius | 6 × conduit OD |
| Maximum fill ratio | 40% (3+ cables) |

**3. Real Project Lens**
A power circuit from DB-L3 to a socket cluster 12m away passes through a 90° bend at the ceiling, a 90° bend into the wall, and a 90° bend into the floor socket box — three 90° bends totaling 270°. This is within limits (270° < 360°) and the run is only 12m, so no pull box is needed. The modeler confirms this before finalizing the routing.

**4. BIM Check**
- Check: No conduit run exceeds 15m without a pull box modeled
- Check: No run has more than 2 × 90° bends between boxes (or 360° total, check local code)
- Check: Pull boxes are accessible — not concealed inside sealed walls or above inaccessible ceiling

**5. Common Mistake**
Routing a conduit from the cable tray directly to an outlet with 4 × 90° bends over a 20m run — no pull boxes modeled. On site, the cable puller cannot pull the cable through the conduit, requiring conduit to be cut open and pull boxes retrofitted.

**6. Today's Action**
Sketch a conduit run from a cable tray to a wall socket 10m away with two 90° bends. Count the total bend angle. Determine whether a pull box is required based on the 360° rule.

---

### Day 65 — Electrical Separation — HV, LV, Data

**1. Why This Matters**
Electrical systems of different voltage categories must be physically separated. High voltage cables near low voltage cables can cause induction, interference, and fire risk. High voltage near data cables can corrupt signals and damage equipment. Separation is a safety and performance requirement — not a preference.

**2. Core Concept**
- Voltage categories (typical classification):
  - **HV (High Voltage)**: Above 1000V AC. Typically utility incoming supply, 11kV or 22kV. Separate shaft, separate cable trays, separate room
  - **LV (Low Voltage)**: 230V–400V AC. Building power distribution — MSB to DBs to final circuits
  - **ELV / Data**: Below 50V AC / 120V DC. IT networks, telephone, fire alarm, BMS, security, AV
- Separation requirements:
  - HV and LV: minimum 600mm separation (or separate enclosed conduit/tray)
  - LV power and data: minimum 300mm separation (or separated by a metal divider in a divided tray)
  - Fire alarm cables: typically in separate conduit or dedicated FAS tray — must be fire-resistant cable
  - BMS cables: separate from power but can run with low-voltage data at 150mm separation
- In Revit: use separate cable tray systems or tray with dividers. Use circuit names and cable categories to keep systems distinct

**Electrical Separation Quick Reference**

| Systems | Minimum Separation |
|---|---|
| HV and LV | 600mm (or separate enclosed pathway) |
| LV Power and Data | 300mm |
| Power and Fire Alarm | 300mm (FAS in dedicated conduit preferred) |
| Data and BMS | 150mm |

**3. Real Project Lens**
An IT room on Level 5 has three cable trays running to a central comms rack: one 450mm LV power tray, one 300mm data tray, and one 150mm fire alarm tray. The LV and data trays are separated by 300mm vertical offset (data above, power below). The fire alarm tray runs in its own rigid conduit. The BIM modeler verifies separations in the 3D model before the coordination model submission.

**4. BIM Check**
- Check: Measure the separation between LV power trays and data trays — confirm 300mm minimum throughout
- Check: HV cables (if any) are in a separate enclosed pathway — not on an open ladder tray adjacent to LV
- Check: Fire alarm cables are in a dedicated fire-resistant conduit or separately labeled FAS cable tray

**5. Common Mistake**
Dividing a cable tray with a central divider and placing LV power on one side and data on the other — this only provides 0mm separation (they share the same enclosure), which violates the 300mm separation rule.

**6. Today's Action**
In a ceiling zone with LV power tray at 2700mm ceiling height, place a data tray at a position that satisfies the 300mm separation rule. Consider whether this means: (1) horizontal separation at the same elevation, or (2) vertical separation at a different elevation.

---

### Day 66 — Electrical Clash with HVAC and Structure

**1. Why This Matters**
Electrical cable trays and conduits must be routed through the same ceiling zones as HVAC ducts, piping, and structure. Electrical systems have strict separation requirements that make clash resolution more complex than other MEP disciplines — because moving an electrical tray to avoid a duct may bring it too close to another electrical system.

**2. Core Concept**
- Common electrical clash types:
  - **Cable tray through structural beam** (same as all MEP — P1 priority)
  - **Cable tray above HVAC duct** (access problem — tray is unreachable for cable installation)
  - **LV tray too close to data tray after HVAC reroute** (separation violation created by a clash fix)
  - **Conduit through fire-rated wall without sleeve** (fire integrity failure)
  - **Electrical cupboard door clearance blocked by pipe** (maintenance access clash)
- Resolution strategy:
  - Electrical trays typically route at the highest point in the ceiling zone (above HVAC and piping) to keep them accessible
  - Use tray drops or conduit to descend from the tray to the device — this is more practical than routing tray at low level
  - When re-routing a tray to avoid a duct clash, immediately recheck separation from adjacent electrical systems

**Electrical Clash Resolution Approach**

| Clash | Resolution |
|---|---|
| Tray through beam | Route around beam or request beam web penetration |
| Tray above inaccessible duct | Re-elevate tray above duct; confirm ceiling access panel below |
| LV/data separation violated | Increase vertical or horizontal offset; use metal divider |
| Conduit through fire wall | Model fire-stopping sleeve in the wall |
| DB access blocked | Reroute pipe or duct — DB clearance takes priority |

**3. Real Project Lens**
On Level 9 of a commercial building, an 800mm HVAC supply duct runs east-west at 2700mm. The 450mm LV cable tray is routed at 2650mm — below the duct, which puts it below the duct soffit and makes it inaccessible for cable installation. The modeler raises the cable tray to 2800mm (above the duct) and confirms it clears the slab soffit at 3000mm. The separation between LV and data trays is re-verified after the move.

**4. BIM Check**
- Check: All cable trays are above HVAC ducts wherever possible — confirm access height above each tray is at least 500mm for cable installation
- Check: After any electrical reroute to fix a structural or HVAC clash, recheck all separation distances to adjacent electrical systems
- Check: All conduits through fire-rated walls have fire-stopping sleeves modeled (or at minimum logged as a coordination item)

**5. Common Mistake**
Moving a cable tray to avoid a duct clash without checking the new position against the adjacent data tray — the two trays end up 200mm apart after the move, creating a new separation violation that triggers a second round of coordination.

**6. Today's Action**
In a BIM model or Navisworks, find one instance where a cable tray and an HVAC duct are at the same elevation. Propose a resolution: which one moves? Why? After the move, what other checks are required?

---

### Day 67 — Week 1 Electrical Review

**1. Why This Matters**
Electrical BIM has specific rules — separation distances, panel clearances, conduit fill limits, tray routing hierarchy — that differ from other MEP disciplines. The Week 1 review ensures these rules are understood before advancing to more complex electrical coordination work.

**2. Core Concept**
**Week 1 Electrical Summary**

| Day | Topic | Key Point |
|---|---|---|
| 61 | Power Distribution | MSB → DB → circuit. Each level has a specific location and function |
| 62 | Cable Tray Sizing | 40% fill max for power, 300mm separation from data |
| 63 | DB Modeling | Use accurate panel family, check front clearance, match panel schedule |
| 64 | Conduit Routing | Max 15m run or 360° bends before pull box. 40% fill maximum |
| 65 | Electrical Separation | HV/LV: 600mm. LV/data: 300mm. Fire alarm: dedicated conduit |
| 66 | Electrical Clashes | Route trays above HVAC. Recheck separation after every reroute |

**Critical Rules — Electrical BIM**
- LV power trays and data trays must maintain 300mm separation — always
- DB must have accurate dimensions — not a placeholder box
- Every conduit through a fire-rated wall needs a fire-stopping sleeve
- Pull boxes are required before 15m and before the third 90° bend
- Re-check electrical separation after every structural or HVAC clash resolution
- DB front clearance (600mm–1000mm) cannot be compromised by other MEP elements

**3. Real Project Lens**
A new electrical modeler on a large office project uses the Week 1 framework on Day 1: (1) maps the MSB-to-DB distribution hierarchy, (2) routes cable trays at the highest ceiling zone with correct separations, (3) places DBs with accurate dimensions and front clearance zones, (4) models conduit runs within length and bend limits, (5) runs clash test against HVAC and structure, (6) rechecks separations after clash resolution. This structured approach catches the five most common electrical BIM failures before the coordination model is submitted.

**4. BIM Check**
- Check: Is the MSB-to-DB distribution hierarchy fully modeled on all floors?
- Check: Do all parallel LV and data cable trays maintain 300mm separation throughout?
- Check: Are all DB front clearance zones (600mm) modeled and free of obstruction?

**5. Common Mistake**
Assuming that electrical is simpler to coordinate than HVAC (because cables are small) — then discovering that the separation requirements mean an electrical reroute triggers a cascade of additional checks and adjustments that take longer than a duct reroute.

**6. Today's Action**
Write a personal electrical BIM checklist — 5 items you will check on every electrical model before submission. Include: distribution hierarchy, tray separation, DB clearance, conduit limits, and fire wall sleeves. Save this list and refine it through Day 90.

---

*End of Starter Plan — Support Materials Pack*
*LUA BIM LABS | www.luabimlabs.com | Practical BIM Education for MEP*
