"""에이전트 정체성 단일 출처(SSOT) 로더.

config/organization.json 한 곳에서 에이전트를 정의하고, 과거 여러 모듈에
흩어져 있던 파생 구조(ORGANIZATION, DISCIPLINE_KEYWORDS, KNOWLEDGE_AGENTS 등)를
이 모듈이 재구성한다. 에이전트 추가/세분화는 config/organization.json 만 편집하면 된다.

핵심: 파생 결과는 기존 리터럴과 동작·값이 동일해야 한다(tests/test_registry_matches_legacy.py 가 보증).
"""
from __future__ import annotations

import json
from collections import OrderedDict
from functools import lru_cache
from typing import Any

from backend.core.paths import CONFIG_DIR, EXTRA_AGENTS_DIR_NAME, TEAM_DIR_NAMES

_CONFIG_PATH = CONFIG_DIR / "organization.json"

# KNOWLEDGE_AGENTS 합집합에서 제외할 상태(추론 전용 에이전트는 등재만, 지원 목록엔 미포함)
_KNOWLEDGE_AGENT_STATUSES = {"active", "extra"}


@lru_cache(maxsize=1)
def _raw() -> dict[str, Any]:
    return json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))


def _agents() -> list[dict]:
    return _raw()["agents"]


def agents() -> list[dict]:
    """등재된 모든 에이전트 엔트리(읽기 전용 사본)."""
    return [dict(a) for a in _agents()]


@lru_cache(maxsize=1)
def organization() -> "OrderedDict[str, list[str]]":
    """팀 → 소속(active) 에이전트 목록. 빈 팀 포함, teams 순서 유지."""
    by_team: "OrderedDict[str, list[str]]" = OrderedDict(
        (t["key"], []) for t in sorted(_raw()["teams"], key=lambda t: t["order"])
    )
    for agent in _agents():
        if agent.get("team") and agent.get("status") == "active":
            by_team.setdefault(agent["team"], []).append(agent["id"])
    return by_team


@lru_cache(maxsize=1)
def all_agents() -> list[str]:
    return [agent for members in organization().values() for agent in members]


@lru_cache(maxsize=1)
def extra_knowledge_agents() -> set[str]:
    # status=="extra" + 팀 소속이면서 EXTRA 에도 등재된 에이전트(extra_alias).
    return {
        a["id"]
        for a in _agents()
        if a.get("status") == "extra" or a.get("extra_alias")
    }


@lru_cache(maxsize=1)
def discipline_keywords() -> "OrderedDict[str, list[str]]":
    """공종 키워드 — config 의 discipline_keyword_order 순서를 보존(추론 루프 순서가 중요)."""
    kw_by_id = {a["id"]: a.get("discipline_keywords") for a in _agents()}
    order = _raw()["discipline_keyword_order"]
    return OrderedDict((k, kw_by_id[k]) for k in order if kw_by_id.get(k) is not None)


@lru_cache(maxsize=1)
def discipline_groups() -> "OrderedDict[str, list[str]]":
    """공통([]) + 싱글톤 그룹(공종→[공종]) + 합성 그룹(MEP통합/전체공정). 기존 순서 보존."""
    groups: "OrderedDict[str, list[str]]" = OrderedDict()
    groups["공통"] = []
    singleton_ids = {a["id"] for a in _agents() if a.get("discipline_group")}
    for k in _raw()["discipline_keyword_order"]:
        if k in singleton_ids:
            groups[k] = [k]
    for k, v in _raw()["discipline_groups"].items():
        groups[k] = list(v)
    return groups


@lru_cache(maxsize=1)
def default_knowledge() -> "OrderedDict[str, str]":
    return OrderedDict(
        (a["id"], a["default_knowledge_seed"])
        for a in _agents()
        if a.get("default_knowledge_seed")
    )


@lru_cache(maxsize=1)
def knowledge_agents() -> list[str]:
    """지원 지식 에이전트 — active+extra ∪ 공종 키워드 키. 정렬(기존과 동일)."""
    ids = {a["id"] for a in _agents() if a.get("status") in _KNOWLEDGE_AGENT_STATUSES}
    return sorted(ids | set(discipline_keywords().keys()))


@lru_cache(maxsize=1)
def agent_team_dir() -> dict[str, str]:
    """팀 소속 에이전트 → KB 팀 폴더명. 팀 없는(확장/공종전용) 에이전트는 미포함(기존과 동일)."""
    return {
        agent: TEAM_DIR_NAMES[team]
        for team, members in organization().items()
        for agent in members
    }


# ── 신규 구조(가산): 본부(division) · 협업 계약 ─────────────────────────────
@lru_cache(maxsize=1)
def divisions() -> list[dict]:
    return _raw().get("divisions", [])


@lru_cache(maxsize=1)
def collaboration_contracts() -> list[dict]:
    return _raw().get("collaboration_contracts", [])


def division_of_team(team: str) -> str | None:
    for div in divisions():
        if team in div.get("teams", []):
            return div["key"]
    return None


# ── 추론 규칙(순서 = 우선순위) ─────────────────────────────────────────────
@lru_cache(maxsize=1)
def inference_rules() -> list[dict]:
    return _raw().get("inference_rules", [])


@lru_cache(maxsize=1)
def inference_default() -> str:
    return _raw().get("inference_default", "지식업데이트")


@lru_cache(maxsize=1)
def all_agent_ids() -> set[str]:
    """등재된 모든 에이전트 id(active+extra+inference_only). 가드레일/검증용."""
    return {a["id"] for a in _agents()}
