# LUA BIM LABS Codebase Maintenance Runbook - 2026-06-12

## Daily Verification

Run this before and after backend or automation changes:

```bash
make verify
```

Equivalent commands:

```bash
python3 -m compileall -q backend scripts tests
.dev-venv/bin/python -m pytest -q
make audit-secrets
```

Expected current result:

```text
108 passed
```

`make audit-secrets` should print:

```text
No tracked secret patterns found.
```

For organization-level maintainability and growth triage:

```bash
make codebase-health
make luachat-metrics-report
make luachat-support-backlog
make org-growth-report
```

Outputs:

- `docs/CODEBASE_HEALTH_LATEST.md`
- `runtime/codebase_health_latest.json`
- `docs/revenue_products/LUACHAT_OPERATIONAL_METRICS_LATEST.md`
- `docs/revenue_products/LUACHAT_SUPPORT_BACKLOG_LATEST.md`
- `docs/ORG_GROWTH_OPPORTUNITIES_LATEST.md`
- `runtime/org_growth_opportunities_latest.json`

## Local Backend

```bash
make serve
```

Health check:

```bash
make luachat-health
```

The LUAChat operational contract is:

- `GET /api/luachat/health`
- `POST /api/luachat`
- `POST /api/luachat/feedback`

When `LUA_CHAT_TOKEN` or `REVIT_ASSISTANT_API_KEYS` is set, clients must send either:

- `X-LUA-BIM-API-Key: <token>`
- `Authorization: Bearer <token>`

## Maintenance Boundaries

- First-party tests live under `tests/`; external reference archives under `data/` are intentionally excluded from pytest collection.
- Runtime tokens and local credentials must stay under ignored paths such as `config/*/token.json` or local environment variables.
- LUAChat operational metrics snapshots are runtime artifacts under `runtime/luachat_metrics_daily.json`.
- External add-in development source must stay outside this operational repository; automation should use `BCC_ADDIN_DEV_SOURCE_ROOT`.
- External BIM script archives are reference material, not product source; daily sync should not auto-commit `data/bim_scripts/`, and new collection can target an external path with `BIM_SCRIPTS_OUTPUT_DIR`.
- `make audit-secrets` checks tracked source for common Google/OpenAI-style token patterns before handoff.
- `make codebase-health` turns repository sprawl, large modules, and test-ratio signals into a repeatable report.
- `make luachat-support-backlog` turns LUAChat operational findings into support snippets, FAQ candidates, owners, and next actions.
- `make org-growth-report` combines codebase health and LUAChat reliability signals into a ranked growth/operations priority queue.
- New API behavior should include a `TestClient` test when possible.
- New pure logic should be placed in a small module outside `backend/server_total.py` before adding route glue.

## Current High-Value Improvement Path

1. Keep extracting pure helpers from `backend/server_total.py`.
2. Add endpoint tests around existing routes before moving them.
3. Add focused tests around scheduled automation scripts with business impact.
4. Continue moving high-traffic API areas from `backend/server_total.py` into router/controller/service modules.
5. Use `make org-growth-report` after metrics/report refreshes to pick the next evidence-backed growth action.
6. Use `make codebase-health` after each improvement cycle to confirm the bottleneck is shrinking.
7. Keep `make verify` green after every extraction.

## Credential Hygiene

Local files observed in this workspace include Google OAuth tokens. They are ignored now, but previously exposed values should be considered compromised.

Required operator action:

1. Revoke/rotate Google OAuth client secrets and refresh tokens.
2. Regenerate local token files with `scripts/setup_calendar_token.py` and Blogger setup flow.
3. Keep generated token files out of commits.
