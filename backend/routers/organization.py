"""조직 구조 API — config/organization.json(SSOT) 의 6본부 트리를 그대로 서빙.

대시보드(frontend)·웹사이트(agents.html)가 이 단일 엔드포인트에서 조직도를 렌더링한다.
하드코딩된 팀/에이전트 목록을 두지 않으므로 조직 변경이 UI 에 자동 반영된다.
"""
from __future__ import annotations

import re

from fastapi import APIRouter

from backend import agent_registry as reg
from backend.core.paths import TEAM_DIR_NAMES

router = APIRouter(tags=["organization"])


def _team_label(team_key: str) -> str:
    """KB 폴더명(예: '01_경영진')에서 정렬용 접두 번호를 떼어 표시 라벨로 쓴다.

    표시 라벨도 단일 출처(TEAM_DIR_NAMES)에서 파생 — UI 가 라벨을 하드코딩하지 않게 한다.
    """
    folder = TEAM_DIR_NAMES.get(team_key)
    if not folder:
        return team_key
    return re.sub(r"^\d+_", "", folder)


def _agent_brief(agent: dict) -> dict:
    return {
        "id": agent["id"],
        "status": agent.get("status"),
        "team": agent.get("team"),
        "extra_alias": bool(agent.get("extra_alias")),
        # 공종(BIM 디스플린) 에이전트 여부 — UI 가 공종/일반 매트릭스를 분리 렌더할 때 쓴다.
        "discipline": bool(agent.get("discipline_keywords") or agent.get("discipline_group")),
    }


def build_organization_tree() -> dict:
    org = reg.organization()  # team -> [active agent ids]
    by_id = {a["id"]: a for a in reg._agents()}

    divisions = []
    for div in reg.divisions():
        teams = []
        for team_key in div.get("teams", []):
            teams.append({
                "key": team_key,
                "label": _team_label(team_key),
                "folder": TEAM_DIR_NAMES.get(team_key),
                "agents": [_agent_brief(by_id[aid]) for aid in org.get(team_key, []) if aid in by_id],
            })
        standalone = [_agent_brief(by_id[aid]) for aid in div.get("agents", []) if aid in by_id]
        divisions.append({
            "key": div["key"],
            "teams": teams,
            "standalone_agents": standalone,
        })

    all_agents = reg._agents()
    return {
        "service": "LUA BIM LABS",
        "divisions": divisions,
        "collaboration_contracts": reg.collaboration_contracts(),
        "counts": {
            "divisions": len(divisions),
            # 정의된 팀 수(현재 미배치 팀 포함) — 공개 메시지 '10팀' 의 출처.
            "teams": len(org),
            # 헤드라인 운영 인원 = 팀 소속 active 에이전트(확장·겸직·라우팅 제외). '34명' 의 출처.
            "operating": len(reg.all_agents()),
            "agents_total": len(all_agents),
            "active": sum(1 for a in all_agents if a.get("status") == "active"),
            "extra": sum(1 for a in all_agents if a.get("status") == "extra"),
            "inference_only": sum(1 for a in all_agents if a.get("status") == "inference_only"),
        },
    }


@router.get("/api/organization")
async def get_organization():
    return build_organization_tree()
