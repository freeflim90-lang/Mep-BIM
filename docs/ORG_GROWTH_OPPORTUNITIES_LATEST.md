# LUA BIM LABS Organization Growth Priorities

## Operating Snapshot

- backend_lines: 11283
- script_lines: 34175
- test_lines: 2603
- test_to_backend_ratio_percent: 23.07
- luachat_chat_total: 1
- luachat_error_total: 0
- luachat_success_rate_percent: 100.0

## Priority Queue

### 1. [P1] engineering_velocity - score 86

- finding: 32 code files are 500+ lines.
- evidence: backend_lines=11283; server_total.py remains a concentrated runtime module.
- owner: Backend Maintainer
- next_action: Extract pure helpers and route/service modules, keeping tests green after each move.
- business_impact: Reduces regression risk and makes revenue-facing backend changes faster to ship.

### 2. [P1] automation_roi - score 78

- finding: Automation scripts are much larger than their tests.
- evidence: script_lines=34175; test_lines=2603
- owner: Operations + Automation Maintainer
- next_action: Promote reusable script logic into small modules and test the scheduling-critical paths.
- business_impact: Turns existing automation into dependable operating leverage instead of opaque scheduled work.

### 3. [P2] delivery_confidence - score 72

- finding: Backend test ratio is still below the next confidence threshold.
- evidence: test_to_backend_ratio_percent=23.07
- owner: Backend Maintainer
- next_action: Add focused tests around remaining Telegram, automation, and BIM Land mutation paths before expanding features.
- business_impact: Raises confidence for frequent releases while preserving current working behavior.

### 4. [P2] repository_boundary - score 66

- finding: Data/knowledge/vendor material is larger than backend source.
- evidence: Knowledge/data/vendor material dominates source volume.
- owner: Operations + Knowledge Curator
- next_action: Keep runtime/vendor data ignored or moved behind explicit import/export workflows.
- business_impact: Keeps product source reviewable while still using knowledge assets for sales and support.
