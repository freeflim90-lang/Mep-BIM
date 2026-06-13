"""조직 구조 API — config/organization.json(SSOT) 의 6본부 트리를 그대로 서빙.

대시보드(frontend)·웹사이트(agents.html)가 이 단일 엔드포인트에서 조직도를 렌더링한다.
하드코딩된 팀/에이전트 목록을 두지 않으므로 조직 변경이 UI 에 자동 반영된다.
"""
from __future__ import annotations

from fastapi import APIRouter

from backend import agent_registry as reg
from backend.core.paths import TEAM_DIR_NAMES

router = APIRouter(tags=["organization"])


def _agent_brief(agent: dict) -> dict:
    return {
        "id": agent["id"],
        "status": agent.get("status"),
        "team": agent.get("team"),
        "extra_alias": bool(agent.get("extra_alias")),
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
            "teams": sum(1 for members in org.values() if members),
            "agents_total": len(all_agents),
            "active": sum(1 for a in all_agents if a.get("status") == "active"),
            "extra": sum(1 for a in all_agents if a.get("status") == "extra"),
            "inference_only": sum(1 for a in all_agents if a.get("status") == "inference_only"),
        },
    }


@router.get("/api/organization")
async def get_organization():
    return build_organization_tree()
