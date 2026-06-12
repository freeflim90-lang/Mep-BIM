PYTHON ?= .dev-venv/bin/python
HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: install-dev compile test audit-secrets codebase-health luachat-metrics-report luachat-support-backlog org-growth-report verify serve luachat-health

install-dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

compile:
	python3 -m compileall -q backend scripts tests

test:
	$(PYTHON) -m pytest -q

audit-secrets:
	@if git grep -n -E '(GOCSPX-|ya29\.|1//[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{20,})' -- ':!Makefile' ':!data/**' ':!dist/**' ':!obsidian_vaults/**' ':!config/*/token.json'; then \
		echo "Potential tracked secret patterns found."; \
		exit 1; \
	else \
		echo "No tracked secret patterns found."; \
	fi

codebase-health:
	$(PYTHON) scripts/codebase_health_report.py --markdown docs/CODEBASE_HEALTH_LATEST.md --json runtime/codebase_health_latest.json

luachat-metrics-report:
	$(PYTHON) scripts/luachat_metrics_report.py --input runtime/luachat_metrics_daily.json --markdown docs/revenue_products/LUACHAT_OPERATIONAL_METRICS_LATEST.md

luachat-support-backlog:
	$(PYTHON) scripts/luachat_support_backlog.py --input runtime/luachat_metrics_daily.json --markdown docs/revenue_products/LUACHAT_SUPPORT_BACKLOG_LATEST.md

org-growth-report:
	$(PYTHON) scripts/org_growth_report.py --health-json runtime/codebase_health_latest.json --luachat-metrics runtime/luachat_metrics_daily.json --markdown docs/ORG_GROWTH_OPPORTUNITIES_LATEST.md --json runtime/org_growth_opportunities_latest.json

verify: compile test audit-secrets

serve:
	$(PYTHON) -m uvicorn backend.server_total:app --host $(HOST) --port $(PORT)

luachat-health:
	curl -fsS http://127.0.0.1:$(PORT)/api/luachat/health
