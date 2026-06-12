# Coordinator Mentor — Case Studies
## LUA BIM LABS | Monthly Case Studies for Coordinator Mentor Subscribers
**Version:** 1.0 | For distribution to Coordinator Mentor clients

---

## Case Study 1: The Uncoordinated Electrical Subcontractor

Month 1 | Case #1

---

### PROJECT BACKGROUND

A 32-story mixed-use tower in Southeast Asia is in the construction document coordination stage. The project uses Autodesk Navisworks for clash detection and BIM 360 for model sharing. The MEP coordination team consists of a BIM Coordinator (you), a mechanical designer, an electrical subcontractor, a plumbing subcontractor, and a fire protection subcontractor. The coordination program is 8 weeks long before the first major model submission to the main contractor.

---

### THE SITUATION

It is Week 4 of the 8-week coordination program. You run the latest federated clash detection after the electrical subcontractor (Elec-Sub) submits their revised model. The results are significantly worse than the Week 3 run:

- **Total clashes detected:** 847
- **Hard clashes:** 203 (up from 58 in Week 3)
- **New electrical clashes this week:** 189 (most of the increase)
- **Most affected area:** Levels 10–22, the main MEP corridor zone

On investigation, you discover that Elec-Sub has routed their cable trays, conduits, and panel riser shafts through zones that were explicitly reserved for HVAC in the MEP zoning plan issued at the project start.

You contact the Elec-Sub BIM coordinator. Their response: *"We never received the MEP zoning plan. No one told us about it."*

You search your email and BIM 360 audit log. The zoning plan was uploaded to BIM 360 at Week 1 and an email notification was sent to all team members including the Elec-Sub project manager — but not their BIM coordinator specifically. The Elec-Sub project manager is now on leave.

You have a coordination meeting in 3 days. The main contractor's project director will attend this meeting expecting a progress update.

---

### KEY QUESTIONS TO CONSIDER

1. Was the zoning plan properly communicated? Who bears responsibility for the breakdown in communication, and how does this change your approach?

2. What do you do in the next 24 hours to contain the damage before the meeting in 3 days?

3. How do you present this situation to the main contractor's project director — and what do you need to have ready before that meeting?

---

### ANALYSIS AND RECOMMENDED APPROACH

**Immediate Priority Assessment**

The first instinct of many coordinators in this situation is to spend 24 hours building a case to prove that the electrical subcontractor is at fault. This instinct — while understandable — is wrong. Blame assignment is a legal and contractual matter, not a coordination matter. Your job in the next 72 hours is to minimize the impact on the project program. The accountability discussion must happen, but separately.

**Step 1 — Verify the communication chain (first 2 hours)**

Before anything else, establish the facts objectively. Pull the BIM 360 audit log and confirm the upload date of the zoning plan. Pull the email records and confirm who received notification. Document that the Elec-Sub BIM coordinator's email was not on the distribution list. This is not about protecting yourself — it is about understanding the real gap so you can prevent it from happening again.

Key finding: a critical project document was distributed to the project manager but not to the technical person who needed to act on it. This is a process failure, not a malicious act. Recognizing this distinction prevents the situation from becoming adversarial.

**Step 2 — Contact the electrical subcontractor immediately (hours 2–4)**

Call the Elec-Sub BIM coordinator directly. Not email — phone or video call. The message is collaborative, not accusatory: "I've found the issue. The zoning plan wasn't in your hands at the working level. That's a gap in the process. I want to work through this with you directly. Can we have a call today to look at the worst clashes and understand what's possible to reroute?"

This call has two goals: (1) establish a working relationship with the technical person who can actually solve the problem, and (2) get a realistic assessment of what can be changed and in how long. Request that they prioritize the 203 hard clashes, specifically any that are in the main mechanical corridor on Levels 10–22.

**Step 3 — Quantify the recovery timeline (hours 4–8)**

With the information from the Elec-Sub call, create a recovery plan. This plan does not need to be perfect — it needs to be credible and specific. For example:
- Clashes with Priority Score ≥ 15 (critical zone conflicts): can be rerouted in 5 business days
- Clashes with Priority Score 8–14 (moderate conflicts): can be rerouted in 10 business days
- Clashes with Priority Score < 8: can be addressed in Week 6–7

Document these numbers in a recovery matrix. This is what you take into the coordination meeting.

**Step 4 — Coordinate the meeting agenda proactively**

Send the meeting chairperson (or the project manager) a heads-up before the meeting: "I want to flag that we have a coordination issue to discuss at Wednesday's meeting. I'll be presenting the situation, the root cause, and the recovery plan. I want to make sure we have 15 minutes on the agenda for this." This gives the project director context and prevents a blindside reaction in the room.

**The Meeting Itself**

Present the situation in four parts: what happened, why it happened, what has been done since, and the recovery plan. Lead with the recovery plan — not with the problem. Coordinators who walk into meetings with problems get defensive. Coordinators who walk in with plans get credibility.

**Documentation**

Issue a written coordination notice (via BIM 360 or email) to all parties after the meeting confirming: the zoning plan reference, the distribution confirmation date, the gap identified, the corrective action agreed, and the revised schedule. This is not legal documentation — it is project documentation. It protects everyone and keeps the record clear.

**Key Lesson on Communication Gaps**

This situation reveals a systemic risk that exists on almost every project: critical BIM coordination documents are distributed to project managers, not to the BIM operators who need to act on them. As a BIM Coordinator, it is part of your role to verify that the technical team on each subcontractor has received and acknowledged key coordination documents — not just that the documents were sent. A simple confirmation email to each BIM operator ("Can you confirm you have received and reviewed the MEP Zoning Plan Rev A?") at the start of a coordination program takes 10 minutes and prevents this scenario.

---

### KEY LESSONS

1. **Communication confirmation is the coordinator's responsibility, not just the PM's.** Ensure that key coordination documents are acknowledged by the technical person who will act on them — not just the person who manages the contract.

2. **Lead with the recovery plan, not the problem.** In coordination meetings — especially with senior stakeholders — the credibility you need comes from demonstrating that you have a plan, not from demonstrating that someone else made a mistake.

3. **Collaboration before accountability.** In the short term, the project needs the clashes resolved — not a dispute. Work collaboratively to fix the problem first. Document the root cause clearly. Let the contractual accountability discussion happen at the right level, with the right people, after the immediate crisis is contained.

---

## Case Study 2: The Structural Beam Surprise

Month 2 | Case #2

---

### PROJECT BACKGROUND

A commercial office tower project (26 floors, 62,000 m² gross floor area) is in the construction document coordination stage, Week 9 of a planned 12-week coordination program. The project uses Navisworks for clash detection and ACC BIM 360 for model management. The coordination team has been working well — a rhythm of weekly clash runs and biweekly coordination meetings has kept the program on track. As of last week's report, 412 of the original 580 identified clashes were resolved or accepted, leaving 168 active clashes — all within manageable range.

---

### THE SITUATION

On Monday morning of Week 9, you receive a structural revision package via BIM 360. The structural engineer has issued a revised structural model (Rev D) and a design change notice. The change: **beam depths on Levels 12, 13, and 14 have been increased from 500mm to 650mm** to address a load transfer requirement identified by the structural engineer late in the design process.

The increase of 150mm applies to all secondary beams on those three floors — approximately 180 beams in total, spread across the entire floorplate.

You run an immediate clash test: **340 previously resolved clashes are now reactivated** across HVAC (largest impact — duct routing now conflicts with deeper beams), fire protection (sprinkler drops and branch pipes), and electrical (cable tray routes and conduit runs). 67 of those reactivated clashes were previously assessed as critical.

You have a client progress meeting on Friday (5 days away) where you were planning to report that coordination was on track for completion in 3 weeks. That timeline is now impossible without a program extension.

You also have a practical issue: the HVAC subcontractor's BIM modeler is fully booked on another project this week. Electrical can respond but is 2 time zones away with limited overlap hours.

---

### KEY QUESTIONS TO CONSIDER

1. Before contacting anyone, what do you need to understand about the structural change in order to manage it?

2. How do you communicate the impact of this change to the project manager and client — and what information do they need from you by Friday?

3. What coordination triage strategy do you apply when 340 previously resolved clashes are suddenly active again?

---

### ANALYSIS AND RECOMMENDED APPROACH

**Understanding the Change Before Reacting**

The most dangerous response to a large structural revision is to immediately forward it to all subcontractors with a message like "please update your models." This creates chaos without direction. Before communicating the change to the team, you need to understand it yourself.

Spend the first 2–3 hours answering three questions by reviewing the structural drawings and running preliminary analysis in Navisworks:

1. Which specific grids and levels are affected? (Not all beams everywhere — only secondary beams on L12, L13, L14)
2. What is the new underside of beam elevation at the affected locations? (500mm → 650mm means the underside drops 150mm — from, for example, 2,900mm AFF to 2,750mm AFF)
3. Which MEP systems were routed in the zone between the old and new underside elevations? These are the reactivated clashes.

This analysis takes a few hours but changes your communication from "we have 340 new clashes" (panic message) to "the structural change affects Levels 12–14. In those zones, the available ceiling zone has decreased by 150mm. Based on my initial review, 67 critical clashes require redesign of the HVAC main duct routing; the remaining 273 reactivated clashes are predominantly secondary systems that can be rerouted with minor adjustments."

The difference between those two messages is the difference between a coordinator who creates alarm and one who manages it.

**Triage: Three Tiers of Response**

Not all 340 reactivated clashes are equal. Create a triage classification immediately:

**Tier 1 — Requires Design Decision (estimate: ~40–60 clashes):** HVAC main duct routes that cannot be rerouted without changing duct sizing or adding new duct shafts. These require input from the MEP design engineer, not just the BIM modeler. Flag these immediately, escalate to the lead engineer, and do not allow modeling work to begin on these until the design decision is made.

**Tier 2 — Requires Coordination Rerouting (estimate: ~150–180 clashes):** Clashes that can be resolved by adjusting routes within the existing system design — lowering conduit runs, adjusting cable tray elevations, rerouting sprinkler branches below the new beam depth. These can be done by the BIM modelers working to the new structural model.

**Tier 3 — Minor Adjustments or Accept (estimate: ~80–100 clashes):** Soft clashes or near-misses that were previously borderline. Review these last. Many may be acceptably resolved with a documented tolerance.

**Resource Constraints**

The HVAC modeler being unavailable this week is a real constraint. Address it directly with the HVAC subcontractor's project manager — not their modeler. Explain the structural revision, the impact, and the 5-day window before the client meeting. Ask: "What can be done this week to at least resolve the Tier 1 design questions?" A good project manager will find a way. Document the response.

**Client Meeting on Friday**

You cannot walk into Friday's meeting and report that coordination is on track. You must report the structural revision impact accurately and present a revised program. Prepare the following for the meeting:

1. A written impact summary: what changed, when it was issued, how many previously resolved clashes are affected, and which floor levels are affected.
2. A revised coordination schedule showing the new realistic completion date. Be conservative — do not promise a date you cannot deliver.
3. A responsibility note: this change was issued by the structural engineer in Week 9 of a 12-week program. The cost and program impact are a structural design change issue, not a coordination team failure. This should be clearly documented and the project manager should be briefed on this point before Friday.

**The Broader Lesson on Structural Revisions**

Structural revisions mid-coordination are one of the most common causes of coordination program overruns. The root cause is almost never the structural engineer being careless — it is that structural design changes, especially for load transfer and transfer plate adjustments, are sometimes not finalized until late in the process. The BIM coordinator's role is to monitor for this risk proactively. At every coordination meeting, the question should be: "Are there any structural changes anticipated in the next two weeks?" This does not prevent the change — but it can give 1–2 weeks of early warning, which significantly reduces the impact.

**Documentation After the Revision**

Issue a formal Coordination Impact Notice to all subcontractors within 24 hours of identifying the reactivated clashes. This notice should state: the structural revision reference, the date it was issued, the number of reactivated clashes by discipline, the triage classification, and the revised target dates by tier. This document is the paper trail that protects the coordination team if there are later claims about program delays.

---

### KEY LESSONS

1. **Translate impact before communicating it.** When a major change hits, invest time in understanding it fully before sending any messages to the team. A coordinator who communicates "340 clashes reactivated" without context creates panic. One who communicates "here's the three-tier impact, here's the revised plan" creates confidence.

2. **Triage is the coordinator's most valuable skill in a crisis.** Not all 340 reactivated clashes can or should be addressed at once. The ability to quickly classify clashes by complexity and dependency (Tier 1 / 2 / 3) allows the team to use limited resources on the right problems first.

3. **Late structural changes are a risk to monitor, not a surprise to absorb.** Asking "are any structural changes coming?" at every coordination meeting is not paranoia — it is professional risk management. Build this question into your standard meeting agenda. Early warning of structural revisions, even rough warning, allows the coordination team to plan rather than react.

---

*LUA BIM LABS | Coordinator Mentor Case Studies — For subscriber use only. Do not redistribute.*
