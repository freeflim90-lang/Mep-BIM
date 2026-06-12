# Starter Plan Lesson Quality Standard

## Purpose

Starter Plan lessons must feel more polished than internal year-based training messages.

Internal career-year education can guide the long-term sequence, but paid product lessons must provide clear daily value, practical judgment, and a small action item in every message.

## Lesson Promise

Each Starter lesson should help a beginner or early-stage BIM learner understand one practical MEP BIM issue and know what to check next.

## Standard Lesson Structure

Use this structure for every paid Starter lesson:

```text
LUA BIM LABS Starter
Day N - Topic

1. Why This Matters
Explain the practical coordination, modeling, or site consequence.

2. Core Concept
Define the concept in beginner-friendly language.

3. Real Project Lens
Describe a realistic situation without using confidential project details.

4. BIM Check
Give 3 practical checks the learner can apply.

5. Common Mistake
Name one mistake beginners often make.

6. Today's Action
Give one small task, reflection, or checklist item.

Scope note:
This is general educational content, not project review, engineering verification, code compliance confirmation, or construction approval.
```

## Quality Checklist

A paid Starter lesson should pass all checks:

- One focused topic only
- MEP BIM relevance is obvious
- Beginner can understand it without project files
- Includes practical coordination consequence
- Includes at least three check items
- Includes one common mistake
- Includes one small action
- Avoids confidential, legal, code, approval, or design verification claims
- Avoids vague motivation-only writing
- Avoids repeated generic paragraphs

## Tone

Use a calm, professional, practical tone.

Prefer:

- "Check"
- "Review"
- "Confirm"
- "Compare"
- "Record"

Avoid:

- Overpromising expertise
- Claiming certification or approval outcomes
- Saying that a lesson replaces professional engineering judgment

## Difference From Internal Career-Year Training

Internal career-year curriculum:

- Can include company standards
- Can use Korean internal language
- Can focus on employee growth and discipline

Starter paid lessons:

- Must be public-safe
- Must be client-facing
- Must be in English by default
- Must have clear daily value
- Must reinforce service scope

## Starter Launch Curriculum

The first productized Starter launch runs as a 30-day customer-facing curriculum.

The curriculum is stored here:

```text
data/starter_plan/starter_plan_curriculum.json
data/starter_plan/messages/day_001.txt ... day_030.txt
```

Recommended 30-day launch structure:

1. MEP BIM orientation
2. Revit MEP basics
3. HVAC, piping, electrical, fire protection, and plumbing coordination
4. Drawing and system reading
5. Model quality basics
6. Clash and clearance thinking
7. Data and schedule basics
8. Site-readiness thinking
9. BIM reporting and professional habits
10. Monthly review and next learning direction

## Product Ladder Connection

Starter should create demand for deeper products without overpromising.

- Starter identifies topic interest and beginner gaps.
- Personal Tutor can later use those gaps for level diagnosis and personalized learning paths.
- Coordinator Mentor can later use repeated coordination issues for deeper clash, QA, and workflow mentoring.
- Project Mentor should remain separate because project-specific material has higher confidentiality and responsibility risk.
