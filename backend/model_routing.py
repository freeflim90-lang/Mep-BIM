from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from backend.core.paths import PROJECT_ROOT


ROUTING_CONFIG = PROJECT_ROOT / "config" / "ai_model_routing.json"

HIGH_STAKES_KEYWORDS = [
    "가격",
    "pricing",
    "투자",
    "investment",
    "손익분기",
    "mrr",
    "arr",
    "스토어",
    "store",
    "로드맵",
    "roadmap",
    "상품화 우선순위",
]


def load_ai_model_routing() -> dict[str, Any]:
    if not ROUTING_CONFIG.exists():
        return {}
    try:
        return json.loads(ROUTING_CONFIG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def env_or_default(env_name: str, default: str) -> str:
    return os.environ.get(env_name, default)


def deepseek_final_review_model(text: str = "") -> str:
    config = load_ai_model_routing().get("deepseek_models", {})
    final_review = config.get("final_review", {})
    high_stakes = config.get("high_stakes_strategy", {})
    high_enabled_env = high_stakes.get("enabled_env", "DEEPSEEK_HIGH_STAKES_REVIEW_ENABLED")
    high_enabled = os.environ.get(high_enabled_env, str(high_stakes.get("default_enabled", False))).lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    lowered = text.lower()
    if high_enabled and any(keyword.lower() in lowered for keyword in HIGH_STAKES_KEYWORDS):
        return env_or_default(
            high_stakes.get("model_env", "DEEPSEEK_HIGH_STAKES_MODEL"),
            high_stakes.get("default_model", "deepseek-v4-pro"),
        )
    return env_or_default(
        final_review.get("model_env", "DEEPSEEK_FINAL_REVIEW_MODEL"),
        final_review.get("default_model", "deepseek-v4-flash"),
    )


def _local_model(status: dict[str, Any], key: str, fallback: str) -> str:
    return status.get("local", {}).get(key, {}).get("model") or fallback


def _deepseek_model(status: dict[str, Any], key: str, fallback: str) -> str:
    return status.get("deepseek", {}).get(key, {}).get("model") or fallback


def agent_model_map(status: dict[str, Any] | None = None) -> dict[str, str]:
    routing = status or model_routing_status()
    knowledge_model = _local_model(routing, "knowledge_qa", "qwen2.5:7b")
    coder_model = _local_model(routing, "coder", "qwen2.5-coder:7b")
    final_review_model = _deepseek_model(routing, "final_review", "deepseek-v4-flash")
    high_stakes_model = _deepseek_model(routing, "high_stakes_strategy", "deepseek-v4-pro")
    high_stakes_enabled = routing.get("deepseek", {}).get("high_stakes_strategy", {}).get("enabled", False)

    local_label = f"Local: {knowledge_model}"
    coder_label = f"Coder: {coder_model}"
    hybrid_label = f"Local + DeepSeek: {knowledge_model} / {final_review_model}"
    coder_hybrid_label = f"Coder + DeepSeek: {coder_model} / {final_review_model}"
    strategy_label = f"Review: {final_review_model}"
    high_stakes_label = f"Strategy Review: {high_stakes_model}" if high_stakes_enabled else hybrid_label

    agent_models = {
        "최고지배자": hybrid_label,
        "CEO": hybrid_label,
        "조율차장": hybrid_label,
        "COO": hybrid_label,
        "CFO": hybrid_label,
        "최고전략 (CSO)": high_stakes_label,
        "전략기획": hybrid_label,
        "아이디어발굴": hybrid_label,
        "프로젝트분석": hybrid_label,
        "요구사항분석": hybrid_label,
        "브랜드마케팅": hybrid_label,
        "견적심사원": hybrid_label,
        "스토어심사": high_stakes_label,
        "교육컨설팅": hybrid_label,
        "러닝콘텐츠디자이너": hybrid_label,
        "HR_인재분석관": hybrid_label,
        "경영지원": local_label,
        "경비정산": local_label,
        "회계세무": local_label,
        "법무검토": local_label,
        "보안책임자": local_label,
        "고객지원": local_label,
        "라이선스정산": local_label,
        "지식업데이트": local_label,
        "지식큐레이터": local_label,
        "공통": local_label,
        "건축": local_label,
        "구조": local_label,
        "토목": local_label,
        "기계": local_label,
        "전기": local_label,
        "통신": local_label,
        "소방전기": local_label,
        "소방기계": local_label,
        "위생": local_label,
        "자동제어": local_label,
        "철골": local_label,
        "커튼월": local_label,
        "인테리어": local_label,
        "프로그램개발": coder_label,
        "Qwen_Coder_8B": coder_label,
        "엑셀자동화": coder_label,
        "Revit_Addin": coder_hybrid_label,
        "Navisworks_Addin": coder_hybrid_label,
        "파이프라인_오케스트레이터": coder_label,
        "빌드검증": coder_label,
        "배포문서": local_label,
        "제품패키징": coder_hybrid_label,
        "인프라_DevOps (Obsidian)": local_label,
        "Caveman_토큰다이어터": local_label,
        "최종검토자": strategy_label,
    }
    return agent_models


def model_routing_status() -> dict[str, Any]:
    config = load_ai_model_routing()
    local = config.get("local_models", {})
    deepseek = config.get("deepseek_models", {})
    status = {
        "config_path": ROUTING_CONFIG.relative_to(PROJECT_ROOT).as_posix(),
        "principle": config.get("default_principle", "local_first_deepseek_final_review"),
        "local": {
            name: {
                "provider": item.get("provider", "ollama"),
                "model": env_or_default(item.get("model_env", ""), item.get("default_model", "")),
                "use_for": item.get("use_for", []),
            }
            for name, item in local.items()
        },
        "deepseek": {
            name: {
                "model": env_or_default(item.get("model_env", ""), item.get("default_model", "")),
                "enabled": (
                    os.environ.get(item.get("enabled_env", ""), str(item.get("default_enabled", True))).lower()
                    in {"1", "true", "yes", "on"}
                )
                if item.get("enabled_env")
                else True,
                "use_for": item.get("use_for", []),
            }
            for name, item in deepseek.items()
        },
        "rules": config.get("routing_rules", []),
    }
    status["agent_models"] = agent_model_map(status)
    return status
