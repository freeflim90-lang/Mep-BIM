# BIM Execution Plan (BEP) Template
## LUA BIM LABS | Project Mentor Template Pack | PM-T01
**Aligned to:** ISO 19650-2:2018 (Information management during design and construction)
**Version:** 1.0

---

## HOW TO USE THIS TEMPLATE

This template contains 8 sections that form the core of a project BEP. Each section includes:
- **Writing instructions** in [square brackets] — these tell you what to write. Remove all bracketed instructions from your final document.
- **Example text** in *italics* for at least one key subsection — this shows what finished content looks like.
- **Placeholder fields** in [CAPS BRACKETS] — replace these with project-specific information.

This template is designed to be adapted. Every project is different. Add, remove, or adjust subsections to suit your project's specific requirements and employer/client BIM requirements.

**Recommended: discuss the BEP structure with your client or main contractor before starting Section 1.** Many clients have a preferred format or mandatory sections. This template is a starting point, not a constraint.

---

# BIM EXECUTION PLAN

**Project Name:** [PROJECT NAME]
**Project Reference:** [PROJECT CODE / NUMBER]
**Client / Employer:** [CLIENT ORGANIZATION NAME]
**Lead Appointed Party:** [YOUR ORGANIZATION NAME]
**BEP Version:** [v1.0]
**BEP Status:** [Draft / Issued for Review / Approved]
**Date of Issue:** [DD MMM YYYY]
**Prepared By:** [NAME, TITLE]
**Approved By:** [NAME, TITLE]

**Document History:**

| Version | Date | Prepared By | Description of Change | Status |
|---------|------|-------------|----------------------|--------|
| v0.1 | | | Initial draft | Draft |
| v1.0 | | | Issued for review | For Review |

---

# SECTION 1: PROJECT INFORMATION AND BIM GOALS

## 1.1 Project Overview

[Write 3–5 sentences describing the project: building type, scale (GFA, number of floors, storeys), location, key program drivers (completion date, phasing), and the primary use of the building. This section gives any reader enough context to understand the project without needing to refer to another document.]

**Project Name:** [PROJECT NAME]
**Project Location:** [ADDRESS / CITY / COUNTRY]
**Building Type:** [e.g., 8-floor private hospital]
**Gross Floor Area:** [XX,XXX m²]
**Number of Floors:** [Above ground: XX | Below ground: XX]
**Project Value (if applicable):** [USD/SGD/AUD XX million — include if permitted by client]
**Planned Construction Start:** [Month YYYY]
**Planned Practical Completion:** [Month YYYY]
**Project Phases:** [List phases if the project is phased — e.g., Phase 1: Podium / Phase 2: Tower]

**Project Description:**
[2–4 sentences describing the building program and any BIM-specific context. For example: what systems are present, any unusual MEP complexity, whether the project has a mandatory BIM Level requirement from the client.]

*Example:*
*The project is an 8-floor private hospital located in [City], comprising approximately 32,000 m² gross floor area with a full-floor basement car park. The building includes operating theatres, ICU, inpatient wards, specialist clinics, and associated back-of-house facilities. MEP systems are highly complex, including medical gas, clean room HVAC, and redundant electrical supply systems. The client requires ISO 19650-compliant information management throughout the project lifecycle.*

## 1.2 BIM Goals

[List the specific goals for BIM use on this project. Be direct — "use BIM" is not a goal. Goals should describe outcomes: what problem does BIM solve on this project? What decisions will BIM inform? What deliverables will BIM produce?]

| # | BIM Goal | Priority | Responsible Party |
|---|----------|----------|------------------|
| 1 | [e.g., Detect and resolve all MEP-structural hard clashes prior to construction document issue] | High | [BIM Lead — Your organization] |
| 2 | [e.g., Produce coordinated MEP shop drawings for all floor levels before fabrication] | High | [MEP subcontractors] |
| 3 | [e.g., Maintain a single federated model updated fortnightly for client progress review] | Medium | [BIM Lead] |
| 4 | [e.g., Deliver an as-built BIM model for handover to facility management] | Medium | [All disciplines] |
| 5 | [e.g., Use BIM for quantification and material scheduling during procurement stage] | Low | [Main contractor] |

## 1.3 Scope of BIM Use on This Project

[Specify exactly which project stages BIM will be used and in what capacity. Not all stages need to be included — be honest about what is actually contracted and expected.]

| Stage | BIM Use | Deliverable |
|-------|---------|-------------|
| Schematic Design | Massing model, structural grid | Concept model (LOD 100) |
| Design Development | Discipline models, initial coordination | Coordinated DD model (LOD 200) |
| Construction Documents | Full MEP coordination, clash resolution | Coordinated CD model (LOD 300) |
| Shop Drawings | Fabrication coordination, spool drawings | Coordinated shop model (LOD 350) |
| As-Built | Record model updated to as-built condition | As-built model (LOD 400) |
| Operations | Handover model for FM system | FM model (LOD 500 elements as specified) |

---

# SECTION 2: BIM TEAM ROLES AND RESPONSIBILITIES

## 2.1 BIM Team Overview

[Identify all organizations on the project who are responsible for BIM deliverables. List each organization with their role and the BIM contact person. This is not just the MEP team — it includes structural, architectural, civil, and any specialists who will produce models.]

| Organization | Project Role | BIM Role | BIM Contact | Contact Email |
|-------------|-------------|---------|------------|--------------|
| [YOUR ORG] | [MEP Lead Contractor] | Lead Appointed Party / BIM Lead | [NAME] | [email] |
| [STRUCTURAL FIRM] | Structural Engineer | Appointed Party | [NAME] | [email] |
| [ARCHITECT] | Architect of Record | Appointed Party | [NAME] | [email] |
| [HVAC SUBCONTRACTOR] | MEP Subcontractor — HVAC | Sub-Appointed Party | [NAME] | [email] |
| [ELECTRICAL SUBCONTRACTOR] | MEP Subcontractor — Electrical | Sub-Appointed Party | [NAME] | [email] |
| [PLUMBING SUBCONTRACTOR] | MEP Subcontractor — Plumbing | Sub-Appointed Party | [NAME] | [email] |
| [CLIENT] | Employer | Information Manager (Approving) | [NAME] | [email] |

## 2.2 BIM Lead Responsibilities

[Describe the BIM Lead's specific responsibilities on this project. This should be specific — not a generic job description. It should reflect what this BIM Lead will actually do on this project.]

The BIM Lead ([NAME], [ORGANIZATION]) is responsible for:

- Authoring and maintaining this BEP, and issuing revised versions as required
- Managing the Common Data Environment (CDE) — folder structure, access permissions, and naming convention compliance
- Running clash detection tests on a [weekly / fortnightly] basis and distributing clash reports to the coordination team
- Chairing coordination meetings and distributing minutes within 24 hours
- Reviewing all model submissions from sub-appointed parties against the QA/QC checklist before acceptance
- Maintaining the Master Issue Log
- Producing the federated model and distributing it to the client at agreed milestones
- Preparing and issuing the Monthly BIM Progress Report to the client
- Managing model version control and ensuring the CDE's Work In Progress / Shared / Published zones are maintained correctly

## 2.3 Sub-Appointed Party Responsibilities (MEP Subcontractors)

[Describe the responsibilities shared by all MEP subcontractors producing models. Each subcontractor accepts these responsibilities by signing the BEP or a BEP Acceptance Form.]

Each sub-appointed party producing a BIM model on this project is responsible for:

- Producing and maintaining their discipline model in accordance with this BEP and the project naming convention
- Submitting models to the CDE Shared zone on the agreed [weekly / fortnightly] schedule
- Confirming in writing that each submitted model has been checked against the QA/QC checklist (Section 8) before upload
- Attending coordination meetings and acting on action items within agreed timeframes
- Notifying the BIM Lead of any design changes that may affect other disciplines' models within [24 / 48] hours of receiving a change notice

*Example — how this looks in a completed BEP:*
*Each sub-appointed party agrees to submit updated models to the BIM 360 project folder (path: [PROJECT] / MEP Coordination / WIP / [Discipline]) every Friday by 17:00. The BIM Lead will run clash detection on Monday mornings against all submitted models. Any model submitted after 17:00 Friday will be included in the following week's clash run. Late submissions must be notified to the BIM Lead by email.*

---

# SECTION 3: BIM USES

## 3.1 Defined BIM Uses for This Project

[A BIM Use is a specific way that BIM is applied to achieve a project outcome. List only the BIM Uses that are actually contracted or agreed — do not list aspirational uses. For each BIM Use, specify who does it, which tools are used, and what the output is.]

| # | BIM Use | Stage | Responsible | Software | Output |
|---|---------|-------|-------------|---------|--------|
| 1 | Design Authoring | All stages | All disciplines | Revit [version] | Discipline models |
| 2 | Clash Detection and Coordination | CD / Shop | BIM Lead | Navisworks Manage [version] | Clash reports, Coordinated federated model |
| 3 | 4D Construction Sequencing | Pre-construction | Main Contractor BIM team | Navisworks + P6 | 4D simulation video |
| 4 | Design Review (Client) | DD and CD | BIM Lead | BIM 360 / Navisworks Freedom | Federated model for review |
| 5 | Quantity Take-off | CD | Main Contractor | [Tool] | BOQ extract |
| 6 | As-Built Documentation | Construction | All disciplines | Revit | As-built models |
| 7 | Facility Management Handover | Handover | All disciplines | Revit + [FM platform] | FM-ready model |

## 3.2 BIM Use Descriptions

[For each BIM Use above, write 1–3 sentences describing how it will be executed on this specific project. Not all BIM Uses require the same depth of description — focus on the ones that involve coordination between parties or that are complex.]

**BIM Use 1 — Design Authoring:**
All disciplines will produce their models in Autodesk Revit [YEAR VERSION]. Shared Coordinates must be set using the project coordinate file provided by [STRUCTURAL / ARCHITECT] at the project start. Grid and level names must match the reference model exactly.

**BIM Use 2 — Clash Detection and Coordination:**
[Description of how clash detection will be run — frequency, discipline pairs tested, tools, report format, distribution. Refer to Section 5 for the full coordination procedure.]

[Continue for remaining BIM Uses]

---

# SECTION 4: LEVEL OF DEVELOPMENT (LOD) REQUIREMENTS BY STAGE

## 4.1 LOD Definitions Used on This Project

[Specify which LOD framework this project uses. Common frameworks: AIA LOD Specification, UK RIBA LOD equivalents, Singapore BIM Guide LOD, or a project-specific LOD matrix. Specify this clearly to prevent misunderstandings between parties.]

This project uses the [AIA LOD Specification / PROJECT-SPECIFIC] framework. LOD is defined as follows:

| LOD | Description | What Must Be Modeled |
|-----|-------------|---------------------|
| LOD 100 | Conceptual | Overall size, shape, location, orientation — approximate |
| LOD 200 | Approximate geometry | Systems and assemblies with approximate quantities, size, shape, location |
| LOD 300 | Precise geometry | Specific systems, assemblies and objects. Quantities, size, shape, location precisely defined |
| LOD 350 | Construction-level detail | As LOD 300 plus interfaces with other systems modeled. Sufficient for fabrication coordination |
| LOD 400 | Fabrication / as-installed | As LOD 350 plus fabrication, assembly, installation detail |
| LOD 500 | As-built / FM record | As LOD 400 plus verified in-situ condition. FM data populated as specified |

## 4.2 LOD Requirements by Discipline and Stage

[Complete this matrix for your project. Only include what is actually required. If a discipline is not required to model certain elements, state "Not modeled" rather than leaving it blank.]

| Discipline | SD | DD | CD | Shop | As-Built | Handover |
|-----------|----|----|----|----|---------|---------|
| Architecture | 100 | 200 | 300 | N/A | 400 | N/A |
| Structure | 100 | 200 | 300 | 350 | 400 | N/A |
| HVAC | 100 | 200 | 300 | 350 | 400 | 500* |
| Electrical | 100 | 200 | 300 | 350 | 400 | 500* |
| Plumbing | N/A | 200 | 300 | 350 | 400 | 500* |
| Fire Protection | N/A | 200 | 300 | 350 | 400 | N/A |
| Medical Gas | N/A | N/A | 300 | 350 | 400 | 500* |

*LOD 500 elements for FM handover are specified in the separate Information Requirements schedule. Not all elements require LOD 500 — only those on the FM asset list.

## 4.3 Non-Geometric Information Requirements

[Specify what parameter data must be included in elements at each LOD stage. This is critical for QA/QC compliance and FM handover.]

| Stage | Required Parameters (examples — adjust to project) |
|-------|--------------------------------------------------|
| LOD 300 | Element mark, system name, manufacturer (if specified), model number, material |
| LOD 350 | All LOD 300 parameters + installation notes, clearance zones |
| LOD 400 | All LOD 350 parameters + actual installed size, connection details |
| LOD 500 | All LOD 400 parameters + asset tag, warranty expiry, maintenance schedule reference |

---

# SECTION 5: COORDINATION PROCEDURE

## 5.1 Coordination Philosophy

[Write 1 paragraph describing the approach to coordination on this project. This is not a list — it is a statement of intent that sets the culture.]

*Example:*
*MEP coordination on this project is managed as a proactive, integrated process — not a reactive clash-fixing exercise. The BIM Lead is responsible for establishing a coordination environment where clashes are detected early, resolved collaboratively, and documented consistently. All sub-appointed parties are expected to attend coordination meetings, act on action items within agreed timeframes, and communicate design changes to the BIM Lead before updating their models. Coordination decisions are documented in the Master Issue Log, which is the single source of truth for all coordination issues on this project.*

## 5.2 Model Submission Schedule

[Specify exactly when models must be submitted and in what format.]

| Discipline | Submission Frequency | Submission Day | Submission Format | CDE Location |
|-----------|---------------------|---------------|------------------|-------------|
| HVAC | Weekly | Friday, 17:00 | RVT + IFC 2x3 | [CDE path] |
| Electrical | Weekly | Friday, 17:00 | RVT + IFC 2x3 | [CDE path] |
| Plumbing | Weekly | Friday, 17:00 | RVT + IFC 2x3 | [CDE path] |
| Fire Protection | Fortnightly | Friday, 17:00 | RVT + IFC 2x3 | [CDE path] |
| Structural | Fortnightly | [Day] | RVT + IFC 2x3 | [CDE path] |

## 5.3 Clash Detection Protocol

**Frequency:** Clash detection is run every [Monday / fortnightly on [day]] by the BIM Lead.

**Discipline pairs tested:**

| Test | Discipline A | Discipline B | Test Type |
|------|-------------|-------------|----------|
| 1 | HVAC | Structural | Hard + Clearance |
| 2 | HVAC | Electrical | Hard |
| 3 | HVAC | Plumbing | Hard |
| 4 | HVAC | Fire Protection | Hard |
| 5 | Electrical | Structural | Hard |
| 6 | Plumbing | Structural | Hard |
| 7 | Fire Protection | Structural | Hard |
| 8 | Electrical | Plumbing | Hard |

**Clash report distribution:** Within 24 hours of each clash detection run. Distributed via [BIM 360 issue tracker / email]. All parties with clashes in their discipline receive the relevant sections.

**Clash priority scoring:** Using the Clash Priority Matrix (Appendix [X]). All Critical and High priority clashes must be resolved within [5 / 7] business days of issue.

## 5.4 Coordination Meeting Schedule

| Meeting Type | Frequency | Chair | Required Attendees |
|-------------|-----------|-------|-------------------|
| MEP Coordination Meeting | Weekly | BIM Lead | All MEP discipline BIM leads |
| Multi-Discipline Coordination | Fortnightly | Project BIM Manager | All disciplines |
| Client Progress Meeting | Monthly | [Client PM] | BIM Lead + Project Manager |

---

# SECTION 6: COMMON DATA ENVIRONMENT (CDE) SETUP

## 6.1 CDE Platform

**CDE Platform Used:** [Autodesk Construction Cloud (ACC) / BIM 360 / SharePoint / ProjectWise / Other]
**CDE Administrator:** [NAME, ORGANIZATION]
**Access Request Contact:** [NAME, email]
**Platform URL:** [https://...]

All model submissions, coordination reports, and project documents are managed through this platform. Email attachments are not acceptable as model submissions.

## 6.2 CDE Zone Structure

This project uses the following CDE zones in accordance with ISO 19650:

| Zone | Purpose | Who Can Upload | Who Can View |
|------|---------|---------------|-------------|
| Work In Progress (WIP) | Working models — in progress, not yet reviewed | Each party in their own folder | Uploader only |
| Shared | Models reviewed and approved for coordination use | BIM Lead (after QA check) | All project parties |
| Published | Formally issued documents — milestone deliverables | Project Manager / BIM Lead | All + Client |
| Archive | Superseded versions retained for record | BIM Lead | BIM Lead + Project Manager |

## 6.3 Folder Structure

[Specify the exact folder structure within the CDE. This must be set up by the CDE Administrator before the project starts. All parties must use this structure — no ad-hoc folders.]

```
[PROJECT CODE]/
├── 00_Project Admin/
│   ├── BEP/
│   ├── Contracts/
│   └── Meeting Minutes/
├── 01_Reference Models/
│   ├── Architecture/
│   ├── Structure/
│   └── Survey/
├── 02_MEP Coordination/
│   ├── WIP/
│   │   ├── HVAC/
│   │   ├── Electrical/
│   │   ├── Plumbing/
│   │   └── Fire Protection/
│   ├── Shared/
│   │   └── Federated/
│   ├── Clash Reports/
│   │   └── [YYYY-MM-DD]/
│   └── Issue Log/
├── 03_Drawings/
│   ├── WIP/
│   └── Issued/
├── 04_Deliverables/
│   └── [Milestone Name]/
└── 05_Archive/
```

## 6.4 CDE Access and Permissions

[List access levels. Do not leave access ad hoc — all parties must be granted access before project start.]

| Role | CDE Access Level | Can Upload to Shared? | Can Publish? |
|------|-----------------|----------------------|-------------|
| BIM Lead | Admin | Yes | Yes |
| MEP Subcontractor BIM Coordinator | Contributor | WIP only | No |
| Structural BIM Lead | Contributor | Shared (own models only) | No |
| Client BIM Representative | Viewer | No | No |
| Project Manager | Editor | Yes | Yes |

---

# SECTION 7: DELIVERABLE SCHEDULE AND NAMING CONVENTION

## 7.1 Deliverable Schedule

[List all formal BIM deliverables — the files submitted to the client at each milestone. This is different from the ongoing coordination model submissions in Section 5.]

| Deliverable | Format | Stage | Target Date | Responsible |
|------------|--------|-------|-------------|-------------|
| Federated MEP Model (Coordination) | RVT + IFC | CD Stage | [Date] | BIM Lead |
| MEP Coordination Drawings (PDFs) | PDF | CD Stage | [Date] | BIM Lead |
| Clash Resolution Report | PDF | CD Stage | [Date] | BIM Lead |
| BEP Compliance Confirmation | PDF | CD Stage | [Date] | BIM Lead |
| Shop Drawing Coordination Model | RVT + IFC | Shop Drawing Stage | [Date] | All MEP |
| As-Built Models (per discipline) | RVT | Handover | [Date] | Each discipline |
| FM-Ready Federated Model | RVT + IFC | Handover | [Date] | BIM Lead |

## 7.2 File Naming Convention

[Specify the exact naming convention for all files in the CDE. This must be defined before any files are created. The convention applies to models, drawings, reports, and all documents.]

**Format:**
```
[Project Code]-[Originator]-[Volume/System]-[Level/Location]-[Type]-[Role]-[Number]-[Revision]
```

**Field Definitions:**

| Field | Description | Example Values |
|-------|-------------|---------------|
| Project Code | 3–6 character project abbreviation | PRJ01, HSP, TWR2 |
| Originator | 3–4 character organization code | LUA, HVAC, ELEC |
| Volume/System | Building volume or MEP system | Z1 (Zone 1), MEP, STR |
| Level | Floor level or zone | L01, L02, RF, B1 |
| Type | Document type | M (Model), D (Drawing), R (Report) |
| Role | Status code | S1 (Suitable for coordination), A1 (Suitable for construction), etc. |
| Number | 4-digit sequential | 0001, 0002 |
| Revision | Revision letter | A, B, C |

**Example file name:**
`PRJ01-LUA-MEP-L03-M-S1-0001-A`
*(Project PRJ01, originator LUA, MEP systems, Level 3, Model file, Suitable for Coordination, First file, Revision A)*

## 7.3 Revision Status Codes

| Code | Meaning | Who Can Assign |
|------|---------|---------------|
| S0 | Work in Progress | Any party |
| S1 | Suitable for Coordination | BIM Lead (after QA check) |
| S2 | Suitable for Information | BIM Lead |
| A0 | Suitable for Review | BIM Lead |
| A1 | Suitable for Construction | Project Manager + BIM Lead |
| A4 | As-Built | BIM Lead |

---

# SECTION 8: QUALITY ASSURANCE AND QUALITY CONTROL (QA/QC)

## 8.1 QA/QC Policy Statement

[Write 1 paragraph on the project's QA/QC commitment. This is the governing statement that all parties are held to.]

*Example:*
*No model is submitted to the CDE Shared zone without passing a QA/QC review. Each sub-appointed party is responsible for self-reviewing their model against the discipline-specific QA/QC checklist before submission. The BIM Lead conducts an independent QA/QC review on all models within 48 hours of submission. Models that fail QA/QC are returned to the submitting party with a written review note specifying the deficiencies. The submitting party must address all noted deficiencies and resubmit before the model is accepted for coordination use.*

## 8.2 Model Health Standards

All models submitted for coordination must meet the following minimum health standards:

| Check | Standard | Tool |
|-------|---------|------|
| File size | Maximum [150 MB / adjust per project] per discipline model | File system |
| Warnings | Zero critical warnings; maximum [X] non-critical warnings | Revit |
| Unjoined elements | Zero unjoined elements in active systems | Revit |
| Shared coordinates | Set to project coordinate system | Revit |
| Grid and level match | Matches reference structural model | Revit |
| Naming convention | All elements named per Section 7 convention | Manual review |
| System classifications | All elements assigned to correct system | Revit |
| No worksets in wrong file | Each model contains only its own discipline | Revit |

## 8.3 QA/QC Checklist Reference

Full discipline-specific QA/QC checklists are provided in the Project Mentor Template Pack (QA_CHECKLISTS.md). These checklists must be completed and signed before each model submission.

Disciplines with dedicated checklists:
- HVAC BIM Model QA/QC Checklist (PM-T02)
- Electrical BIM Model QA/QC Checklist (PM-T03)
- Plumbing: use the HVAC checklist as a base, adapted for plumbing systems
- Fire Protection: use the HVAC checklist as a base, adapted for FP systems

## 8.4 Non-Compliance Procedure

If a submitted model fails the QA/QC review:

1. The BIM Lead issues a **Model Review Notice** to the submitting party within 48 hours of receiving the model.
2. The notice specifies each deficiency with a reference to the failed checklist item.
3. The submitting party must correct all deficiencies and resubmit within [3 / 5] business days.
4. Repeated non-compliance (3 or more failed submissions) is escalated to the Project Manager for commercial review.
5. All model review notices and resubmissions are logged in the CDE under [path] and in the Master Issue Log.

## 8.5 Milestone Delivery QA

Before any milestone delivery (Section 7.1), the BIM Lead must complete the following:

- [ ] All discipline models updated to the correct LOD for the milestone
- [ ] All critical and high-priority clashes resolved (or documented as accepted with written approval)
- [ ] Federated model assembled and checked for shared coordinates
- [ ] Naming convention compliance verified for all submitted files
- [ ] Model health check passed for all discipline models
- [ ] BEP compliance confirmed (this BEP reviewed against deliverable)
- [ ] Clash Resolution Report prepared and reviewed by Project Manager
- [ ] Deliverable package reviewed and signed off by BIM Lead before issue

---

## BEP SIGN-OFF

This BEP is a living document. It is reviewed and updated at each project milestone, or when a significant change affects the project's information management requirements.

**Prepared By:**
Name: _________________ Title: _________________ Date: _________
Organization: _______________ Signature: _____________________

**Approved By (Lead Appointed Party):**
Name: _________________ Title: _________________ Date: _________
Organization: _______________ Signature: _____________________

**Acknowledged By (Client / Employer):**
Name: _________________ Title: _________________ Date: _________
Organization: _______________ Signature: _____________________

**Acknowledged By (Sub-Appointed Parties):**

| Organization | Name | Title | Date | Signature |
|-------------|------|-------|------|-----------|
| | | | | |
| | | | | |
| | | | | |

---

*LUA BIM LABS Project Mentor Template Pack PM-T01 v1.0 — For subscriber use only.*
*Aligned to ISO 19650-2:2018. Adapt to your project's specific requirements.*
