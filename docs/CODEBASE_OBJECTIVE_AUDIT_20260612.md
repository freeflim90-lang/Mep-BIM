# LUA BIM LABS Codebase Objective Audit - 2026-06-12

## Scope

This audit covers the current workspace as an integrated organization repository: backend API, automation scripts, web/static assets, knowledge base, product documentation, Revit add-in commercialization materials, runtime data folders, and collected external BIM script archives.

## Current Architecture

- Primary runtime: FastAPI backend in `backend/server_total.py`.
- API surface: dashboard, knowledge updates, local coder, GitHub integration, Qwen product drafts, BIM Command Center settings/features, LUAChat/Revit Assistant, visitor counting, BIM Land router.
- Automation layer: `scripts/` contains scheduled crawlers, Blogger/Telegram/Calendar flows, market intelligence, knowledge curation, add-in packaging, and education delivery.
- Knowledge layer: `data/knowledge_base`, `docs/knowledge_updates`, `obsidian_vaults`, and generated Q&A material.
- Product layer: `commercial_addins/BIM_Command_Center_For_Revit` and BIM Command Center backend modules.
- Deployment layer: Dockerfile, docker-compose, launch agents, Cloudflare tunnel config.

## Objective Findings

### Critical

1. Local OAuth token files exist in the workspace.
   - Observed: `config/blogger/token.json`, `config/calendar/token.json`.
   - Risk: refresh tokens and client secrets can be leaked by copy, backup, sync, or accidental commit.
   - Action taken: `.gitignore` now excludes Calendar token/client secret and generic `config/*/token.json`.
   - Remaining action: rotate the exposed Google OAuth credentials and regenerate local tokens.

2. Revit Assistant feedback path accepted user-provided relative paths.
   - Risk: a valid API key could write feedback into files outside the intended QA note directory.
   - Action taken: `resolve_revit_feedback_note_path()` now rejects empty, absolute, traversal, and non-Revit-QA paths.
   - Verification: tests added for accepted and rejected paths.

### High

3. `backend/server_total.py` is oversized and multi-responsibility.
   - Evidence: 1,484 lines remain after repeated route/service/helper extractions, but many unrelated concerns still share one module.
   - Risk: changes to Telegram, AI, contracts, visitor counting, and Revit Assistant can interfere with each other.
   - Recommended split:
     - `backend/routers/revit_assistant.py`
     - `backend/routers/dashboard.py`
     - `backend/routers/contracts.py`
     - `backend/services/auth.py`
     - `backend/services/visitor_counter.py`
     - `backend/services/telegram_bot.py`

4. Test discovery was unsafe for a mixed repository.
   - Evidence: root `pytest` discovered external tests under `data/bim_scripts` and failed during collection.
   - Action taken: `pytest.ini` limits test collection to first-party `tests/`.
   - Verification: `.dev-venv/bin/python -m pytest -q` passes.

5. Test coverage is still narrow outside the recently extracted backend surfaces.
   - Evidence: 108 passing first-party tests after additions; coverage proxy improved, but automation scripts and remaining Telegram flows still need broader regression tests.
   - Risk: broad API behavior, Telegram flows, file persistence, routing decisions, and BIM Land operations are not protected.
   - Recommended next tests:
     - Revit Assistant API auth/feedback endpoint tests.
     - BIM Land mutation tests with temp data directories.
     - Knowledge append/search regression tests.
     - Contract draft generation tests.
     - Visitor count race/error tests.

### Medium

6. Mutable defaults existed in Pydantic request models.
   - Action taken: changed dict/list defaults to `Field(default_factory=...)` for affected models.

7. API key comparison used normal membership comparison.
   - Action taken: changed to `secrets.compare_digest()` for configured Revit Assistant/LUAChat tokens.

8. Runtime state and generated artifacts are mixed with source.
   - Evidence: `data`, `runtime`, `logs`, `obsidian_vaults`, `dist`, `.wrangler`, launch agent state, and generated docs coexist with application source.
   - Risk: noisy diffs, accidental publication, slow tests, unclear deploy boundary.
   - Recommended structure:
     - `apps/api`
     - `apps/website`
     - `packages/bim_command_center`
     - `automation`
     - `knowledge`
     - `runtime-local` ignored
     - `vendor-research` ignored or submodule

9. FastAPI startup/shutdown used deprecated `on_event`.
   - Evidence: pytest previously reported deprecation warnings.
   - Action taken: startup/shutdown now run through FastAPI lifespan.

## Changes Applied In This Audit Pass

- Removed hardcoded Google Calendar OAuth client secret from `scripts/setup_calendar_token.py`.
- Added local secret ignores in `.gitignore`.
- Added `requirements-dev.txt` with pytest.
- Added `pytest.ini` to constrain first-party test discovery.
- Hardened Revit Assistant API key comparison.
- Restricted Revit Assistant feedback writes to the intended Obsidian Revit QA directory.
- Extracted Revit Assistant auth/path logic into `backend/revit_assistant_security.py`.
- Replaced mutable request defaults with `Field(default_factory=...)`.
- Added security tests for Revit Assistant token/path handling.
- Added API-level LUAChat health/auth/feedback tests.
- Added `Makefile` and maintenance runbook for repeatable verification and local operation.
- Added `scripts/codebase_health_report.py` and `make codebase-health` for repeatable maintainability/growth triage.
- Added visitor counter service extraction and endpoint/service tests.
- Added `backend/routers/revit_assistant.py` and route registration tests for LUAChat/Revit Assistant public paths.
- Added `backend/revit_assistant_service.py` for source serialization, health payload, and feedback note text updates.
- Added tested Revit Assistant source-tag and search-assisted knowledge-candidate rules.
- Added `compose_revit_assistant_answer()` to service local-knowledge vs search-assisted answer composition.
- Added Revit Assistant chat response assembly and agent-state update service helpers.
- Added `finalize_revit_assistant_chat()` to service Obsidian save, dashboard state broadcasts, background refresh scheduling, and response payload assembly.
- Added `persist_revit_knowledge_side_effects()` to service search-assisted knowledge candidate persistence and automatic gap logging.
- Added `update_revit_feedback_note()` to service Revit QA feedback file updates, MOC rebuilds, and knowledge refresh scheduling.
- Added TestClient coverage for successful LUAChat/Revit Assistant feedback note updates.
- Removed the untracked `260519` external development source folder from this operational repository.
- Added `scripts/addin_dev_paths.py` and migrated BIM Command Center add-in automation to `BCC_ADDIN_DEV_SOURCE_ROOT`.
- Updated commercial add-in release docs to treat development source as an external input instead of repo-local source.
- Updated codebase health reporting to exclude `data/bim_scripts/` as reference archive material.
- Stopped daily knowledge sync from auto-committing `data/bim_scripts/`; BIM script collection can now target `BIM_SCRIPTS_OUTPUT_DIR`.
- Added TestClient coverage for search-assisted LUAChat answers persisting knowledge candidates and automatic gap logs.
- Added structured Revit Assistant/LUAChat error responses for knowledge lookup, answer generation, knowledge persistence, and note persistence stages.
- Added TestClient coverage for search failure, synthesis failure, and note persistence failure responses.
- Added in-memory Revit Assistant/LUAChat metrics for chat success, local answers, search-assisted answers, feedback updates, and error stages.
- Exposed LUAChat metrics through `/api/luachat/health`.
- Added daily LUAChat metrics snapshot persistence to `runtime/luachat_metrics_daily.json`.
- Ignored the generated LUAChat metrics snapshot file.
- Added `scripts/luachat_metrics_report.py` and `make luachat-metrics-report` to convert metrics snapshots into support/FAQ prioritization.
- Generated `docs/revenue_products/LUACHAT_OPERATIONAL_METRICS_LATEST.md`.
- Added fallback archive support for Revit Assistant note persistence failures so generated answers and internal replay context survive even when primary Obsidian QA archiving is unavailable.
- Updated LUAChat operational metrics recommendations to distinguish note-archive warnings from answer-blocking errors.
- Added `scripts/luachat_support_backlog.py` and `make luachat-support-backlog` to convert LUAChat metrics into support snippets, FAQ candidates, owners, and next actions.
- Generated `docs/revenue_products/LUACHAT_SUPPORT_BACKLOG_LATEST.md`.
- Added `backend/revit_assistant_controller.py` so LUAChat/Revit Assistant chat and feedback orchestration no longer lives directly in `backend/server_total.py`.
- Kept Revit Assistant pure helper logic under 500 lines by separating controller orchestration from service helpers.
- Added `backend/routers/bim_command_center.py` so BIM Command Center feature and settings-profile API routes are registered outside `backend/server_total.py`.
- Added router and integrated-app tests for BIM Command Center commercial API endpoints.
- Added `backend/routers/development_operations.py` so GitHub, local Qwen coder, and Qwen product-draft API routes are registered outside `backend/server_total.py`.
- Preserved local-coder Excel guardrails and Qwen queue dashboard state updates with router-level regression tests.
- Added `backend/contract_drafts.py` and `backend/routers/contact_intake.py` so web contact intake, BIM contract draft generation, email notification, Telegram notification, and lead logging no longer live directly in `backend/server_total.py`.
- Added contact-intake tests covering budget parsing, LOD/area risk assessment, contract file generation, email body generation, log writing, validation errors, and integrated route registration.
- Added `backend/routers/knowledge_operations.py` so knowledge agents, knowledge update, knowledge graph stats, and persistent knowledge-gap endpoints are registered outside `backend/server_total.py`.
- Added knowledge operations tests covering stats log parsing, approval-candidate propagation, dashboard state updates, rejection handling, persistent gap reporting, and integrated route registration.
- Added `backend/routers/collaboration_operations.py` so collaboration workflows, role boundaries, collaboration audit, daily idea report, and route preview endpoints are registered outside `backend/server_total.py`.
- Added collaboration operations tests covering public workflow shaping, route-preview rejection, daily idea dashboard state updates, audit payloads, and integrated route registration.
- Added `backend/routers/dashboard_tasks.py` so dashboard Add-in development task intake is registered outside `backend/server_total.py`.
- Added dashboard task tests covering Add-in prompt construction, empty request rejection, background scheduling, and integrated route registration.
- Added `backend/dashboard_ws.py` so dashboard WebSocket connection management, state payload construction, decision-log payload construction, stale connection cleanup, and PING/PONG session handling are tested outside `backend/server_total.py`.
- Kept `/ws/office` and `/ws/state` compatibility routes while moving the shared session loop into the dashboard WebSocket helper.
- Added `backend/knowledge_approval.py` so knowledge approval registry loading, saving, candidate lookup, candidate creation, required-review detection, and approval notification text generation are tested outside `backend/server_total.py`.
- Kept Telegram notification dispatch in `backend/server_total.py` while moving the pure approval state machine into a reusable helper module.
- Added `backend/telegram_team_access.py` so Telegram team allowlist parsing, enabled-user registry loading, disabled-user exclusion, and update chat-id matching are tested outside `backend/server_total.py`.
- Kept the existing `telegram_chat_allowed(update)` wrapper for handler compatibility while moving file parsing and allowlist logic into a reusable helper.
- Added `backend/management_excel_approval.py` so management Excel automation request loading, saving, ID generation, summary risk flags, approval/rejection state transitions, report text, and pipeline prompt construction are tested outside routing/server code.
- Kept Telegram approval/rejection command handlers in `backend/server_total.py` while moving state mutation and approved pipeline prompt construction into the reusable helper.
- Fixed the `/approve` and `/reject` handler dependency on `find_management_excel_request` by importing it from the extracted approval helper.
- Added `backend/routers/operations_status.py` so root health, dashboard file serving, visitor-count recording, and AI model routing status are registered outside `backend/server_total.py`.
- Added operations-status tests covering health payload flags, model-routing payload shape, visitor deduplication through the router, and integrated route registration.
- Preserved test/runtime override flexibility for visitor counting by resolving the visitor counter through a provider instead of capturing a single object at router creation time.
- Added `scripts/org_growth_report.py` and `make org-growth-report` so codebase health and LUAChat metrics produce one ranked growth/operations priority queue.
- Generated `docs/ORG_GROWTH_OPPORTUNITIES_LATEST.md` and `runtime/org_growth_opportunities_latest.json`; current top priorities are LUAChat QA archive reliability, continued backend responsibility extraction, and automation ROI hardening.
- Added tests for organization growth priority scoring, operating metric summary generation, and stable markdown/JSON output.
- Added runtime fallback QA note archiving under `runtime/revit_assistant_qa_fallback/` when primary Revit Assistant Obsidian note persistence fails.
- Added service and API tests proving note persistence failures now return successful LUAChat answers with `note_archive_mode: fallback` instead of losing archive context.
- Regenerated growth priorities after the fallback mitigation; current top priorities shifted to backend responsibility extraction, automation ROI hardening, delivery confidence, and repository-boundary cleanup.

## Verification

- `.dev-venv/bin/python -m pytest -q`: 108 passed.
- `python3 -m compileall -q backend scripts tests`: passed.
- `make verify`: compile, pytest, and tracked-secret audit passed.
- `make codebase-health`: generated `docs/CODEBASE_HEALTH_LATEST.md`.
- `make org-growth-report`: generated `docs/ORG_GROWTH_OPPORTUNITIES_LATEST.md`.

## Next Improvement Order

1. Rotate Google OAuth credentials and regenerate local token files.
2. Move remaining runtime/generated/vendor data out of the source/test path.
3. Add CI command documentation: install `requirements-dev.txt`, then run compileall and pytest.
4. Continue moving high-traffic API areas from `backend/server_total.py` into router/controller/service modules.
5. Review `docs/revenue_products/LUACHAT_SUPPORT_BACKLOG_LATEST.md` weekly and promote approved items into customer-facing FAQ pages.
6. Use `docs/ORG_GROWTH_OPPORTUNITIES_LATEST.md` as the objective backlog input for growth and maintainability cycles.
