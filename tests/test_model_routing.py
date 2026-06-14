from __future__ import annotations

from backend.model_routing import agent_model_map, deepseek_final_review_model, model_routing_status


def test_dashboard_agents_use_deepseek_v4_pro_or_flash(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_FINAL_REVIEW_MODEL", raising=False)
    monkeypatch.delenv("DEEPSEEK_HIGH_STAKES_MODEL", raising=False)

    labels = agent_model_map(model_routing_status())

    assert labels["CEO"] == "DeepSeek V4 Pro: deepseek-v4-pro"
    assert labels["스토어심사"] == "DeepSeek V4 Pro: deepseek-v4-pro"
    assert labels["Revit_Addin"] == "DeepSeek V4 Pro: deepseek-v4-pro"
    assert labels["지식업데이트"] == "DeepSeek V4 Flash: deepseek-v4-flash"
    assert labels["고객지원 CS"] == "DeepSeek V4 Flash: deepseek-v4-flash"
    assert {
        label.split(": ", 1)[1]
        for label in labels.values()
    } == {"deepseek-v4-pro", "deepseek-v4-flash"}


def test_deepseek_final_review_routes_high_stakes_to_pro(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_FINAL_REVIEW_MODEL", raising=False)
    monkeypatch.delenv("DEEPSEEK_HIGH_STAKES_MODEL", raising=False)
    monkeypatch.delenv("DEEPSEEK_HIGH_STAKES_REVIEW_ENABLED", raising=False)

    assert deepseek_final_review_model("일반 QA 검토") == "deepseek-v4-flash"
    assert deepseek_final_review_model("가격 전략과 투자 우선순위 검토") == "deepseek-v4-pro"
