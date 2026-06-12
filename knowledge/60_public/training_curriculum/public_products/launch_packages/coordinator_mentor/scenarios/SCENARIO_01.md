# Coordinator Mentor — Scenario Challenge #1
## LUA BIM LABS | Monthly Scenario Challenge
**Topic:** The Impossible Ceiling Zone
**Version:** 1.0

---

## HOW THIS WORKS

Read the scenario below carefully. Then write your response — your approach to solving the problem — and send it to your mentor via Telegram. You have 5 business days from the date this was sent to you.

There is no single correct answer. LUA BIM LABS will evaluate your response based on four criteria explained at the end of this document. You'll receive written feedback within 48 hours of your submission.

Length of your response: 200–500 words. Diagrams, sketches, or tables are welcome but not required.

---

## THE SCENARIO

**Project:** 6-floor private hospital, Southeast Asia
**Location:** Typical patient corridor, Levels 2–5 (identical conditions on each floor)
**Corridor dimensions:** 2,800mm wide × 38m long

**The Constraint:**
Floor-to-ceiling height in this corridor is **2,400mm** (measured from finished floor level to underside of slab above). This is a firm architectural requirement — it cannot be changed. The ceiling height is fixed. The structural slab depth is 250mm. There are no structural beams in this corridor run.

**What Needs to Fit:**

1. **HVAC supply air duct:** 800mm wide × 400mm deep (flat-oval not possible on this project — rectangular only)
2. **Fire sprinkler branch piping:** 50mm nominal pipe diameter, with a minimum 100mm clearance required above the branch pipe for access to the pipe coupling above
3. **Electrical cable tray:** 600mm wide × 100mm deep (hot works prohibited — cannot cut or weld in hospital; the cable tray must be installed in one piece)
4. **False ceiling:** 100mm depth (tile system — this is the minimum; it cannot be reduced)

**The Rules:**
- All services must sit **above** the false ceiling (i.e., within the ceiling plenum)
- Maintenance access must be maintained to all services — specifically: the HVAC duct must have a minimum 150mm access clearance above it to the slab (for filter access and joint inspection), and the cable tray must have a minimum 100mm access clearance above it
- The fire sprinkler branch pipe must be within 200mm of the slab soffit (this is an installer requirement from the fire protection subcontractor — they need to fix the pipe hangers to the slab)
- All services must clear the finished ceiling tile by a minimum of 50mm (tolerance and deflection buffer)

**Available Ceiling Plenum Space:**

Let's calculate what you're working with:

- Floor-to-ceiling height: 2,400mm
- False ceiling depth: 100mm
- Clearance above ceiling: 50mm
- **Total available plenum height from FFL: 2,400 – 100 – 50 = 2,250mm** (ceiling plenum starts at 2,250mm AFF)
- Structural slab soffit: 2,400mm + 250mm slab = **2,650mm AFF** (underside of slab is at 2,650mm AFF)
- **Total available ceiling plenum depth: 2,650 – 2,250 = 400mm**

You have **400mm of usable ceiling plenum** to fit:
- 400mm (HVAC duct depth) + 150mm (duct access above) = **550mm needed for HVAC alone**
- This is already 150mm over budget before any other service is included.

**The Team's Positions:**
- HVAC engineer: "The duct size cannot change. The supply air volume is fixed and the velocity limit cannot be exceeded."
- Electrical engineer: "The cable tray size is fixed. We cannot split it into smaller trays — hot works are prohibited."
- Fire protection subcontractor: "The sprinkler branch must be within 200mm of the slab. This is non-negotiable."
- Architect: "The 2,400mm ceiling height is a clinical requirement. It cannot be reduced."

**Your role:** You are the BIM Coordinator. You are not the engineer for any of these systems. You are responsible for finding a coordination solution that works physically and that the team can agree on.

---

## EVALUATION CRITERIA

LUA BIM LABS will evaluate your response on the following four criteria. Each criterion is scored 1–5.

**Criterion 1: Spatial Analysis Accuracy (1–5)**
Did you correctly understand and quantify the constraint? Did you identify the actual available space and what the shortfall is — rather than just describing the problem generally? A strong response includes clear numbers and shows that you understand *why* this is impossible as currently stated.

| Score | Description |
|-------|-------------|
| 1 | Describes the problem but uses no numbers or calculations |
| 2 | Attempts to quantify but with errors in the calculation |
| 3 | Correct spatial analysis but incomplete (misses one constraint) |
| 4 | Full, accurate spatial analysis with all constraints identified |
| 5 | Full spatial analysis plus identifies which constraint has the most leverage for change |

**Criterion 2: Solution Generation (1–5)**
Did you propose at least 2 viable options or approaches? A solution doesn't have to solve everything — but it must be technically grounded. "Tell the architect to raise the ceiling" is not a solution; it's an escalation. Escalation is sometimes right, but it must be accompanied by technical justification.

| Score | Description |
|-------|-------------|
| 1 | No concrete solution proposed |
| 2 | One option proposed, but not technically justified |
| 3 | One technically sound option with justification |
| 4 | Two or more options with trade-offs identified for each |
| 5 | Two or more options, clearly prioritized, with specific numbers and a recommended path forward |

**Criterion 3: Stakeholder Management Approach (1–5)**
Did you identify who needs to make decisions, and in what order? Coordination is not just a technical problem — it's a people problem. Who do you talk to first, and what do you ask them?

| Score | Description |
|-------|-------------|
| 1 | No mention of stakeholders or decision-making process |
| 2 | Mentions contacting people but no sequence or logic |
| 3 | Identifies the key decision-makers but doesn't explain the escalation path |
| 4 | Clear sequence of contacts with reasoning for the order |
| 5 | Full stakeholder plan including what each party needs to provide, in sequence, with a realistic timeline |

**Criterion 4: Documentation and Escalation (1–5)**
Did you explain how you would document this issue and escalate it appropriately? A BIM Coordinator who finds an impossible constraint and solves it without a paper trail has not fully solved it.

| Score | Description |
|-------|-------------|
| 1 | No mention of documentation |
| 2 | Mentions documentation but doesn't specify what to document |
| 3 | Identifies the need for a Coordination Issue Notice or similar |
| 4 | Describes documentation content and distribution |
| 5 | Full documentation and escalation plan, including who signs off on the accepted solution |

**Maximum score: 20 points**
**Strong response: 15–20 | Adequate response: 10–14 | Developing response: below 10**

---

## SAMPLE STRONG RESPONSE
### [LUA BIM LABS INTERNAL REFERENCE ONLY — DO NOT SEND TO CLIENTS]

---

**Spatial Analysis**

The ceiling plenum is 400mm deep (2,650mm slab soffit – 2,250mm top of plenum zone). The total service stack depth required, if all services are stacked vertically, is:

- HVAC duct: 400mm deep
- HVAC access clearance above duct: 150mm
- Total for HVAC alone: 550mm

This exceeds the available 400mm by 150mm — even before placing the sprinkler pipe or cable tray. The spatial problem is severe and cannot be resolved by small adjustments. One of the "fixed" constraints must be re-examined.

**Solution Options**

*Option 1 — Challenge the HVAC duct size*

The HVAC engineer states the duct cannot change because the supply air volume and velocity limit are fixed. However, velocity limits apply to rectangular ducts in occupied zones. In ceiling plenums above false ceilings in hospital corridors, a slightly higher velocity may be acceptable — particularly for a short 38m run. Request the HVAC engineer to recalculate with a velocity up to 6.0 m/s (from a typical 5.0 m/s). At 6.0 m/s, the same volume may be achievable with a 700×350mm duct — saving 100mm in depth. This does not fully solve the 150mm shortfall but reduces it significantly.

Additionally, raise the question of a flat-oval duct alternative: the engineer stated this is "not possible on this project" — but this constraint should be verified in writing. If the prohibition is a preference rather than a specification requirement, it should be challenged through formal RFI.

*Option 2 — Offset routing*

Not all four services need to occupy the same cross-section of the corridor for the full 38m. If the corridor has zones with different ceiling-zone contents, a staggered routing approach can be used: the HVAC duct runs on one side of the corridor (closer to the wall), the cable tray runs on the other side, and the sprinkler branch runs centrally near the slab. This does not eliminate the stacking problem but allows each service to use the full 400mm zone independently rather than sharing it.

This requires a corridor section drawing with all services shown at key cross-sections — not just the worst-case cross-section.

*Option 3 — Formal escalation with quantified options*

If neither Option 1 nor Option 2 provides a viable technical solution, the issue must be escalated to the design team as a Coordination Design Issue (CDI). The escalation document must include: (1) the calculated shortfall with all constraints listed, (2) the options investigated and their outcomes, (3) a formal request for a design team meeting within 5 business days. The escalation should be addressed to the lead MEP consultant and the project manager.

**Stakeholder Sequence**

1. HVAC engineer first — they control the largest service and potentially have the most flexibility (velocity recalculation, RFI on flat-oval).
2. Architect second — present the spatial analysis. Ask: "Is the 2,400mm ceiling height a clinical standard requirement or a design target? Who specified it, and what document does it appear in?"
3. Fire protection subcontractor — verify that "within 200mm of slab" is their installation requirement, not a code requirement. If it is a code requirement, ask which code clause so the team can review.
4. Project manager — brief before the design team meeting. Do not let them be surprised.

**Documentation**

Issue a Coordination Issue Notice (CIN-001) to all parties within 24 hours of identifying the impossibility. The notice includes: the location, the spatial analysis, the services involved, the shortfall in millimetres, and the options under investigation. Log in the Issue Log Master as PRJ-ISS-[number], Priority = Critical.

After the design team meeting: document the agreed solution in a Coordination Resolution Notice signed off by the lead MEP consultant and distributed to all parties.

---

## SAMPLE FEEDBACK STRUCTURE
### [LUA BIM LABS INTERNAL — How to structure the feedback message to the client]

Send feedback via Telegram within 48 hours of the client's submission. Structure:

```
─────────────────────────────────────────────
SCENARIO CHALLENGE FEEDBACK
Coordinator Mentor | [Client Name]
Scenario #1: The Impossible Ceiling Zone
─────────────────────────────────────────────

YOUR SCORE: [X] / 20

CRITERION 1 — Spatial Analysis: [X/5]
[2–3 sentences of specific feedback on what they did well and what was missing or incorrect in their spatial calculation]

CRITERION 2 — Solution Generation: [X/5]
[2–3 sentences on the quality and number of solutions proposed. Reference specific numbers if they used them well or incorrectly]

CRITERION 3 — Stakeholder Management: [X/5]
[2–3 sentences on whether they identified the right people in the right order. If they jumped straight to escalation without technical analysis, note this]

CRITERION 4 — Documentation: [X/5]
[2–3 sentences on whether they addressed documentation. Many candidates skip this — if they did, note it directly]

─────────────────────────────────────────────
KEY INSIGHT FOR YOU:

[One paragraph — the most important lesson from their response. Be direct and specific. Do not soften a genuine gap. Do not over-praise a generic response. This paragraph should be something they can apply on a real project next week.]

─────────────────────────────────────────────
WHAT A STRONG RESPONSE LOOKS LIKE:

[Briefly describe — in 3–4 bullet points — the key elements of a strong response that they may have missed. This is not a criticism; it's the learning.]

Overall: [1–2 sentences of genuine, specific encouragement or forward momentum]

— [Mentor Name], LUA BIM LABS
─────────────────────────────────────────────
```

---

*LUA BIM LABS | Coordinator Mentor Scenario Challenges — For subscriber use only.*
