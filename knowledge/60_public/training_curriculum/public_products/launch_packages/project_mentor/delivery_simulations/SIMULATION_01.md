# Project Mentor — Delivery Simulation #1
## LUA BIM LABS | Monthly Delivery Simulation
**Topic:** Hospital MEP BIM Delivery — Construction Stage Submission
**Version:** 1.0

---

## HOW THIS WORKS

This simulation tests your ability to plan and execute a formal BIM milestone delivery. You are not asked to produce actual files — you are asked to write a delivery package plan: what you would prepare, in what sequence, and how you would ensure quality before submission.

**What to submit:** A written delivery plan (300–600 words). Tables, checklists, and structured lists are encouraged. No word-processing format required — plain text is fine.

**Submission:** Send your response to your mentor via Telegram within 7 business days of receiving this scenario.

**Feedback:** LUA BIM LABS will send you detailed written feedback within 48 hours of your submission. We will discuss your response in the next monthly Zoom session if timing allows.

---

## THE SCENARIO

### Project Overview

**Project:** Greenhill Private Hospital — MEP BIM Construction Stage Delivery
**Location:** [City], Southeast Asia
**Scale:** 8 floors above ground + 1 basement level | 28,400 m² gross floor area
**Structure:** Reinforced concrete frame with post-tensioned transfer slabs on Levels 2 and 5
**MEP Scope:** Full MEP — HVAC, electrical (LV power, lighting, ELV), plumbing, medical gas, fire protection

**MEP Team:**
- BIM Lead: You (the learner)
- HVAC subcontractor: 2 modelers
- Electrical subcontractor: 2 modelers
- Plumbing subcontractor: 1 modeler
- Medical gas: 1 modeler (specialist subcontractor)
- Fire protection: 1 modeler (specialist subcontractor)

**Software used:** Autodesk Revit (all disciplines), Autodesk Navisworks Manage (clash detection), Autodesk Construction Cloud BIM 360 (CDE)

**Project stage:** Construction document coordination complete. First major MEP milestone delivery to the Main Contractor.

---

### The Delivery Requirement

The Main Contractor (MC) has issued a Delivery Requirements Notice requiring the following deliverables to be submitted by **Friday, 17:00 [in 10 calendar days from now]**:

**Required deliverables:**

1. **Federated MEP Model** — in both RVT and IFC 2x3 formats. Must include all MEP disciplines. Must be set to project shared coordinates. Must use the project naming convention from the BEP.

2. **Coordination Drawings (PDFs)** — Coordinated MEP plan views and section views at a minimum of 1:50 scale for all occupied floors. Key mechanical plant rooms at 1:20. PDF format, compiled in a single file per floor level.

3. **Clash Resolution Report** — A report documenting: total clashes detected, total clashes resolved, remaining open clashes (with status and reason for deferral), and any clashes formally accepted.

4. **BEP Compliance Confirmation** — A written confirmation (1–2 pages) that the delivered models comply with the BEP requirements, including: LOD, naming convention, system classification, model health, and CDE management.

5. **Model Health Report** — A summary of model health for all discipline models: file sizes, warning counts, shared coordinate status, and model completeness statement.

**Main Contractor's Stated Conditions:**
- All 5 deliverables must be submitted simultaneously — partial submission is not accepted.
- Any critical clash (Priority Score 20–25) remaining unresolved must be documented with a written explanation and a resolution plan.
- The Federated Model IFC must open correctly in Navisworks Freedom (the MC will verify this).
- All deliverables must be uploaded to BIM 360 under the folder: `[PROJECT] / Deliverables / CD01_MEP_[DATE]`.

**Known current state (what you are starting from):**
- HVAC model: last updated 3 days ago. QA/QC checklist not yet run.
- Electrical model: updated yesterday. QA/QC checklist completed — Conditional Pass (3 items flagged).
- Plumbing model: updated today. QA/QC checklist not yet run.
- Medical gas model: updated 5 days ago. The medical gas subcontractor reports they have 1 critical open clash (with structural) that is unresolved — the structural engineer has not responded to their RFI in 7 days.
- Fire protection model: updated 4 days ago. QA/QC checklist not yet run.
- Last federated clash detection: 5 days ago. 2 critical clashes outstanding, 14 high-priority clashes outstanding.
- Clash Resolution Report: draft prepared but not yet updated with last 3 days of resolution work.
- Federated model has not been rebuilt since the electrical and plumbing updates from the last 2 days.
- BEP Compliance Confirmation: not yet started.
- Model Health Report: not yet started.

---

## WHAT YOU MUST PREPARE

Write your delivery package plan covering all of the following:

**1. Delivery timeline.** You have 10 calendar days. Working backwards from the Friday submission deadline, lay out your day-by-day schedule for completing all 5 deliverables. Include which tasks must happen before others (dependencies).

**2. QA/QC completion plan.** Which models still need QA/QC? Who runs the checks? What do you do if a model fails QA/QC with 2 days to the deadline?

**3. Critical clash resolution plan.** You have 2 critical clashes outstanding and 1 unresolved medical gas clash with no RFI response from the structural engineer. How do you handle each of these before the submission?

**4. Federated model rebuild and IFC export.** What is your process for rebuilding the federated model, running a final clash check, and exporting the IFC? What do you verify before the IFC export is considered delivery-ready?

**5. Document preparation plan.** How do you prepare the Clash Resolution Report, BEP Compliance Confirmation, and Model Health Report? Who writes them? What information do you need from the team?

**6. Upload and handover.** What is your final step before clicking "submit"? What do you verify in BIM 360 before notifying the Main Contractor that the delivery package is ready?

---

## EVALUATION CRITERIA

LUA BIM LABS will evaluate your response on the following four criteria. Each is scored 1–5.

---

**Criterion 1: Delivery Planning and Sequencing (1–5)**

Does the response demonstrate a clear, realistic understanding of the sequence and dependencies in preparing a BIM delivery package?

| Score | Description |
|-------|-------------|
| 1 | No sequence or timeline. Response lists deliverables without a plan for producing them. |
| 2 | Basic timeline present but missing key dependencies (e.g., builds the federated model before QA/QC is complete on all disciplines). |
| 3 | Correct sequencing of most tasks. Realistic timeline. Missing 1–2 key steps. |
| 4 | Correct sequencing of all key tasks with realistic time allocation and clear dependency logic. |
| 5 | Full delivery timeline, well-sequenced, realistic, with built-in buffer for QA/QC failures and rework. Identifies the critical path. |

**What a strong response includes:** Rebuilding the federated model after all discipline QA/QC checks are complete (not before). Running a final clash check on the rebuilt federated model. Completing the Clash Resolution Report after the final clash check (not before). Completing the BEP Compliance Confirmation based on the final submitted models (not a draft). BIM 360 upload verification after upload (not assumed correct).

---

**Criterion 2: QA/QC Execution (1–5)**

Does the response demonstrate a clear, structured QA/QC execution approach — not just "run the checklist" but an understanding of what to do when results are not clean?

| Score | Description |
|-------|-------------|
| 1 | No mention of QA/QC process. |
| 2 | Mentions running QA/QC checklists but no plan for managing failures or conditional passes. |
| 3 | Runs QA/QC checks and handles failures by returning to the subcontractor. Timeline impact acknowledged. |
| 4 | Full QA/QC process including: what happens when a model fails 3 days before deadline, how to escalate, what conditional acceptance means. |
| 5 | As per 4, plus a clear decision framework: what QA/QC failures are blocking vs. acceptable on a conditional basis for this delivery. Includes verification of the IFC export separately from the RVT QA/QC. |

**What a strong response includes:** The 3 conditional pass items on the electrical model must be addressed and re-checked before delivery. The unreviewed models (HVAC, plumbing, fire protection) each need a QA/QC run with a defined pass/fail threshold. A late-stage QA/QC failure has a different response than one discovered 7 days out. The BIM Lead must verify the IFC independently — a clean RVT does not guarantee a clean IFC.

---

**Criterion 3: Stakeholder and Problem Management (1–5)**

Does the response demonstrate mature handling of the two main non-technical problems: the unresolved structural RFI (medical gas clash) and the upstream dependency on subcontractor model updates?

| Score | Description |
|-------|-------------|
| 1 | No mention of the structural RFI issue or stakeholder dependencies. |
| 2 | Mentions the RFI issue but the proposed action is to "wait for the structural engineer." |
| 3 | Escalates the RFI to the project manager. Acknowledges the risk to the delivery timeline. |
| 4 | Escalates the RFI with a specific written request and a deadline. Has a contingency plan if the RFI is not resolved by delivery day. |
| 5 | Full stakeholder plan: escalates RFI immediately with written evidence (dates sent, no response). Proposes a documented interim solution (e.g., formally accept the clash with a written note in the Clash Resolution Report, pending RFI response — with MC's approval). Anticipates that the MC may accept a documented unresolved critical clash if the reason is outside the BIM Lead's control and properly documented. |

**What a strong response includes:** Treating the 7-day non-response on a critical clash as a risk requiring immediate escalation, not passive waiting. Understanding that a critical clash in the delivery report must either be resolved, formally accepted, or documented with a resolution plan and owner — it cannot simply be omitted. Recognizing that the MC's stated requirement ("any critical clash remaining unresolved must be documented with a written explanation and a resolution plan") is actually a provision for this exact scenario, not a prohibition.

---

**Criterion 4: Documentation Quality and Completeness (1–5)**

Does the response demonstrate a clear understanding of what each document in the delivery package must contain and how it is produced?

| Score | Description |
|-------|-------------|
| 1 | Mentions the 5 deliverables but has no detail on how each is produced or what it contains. |
| 2 | Describes 2–3 deliverables in reasonable detail. The others are acknowledged but not developed. |
| 3 | All 5 deliverables addressed. Clash Resolution Report and BEP Compliance Confirmation are described at a general level. |
| 4 | All 5 deliverables addressed in detail. Clash Resolution Report structure is correct (total / resolved / open / accepted). BEP Compliance Confirmation lists the specific BEP sections being confirmed. Model Health Report includes specific data points (file sizes, warnings, coordinate status). |
| 5 | As per 4, plus the response demonstrates understanding that: (a) the Clash Resolution Report must reflect the state of the final submitted model, not a previous state; (b) the BEP Compliance Confirmation is a formal document, not an email; (c) the Model Health Report data must be pulled after the final model is saved and synchronized (not from memory). |

**Maximum score: 20 points**
**Strong response: 16–20 | Competent response: 11–15 | Developing response: 6–10 | Foundational: below 6**

---

## SAMPLE STRONG RESPONSE
### [LUA BIM LABS INTERNAL REFERENCE ONLY — DO NOT SEND TO CLIENTS]

---

**DELIVERY PACKAGE PLAN — Greenhill Hospital CD01 MEP Submission**

**Day 1–2 (Weekend, if available, or Monday–Tuesday)**

Priority 1: Resolve the medical gas critical clash. I will immediately send a written escalation to the structural engineer with a 48-hour response request, copied to the project manager. The message will document: the RFI number, date first sent, no response received after 7 days, and the impact on the project delivery schedule. Simultaneously, I will draft the interim documentation: if no response is received by Day 3, I will prepare a Clash Acceptance Memorandum for the MC's review, proposing to formally accept the critical clash with a documented owner (structural engineer) and resolution plan tied to the RFI response.

Priority 2: Initiate QA/QC checks on HVAC, plumbing, and fire protection models in parallel with the escalation. Assign to the discipline BIM coordinators with a deadline of Day 3 for results. Provide them with the QA/QC checklists. If any model fails a critical item, they must correct and resubmit by Day 4.

Priority 3: Resolve the 3 conditional pass items on the electrical model. Confirm completion by Day 2.

**Day 3–4**

Receive QA/QC results from all disciplines. Review each checklist. For any conditional passes: assess whether the flagged items are blocking (must fix before delivery) or non-blocking (can be noted in the BEP Compliance Confirmation as known minor items to be resolved post-delivery). Anything structural-coordinate related or system-classification related is blocking. View naming and parameter completeness may be conditional.

Rebuild the federated model in Navisworks after all QA/QC-approved RVT files have been submitted to BIM 360. Do not rebuild until all disciplines have passed (or conditionally passed) QA/QC. Run a final full clash detection across all discipline pairs. Document the results.

**Day 5**

Complete the Clash Resolution Report based on the final clash detection. Structure: (1) summary statistics — total detected, total resolved, total accepted, total outstanding; (2) outstanding critical clashes — medical gas clash with full escalation history and interim resolution plan; (3) outstanding high-priority clashes — status and owner for each; (4) accepted clashes — list with written acceptance justification for each. This document is prepared only after the final clash detection run.

**Day 6**

Prepare the BEP Compliance Confirmation. Review the BEP Section by section: LOD compliance (confirmed per discipline and stage), naming convention (verified during QA/QC), system classification (verified during QA/QC), model health (confirmed via QA/QC checklists), CDE management (confirm all models are in the correct CDE folder under the correct revision status code). Where a BEP requirement was not fully met, state it clearly with a note on the status.

Prepare the Model Health Report. Pull data from the final synchronized models: file size per discipline, warning count per discipline, shared coordinate status, revision code, QA/QC checklist result. Compile into a table. The BIM Lead signs the report.

**Day 7**

Export the IFC from the federated Revit model. Open the IFC in Navisworks Freedom and verify: all disciplines are present, elements are correctly classified, no missing geometry, coordinate system is correct. Do not submit the IFC until this verification is complete.

Compile the coordination drawings. Generate coordinated plan views for all floors at 1:50 and key plant rooms at 1:20. Export as PDFs compiled by floor level. Review each drawing for visible errors or missing elements before compilation.

**Day 8–9 (Buffer)**

Final internal review of all 5 deliverables together — check that they are consistent with each other. The clash counts in the Clash Resolution Report must match the final clash detection. The model revision in the BEP Compliance Confirmation must match the uploaded RVT files.

Upload all files to BIM 360 under `[PROJECT] / Deliverables / CD01_MEP_[DATE]`. Verify each file uploads successfully and is the correct version. Check file sizes and names against the delivery checklist.

**Day 10 (Friday)**

Send the formal delivery notification to the Main Contractor before 17:00. The notification is an email (or BIM 360 message) stating: the deliverable list, BIM 360 folder path, date and time of upload, BIM Lead signature, and any known issues with the package (e.g., medical gas critical clash status). This message is the formal record that the delivery was made.

**Critical risk: the unresolved structural RFI.** If the structural engineer does not respond by Day 3, I will submit a Clash Acceptance Memorandum to the MC's project manager on Day 4 asking for their written acceptance of the interim approach. I will not submit the delivery package without this acceptance in hand. If the MC refuses to accept the clash in this format, I will escalate to the project manager immediately and request a 2-day extension to the delivery deadline — with documentation of the reason being the structural engineer's non-response.

---

## SAMPLE FEEDBACK MESSAGE STRUCTURE
### [LUA BIM LABS INTERNAL — How to structure the feedback message to the client]

```
─────────────────────────────────────────────────────
DELIVERY SIMULATION FEEDBACK
Project Mentor | [Client Name]
Simulation #1: Hospital MEP BIM Delivery
─────────────────────────────────────────────────────

YOUR SCORE: [X] / 20

─────────────────────────────────────────────────────
CRITERION 1 — Delivery Planning and Sequencing: [X/5]

[3–4 sentences of specific feedback. If the client built the federated model
before QA/QC was complete: call this out explicitly and explain why the
sequence matters. If the timeline was realistic and well-sequenced: say so
and note specifically what was done well. Reference their actual response.]

─────────────────────────────────────────────────────
CRITERION 2 — QA/QC Execution: [X/5]

[3–4 sentences. Did they address the 3 conditional pass items on the
electrical model? Did they have a plan for QA/QC failures close to the
deadline? Did they mention IFC verification separately from RVT QA/QC?]

─────────────────────────────────────────────────────
CRITERION 3 — Stakeholder and Problem Management: [X/5]

[3–4 sentences. How did they handle the structural RFI? Waiting passively
is a common gap — if they did this, explain why it's a career-limiting
approach: "In a real delivery situation, passive waiting on a 7-day-old RFI
with a hard deadline is a failure to manage. You own the delivery timeline
as BIM Lead — not the structural engineer."]

─────────────────────────────────────────────────────
CRITERION 4 — Documentation Quality: [X/5]

[3–4 sentences. Did they describe what each document contains? Did they
understand that the Clash Resolution Report must reflect the final model
state? Did they understand the BEP Compliance Confirmation is a formal
document, not an email?]

─────────────────────────────────────────────────────
THE MOST IMPORTANT THING I WANT YOU TO TAKE FROM THIS:

[One focused paragraph — the single most important lesson from their
specific response. Do not write a generic lesson. Reference something from
their actual submission and connect it to a real career implication.

For example: "You started rebuilding the federated model on Day 2 before
the QA/QC checks were complete on HVAC and plumbing. I understand why —
you want to know what the federated state looks like early. But doing this
means your final federated model will be based on unchecked discipline
models, which means the final clash report and BEP Compliance Confirmation
will be based on models that haven't been formally approved. In a real
delivery, this is the kind of gap that creates accountability problems when
the MC discovers a model issue after acceptance. The rule is: federated
model is built last, on approved models only."]

─────────────────────────────────────────────────────
WHAT A STRONG RESPONSE LOOKS LIKE (briefly):

• Day-by-day timeline with explicit dependency logic
• QA/QC failure contingency plan (not just "run the checklist")
• Immediate escalation of the 7-day-old structural RFI with a documented
  interim acceptance plan
• Clash Resolution Report prepared after final clash detection (not before)
• IFC verified in Navisworks Freedom before submission (not assumed clean)

Let's talk through this in our next session — I want to hear your thinking
on [specific aspect of their response that is worth a deeper conversation].

— [Mentor Name], LUA BIM LABS
─────────────────────────────────────────────────────
```

---

*LUA BIM LABS | Project Mentor Delivery Simulations — For subscriber use only.*
