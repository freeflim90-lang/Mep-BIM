"""/api/organization 트리 가드레일.

팀 표시 라벨은 UI 가 하드코딩하지 않고 이 API(TEAM_DIR_NAMES 에서 파생) 만 따른다.
그 계약이 깨지지 않도록 강제한다.
"""
from __future__ import annotations

import re

import backend.agent_registry as reg
from backend.core.paths import TEAM_DIR_NAMES
from backend.routers.organization import build_organization_tree


def test_every_team_has_label_derived_from_folder():
    tree = build_organization_tree()
    seen = 0
    for div in tree["divisions"]:
        for team in div["teams"]:
            seen += 1
            expected = re.sub(r"^\d+_", "", TEAM_DIR_NAMES[team["key"]])
            assert team["label"] == expected, f"{team['key']} 라벨 불일치: {team['label']} != {expected}"
            assert team["label"] and not team["label"][0].isdigit()
    assert seen, "본부 트리에 팀이 하나도 없다"


def test_counts_present_and_consistent():
    tree = build_organization_tree()
    counts = tree["counts"]
    assert counts["divisions"] == len(tree["divisions"])
    assert counts["agents_total"] == counts["active"] + counts["extra"] + counts["inference_only"]


def test_headline_counts_match_registry():
    """공개 메시지 '10팀 34명' 의 출처가 레지스트리에서 파생됨을 강제한다."""
    counts = build_organization_tree()["counts"]
    # 팀 수 = 정의된 모든 팀(미배치 팀 포함)
    assert counts["teams"] == len(reg.organization())
    # 운영 인원 = 팀 소속 active 에이전트
    assert counts["operating"] == len(reg.all_agents())
    assert counts["operating"] <= counts["active"]  # 팀 없는 active 가 있을 수 있다
