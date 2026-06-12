#!/usr/bin/env python3
"""Generate productized Starter Plan curriculum and daily Telegram lessons."""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys  # noqa: E402
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import STARTER_PLAN_DIR  # noqa: E402

STARTER_DIR = STARTER_PLAN_DIR
MESSAGES_DIR = STARTER_DIR / "messages"
CURRICULUM_FILE = STARTER_DIR / "starter_plan_curriculum.json"
OBSIDIAN_INDEX = (
    PROJECT_ROOT
    / "obsidian_vaults"
    / "lua_bim_lab_global_map"
    / "NAS_Knowledge"
    / "Product_Knowledge"
    / "Starter"
    / "Starter Plan - 30 Day Launch Curriculum.md"
)

SCOPE_NOTE = (
    "This is general educational content, not project review, engineering verification, "
    "code compliance confirmation, or construction approval."
)

LESSONS = [
    {
        "day": 1,
        "phase": "MEP BIM orientation",
        "topic": "What MEP BIM Coordination Really Means",
        "why": "MEP BIM is not only about drawing ducts, pipes, trays, or equipment in 3D. The real value is helping a project team see whether systems can be installed, accessed, maintained, and coordinated before site work becomes expensive.",
        "core": "MEP BIM coordination means checking how mechanical, electrical, plumbing, fire protection, architecture, and structure affect each other inside the same project space.",
        "lens": "A duct route may look clean in plan view, but it can still block a valve, conflict with a cable tray, reduce ceiling space, or leave no room for insulation and maintenance access.",
        "checks": ["Check whether the element has enough physical clearance.", "Check whether access is still possible after installation.", "Check whether the model data matches the intended system and discipline."],
        "mistake": "Beginners often think no clash means ready for construction. In real coordination, clearance, access, sequence, and maintainability matter too.",
        "action": "Open any MEP model or sample drawing and choose one crowded ceiling area. Write down three things that could become a coordination issue even if there is no hard clash.",
    },
    {
        "day": 2,
        "phase": "Revit MEP basics",
        "topic": "Why System Names Matter in Revit MEP",
        "why": "System names affect visibility, filtering, schedules, clash grouping, and team communication. A model can look correct geometrically but still create confusion if systems are named incorrectly.",
        "core": "In Revit MEP, a system is a logical grouping of connected elements such as supply air, return air, chilled water, sanitary, fire protection, power, or communication.",
        "lens": "If a chilled water return pipe is assigned to the wrong system, it may appear in the wrong schedule, clash group, or color filter. This makes QA and coordination slower.",
        "checks": ["Review the system name of a selected duct, pipe, tray, or equipment item.", "Compare the system name with the drawing legend or project naming rule.", "Check whether filters and schedules rely on that system value."],
        "mistake": "Beginners often focus only on size and location, then forget that incorrect system data can damage downstream coordination.",
        "action": "Pick five MEP elements in a sample model. Record category, system name, size, and level for each one.",
    },
    {
        "day": 3,
        "phase": "Coordination basics",
        "topic": "Clearance Is Not the Same as Clash",
        "why": "Many beginners learn clash detection first, but real MEP coordination also depends on clearance. An element can avoid touching another element and still be impossible to install or maintain.",
        "core": "A hard clash means two modeled objects overlap. Clearance means the usable space around an object is enough for insulation, hangers, access panels, valves, maintenance, and installation sequence.",
        "lens": "A pipe may not clash with a tray, but if there is no space to install insulation or operate a valve handle, the routing still needs review.",
        "checks": ["Check modeled object size and real installed size.", "Include insulation, flange, valve handle, support, and access space.", "Review crowded areas in section view, not only in plan view."],
        "mistake": "Beginners often export clash reports and assume all important problems are captured. Clearance problems often require human judgment and project rules.",
        "action": "Choose one pipe, duct, or cable tray route. Describe the extra space needed around it for installation and maintenance.",
    },
    {
        "day": 4,
        "phase": "Drawing literacy",
        "topic": "Reading MEP Drawings Before Modeling",
        "why": "Modeling without reading the drawings first often creates rework. BIM modelers need to understand system intent before placing elements in Revit.",
        "core": "MEP drawings communicate system type, route, size, elevation, equipment connection, flow direction, control intent, and installation constraints.",
        "lens": "A pipe route may be drawn simply in plan view, but the riser diagram, equipment schedule, and section detail may reveal the correct connection or elevation.",
        "checks": ["Read the plan, section, riser, and schedule together.", "Confirm system abbreviation and drawing legend.", "Check whether equipment connections match the modeled route."],
        "mistake": "Beginners often model from one plan view only, missing elevation, slope, system connection, and equipment relationship.",
        "action": "Take one MEP drawing sheet and identify three pieces of information that cannot be fully understood from plan view alone.",
    },
    {
        "day": 5,
        "phase": "Model QA basics",
        "topic": "The Beginner's Model QA Mindset",
        "why": "Model QA is not a final inspection at the end. It is a daily habit that keeps the model useful for coordination, reporting, and construction discussion.",
        "core": "Model QA means checking whether geometry, data, view settings, naming, systems, levels, and coordination assumptions are consistent enough for the next person to trust the model.",
        "lens": "A model may look acceptable in 3D, but missing levels, wrong worksets, inconsistent names, or empty parameters can make schedules and exports unreliable.",
        "checks": ["Check geometry: location, size, elevation, and connection.", "Check data: system name, type, level, and key parameters.", "Check coordination: view filters, worksets, links, and shared coordinates."],
        "mistake": "Beginners often treat QA as someone else's job. Strong BIM teams expect every modeler to perform small QA checks before sharing work.",
        "action": "Create a three-column checklist: Geometry, Data, Coordination. Add three checks under each column.",
    },
    {
        "day": 6,
        "phase": "HVAC BIM",
        "topic": "Supply Air, Return Air, Exhaust Air, and Outdoor Air",
        "why": "Air systems drive ceiling coordination, equipment connection, fire damper placement, and balancing discussions. Misunderstanding the air system can lead to wrong routes and wrong clash priorities.",
        "core": "SA, RA, EA, and OA represent different air purposes. Each system has different routing logic, pressure relationships, equipment connections, and coordination risks.",
        "lens": "A return air duct near a supply air duct may look similar in the model, but its connection, insulation, grille relationship, and balancing intent can be different.",
        "checks": ["Confirm the system abbreviation in the drawing legend.", "Check whether duct route and terminal connection match the system.", "Review whether color filters clearly separate air systems."],
        "mistake": "Beginners often model ducts by shape and size only, without understanding what the air system is doing.",
        "action": "List four air systems and write one coordination concern for each.",
    },
    {
        "day": 7,
        "phase": "Piping BIM",
        "topic": "Supply and Return Piping Logic",
        "why": "Piping systems are not just lines. Supply and return logic affects equipment connection, valve location, flow direction, insulation, and maintenance access.",
        "core": "Supply piping delivers fluid to equipment or terminals; return piping brings it back. Correct separation helps the team understand system performance and coordination sequence.",
        "lens": "In a mechanical room, chilled water supply and return pipes may run close together. If the model does not clearly separate them, schedules and review comments become confusing.",
        "checks": ["Confirm flow direction and equipment connection.", "Check supply and return naming consistency.", "Review valve and strainer access on both sides of equipment."],
        "mistake": "Beginners often copy pipe routes without checking whether the connection is supply or return.",
        "action": "Sketch one simple supply-return loop and mark equipment, valves, and flow direction.",
    },
    {
        "day": 8,
        "phase": "Electrical BIM",
        "topic": "Cable Tray Coordination Basics",
        "why": "Cable trays occupy large ceiling space and need bend radius, access, separation, and support space. They can become major coordination drivers in corridors and plant rooms.",
        "core": "Cable tray BIM coordination checks not only the tray body but also installation access, branching space, vertical drops, and separation from wet systems or heat sources.",
        "lens": "A tray route may pass a hard clash test but still block access to dampers, valves, or ceiling panels if the corridor is crowded.",
        "checks": ["Review tray width, bend area, and drop points.", "Check separation from piping and mechanical equipment.", "Confirm access below and beside the tray route."],
        "mistake": "Beginners often model tray centerlines but forget the real width and bend space.",
        "action": "Choose one tray route and identify where a bend, drop, or access issue could happen.",
    },
    {
        "day": 9,
        "phase": "Fire protection BIM",
        "topic": "Sprinkler Coordination Is More Than Head Layout",
        "why": "Sprinkler modeling affects ceiling devices, branch pipes, structural coordination, and maintenance access. It also interacts heavily with architectural ceiling plans.",
        "core": "A sprinkler layout should be reviewed with ceiling grids, lights, diffusers, detectors, beams, branch pipe routes, and access requirements in mind.",
        "lens": "A sprinkler head may be positioned correctly in plan but still conflict with a ceiling device, beam zone, or branch pipe routing constraint.",
        "checks": ["Compare sprinkler heads with ceiling device layout.", "Review branch pipe route and support space.", "Check coordination with beams and ceiling zones."],
        "mistake": "Beginners often place heads first and think the system is complete before reviewing branch pipe routing.",
        "action": "Take a small ceiling area and list every ceiling device that must coordinate with sprinkler heads.",
    },
    {
        "day": 10,
        "phase": "Sanitary and plumbing BIM",
        "topic": "Why Drainage Slope Changes Coordination",
        "why": "Drainage systems need slope, and slope changes vertical space. A route that looks possible in plan can fail when elevation and fall are considered.",
        "core": "Drainage slope means the pipe elevation changes along its route. BIM coordination must account for start elevation, end elevation, pipe size, fittings, and ceiling space.",
        "lens": "A long horizontal drain may begin above the ceiling but gradually drop into a conflict zone near beams, ductwork, or cable trays.",
        "checks": ["Confirm slope direction and slope value.", "Review start and end elevations.", "Check the route in section view along the pipe run."],
        "mistake": "Beginners often model drainage as flat piping, then discover elevation conflicts later.",
        "action": "Pick one drainage route and calculate whether the end elevation will be lower than the start elevation.",
    },
    {
        "day": 11,
        "phase": "Revit workflow",
        "topic": "Levels, Views, and Why They Affect MEP Modeling",
        "why": "MEP elements depend on level, offset, view range, and discipline views. Wrong level logic can make elements appear missing or incorrectly scheduled.",
        "core": "Levels define vertical reference. Views control what you see. Offsets position elements relative to levels. All three affect modeling confidence.",
        "lens": "A duct may exist in the model but appear missing because the view range or discipline setting hides it. This can cause false QA comments.",
        "checks": ["Check element level and offset.", "Review view range and discipline settings.", "Confirm whether the element appears in section and 3D views."],
        "mistake": "Beginners often assume hidden means deleted, when it may be a view setting issue.",
        "action": "Select one MEP element and record its level, offset, and visibility in plan, section, and 3D.",
    },
    {
        "day": 12,
        "phase": "Revit workflow",
        "topic": "Families, Types, and Instances",
        "why": "Understanding families, types, and instances helps beginners edit the right thing without damaging many elements accidentally.",
        "core": "A family defines the object category and behavior, a type defines shared properties, and an instance is one placed object in the model.",
        "lens": "Changing a type parameter may update many diffusers or valves at once. Changing an instance parameter affects only one placed element.",
        "checks": ["Identify whether a property is type-based or instance-based.", "Check how many elements use the same type.", "Duplicate a type before making risky changes."],
        "mistake": "Beginners often edit type properties when they only meant to change one element.",
        "action": "Select one MEP family and identify three type parameters and three instance parameters.",
    },
    {
        "day": 13,
        "phase": "Coordination workflow",
        "topic": "Using Sections to Understand Congested Areas",
        "why": "Plan view can hide vertical conflicts. Sections reveal elevation, clearance, support space, and installation sequence more clearly.",
        "core": "A section is a vertical slice through the model. It helps you understand how elements stack above ceilings, inside shafts, and around equipment.",
        "lens": "A corridor may look organized in plan but show stacked ducts, trays, pipes, and beams competing for the same vertical space in section.",
        "checks": ["Cut sections through congested areas.", "Review top and bottom elevations of major systems.", "Compare model clearance with required installation space."],
        "mistake": "Beginners often review coordination only in plan and 3D, skipping the most useful section views.",
        "action": "Create or imagine one section through a crowded ceiling zone and list the systems from top to bottom.",
    },
    {
        "day": 14,
        "phase": "Navisworks basics",
        "topic": "Clash Results Need Classification",
        "why": "A clash report with hundreds of items is not useful until the issues are grouped and prioritized. Classification turns noise into action.",
        "core": "Clash classification means sorting results by system, location, severity, repetition, responsible discipline, and practical impact.",
        "lens": "Ten clashes from the same repeated pipe sleeve issue may require one modeling rule, while one critical plant room clash may need a coordination decision.",
        "checks": ["Group repeated clashes before assigning actions.", "Separate hard clashes from clearance concerns.", "Prioritize issues that block installation or access."],
        "mistake": "Beginners often count clash quantity instead of judging clash importance.",
        "action": "Look at a sample clash list and create three groups: critical, repeated, and low-priority.",
    },
    {
        "day": 15,
        "phase": "Midpoint review",
        "topic": "The First 15-Day MEP BIM Review",
        "why": "Learning becomes stronger when concepts are connected. The first two weeks should build a basic mental model of systems, views, clearance, data, and QA.",
        "core": "MEP BIM skill is a combination of drawing reading, model operation, system understanding, and coordination judgment.",
        "lens": "A beginner who understands only Revit commands may model quickly but still miss drawing intent, access problems, and wrong system data.",
        "checks": ["Review one HVAC concept, one piping concept, and one coordination concept.", "Identify one Revit setting that affects visibility.", "Name one QA check you can perform before sharing work."],
        "mistake": "Beginners often collect isolated tips without building a repeatable checking routine.",
        "action": "Write a 10-line personal MEP BIM checklist based on Days 1-14.",
    },
    {
        "day": 16,
        "phase": "Model data",
        "topic": "Parameters Are Coordination Data",
        "why": "Parameters are not just optional text fields. They support schedules, filters, QA, exports, reports, and automation.",
        "core": "A parameter stores information about an element, such as system name, size, level, type, manufacturer, flow, or installation zone.",
        "lens": "If equipment data is missing, a schedule may look incomplete even though the 3D model looks finished.",
        "checks": ["Review which parameters are required for schedules.", "Check whether filters depend on parameter values.", "Look for empty or inconsistent values in key fields."],
        "mistake": "Beginners often focus on geometry and leave data cleanup for later, making later QA harder.",
        "action": "Choose one element category and list five parameters that would matter for coordination or reporting.",
    },
    {
        "day": 17,
        "phase": "Model data",
        "topic": "Schedules as a QA Tool",
        "why": "Schedules are not only for quantity takeoff. They can reveal missing data, inconsistent types, wrong levels, and unexpected system values.",
        "core": "A Revit schedule is a structured view of model data. It helps you review many elements faster than selecting them one by one.",
        "lens": "A schedule can quickly show that some diffusers have no system name or that equipment is assigned to the wrong level.",
        "checks": ["Sort schedules by system, level, and type.", "Look for blank values in important columns.", "Use schedules to find outliers before sharing the model."],
        "mistake": "Beginners often treat schedules as output only, not as a daily model checking tool.",
        "action": "Create a sample schedule idea for one category and decide which columns would help QA.",
    },
    {
        "day": 18,
        "phase": "Shared coordinates",
        "topic": "Why Coordinates Matter Before Clash Review",
        "why": "If linked models are not aligned, clash results become unreliable. Coordination begins with confirming model position, not with running clash tests.",
        "core": "Coordinates define where each model sits in the shared project space. Architecture, structure, and MEP must use the same reference strategy.",
        "lens": "A perfectly modeled duct can appear to clash everywhere if the MEP model is shifted relative to the architectural model.",
        "checks": ["Confirm model origin and shared coordinate strategy.", "Check levels and grids across linked models.", "Review one known reference point in 3D before clash testing."],
        "mistake": "Beginners often start clash detection before confirming whether the models are aligned.",
        "action": "Write down three alignment checks you would perform before a coordination review.",
    },
    {
        "day": 19,
        "phase": "Worksets and collaboration",
        "topic": "Worksets and Model Sharing Discipline",
        "why": "Worksets affect visibility, ownership, performance, and collaboration. Poor workset habits can slow down the whole BIM team.",
        "core": "A workset is a collaboration container in a Revit workshared model. It helps control who works on what and how linked or internal elements are organized.",
        "lens": "If MEP elements are placed on the wrong workset, they may disappear in views, export incorrectly, or confuse coordination filters.",
        "checks": ["Check the active workset before modeling.", "Review whether linked models and MEP elements are on expected worksets.", "Use worksets carefully with view templates and exports."],
        "mistake": "Beginners often ignore the active workset and create cleanup work for others.",
        "action": "List the workset types you would expect in a simple MEP coordination model.",
    },
    {
        "day": 20,
        "phase": "Issue management",
        "topic": "Writing Clear BIM Coordination Issues",
        "why": "A coordination issue is useful only when another person can understand the problem, location, impact, and expected action.",
        "core": "A good issue note includes location, involved systems, problem type, practical impact, proposed action, and owner.",
        "lens": "Saying pipe clash is weak. Saying CHW pipe conflicts with cable tray at Level 03 corridor grid B-4 and blocks tray access is much more useful.",
        "checks": ["State the location clearly.", "Name the involved systems and disciplines.", "Describe the impact and next action."],
        "mistake": "Beginners often write issue notes that describe what they see but not what needs to happen next.",
        "action": "Rewrite a vague issue into a clear coordination issue using location, systems, impact, and action.",
    },
    {
        "day": 21,
        "phase": "Site-readiness thinking",
        "topic": "Installability as a BIM Thinking Habit",
        "why": "A model is more valuable when it helps the team understand whether work can actually be installed on site.",
        "core": "Installability means checking whether routing, access, supports, sequence, and working space make practical sense for construction.",
        "lens": "A pipe route may be geometrically possible but impossible to install because the support, equipment access, or assembly sequence was not considered.",
        "checks": ["Review access for installation and maintenance.", "Consider support and hanger space.", "Ask whether the element can be installed in the planned sequence."],
        "mistake": "Beginners often model final positions without thinking about how the element gets installed.",
        "action": "Choose one routed element and describe the installation sequence in three simple steps.",
    },
    {
        "day": 22,
        "phase": "Site-readiness thinking",
        "topic": "Maintenance Access in MEP BIM",
        "why": "MEP systems must be maintained after construction. BIM coordination should protect access to valves, filters, panels, dampers, and equipment.",
        "core": "Maintenance access is the space needed for inspection, operation, replacement, and safe work after installation.",
        "lens": "A valve above a ceiling may not clash with anything, but if no one can reach or operate it, the coordination is weak.",
        "checks": ["Identify elements that need future access.", "Check access panel or ceiling opening logic.", "Review whether another system blocks operation or replacement."],
        "mistake": "Beginners often coordinate only physical overlap and miss access needs.",
        "action": "Make a list of five MEP elements that usually require maintenance access.",
    },
    {
        "day": 23,
        "phase": "MEP rooms",
        "topic": "Mechanical Room Coordination Basics",
        "why": "Mechanical rooms concentrate equipment, pipes, ducts, valves, drains, electrical panels, and maintenance access in one tight area.",
        "core": "Mechanical room BIM coordination should review equipment clearance, pipe connection, duct connection, valve access, floor drain logic, and replacement path.",
        "lens": "A pump may fit in the model but still have poor access if valves, strainers, cable trays, or walls block maintenance space.",
        "checks": ["Check equipment clearance and replacement path.", "Review pipe and duct connection direction.", "Confirm valve, strainer, and drain access."],
        "mistake": "Beginners often coordinate equipment footprint only and ignore maintenance and replacement space.",
        "action": "Choose one mechanical equipment item and list the access zones needed around it.",
    },
    {
        "day": 24,
        "phase": "Vertical coordination",
        "topic": "Shaft Coordination Basics",
        "why": "Shafts are vertical coordination zones where multiple systems compete for limited space across many floors.",
        "core": "Shaft coordination reviews system stacking, riser spacing, fire stopping assumptions, access doors, sleeves, and floor-by-floor consistency.",
        "lens": "A riser may fit on one floor but shift into conflict on another if architectural or structural conditions change.",
        "checks": ["Compare shaft layout across floors.", "Check riser spacing and access.", "Review sleeve and penetration assumptions."],
        "mistake": "Beginners often check one floor and assume the entire shaft is consistent.",
        "action": "Describe how you would compare a shaft on three different floors.",
    },
    {
        "day": 25,
        "phase": "Ceiling coordination",
        "topic": "Ceiling Device Coordination",
        "why": "Ceilings contain diffusers, lights, sprinklers, detectors, speakers, access panels, and sometimes tight duct or pipe routes above.",
        "core": "Ceiling coordination aligns visible devices and hidden services so the ceiling can be built, maintained, and reviewed clearly.",
        "lens": "A diffuser, sprinkler head, and light fixture may each be correct individually but conflict visually or physically when combined in the ceiling grid.",
        "checks": ["Compare reflected ceiling plan with MEP device layout.", "Check above-ceiling service routes.", "Review access panels for valves, dampers, and equipment."],
        "mistake": "Beginners often coordinate hidden services and visible ceiling devices separately.",
        "action": "Choose one small ceiling grid and list all devices that need coordinated positions.",
    },
    {
        "day": 26,
        "phase": "Automation awareness",
        "topic": "Automation Should Reduce Repetition, Not Judgment",
        "why": "BIM automation is powerful, but it should support human review. Automated output still needs checking against project intent.",
        "core": "Automation is best for repetitive, rule-based tasks such as renaming, filtering, exporting, checking missing values, or creating draft reports.",
        "lens": "A script can rename systems quickly, but if the mapping rule is wrong, it can create many wrong values faster than manual work.",
        "checks": ["Use automation on repetitive tasks first.", "Test on a small sample before full execution.", "Keep a rollback copy and review the result."],
        "mistake": "Beginners often trust automated output without validating the rule and result.",
        "action": "Name one BIM task you would automate and one check you would perform after automation.",
    },
    {
        "day": 27,
        "phase": "Reporting",
        "topic": "Turning Model Review Into a Useful Report",
        "why": "A report should help people decide what to fix, who owns it, and how urgent it is. Screenshots alone are not enough.",
        "core": "A useful BIM report combines issue description, location, discipline, priority, screenshot, proposed action, and status.",
        "lens": "A report with many screenshots but no priority or owner can slow a meeting down instead of helping it.",
        "checks": ["Group issues by location or system.", "Add owner, priority, and next action.", "Separate observations from decisions."],
        "mistake": "Beginners often create reports as image collections, not decision tools.",
        "action": "Design a five-column issue report template for beginner coordination review.",
    },
    {
        "day": 28,
        "phase": "Professional habit",
        "topic": "Asking Better BIM Questions",
        "why": "Good questions help mentors, coordinators, and engineers answer faster. Weak questions create back-and-forth and delay learning.",
        "core": "A strong BIM question includes context, tool, system, location, what you checked, and the decision you need.",
        "lens": "Instead of saying this pipe is wrong, ask whether the chilled water return pipe at Level 02 grid C-5 should route below the tray because the current clearance is limited.",
        "checks": ["Include system and location.", "Say what you already checked.", "Ask for a clear decision or next step."],
        "mistake": "Beginners often ask broad questions without context, making it hard to give practical guidance.",
        "action": "Rewrite one broad BIM question into a specific question with context and desired decision.",
    },
    {
        "day": 29,
        "phase": "Career habit",
        "topic": "Building a Personal BIM Learning Log",
        "why": "A learning log turns daily mistakes and discoveries into career growth. It also helps future mentoring become more personalized.",
        "core": "A BIM learning log records topic, problem, what you checked, what you learned, and how you will apply it next time.",
        "lens": "If you repeatedly write down clearance issues, you may discover that vertical coordination or section review is your weak point.",
        "checks": ["Record one issue per day.", "Separate tool skill from coordination judgment.", "Review repeated patterns every week."],
        "mistake": "Beginners often learn the same lesson many times because they never record the pattern.",
        "action": "Create a simple five-line BIM learning log template and fill it with one recent lesson.",
    },
    {
        "day": 30,
        "phase": "Monthly review",
        "topic": "Your First Month Starter Review",
        "why": "The first month should give you a practical foundation: systems, drawings, model data, QA, clash thinking, access, installability, and reporting.",
        "core": "Starter Plan is not about memorizing every BIM command. It is about building a daily habit of checking model meaning, coordination risk, and practical next actions.",
        "lens": "A beginner who can explain why an issue matters, what to check, and what action to take is already becoming more useful in a BIM team.",
        "checks": ["Review your strongest topic from the month.", "Identify your weakest topic from the month.", "Choose one habit to repeat for the next 30 days."],
        "mistake": "Beginners often finish lessons passively. The value comes from turning them into a repeatable checking habit.",
        "action": "Write your own 30-day MEP BIM improvement plan with three focus areas: tool skill, system understanding, and coordination judgment.",
    },
]


def render_lesson(item: dict) -> str:
    checks = "\n".join(f"- {check}" for check in item["checks"])
    return "\n".join(
        [
            "LUA BIM LABS Starter",
            f"Day {item['day']} - {item['topic']}",
            "",
            "1. Why This Matters",
            item["why"],
            "",
            "2. Core Concept",
            item["core"],
            "",
            "3. Real Project Lens",
            item["lens"],
            "",
            "4. BIM Check",
            checks,
            "",
            "5. Common Mistake",
            item["mistake"],
            "",
            "6. Today's Action",
            item["action"],
            "",
            "Scope note:",
            SCOPE_NOTE,
        ]
    )


def write_curriculum() -> None:
    payload = {
        "version": 1,
        "product": "LUA BIM LABS Starter Plan",
        "price": "USD 39 / month",
        "duration_days": 30,
        "positioning": "Productized daily MEP BIM education for beginners and early-stage BIM learners.",
        "quality_standard": "docs/starter_plan_lesson_quality_standard.md",
        "lessons": [
            {
                "day": item["day"],
                "phase": item["phase"],
                "topic": item["topic"],
                "learning_outcome": item["action"],
            }
            for item in LESSONS
        ],
    }
    STARTER_DIR.mkdir(parents=True, exist_ok=True)
    CURRICULUM_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_messages() -> None:
    en_dir = MESSAGES_DIR / "en"
    en_dir.mkdir(parents=True, exist_ok=True)
    for item in LESSONS:
        path = en_dir / f"day_{item['day']:03d}.txt"
        path.write_text(render_lesson(item) + "\n", encoding="utf-8")


def write_obsidian_index() -> None:
    OBSIDIAN_INDEX.parent.mkdir(parents=True, exist_ok=True)
    rows = "\n".join(
        f"| {item['day']} | {item['phase']} | {item['topic']} |"
        for item in LESSONS
    )
    content = f"""---
type: product-curriculum
product: starter
status: public
duration_days: 30
---

# Starter Plan - 30 Day Launch Curriculum

## Product Promise

Daily productized MEP BIM education for beginners and early-stage BIM learners.

Each lesson delivers:

- one focused MEP BIM topic
- one practical project lens
- three BIM checks
- one common mistake
- one action item
- one scope reminder

## Curriculum Table

| Day | Phase | Topic |
| --- | --- | --- |
{rows}

## Quality Standard

[[Starter/README|Starter Product Knowledge]]

Local standard:

`docs/starter_plan_lesson_quality_standard.md`
"""
    OBSIDIAN_INDEX.write_text(content, encoding="utf-8")


def main() -> None:
    write_curriculum()
    write_messages()
    write_obsidian_index()
    print(f"curriculum={CURRICULUM_FILE}")
    print(f"messages={MESSAGES_DIR}")
    print(f"obsidian={OBSIDIAN_INDEX}")
    print(f"lesson_count={len(LESSONS)}")


if __name__ == "__main__":
    main()
