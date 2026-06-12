# Clash Types & Priority Matrix
**LUA BIM LABS Starter — Track 5 Quick Reference**
*Track completion card — Day 38*

---

## Clash Type Definitions

| Clash Type | Definition | Example |
|---|---|---|
| Hard Clash | Two solid elements physically intersect — they occupy the same space | HVAC duct passing through a structural beam web |
| Soft / Clearance Clash | Two elements are within a defined minimum clearance distance — they do not touch but violate required access or maintenance space | Cable tray within 50mm of a sprinkler pipe, violating minimum separation |
| Duplicate | Two identical elements are stacked at exactly the same position — usually a modeling or import error | Two pipe segments with the same path and elevation from different model imports |
| Workflow Clash (4D) | Two activities are scheduled for the same location at the same time — a time-space conflict, not a geometric one | HVAC installation and structural slab formwork both planned for Level 5 in the same week |

---

## Priority Level Matrix

| Priority | Criteria | Required Action |
|---|---|---|
| **Critical** | Blocks structural work, prevents slab completion, or stops a safety-critical system from being installed | Must be resolved before any work in the affected zone proceeds — escalate immediately |
| **High** | Requires rerouting of a major system (main duct trunk, primary pipe run) — affects multiple connected elements | Resolve within current coordination cycle; assign to responsible trade with deadline |
| **Medium** | Requires a minor adjustment (elevation shift, small offset) — affects one or a few elements | Resolve before coordination drawing is issued for the zone |
| **Low** | Minor clearance violation with documented acceptance option; or affects only a non-critical element | Review and accept with documentation, or resolve at next available opportunity |

---

## Clash Grouping Rules

Before any coordination meeting, group raw clash results to reduce noise and focus effort:

- **Group by Level**: Separate clashes by floor so each trade addresses one zone at a time
- **Group by Grid Bay**: Cluster clashes within the same structural bay for efficient spatial review
- **Group by Discipline Pair**: Separate HVAC-vs-Structure from Electrical-vs-Plumbing — different trades, different meeting agenda items
- **Filter by Status**: Show only New and Active items — exclude Reviewed, Approved, and Resolved from the live discussion list
- **Remove Duplicates**: Many raw clashes are the same physical conflict reported from both element directions — review and consolidate before presenting

---

## Coordination Meeting Agenda Template

```
MEP COORDINATION MEETING — [Zone / Level] — [Date]

1. Attendance (5 min)
   - Record all attendees and represented trades

2. Previous actions review (10 min)
   - Confirm resolution of items from last meeting
   - Update status of Resolved items in tracker

3. Clash review — Critical items (15 min)
   - Screen-share Navisworks / clash report
   - Decision: Fix / Hold / Accept for each item
   - Assign owner and deadline

4. Clash review — High priority items (15 min)
   - Same process as Critical

5. New issues flagged by trades (10 min)
   - Any site or model issues not yet in the tracker

6. Actions summary (5 min)
   - Read back all assigned actions, owners, and due dates

7. Next meeting date confirmed
```

---
*LUA BIM LABS | Practical BIM Education for MEP*
*Educational reference only — not project specification or code compliance guidance.*
