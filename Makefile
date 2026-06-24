PYTHON ?= .dev-venv/bin/python
HOST ?= 0.0.0.0
PORT ?= 8000

.PHONY: install-dev compile test audit-secrets codebase-health luachat-metrics-report luachat-support-backlog org-growth-report knowledge-qa knowledge-audit qa-simulation agent-qa agent-qa-coverage auto-enrich-guardrails knowledge-verify web-search-health starter-localize verify serve luachat-health

install-dev:
	$(PYTHON) -m pip install -r requirements-dev.txt

compile:
	python3 -m compileall -q backend scripts tests

test:
	$(PYTHON) -m pytest -q

audit-secrets:
	@if git grep -n -E '(GOCSPX-|ya29\.|1//[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{20,})' -- ':!Makefile' ':!data/**' ':!knowledge/**' ':!products/**' ':!dist/**' ':!obsidian_vaults/**' ':!config/*/token.json'; then \
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

knowledge-qa:
	$(PYTHON) scripts/validate_knowledge_qa.py

knowledge-audit:
	$(PYTHON) scripts/knowledge_connection_audit.py --verbose --min-rate 1.0 --min-top-score 68

qa-simulation:
	$(PYTHON) scripts/simulate_qa_quality.py --min-score 99 --min-pass-rate 100 --no-save

agent-qa:
	$(PYTHON) scripts/validate_agent_qa_quality.py --no-save --min-score 100 --min-pass-rate 100

agent-qa-coverage:
	$(PYTHON) scripts/validate_agent_qa_coverage.py --min-pairs 5 --max-single-pair-count 0 --max-min-pair-count 36

auto-enrich-guardrails:
	$(PYTHON) scripts/validate_auto_enrich_guardrails.py --max-unguarded 0

knowledge-verify: knowledge-qa knowledge-audit qa-simulation agent-qa agent-qa-coverage auto-enrich-guardrails

web-search-health:
	$(PYTHON) scripts/web_search_health.py

# Starter Plan 레퍼런스 카드 현지화: 누락 언어 번역 + 전 언어 PDF 재생성.
# en 카드(.md)를 수정한 뒤에는 translate에 --force를 붙여 재번역할 것.
starter-localize:
	$(PYTHON) scripts/bim_education/translate_reference_cards.py --lang ko
	$(PYTHON) scripts/bim_education/translate_reference_cards.py --lang ja
	$(PYTHON) scripts/bim_education/translate_reference_cards.py --lang zh
	$(PYTHON) scripts/bim_education/translate_reference_cards.py --lang ar
	$(PYTHON) scripts/generate_reference_card_pdfs.py --lang ko --force
	$(PYTHON) scripts/generate_reference_card_pdfs.py --lang ja --force
	$(PYTHON) scripts/generate_reference_card_pdfs.py --lang zh --force
	$(PYTHON) scripts/generate_reference_card_pdfs.py --lang ar --force

verify: compile test audit-secrets

serve:
	$(PYTHON) -m uvicorn backend.server_total:app --host $(HOST) --port $(PORT)

luachat-health:
	curl -fsS http://127.0.0.1:$(PORT)/api/luachat/health
