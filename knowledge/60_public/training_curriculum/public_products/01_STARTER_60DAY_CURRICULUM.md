# LUA BIM LABS Starter — 90-Day MEP BIM Curriculum (v2)

문서번호: LBL-TRN-PUB-001
문서상태: 배포용 커리큘럼 (Starter Plan) — v2 가격-가치 정렬 개발판
작성일: 2026-05-29
가격: USD 39/월 (→ 2027 Q2 USD 49로 조정 예정, 90일 커리큘럼 완성 시)
전달 방식: Telegram 1일 1레슨 + 주간 퀴즈 + 마일스톤 자료

---

## v2 업그레이드 핵심 변경

| 변경 항목 | v1 (초판) | v2 (개발판) |
|---|---|---|
| 커리큘럼 기간 | 60일 | **90일** (공종별 심화 트랙 추가) |
| 진행감 표시 | 없음 | **30일/60일/90일 마일스톤 메시지** |
| 다운로드 자료 | 없음 | **Track별 퀵 레퍼런스 카드 8장 (PDF)** |
| 마일스톤 인증 | 없음 | **60일 수료 인증서 + 90일 공종 수료 인증서** |
| 공종 특화 | 없음 | **Day 61~90: 공종 선택 심화 트랙 5개** |
| 주간 참여 이벤트 | 없음 | **"BIM Check Friday" 퀴즈 (매주 금요일)** |
| 재구독 이유 | 없음 | **90일 완료 후 Month 4 트랙 예고 + Personal Tutor 업셀** |

---

## 커리큘럼 목표

90일 과정을 완료한 학습자는:

- MEP BIM의 기본 개념과 실무 목적을 설명할 수 있다.
- Revit MEP 기본 인터페이스와 모델 구조를 이해한다.
- MEP 도면과 계통도를 읽고 BIM 모델과 연결할 수 있다.
- 모델 품질의 핵심 기준(LOD, 명명, 파라미터)을 알고 자체 점검할 수 있다.
- 간섭(clash)의 개념과 조율 회의의 흐름을 이해한다.
- **선택한 공종(HVAC/배관/소방/전기/위생) 심화 개념을 이해한다.**
- 일상적인 BIM 학습 습관과 실무 도구 활용 방식을 갖춘다.

---

## 전체 트랙 구성 (90일)

### Month 1–2: Foundation Tracks (Day 01–60)

| 트랙 | 기간 | 주제 |
|---|---|---|
| Track 1 | Day 01–07 | MEP BIM Orientation |
| Track 2 | Day 08–14 | Revit MEP Basics |
| Track 3 | Day 15–21 | Drawing and System Reading |
| Track 4 | Day 22–28 | Model Quality Basics |
| Track 5 | Day 29–38 | Clash Coordination Basics |
| Track 6 | Day 39–47 | Data and Schedule Basics |
| Track 7 | Day 48–54 | Site-Readiness Thinking |
| Track 8 | Day 55–60 | BIM Career Habit Building |

### Month 3: Discipline Deep-Dive Tracks (Day 61–90)

학습자가 신청 시 선택한 공종에 따라 아래 5개 트랙 중 1개 배정.

| 트랙 | 기간 | 공종 | 주요 내용 |
|---|---|---|---|
| Track 9A | Day 61–90 | HVAC | 덕트 사이징 로직, VAV 시스템, 공조기실 조율 |
| Track 9B | Day 61–90 | Piping / Mechanical | 냉온수 계통, 펌프 배치, 밸브 계획 |
| Track 9C | Day 61–90 | Plumbing / Sanitary | 위생 계통, 경사 배관, 수직 라이저 |
| Track 9D | Day 61–90 | Fire Protection | 스프링클러 계통, 헤더 배치, 유량 기준 |
| Track 9E | Day 61–90 | Electrical | 케이블 트레이, 패널 구성, 부하 스케줄 |

---

## Track 1: MEP BIM Orientation (Day 01–07)

### Day 01 — What Is BIM and Why MEP Needs It

**1. Why This Matters**
MEP systems (mechanical, electrical, plumbing) occupy the most crowded space in a building. Without BIM coordination, pipes, ducts, and conduits collide — causing expensive rework on site.

**2. Core Concept**
BIM (Building Information Modeling) is not just 3D drawing. It is a shared digital model that carries geometry, system data, and project information. MEP BIM means every duct, pipe, and cable is modeled with real dimensions, elevation, and system connections.

**3. Real Project Lens**
On a hospital project, the MEP models from HVAC, plumbing, fire protection, and electrical teams are merged into one coordination model. Without BIM, teams discover clashes during construction. With BIM, clashes are found and fixed before steel is cut.

**4. BIM Check**
- Check: Do you know which MEP disciplines are on your project?
- Check: Do you know who owns the BIM coordination model?
- Check: Can you open the project coordination model in a viewer?

**5. Common Mistake**
Treating BIM as just a 3D drawing tool. BIM is a data management workflow, not a drafting upgrade.

**6. Today's Action**
Write down the MEP disciplines on a current or imagined project. List one BIM task each discipline might need to coordinate.

---

### Day 02 — MEP Systems Overview

**1. Why This Matters**
To model or coordinate MEP BIM, you must understand what each system does and why it occupies the space it does. Wrong assumptions about system priority lead to poor clash resolution.

**2. Core Concept**
- **HVAC**: Air handling units, ductwork, diffusers, VAV boxes. Large and ceiling-dominant.
- **Piping (Mechanical)**: Chilled water, hot water, condenser water. Runs in ceiling and plant rooms.
- **Plumbing/Sanitary**: Domestic water, drainage, vents. Gravity drainage requires slope.
- **Fire Protection**: Sprinkler heads, mains, branches. Must not be blocked.
- **Electrical**: Cable trays, conduits, panels, transformers. Often flexible routing but large in quantity.
- **Low Voltage / Communication**: Data, security, AV, BMS. Runs separately from power.

**3. Real Project Lens**
In a typical office floor, HVAC ducts dominate the main corridor ceiling zone. Cable trays run parallel. Chilled water pipes stack below ducts. Drainage pipes drop to a lower floor. Understanding this stacking order prevents basic routing errors.

**4. BIM Check**
- Check: Can you name all six MEP disciplines?
- Check: Which system is most constrained by gravity in routing?
- Check: Which system is typically the most spatially dominant in ceiling zones?

**5. Common Mistake**
Modeling electrical conduits at the same elevation as HVAC ducts without checking clearance. Conduits are often smaller but must maintain minimum separation from high-voltage equipment.

**6. Today's Action**
Find a photo or cross-section drawing of a ceiling MEP installation. Identify at least three systems and their relative position.

---

### Day 03 — BIM Workflow and Stakeholders

**1. Why This Matters**
A BIM model is not created by one person. Understanding who does what prevents duplicate work, confusion about model ownership, and missed deliverables.

**2. Core Concept**
| Role | Responsibility |
|---|---|
| BIM Manager | Sets standards, manages CDE, reviews quality |
| MEP BIM Modeler | Creates and maintains discipline models |
| BIM Coordinator | Runs coordination, manages clashes, leads meetings |
| MEP Engineer | Provides design intent, approves changes |
| BIM Lead | Owns BEP, monitors delivery, mentors team |
| Client / Developer | Sets BIM requirements (EIR) |

**3. Real Project Lens**
On a large data center project, the MEP BIM modeler builds the HVAC model. The BIM coordinator merges it with electrical and plumbing. The BIM manager checks that all models follow the BEP naming standard before sharing with the client.

**4. BIM Check**
- Check: Which role is responsible for creating the MEP model?
- Check: Who decides how to resolve a clash?
- Check: What document sets the BIM rules on a project?

**5. Common Mistake**
Assuming the modeler also owns coordination. Many projects separate modeling and coordination into different roles.

**6. Today's Action**
Map the BIM roles for one project you know or imagine. Write each role and one task they perform.

---

### Day 04 — Understanding LOD (Level of Development)

**1. Why This Matters**
LOD defines how detailed and reliable a BIM model is at each project stage. Without LOD awareness, teams spend time modeling detail that is not yet needed — or miss critical information at delivery.

**2. Core Concept**
| LOD | Description | MEP Example |
|---|---|---|
| LOD 100 | Concept geometry | Schematic duct zone |
| LOD 200 | Approximate geometry | Duct routing with approx. size |
| LOD 300 | Precise geometry | Duct with accurate dimensions, elevations, connections |
| LOD 350 | Coordination geometry | Duct with hangers, supports, clash-checked |
| LOD 400 | Fabrication geometry | Shop-drawing level detail |
| LOD 500 | As-built | Verified field conditions |

**3. Real Project Lens**
At design stage, the HVAC duct model is LOD 200 — enough to show system concept and rough space requirements. At coordination stage before construction, it must reach LOD 350 — accurate enough to detect clashes with structural beams and other MEP systems.

**4. BIM Check**
- Check: What LOD is required by your project's BEP or EIR?
- Check: Is the current model LOD realistic for the project stage?
- Check: Does the model include hangers and supports (LOD 350)?

**5. Common Mistake**
Submitting an LOD 200 model for a clash coordination review. Low LOD models produce unreliable clash results that waste coordination meeting time.

**6. Today's Action**
Find an LOD specification chart (BIMForum LOD Spec is publicly available). Pick one MEP element and write what it looks like at LOD 200 vs. LOD 350.

---

### Day 05 — Revit MEP Interface Overview

**1. Why This Matters**
Revit MEP is the dominant BIM authoring tool for MEP modeling globally. Knowing the interface reduces time spent searching for commands and increases modeling confidence.

**2. Core Concept**
Key Revit MEP interface areas:
- **Ribbon**: Tool categories — Mechanical, Piping, Electrical, Systems.
- **Project Browser**: View tree — Floor Plans, Sections, 3D Views, Schedules, Sheets.
- **Properties Panel**: Element and view properties.
- **View Controls**: Visual style, scale, discipline filter.
- **Systems Browser**: MEP system hierarchy — where your ducts and pipes belong.

**3. Real Project Lens**
A new modeler spends the first 30 minutes trying to find the duct placement tool. It is in the Ribbon → Systems tab → Mechanical group. Knowing the layout before touching a real project saves time and frustration.

**4. BIM Check**
- Check: Can you locate the Systems tab in the Ribbon?
- Check: Can you open a floor plan view for each level?
- Check: Can you open the Systems Browser?

**5. Common Mistake**
Working entirely in 3D view while modeling. Modelers should primarily work in plan view and use 3D view for spatial checking — not for placement.

**6. Today's Action**
Open Revit MEP (trial or student version). Open the default project template. Identify the Systems tab, the Project Browser, and the Systems Browser. Take a mental note of their locations.

---

### Day 06 — File Structure and Project Setup

**1. Why This Matters**
A poorly structured Revit project creates coordination problems from day one. Correct file setup is the foundation that makes sharing, linking, and coordination reliable.

**2. Core Concept**
| Element | Purpose |
|---|---|
| Central File | Shared master model on server or CDE |
| Local File | Each user's working copy |
| Linked Files | Architectural, structural models linked into MEP model |
| Worksets | Division of model ownership within one file |
| Shared Coordinates | Ensures all models align to the same site point |

**3. Real Project Lens**
If the MEP team starts modeling without linking the architectural model, their levels, grid lines, and wall locations may not match. When the models are later merged, every element is in the wrong position.

**4. BIM Check**
- Check: Is the MEP model set up with shared coordinates from the architectural model?
- Check: Are worksets created and assigned to team members?
- Check: Is the file saved to the project CDE (not a local desktop)?

**5. Common Mistake**
Using the wrong shared coordinate base point. This causes all linked models to appear offset in the coordination model.

**6. Today's Action**
Review the BIM Execution Plan or project setup guide for one project. Find the answer to: where is the central file saved, and who is responsible for each discipline's model?

---

### Day 07 — Track 1 Review: MEP BIM Orientation

**1. Why This Matters**
Reviewing week one topics solidifies the conceptual foundation before moving into hands-on modeling topics.

**2. Core Concept — Week 1 Summary**
- BIM is a data workflow, not just 3D drawing.
- Six MEP disciplines have different space priorities and routing logic.
- BIM roles divide responsibility for modeling, coordination, and delivery.
- LOD defines what a model should contain at each stage.
- Revit MEP interface is organized by system type.
- File setup with shared coordinates and CDE is the project foundation.

**3. Real Project Lens**
A project that skips any of these foundations — wrong LOD, no shared coordinates, unclear role ownership — creates problems that are difficult to fix later.

**4. BIM Check**
- Check: Can you explain LOD 300 vs. LOD 350 to a colleague?
- Check: Can you name three BIM roles and their responsibilities?
- Check: Do you know where to find the Systems tab in Revit MEP?

**5. Common Mistake**
Skipping the orientation phase and jumping straight into modeling. Learners who skip orientation frequently repeat avoidable errors throughout a project.

**6. Today's Action**
Write a one-paragraph summary of what BIM coordination means for MEP work. Use your own words. Save it as your personal reference note for week 1.

---

## Track 2: Revit MEP Basics (Day 08–14)

### Day 08 — Setting Up a Revit MEP Project

**1. Why This Matters**
Correct project setup prevents coordination failures before modeling even starts. A wrong template or missing discipline setup creates rework from day one.

**2. Core Concept**
- Use the correct Revit MEP template (Mechanical, Electrical, or Plumbing).
- Link the architectural model before placing any MEP elements.
- Confirm shared coordinates are acquired from the architectural model.
- Set up the discipline filter in each view so only the relevant system is visible.

**3. Real Project Lens**
A piping modeler sets up a new Revit project using the mechanical template but skips linking the architectural model. Two weeks of piping are placed at wrong elevations because the floor-to-floor height was assumed, not taken from the architecture.

**4. BIM Check**
- Check: Is the correct discipline template selected?
- Check: Is the architectural model linked with shared coordinates?
- Check: Is the view discipline filter set to the correct system?

**5. Common Mistake**
Linking the architectural model without acquiring shared coordinates. This leaves all MEP elements uncoordinated with the building structure.

**6. Today's Action**
Create a new Revit MEP project using the Mechanical template. Link a simple architectural file (even a sample). Confirm the shared coordinates are set correctly.

---

### Day 09 — Levels and Grids in MEP Context

**1. Why This Matters**
MEP elements are placed relative to levels. If levels are wrong or inconsistently set, every duct, pipe, and tray will be at the wrong elevation.

**2. Core Concept**
- Levels define the floor-to-floor height reference.
- MEP elements are offset from levels (e.g., bottom of duct = Level 3 + 2400mm).
- Grids help locate MEP equipment relative to structural columns.
- MEP teams should not create their own levels — they should use the architectural/structural levels.

**3. Real Project Lens**
A plumbing modeler creates a custom level called "Basement MEP" instead of using the architectural "B1" level. When the coordination model is assembled, the plumbing model appears 150mm above the correct position because the custom level had a different elevation.

**4. BIM Check**
- Check: Are MEP model levels copied or monitored from the architectural model?
- Check: Is each MEP element offset correctly from the reference level?
- Check: Have levels been renamed to match the project naming convention?

**5. Common Mistake**
Placing MEP elements by dragging them to a visual position in 3D view rather than entering a precise offset from a level.

**6. Today's Action**
Open a Revit MEP file. Check the levels in the Project Browser. Confirm that they match the architectural model levels. Note the floor-to-floor height for at least one floor.

---

### Day 10 — Linked Models and Coordination

**1. Why This Matters**
MEP modeling only makes sense in context of the building structure. Linked models let the MEP modeler see walls, beams, slabs, and other disciplines — without editing them.

**2. Core Concept**
- Linked files appear in the MEP model as read-only references.
- The architectural and structural models are usually the first links to add.
- Other MEP discipline models (HVAC, piping, electrical) are also linked for coordination.
- Visibility of linked elements is controlled per view.

**3. Real Project Lens**
An electrical modeler does not link the structural model. A major cable tray route is placed directly through a structural beam. The clash is only found during site coordination, requiring an expensive reroute.

**4. BIM Check**
- Check: Are all required linked models (architecture, structure, other MEP) loaded?
- Check: Is the link visibility set correctly in the active view?
- Check: Are linked models visible but not accidentally editable?

**5. Common Mistake**
Hiding linked models to improve viewport performance during modeling. This removes the context needed to spot immediate spatial conflicts.

**6. Today's Action**
Open your Revit MEP project. Load or check a linked architectural model. Confirm it appears in the correct position. Set its visibility to "Halftone" so your MEP work is visually clear.

---

### Day 11 — Basic Duct and Pipe Placement

**1. Why This Matters**
Duct and pipe placement is the core daily task for MEP BIM modelers. Correct placement technique avoids common errors that create poor-quality models.

**2. Core Concept**
Duct placement steps:
1. Select the correct system type (Supply Air, Return Air, etc.).
2. Set the duct size (width × height for rectangular, diameter for round).
3. Set the offset from the level (e.g., Bottom of Duct = 2800mm from Level 3).
4. Route the duct in plan view.
5. Add fittings (elbows, tees, reducers) as needed.

Pipe placement follows the same logic — select system, set size, set elevation, route.

**3. Real Project Lens**
A modeler places a supply air duct in 3D view by dragging. The duct is placed at an approximate height. During coordination, it is found to be 80mm too high, intersecting with the structural beam zone.

**4. BIM Check**
- Check: Is the duct offset entered numerically, not visually estimated?
- Check: Is the system type correctly assigned (Supply Air, not undefined)?
- Check: Are all fittings connecting properly (no open ends)?

**5. Common Mistake**
Leaving duct or pipe ends unconnected. Open-ended systems create errors in the Revit Systems Browser and produce incorrect schedules.

**6. Today's Action**
In a Revit MEP file, place 3 meters of rectangular supply air duct at an offset of 2500mm above Level 1. Add one elbow at the end. Confirm it connects correctly in the Systems Browser.

---

### Day 12 — MEP System Connections

**1. Why This Matters**
Revit MEP uses a connected system model — elements must be logically connected to form a functioning system. Disconnected elements produce incomplete data, wrong schedules, and false results in system checks.

**2. Core Concept**
- Each duct or pipe belongs to a system (e.g., Supply Air, Chilled Water Supply).
- Elements must be connected end-to-end or through fittings.
- Equipment (AHU, fan coil, pump) connects to ductwork and piping through connectors.
- The System Inspector in Revit highlights broken connections.

**3. Real Project Lens**
A modeler creates a complete duct route but forgets to connect it to the air handling unit. The schedule shows zero total flow for that system because the system calculation cannot trace from source to end.

**4. BIM Check**
- Check: Are all duct/pipe ends connected (no open connectors)?
- Check: Is each element assigned to the correct named system?
- Check: Does the System Inspector show zero errors for this system?

**5. Common Mistake**
Connecting ducts visually (they appear touching) but not actually connecting them in Revit. Use "Connect" tool, not just snap-to-visual.

**6. Today's Action**
Check an existing Revit MEP system for open connectors. Use the System Inspector to find any broken connections. Record how many you find and where.

---

### Day 13 — View Creation and MEP Views

**1. Why This Matters**
MEP models require discipline-specific views to work efficiently and produce accurate drawings. Incorrect view setup is one of the most common sources of coordination drawing errors.

**2. Core Concept**
Essential MEP views:
- **Plan Views by Level**: One plan view per floor, per discipline (HVAC, Piping, Electrical separately).
- **Sections**: Show vertical routing and inter-discipline conflicts.
- **3D Coordination View**: All disciplines visible, used for coordination checking.
- **Schedules**: Equipment lists, duct schedules, pipe schedules.

View properties to confirm:
- Discipline filter (Mechanical / Electrical / Plumbing)
- View range (cut height must capture the relevant MEP zone)
- Visibility/Graphics overrides per view

**3. Real Project Lens**
A coordination drawing shows only architectural elements because the view discipline filter was left at "Architectural" instead of "Mechanical." The reviewer thinks MEP modeling was not done, triggering an unnecessary coordination meeting.

**4. BIM Check**
- Check: Is the view discipline filter set to the correct MEP discipline?
- Check: Is the view range set to capture the ceiling MEP zone?
- Check: Are all linked models visible in the view as needed?

**5. Common Mistake**
Using one shared view for all disciplines. Separate views per discipline prevent confusion and allow proper discipline-specific printing and sharing.

**6. Today's Action**
Create a mechanical plan view for Level 1 in a Revit MEP project. Set the discipline filter to Mechanical. Confirm that ducts are visible and walls are halftone.

---

### Day 14 — Track 2 Review: Revit MEP Basics

**1. Why This Matters**
The Revit basics covered this week form the daily work foundation for every MEP BIM modeler. Gaps in any of these areas produce models that cannot be coordinated or delivered.

**2. Core Concept — Week 2 Summary**
- Project setup requires the correct template, linked models, and shared coordinates.
- Levels and grids from architecture must be used — not recreated.
- Linked models provide essential context for collision-free routing.
- Duct and pipe placement must use numeric offsets, not visual estimation.
- System connections must be verified — visual proximity is not connection.
- Views must have the correct discipline filter and view range.

**3. Real Project Lens**
A modeler who skips system connection checks produces a model that looks correct in 3D but fails every schedule and system analysis check at delivery.

**4. BIM Check**
- Check: Can you set up a new Revit MEP project with a linked architectural model?
- Check: Can you place a duct with a correct numeric offset?
- Check: Can you find and fix an open connector using the System Inspector?

**5. Common Mistake**
Believing that a model that "looks right" in 3D is a complete and correct BIM model. Visual correctness and data correctness are different.

**6. Today's Action**
Review a Revit MEP model (sample or personal) using these checks: linked model present, levels correct, system connections complete, discipline views set up. Record which checks pass and which need attention.

---

## Track 3: Drawing and System Reading (Day 15–21)

### Day 15 — Reading MEP Drawings

**1. Why This Matters**
BIM models are built from design drawings. A modeler who cannot read drawings accurately models the wrong system — causing coordination failures and delivery rejections.

**2. Core Concept**
MEP drawings have layers of information:
- **Plan drawings**: Top-down view of each floor's MEP layout.
- **Schematic diagrams**: Logic of system connections (not spatially accurate).
- **Sections and details**: Vertical routing and installation specifics.
- **Legends and schedules**: Equipment tags, sizes, specifications.
- **Notes and call-outs**: Contractor instructions, material specifications.

**3. Real Project Lens**
A plumbing modeler reads a drainage plan and models all horizontal pipes. The schematic diagram shows a vertical drop-down that the plan did not clearly indicate. Without reading both, the model is missing a critical riser.

**4. BIM Check**
- Check: Have you reviewed the plan, schematic, and detail drawings for this system?
- Check: Do you understand what each annotation and tag means?
- Check: Have you confirmed equipment locations from the equipment schedule?

**5. Common Mistake**
Modeling from plan drawings only without cross-referencing the schematic. Plans show location, schematics show logic.

**6. Today's Action**
Find a sample MEP drawing set (publicly available from Revit tutorials or BIM education sites). Identify: one element shown on plan only, one element shown on schematic only, and one element shown on both.

---

### Day 16 — HVAC System Diagrams

**1. Why This Matters**
HVAC BIM modeling requires understanding airflow logic, not just geometry. Without system understanding, ducts are placed without knowing where supply air starts and where exhaust ends.

**2. Core Concept**
HVAC system diagram components:
- **AHU (Air Handling Unit)**: Source of treated air.
- **Supply Air Ductwork**: From AHU to diffusers (delivers conditioned air).
- **Return Air Ductwork**: From spaces back to AHU (collects used air).
- **Exhaust Ductwork**: Air discharged outside.
- **VAV Boxes**: Control airflow per zone.
- **Diffusers and Grilles**: Terminal delivery devices at ceiling or wall.

**3. Real Project Lens**
A modeler connects a return air duct to the supply air system because both appear the same in plan. The BIM model looks correct but the system logic is wrong. When the client reviews system flows, the mistake is caught — requiring full redesign of that section.

**4. BIM Check**
- Check: Is each duct assigned to the correct system (Supply, Return, Exhaust)?
- Check: Does the supply air start from the AHU and end at diffusers?
- Check: Does the return air start at grilles and end back at the AHU?

**5. Common Mistake**
Using the wrong system type when placing ducts. Always confirm the system from the schematic before routing.

**6. Today's Action**
Draw a simple HVAC airflow diagram from memory: AHU → supply duct → VAV box → diffuser → return grille → return duct → AHU. Check it against Day 2's system overview.

---

### Day 17 — Piping and Plumbing Schematics

**1. Why This Matters**
Piping systems have specific flow direction, pressure, and connection logic. Reading piping schematics correctly is critical to building accurate BIM models.

**2. Core Concept**
Piping schematic elements:
- **Flow direction arrows**: Show media direction (supply vs. return).
- **Valve symbols**: Isolation valves, check valves, pressure regulators.
- **Equipment connections**: Pumps, heat exchangers, coils.
- **Elevation markers**: Where pipes rise or drop.
- **Pipe sizes and specs**: Labeled on the schematic or schedule.

Plumbing-specific:
- **Soil lines**: Carry waste (gravity-flow, requires slope).
- **Vent pipes**: Allow waste pipes to breathe (no flow — open to atmosphere).
- **Domestic water**: Hot and cold supply lines.

**3. Real Project Lens**
A modeler builds a chilled water system but reverses supply and return lines. The model looks symmetrical and correct visually. The system performance check shows that return water is at a lower temperature than supply — physically impossible, revealing the error.

**4. BIM Check**
- Check: Are flow directions confirmed from the piping schematic?
- Check: Is gravity drainage modeled with the required slope (typically 1:50 for drainage)?
- Check: Are all valves placed as shown in the schematic?

**5. Common Mistake**
Modeling drainage pipes as flat (zero slope). Gravity drainage requires a minimum fall to function.

**6. Today's Action**
Find a sample chilled water piping diagram. Identify: supply pipe, return pipe, at least one pump, and one isolation valve. Note the flow direction for each.

---

### Day 18 — Electrical Single-Line Diagrams

**1. Why This Matters**
Electrical BIM modeling requires understanding power distribution logic. Single-line diagrams show how power flows from the main panel to every circuit.

**2. Core Concept**
Single-line diagram components:
- **Main Switchboard (MSB)**: Building power entry point.
- **Distribution Boards (DB)**: Sub-panels serving zones or floors.
- **Circuits**: Individual branches from DB to equipment or outlets.
- **Cable sizes and breaker ratings**: Labeled at each connection.
- **Load schedules**: Total connected load per board.

**3. Real Project Lens**
An electrical modeler builds cable tray routes from the MSB room to floors but does not reference the distribution board locations shown in the single-line diagram. Three distribution boards are missing from the model, leaving entire floor zones without power in the BIM model.

**4. BIM Check**
- Check: Is the panel board quantity and location consistent with the single-line diagram?
- Check: Is the cable tray routing starting from the correct MSB location?
- Check: Are circuit homerun lines shown from panels to major equipment?

**5. Common Mistake**
Modeling cable trays without confirming the distribution board locations from the single-line diagram.

**6. Today's Action**
Sketch a simple single-line diagram: Main panel → Sub-panel 1 (Floor 1) → three circuits. Confirm you can read: the voltage level, the breaker size, and the load label.

---

### Day 19 — Coordination Drawing Requirements

**1. Why This Matters**
Coordination drawings communicate clash-checked MEP routing to construction teams. Understanding what these drawings must contain prevents rejection during project review.

**2. Core Concept**
Coordination drawings typically show:
- Combined MEP systems overlaid on the structural background.
- Confirmed elevations at key routing zones.
- Clash-resolved MEP paths.
- Grid references and level labels.
- Notes on critical clearances or installation sequence.

Required by:
- Main contractor (MC) for construction planning.
- Site supervision team for checking installation.
- Building authority for permit review in some markets.

**3. Real Project Lens**
A coordination drawing is submitted without confirmed bottom-of-duct elevations. The installation crew cannot determine if ductwork will clear the false ceiling. All sheets must be reissued with elevation annotations.

**4. BIM Check**
- Check: Does the coordination drawing show confirmed MEP elevations at key areas?
- Check: Are grid references visible so dimensions can be verified on site?
- Check: Is the drawing scale adequate for the level of detail shown?

**5. Common Mistake**
Submitting a coordination drawing that is the model view exported as-is, without checking drawing clarity, scale, and annotation completeness.

**6. Today's Action**
Find a sample coordination drawing (MEP combined plan). Identify: three pieces of information a site installer would need, and check if all three are present.

---

### Day 20 — Shop Drawing vs. Design Drawing

**1. Why This Matters**
Confusing design drawings with shop drawings causes incorrect model detail levels, wrong deliverable submissions, and coordination failures.

**2. Core Concept**
| Drawing Type | Purpose | Created By | Level of Detail |
|---|---|---|---|
| Design Drawing | Shows design intent | Design Engineer | Schematic to LOD 300 |
| Coordination Drawing | Shows clash-resolved routing | BIM Coordinator | LOD 350 |
| Shop Drawing | Shows fabrication detail | Contractor/Fabricator | LOD 400 |
| As-Built Drawing | Records actual installation | Contractor | LOD 500 |

For BIM work, Starter-level learners focus on design drawing and coordination drawing.

**3. Real Project Lens**
A modeler receives a "shop drawing" from a subcontractor and models every bolt, flange, and hanger detail. This adds weeks of work not required by the BIM Execution Plan, which only specified LOD 350 coordination geometry.

**4. BIM Check**
- Check: What drawing type are you modeling from — design or shop?
- Check: What LOD is required for this project stage?
- Check: Are you modeling the right level of detail, not more or less?

**5. Common Mistake**
Over-modeling — adding fabrication-level detail at the coordination stage. This delays delivery and adds confusion.

**6. Today's Action**
Review your project's BEP or EIR. Find the LOD requirement for each project stage. Write it down as a reference for your daily modeling work.

---

### Day 21 — Track 3 Review: Drawing and System Reading

**1. Why This Matters**
Reading drawings correctly is a prerequisite for every modeling and coordination task. Errors in drawing interpretation multiply through every downstream activity.

**2. Core Concept — Week 3 Summary**
- MEP drawings include plans, schematics, sections, and schedules — all must be cross-referenced.
- HVAC diagrams show supply, return, and exhaust systems with clear flow direction.
- Piping schematics show flow direction, valve positions, and slope requirements.
- Electrical single-line diagrams show power distribution from MSB to circuits.
- Coordination drawings communicate clash-resolved MEP routing for construction.
- Shop drawings are fabrication-level — not the same as coordination drawings.

**3. BIM Check**
- Check: Can you identify supply vs. return in an HVAC schematic?
- Check: Can you find all distribution boards from a single-line diagram?
- Check: Can you explain the difference between a coordination drawing and a shop drawing?

**5. Common Mistake**
Using only plan drawings for modeling — ignoring schematics, sections, and schedules.

**6. Today's Action**
Take a sample MEP drawing set. In 10 minutes, identify: one HVAC supply element, one drainage gravity line, one panel board, and one coordination note. Record your findings.

---

## Track 4: Model Quality Basics (Day 22–28)

### Day 22 — What Is Model Quality?

**1. Why This Matters**
A model that looks complete in 3D may fail delivery review due to missing parameters, wrong naming, or incorrect system assignments. Model quality is what allows BIM to provide real data value.

**2. Core Concept**
Model quality has four dimensions:
1. **Geometry Quality**: Correct shape, size, elevation, position.
2. **Data Quality**: Parameters populated correctly (size, material, system, tag).
3. **System Quality**: Elements connected and assigned to correct named systems.
4. **Delivery Quality**: File format, naming convention, model health (no warnings, purged).

**3. Real Project Lens**
A duct model is geometrically perfect. However, 40% of ducts have no system assignment and 60% of equipment tags are blank. The client's facility management system cannot import any useful data. The model fails delivery review.

**4. BIM Check**
- Check: Are all MEP elements assigned to a named system?
- Check: Are all required parameters populated (size, material, mark, tag)?
- Check: Does the model open without critical warnings?

**5. Common Mistake**
Checking model quality only at delivery. Quality checks should run throughout the modeling process.

**6. Today's Action**
Open a Revit MEP file. Select 10 duct elements. Check how many have: (1) system assignment, (2) size property populated, (3) mark or tag. Record the result.

---

### Day 23 — Naming Conventions and Parameters

**1. Why This Matters**
Consistent naming allows models to be merged, filtered, sorted, and reported. Inconsistent naming breaks every downstream use of model data.

**2. Core Concept**
Common MEP BIM naming convention elements:
- **File naming**: `[Project]-[Discipline]-[Level]-[Author]-[Date].rvt`
- **System naming**: `HVAC-SA-L03` (HVAC, Supply Air, Level 3)
- **Equipment naming**: `AHU-01-L03` (Air Handling Unit 01, Level 3)
- **View naming**: `MEP-MECH-L03-PLAN` (MEP, Mechanical, Level 3, Plan)
- **Sheet naming**: Follows project standard — usually set in the BEP

Parameter conventions (check your BEP):
- `Mark`: Unique element identifier
- `Comments`: Modeler notes (not for official data)
- `Description`: Element description
- `System Classification`: System type

**3. Real Project Lens**
A project uses three different naming formats for AHUs — "AHU-01", "Air Handler 1", and "Unit_01" — from three different modelers. The equipment schedule shows 30 items that cannot be sorted or identified consistently.

**4. BIM Check**
- Check: Does the file name match the project BEP naming format?
- Check: Are equipment marks unique and consistent?
- Check: Do system names follow the project standard?

**5. Common Mistake**
Using Revit default names without changing them to project-specific names. Defaults like "Mechanical Supply 1" mean nothing in a coordination model with 50 systems.

**6. Today's Action**
Read your project's BEP naming section (or create a sample naming table). Apply the naming format to three elements in your model. Confirm consistency.

---

### Day 24 — LOD Requirements by Project Stage

**1. Why This Matters**
Delivering the wrong LOD — too low or too high — creates deliverable rejection or unnecessary work. LOD must match the project stage.

**2. Core Concept**
| Project Stage | Typical Required LOD | MEP Expectation |
|---|---|---|
| Concept Design | LOD 100–200 | System zones, approximate routing |
| Schematic Design | LOD 200 | Major equipment locations, rough duct/pipe routes |
| Design Development | LOD 300 | Accurate sizing, confirmed routing, all equipment |
| Construction Documents | LOD 300–350 | Clash-coordinated, hanger zone included |
| Construction | LOD 350–400 | Shop-drawing level if required |
| As-Built | LOD 500 | Field-verified installation |

Note: Some projects define custom LOD by element type. Always check the BEP.

**3. Real Project Lens**
A modeler submits an LOD 200 HVAC model for a construction document review. The client rejects it because duct sizes are approximate and coordination with structural beams is not possible. The model must be rebuilt to LOD 350.

**4. BIM Check**
- Check: What project stage is the current submission for?
- Check: What LOD is required for this stage per the BEP?
- Check: Does your current model meet that LOD for every element, not just visually?

**5. Common Mistake**
Assuming LOD 300 means "complete geometry." LOD 300 also requires correct parameters and system connections.

**6. Today's Action**
Review your project BEP. Write the LOD required for your current project stage. Pick five elements in your model and evaluate if they meet that LOD.

---

### Day 25 — Common Modeling Errors

**1. Why This Matters**
The same modeling errors appear in almost every project. Knowing them in advance prevents the most common quality failures.

**2. Core Concept**
Top 10 common MEP BIM modeling errors:

1. Open connectors (duct/pipe ends not connected).
2. Wrong system type assignment.
3. Geometry at wrong elevation (estimated, not numeric).
4. Duplicate elements at the same location.
5. Inconsistent naming or blank marks.
6. Missing equipment (shown in design drawing, not in model).
7. Incorrect pipe slope (drainage modeled as flat).
8. Elements outside project boundary or off-grid.
9. Unresolved warnings (overlapping elements, duplicate types).
10. Missing or blank required parameters.

**3. Real Project Lens**
A large MEP model review finds 87 Revit warnings. Of these, 60 are duplicate pipe types — a result of importing a manufacturer's Revit family that added redundant pipe types to the project.

**4. BIM Check**
- Check: How many warnings does the model currently show?
- Check: Are there any duplicate elements at the same location?
- Check: Are all connectors closed?

**5. Common Mistake**
Ignoring Revit warnings. Warnings are not errors, but unresolved warnings accumulate into model corruption over time.

**6. Today's Action**
Open a Revit MEP model. Go to Manage → Review Warnings. Count the total number. Identify the most common warning type. Record both numbers.

---

### Day 26 — Model Health Checks

**1. Why This Matters**
A model health check before submission prevents embarrassing delivery rejections and ensures the model is usable by all project stakeholders.

**2. Core Concept**
Model health checklist (pre-submission):

**Geometry:**
- [ ] No elements floating in space or off-grid
- [ ] All ducts and pipes have valid sizes
- [ ] All equipment placed at correct elevation

**Data:**
- [ ] All elements have marks populated
- [ ] All elements assigned to named systems
- [ ] No blank required parameters

**File:**
- [ ] Warnings reviewed and reduced
- [ ] Unused families and types purged (File → Purge Unused)
- [ ] File size within project limit
- [ ] Central model synchronized before submission

**Coordination:**
- [ ] All linked models up to date
- [ ] Shared coordinates confirmed
- [ ] Discipline views set up and named correctly

**3. Real Project Lens**
A submitted Revit model is 890 MB. The client's server cannot open it reliably. Purging unused families and types reduces it to 320 MB — the same coordination quality, one-third the file size.

**4. BIM Check**
- Check: Is the file purged of unused families and types?
- Check: Is the file size within the project-defined limit?
- Check: Are all linked model paths valid (not broken)?

**5. Common Mistake**
Running purge only once. Each time new families are loaded during modeling, new unused types accumulate. Purge regularly, not just before submission.

**6. Today's Action**
Run "Purge Unused" on a Revit MEP file. Record the file size before and after. Note how many families or types were removed.

---

### Day 27 — Self-Review Checklist

**1. Why This Matters**
A self-review before submitting to the BIM coordinator prevents the most avoidable errors from reaching the team — saving coordination meeting time and protecting your professional reputation.

**2. Core Concept**
Personal self-review routine (15 minutes per discipline zone):

Step 1 — Visual check in 3D:
- Walk through the model in a coordination 3D view.
- Look for any obvious geometry gaps, wrong positions, or floating elements.

Step 2 — System Browser check:
- Open the Systems Browser.
- Confirm no "default" or unnamed systems remain.
- Confirm all elements are assigned to a system.

Step 3 — View check:
- Open each discipline plan view.
- Confirm MEP elements are visible and at correct elevations.

Step 4 — Schedule check:
- Open the equipment schedule.
- Confirm all equipment is listed and has required data.

Step 5 — Warning check:
- Review Warnings.
- Resolve or document any critical warnings.

**3. Real Project Lens**
A modeler spends 15 minutes on self-review and finds 4 open connectors, 2 blank equipment marks, and one duct floating 600mm above its level. All fixed before submission — no coordination meeting time wasted.

**4. BIM Check**
- Check: Have you completed all 5 self-review steps?
- Check: Are all findings documented or resolved?
- Check: Is the model saved and synchronized before handing over?

**5. Common Mistake**
Skipping the schedule check because "I only model, not data." Data errors in the model are the modeler's responsibility, not the BIM coordinator's.

**6. Today's Action**
Run all 5 self-review steps on a Revit MEP file. Record your findings. Fix what you can. Document what needs team discussion.

---

### Day 28 — Track 4 Review: Model Quality Basics

**1. Why This Matters**
Model quality is the difference between a BIM deliverable and a 3D drawing. Teams that skip quality checks create cascading problems at coordination and delivery stages.

**2. Core Concept — Week 4 Summary**
- Model quality has four dimensions: geometry, data, system, and delivery quality.
- Naming conventions ensure model data is readable across all stakeholders.
- LOD requirements must match the project stage — not more, not less.
- The 10 common modeling errors can be prevented with a basic self-review.
- Model health checks (purge, warnings, file size) should run regularly.
- A 15-minute self-review prevents hours of coordination rework.

**3. BIM Check**
- Check: Can you list the four dimensions of model quality?
- Check: Can you name five common modeling errors?
- Check: Can you perform a complete self-review in under 20 minutes?

**6. Today's Action**
Create your personal MEP BIM self-review checklist. Use today's content plus any project-specific items from your BEP. Save it as a reference for every future submission.

---

## Track 5: Clash Coordination Basics (Day 29–38)

### Day 29 — What Is Clash Detection?

**1. Why This Matters**
Clash detection is the primary reason MEP BIM exists for coordination. Finding clashes in the model prevents collisions on the construction site.

**2. Core Concept**
A clash occurs when two elements occupy the same physical space. Types:
- **Hard clash**: Two solid elements physically intersect.
- **Clearance clash (soft clash)**: Elements are too close, violating required maintenance or installation space.
- **Workflow clash (4D)**: Schedule conflict — two activities planned at the same time in the same space.

Common MEP-to-MEP clashes:
- HVAC duct vs. sprinkler pipe
- Cable tray vs. chilled water pipe
- Drainage riser vs. structural column

Common MEP-to-structure clashes:
- Duct through structural beam
- Pipe penetrating concrete slab without sleeve

**3. Real Project Lens**
A hospital project runs a clash detection report and finds 3,400 clashes. Of these, 60% are clearance clashes from cable tray touching (not penetrating) sprinkler pipes. After grouping and filtering, the true hard clashes requiring action are 240.

**4. BIM Check**
- Check: Do you know which tool is used for clash detection on your project?
- Check: Do you know the difference between a hard clash and a clearance clash?
- Check: Do you know who is responsible for clash report review?

**5. Common Mistake**
Treating all 3,400 clashes as individual tasks. Clash reports must be filtered and grouped before any coordination meeting.

**6. Today's Action**
Write down three types of clashes you would expect in a typical MEP model. Identify which are hard clashes and which are clearance clashes.

---

### Day 30 — Hard Clash vs. Soft Clash

**1. Why This Matters**
Understanding the difference between hard clashes and soft clashes prevents teams from treating every clash result the same way — hard clashes are physical impossibilities; soft clashes are clearance violations that may or may not require action.

**2. Core Concept**
- **Hard clash**: Two solid elements physically intersect. They cannot coexist. One must move.
- **Soft (clearance) clash**: Two elements are too close together, violating a required maintenance or installation clearance. They do not touch but cannot be installed as shown.
- **Duplicate clash**: Two identical elements at exactly the same position — usually a modeling or import error.

Common thresholds for soft clash testing:
- General MEP clearance: 50–100mm minimum between systems
- Valve maintenance access: 600mm clear in front of valve
- AHU filter access: 1000mm clear on filter side

**3. Real Project Lens**
A clash test between HVAC and sprinkler pipes returns 840 results. On investigation, 700 are soft clashes — cable trays within 50mm of sprinkler pipes, technically violating a clearance rule but not physically intersecting. The remaining 140 are hard clashes requiring real resolution.

**4. BIM Check**
- Check: Can you explain the difference between a hard and soft clash to a trade contractor?
- Check: Do you know the clearance tolerance used in your project's clash test settings?
- Check: Can you identify which results in a clash report are hard vs. soft by reading the distance value?

**5. Common Mistake**
Setting the soft clash tolerance too tight (e.g., 5mm) generates thousands of false positives. Setting it too loose (e.g., 500mm) misses real access problems. Always confirm tolerance settings with the BIM coordinator before running tests.

**6. Today's Action**
Write down three MEP system pairs where you would expect hard clashes, and three pairs where soft clashes are more common. Explain why for each.

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

### Day 38 — Track 5 Review: Clash Coordination Basics

**1. Why This Matters**
Clash coordination is the activity that connects BIM modeling to real construction — reviewing the core concepts ensures you can participate in the process, not just observe it.

**2. Core Concept — Track 5 Summary**

| Day | Topic | Key Takeaway |
|---|---|---|
| 30 | Hard vs. Soft Clash | Hard = physical intersection; Soft = clearance violation; different tolerances |
| 31 | Navisworks Basics | Append NWC files; use Clash Detective; save viewpoints |
| 32 | Grouping and Prioritization | Group by level/grid; assign Critical/Major/Minor |
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

## Track 6: Data and Schedule Basics (Day 39–47)

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
Using model quantities for procurement without verifying the model LOD. An LOD 200 duct length schedule may exclude all branch connections and transitions — the delivered quantity could be 20–30% higher than the schedule shows.

**6. Today's Action**
In Revit, create a schedule for Pipe Fittings or Duct Fittings that includes a Count field. Group by Type to see how many of each fitting type the model contains. Note the top three most-used types.

---

### Day 47 — Track 6 Review: Data and Schedule Basics

**1. Why This Matters**
The ability to extract reliable data from a BIM model is what separates a model used for reference from a model used for decision-making — this track built the foundation for that capability.

**2. Core Concept — Track 6 Summary**

| Day | Topic | Key Takeaway |
|---|---|---|
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

## Track 7: Site-Readiness Thinking (Day 48–54)

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

### Day 54 — Track 7 Review: Site-Readiness Thinking

**1. Why This Matters**
A BIM model that cannot be built from is incomplete — site-readiness thinking means designing your coordination process with the construction team's needs as the primary output standard.

**2. Core Concept — Track 7 Summary**

| Day | Topic | Key Takeaway |
|---|---|---|
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

## Track 8: BIM Career Habit Building (Day 55–60)

### Day 55 — Building a Daily BIM Learning Habit

**1. Why This Matters**
MEP BIM skills compound over time. A consistent 30-minute daily practice produces more growth than weekend study sessions.

**2. Core Concept**
Daily learning habit structure:
- 10 min: Review one concept (lesson, note, or standard document)
- 15 min: Practice one task in Revit or Navisworks
- 5 min: Write one observation or question

Weekly rhythm:
- Monday–Friday: Daily 30-minute practice
- Saturday: Review the week's concepts (not new content)
- Sunday: Plan next week's practice topics

**3. Real Project Lens**
A BIM modeler who reviews coordination standards for 15 minutes each morning before project work starts reduces mistakes by recognizing patterns they have studied. Over 12 months, this modeler completes every self-review step without prompting.

**4. BIM Check**
- Check: Do you have a fixed time each day for BIM learning?
- Check: Do you keep a note of questions that arise during modeling?
- Check: Do you review weekly — not just read new content daily?

**5. Common Mistake**
Reading BIM content passively without applying it. Reading a lesson and then practicing the check items produces 3× the retention of reading alone.

**6. Today's Action**
Set a recurring 30-minute calendar block each weekday for BIM learning. Write the first three topics you will practice this week.

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

### Day 57 — MEP BIM Learning Path Beyond Starter

**1. Why This Matters**
Starter gives you the foundation. Knowing what comes next keeps your learning direction clear and prevents plateau.

**2. Core Concept**
**After Starter — Your next learning milestones:**

| Level | Focus | Time Frame |
|---|---|---|
| Level 2 (Modeler) | Modeling quality, families, schedules, system parameters | Months 3–6 |
| Level 3 (Coordinator) | Clash grouping, coordination meetings, issue tracking | Months 7–12 |
| Level 4 (Lead) | BEP authoring, QA/QC, delivery management | Year 2–3 |
| Level 5 (Automation) | Dynamo, Python, Revit API basics | Year 2–4 |

Tools progression:
- Revit MEP (all levels)
- Navisworks (from Level 2)
- BIM 360 / ACC (from Level 3)
- Dynamo (Level 5)
- Python / Revit API (Level 5)

**3. Real Project Lens**
A Starter graduate who immediately tries to learn Dynamo before completing 12 months of coordination experience finds the automation exercises meaningless — they cannot identify what to automate because they have not yet encountered the problems it solves.

**4. BIM Check**
- Check: What is the next skill level after your current position?
- Check: Which tool do you need to learn next?
- Check: Are there gaps in your current Level 1–2 knowledge before moving on?

**5. Common Mistake**
Skipping levels. Jumping to automation without coordination experience produces scripts that do not solve real project problems.

**6. Today's Action**
Write your personal BIM learning roadmap for the next 12 months. Include: current level, target level in 6 months, and two specific skills to practice each month.

---

### Day 58 — BIM Portfolio Building for Beginners

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

### Day 60 — 60-Day Completion Review

**1. Why This Matters**
Reviewing the full 60-day journey reinforces the most important concepts and gives clarity on what to practice next.

**2. Core Concept — 60-Day Summary**
| Track | Key Takeaway |
|---|---|
| Track 1 | BIM is a data workflow; LOD and roles define quality expectations |
| Track 2 | Revit setup, levels, linked models, connections — all must be verified |
| Track 3 | Read plans AND schematics; shop vs. coordination drawings are different |
| Track 4 | Model quality = geometry + data + system + delivery; self-review daily |
| Track 5 | Clash types, grouping, and the coordination meeting workflow |
| Track 6 | Schedules, parameters, and data exports are the BIM value output |
| Track 7 | Site readiness — what construction teams actually need from your BIM |
| Track 8 | Daily learning habit, level roadmap, portfolio building |

**3. Real Project Lens**
A learner who completes all 60 days can join a MEP BIM project as a junior modeler and perform basic modeling, self-review, and coordination preparation tasks without daily supervision.

**4. BIM Check**
- Check: Can you set up a Revit MEP project correctly?
- Check: Can you read a piping schematic and place elements accurately?
- Check: Can you complete a self-review in under 20 minutes?
- Check: Can you identify and describe a clash report?

**5. Common Mistake**
Believing that 60 days makes you a complete BIM professional. Starter gives you the foundation — real skill comes from project experience and continued learning.

**6. Today's Action**
Write a one-page personal summary: what you learned, what you still need to practice, and your 90-day plan from here. This is the beginning of your BIM learning portfolio.

---

## Track 9: Discipline Deep-Dive (Day 61–90)

> 학습자 신청 공종에 따라 아래 5개 중 1개 트랙 배정. 60일 완료 후 자동 전환.

---

### Track 9A — HVAC Deep Dive (Day 61–90)

| 구간 | 주제 | 핵심 내용 |
|---|---|---|
| Day 61–65 | 덕트 사이징 로직 | CFM 기반 덕트 면적 계산, 풍속 기준 (Low/Medium/High Velocity) |
| Day 66–70 | VAV 시스템 이해 | VAV 박스 연결, 존별 공조, 터미널 장치 조율 |
| Day 71–75 | 공조기실 장비 배치 | AHU, FCU, 쿨링 타워 레이아웃과 MEP 연결 |
| Day 76–80 | HVAC 간섭 패턴 | 덕트 vs. 구조보, 덕트 vs. 배관 간섭 해결 패턴 |
| Day 81–85 | HVAC 계통도 완성 | Diagram에서 모델까지 추적하는 방법 |
| Day 86–90 | HVAC 납품 기준 | LOD 350 HVAC 납품 체크리스트 |

---

### Track 9B — Piping / Mechanical Deep Dive (Day 61–90)

| 구간 | 주제 | 핵심 내용 |
|---|---|---|
| Day 61–65 | 냉온수 계통 구조 | 공급/환수 계통, 팽창탱크, 압력 계획 |
| Day 66–70 | 펌프 배치와 연결 | 기계실 레이아웃, 펌프 헤더, 체크밸브 |
| Day 71–75 | 밸브 및 액세서리 | 아이솔레이션 밸브, 플렉시블 조인트, 스트레이너 |
| Day 76–80 | 배관 간섭 패턴 | 배관 vs. 덕트, 배관 vs. 트레이 충돌 해결 |
| Day 81–85 | 파이프 사이징 파라미터 | Revit 파이프 사이즈 파라미터, 플로우 할당 |
| Day 86–90 | 배관 납품 기준 | LOD 350 배관 납품 체크리스트 |

---

### Track 9C — Plumbing / Sanitary Deep Dive (Day 61–90)

| 구간 | 주제 | 핵심 내용 |
|---|---|---|
| Day 61–65 | 위생 계통 구조 | 오수, 우수, 통기, 급수 계통 분류 |
| Day 66–70 | 경사 배관 모델링 | Revit 경사 설정, 최소 경사 기준 (1/50, 1/100) |
| Day 71–75 | 수직 라이저 처리 | 라이저 슬리브 요청, 슬래브 관통 위치 협의 |
| Day 76–80 | 위생기구 연결 | 변기, 세면대, 싱크 연결 계통 추적 |
| Day 81–85 | 위생 계통 간섭 | 경사 배관 vs. 구조 보, 드레인 vs. 바닥 슬래브 |
| Day 86–90 | 위생 납품 기준 | LOD 350 위생 납품 체크리스트 |

---

### Track 9D — Fire Protection Deep Dive (Day 61–90)

| 구간 | 주제 | 핵심 내용 |
|---|---|---|
| Day 61–65 | 소방 계통 구조 | Wet/Dry/Pre-action 시스템, 헤더 구성 |
| Day 66–70 | 스프링클러 헤드 배치 | 헤드 간격 기준, 커버리지, 방해물 고려 |
| Day 71–75 | 소방 배관 라우팅 | 메인/브랜치/스탠드파이프, 사이즈 기준 |
| Day 76–80 | 소방 간섭 패턴 | 헤드 vs. 덕트/트레이, 배관 vs. 구조 |
| Day 81–85 | 소방 계통 검증 | 헤드 위치 검증, 미커버 존 확인 방법 |
| Day 86–90 | 소방 납품 기준 | LOD 350 소방 납품 체크리스트 |

---

### Track 9E — Electrical Deep Dive (Day 61–90)

| 구간 | 주제 | 핵심 내용 |
|---|---|---|
| Day 61–65 | 케이블 트레이 라우팅 | 트레이 사이즈 기준, 경로 계획, 세퍼레이션 |
| Day 66–70 | 패널 보드 모델링 | 배전반 위치, 회로 구성, 부하 스케줄 |
| Day 71–75 | 전기 배관(Conduit) | EMT/GI 배관, 풀박스, 배관 크기 기준 |
| Day 76–80 | 전기 간섭 패턴 | 트레이 vs. 덕트, 고압/저압 분리 기준 |
| Day 81–85 | 전기 계통도 추적 | SLD → 패널 → 회로 → 부하 추적 방법 |
| Day 86–90 | 전기 납품 기준 | LOD 350 전기 납품 체크리스트 |

---

## 마일스톤 시스템 (v2 신규)

### 30일 마일스톤 (Day 30)

> **Telegram 특별 메시지 발송**

```
LUA BIM LABS Starter — 30 Days Complete

You have completed 30 days of MEP BIM Foundation.

Topics covered:
✓ MEP BIM Orientation (7 lessons)
✓ Revit MEP Basics (7 lessons)
✓ Drawing and System Reading (7 lessons)
✓ Model Quality Basics (7 lessons) — in progress

Keep going. The next 30 days cover clash coordination,
data management, site-readiness, and career habits.

Day 31 lesson continues tomorrow.
```

---

### 60일 수료 마일스톤 (Day 60)

> **PDF 수료 인증서 발급 + Telegram 메시지**

인증서 내용:
```
LUA BIM LABS
MEP BIM Foundation Certificate

This certifies that [Name]
has completed the 60-Day MEP BIM Foundation Program
covering all 8 core tracks of MEP BIM practice.

Issued: [Date]
LUA BIM LABS
```

---

### 90일 공종 수료 마일스톤 (Day 90)

> **공종별 PDF 수료 인증서 발급**

인증서 내용:
```
LUA BIM LABS
MEP BIM Discipline Certificate — [Discipline Name]

This certifies that [Name]
has completed the 90-Day MEP BIM Starter Program
including the [HVAC / Piping / Electrical / Fire / Plumbing]
Discipline Deep-Dive Track.

Issued: [Date]
LUA BIM LABS
```

---

## 주간 참여 이벤트: BIM Check Friday (v2 신규)

매주 금요일, 해당 주 학습 내용을 기반으로 한 5문항 퀴즈를 Telegram으로 발송.

### 형식 예시 (Week 1 Friday)

```
LUA BIM LABS — BIM Check Friday ✓
Week 1 Quick Check

Q1. What does LOD stand for?
Q2. Which MEP system is most affected by gravity in routing?
Q3. Who creates the BEP on a BIM project?
Q4. What is the role of shared coordinates in Revit?
Q5. Name one MEP discipline that occupies the most ceiling space.

Reply with your answers or just think through each one.
No grades — this is to test your own understanding.

Next week: Revit MEP Basics check.
```

학습자 응답은 선택 사항. 응답 시 LUA BIM LABS가 1~2줄 피드백 제공.

---

## 퀵 레퍼런스 카드 팩 (v2 신규)

Track 1~8 완료 시점마다 해당 트랙 핵심 내용을 담은 1페이지 PDF 카드 발송.

| 카드 | 제목 | 발송 시점 |
|---|---|---|
| Card 1 | MEP BIM Key Roles & LOD Reference | Day 07 완료 후 |
| Card 2 | Revit MEP Setup Checklist | Day 14 완료 후 |
| Card 3 | MEP Drawing Reading Guide | Day 21 완료 후 |
| Card 4 | Model Quality Self-Review Checklist | Day 28 완료 후 |
| Card 5 | Clash Types & Priority Matrix | Day 38 완료 후 |
| Card 6 | MEP Data & Schedule Reference | Day 47 완료 후 |
| Card 7 | Site-Readiness Check Guide | Day 54 완료 후 |
| Card 8 | BIM Learning Path & Next Steps | Day 60 완료 후 |

---

## 레슨 전달 운영 규칙 (v2 업데이트)

| 항목 | 기준 |
|---|---|
| 전달 채널 | Telegram 1:1 메시지 |
| 전달 주기 | 1일 1레슨 (월~일 중 구독 기간 내) |
| 레슨 길이 | Telegram 메시지 1~2개 (약 300~500단어) |
| 언어 | 영어 (기본) |
| 레슨 번호 | Day 01부터 순서대로 |
| 스킵 정책 | 스킵 없음; 학습자 요청 시 다음 레슨 예약 가능 |
| Q&A 범위 | 주 1회 짧은 확인 질문 허용; 심화 Q&A는 Personal Tutor 안내 |
| 범위 외 요청 | 모델 검토, 프로젝트 파일 검수, 설계 확인 → 서비스 범위 외로 안내 |
| **BIM Check Friday** | **매주 금요일 퀴즈 발송; 응답 선택 사항** |
| **마일스톤 자료** | **Day 30 메시지, Day 60·90 인증서 PDF 발송** |
| **퀵 레퍼런스 카드** | **Track 완료 시마다 PDF 1장 발송** |
| **공종 배정** | **Day 61 전 학습자 공종 확인 후 Track 9 배정** |
