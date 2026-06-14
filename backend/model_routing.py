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
    final_review_model = _deepseek_model(routing, "final_review", "deepseek-v4-flash")
    high_stakes_model = _deepseek_model(routing, "high_stakes_strategy", "deepseek-v4-pro")

    flash_label = f"DeepSeek V4 Flash: {final_review_model}"
    pro_label = f"DeepSeek V4 Pro: {high_stakes_model}"

    agent_models = {
        "최고지배자": pro_label,
        "CEO": pro_label,
        "조율차장": pro_label,
        "COO": pro_label,
        "CFO": pro_label,
        "최고전략 (CSO)": pro_label,
        "전략기획": pro_label,
        "아이디어발굴": pro_label,
        "프로젝트분석": pro_label,
        "요구사항분석": pro_label,
        "브랜드마케팅": pro_label,
        "견적심사원": pro_label,
        "스토어심사": pro_label,
        "글로벌_매출관리원": pro_label,
        "글로벌_유통기획관": pro_label,
        "Revit_Addin": pro_label,
        "Navisworks_Addin": pro_label,
        "제품패키징": pro_label,
        "최종검토자": pro_label,
        "교육컨설팅": flash_label,
        "러닝콘텐츠디자이너": flash_label,
        "HR_인재분석관": flash_label,
        "경영지원": flash_label,
        "경비정산": flash_label,
        "경비정산_AI": flash_label,
        "회계세무": flash_label,
        "법무검토": flash_label,
        "보안책임자": flash_label,
        "고객지원": flash_label,
        "고객지원 CS": flash_label,
        "CS_기술지원관": flash_label,
        "라이선스정산": flash_label,
        "라이선스결제": flash_label,
        "지식업데이트": flash_label,
        "지식큐레이터": flash_label,
        "공통": flash_label,
        "건축": flash_label,
        "구조": flash_label,
        "토목": flash_label,
        "공조배관": flash_label,
        "공조덕트": flash_label,
        "기계": flash_label,
        "전기": flash_label,
        "통신": flash_label,
        "소방전기": flash_label,
        "소방기계": flash_label,
        "위생": flash_label,
        "자동제어": flash_label,
        "철골": flash_label,
        "커튼월": flash_label,
        "인테리어": flash_label,
        "간섭검토": flash_label,
        "프로그램개발": flash_label,
        "Qwen_Coder_8B": flash_label,
        "엑셀자동화": flash_label,
        "파이프라인_오케스트레이터": flash_label,
        "빌드검증": flash_label,
        "배포문서": flash_label,
        "인프라_DevOps (Obsidian)": flash_label,
        "Caveman_토큰다이어터": flash_label,
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
