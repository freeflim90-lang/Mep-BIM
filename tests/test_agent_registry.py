"""에이전트 레지스트리(config/organization.json) 영구 가드레일.

에이전트 추가/세분화는 config 한 곳만 편집하면 되지만, 그 편집이
구조적으로 일관되는지(중복·orphan·디스크 불일치·본부 커버리지)를 여기서 강제한다.
make verify(pytest) 에 자동 포함된다.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

import backend.agent_registry as reg
from backend.core.paths import CONFIG_DIR, TEAM_DIR_NAMES
from backend.knowledge_store import agent_kb_dir

_VALID_STATUSES = {"active", "extra", "inference_only", "planned"}
_SENTINELS = {"@discipline_keywords", "@knowledge_agent_name"}


def test_agent_ids_unique():
    ids = [a["id"] for a in reg._agents()]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, f"중복 에이전트 id: {dupes}"


def test_agent_status_and_team_valid():
    for a in reg._agents():
        assert a.get("status") in _VALID_STATUSES, f"잘못된 status: {a}"
        team = a.get("team")
        if team is not None:
            assert team in TEAM_DIR_NAMES, f"알 수 없는 팀: {team} ({a['id']})"
        # 팀 없는 active 는 공종 전용(키워드 보유)이어야 한다
        if a.get("status") == "active" and team is None:
            assert a.get("discipline_keywords"), f"팀 없는 active 인데 공종 키워드 없음: {a['id']}"


def test_inference_rule_targets_registered():
    ids = reg.all_agent_ids()
    for rule in reg.inference_rules():
        target = rule["target"]
        if target in _SENTINELS:
            continue
        assert target in ids, f"미등록 추론 타깃(orphan): {target}"


def test_discipline_keyword_keys_registered():
    ids = reg.all_agent_ids()
    for key in reg.discipline_keywords():
        assert key in ids, f"미등록 공종 키워드 에이전트: {key}"


def test_division_coverage_exact():
    """모든 비어있지 않은 팀은 정확히 한 본부에 속한다. 한 팀이 두 본부에 중복 금지."""
    teams_with_agents = {t for t, members in reg.organization().items() if members}
    seen: dict[str, str] = {}
    for div in reg.divisions():
        for team in div.get("teams", []):
            assert team in TEAM_DIR_NAMES, f"본부 {div['key']} 의 알 수 없는 팀: {team}"
            assert team not in seen, f"팀 {team} 이 본부 {seen.get(team)}·{div['key']} 에 중복"
            seen[team] = div["key"]
    missing = teams_with_agents - set(seen)
    assert not missing, f"어느 본부에도 속하지 않은 팀: {missing}"


def test_every_division_has_operating_agents():
    """모든 본부는 실제 운영(active) 인력을 보유해야 한다 — 협업계약에만 등장하는
    '껍데기 본부'(팀·active 0명)를 금지한다. 마케팅GTM본부가 standalone extra 만으로
    구성됐던 회귀를 차단한다."""
    org = reg.organization()  # team -> [active ids]
    active_ids = {a["id"] for a in reg._agents() if a.get("status") == "active"}
    for div in reg.divisions():
        team_active = sum(len(org.get(t, [])) for t in div.get("teams", []))
        standalone_active = sum(1 for a in div.get("agents", []) if a in active_ids)
        assert team_active + standalone_active >= 1, (
            f"본부 {div['key']} 에 active 운영 인력이 없음(껍데기 본부)"
        )


def test_every_division_feeds_knowledge_intake():
    """학습조직 폐루프: 지식운영본부를 제외한 모든 본부는 지식운영본부로
    인테이크 협업계약을 최소 1건 보유해야 한다(지식 내재화 회사의 핵심 불변식).
    경영본부 인테이크 누락 회귀를 차단한다."""
    KNOWLEDGE_DIV = "지식운영본부"
    feeders = {c["from"] for c in reg.collaboration_contracts() if c["to"] == KNOWLEDGE_DIV}
    for div in reg.divisions():
        if div["key"] == KNOWLEDGE_DIV:
            continue
        assert div["key"] in feeders, f"본부 {div['key']} 가 지식운영본부로 인테이크하지 않음(학습 루프 단절)"


def test_division_standalone_agents_registered():
    ids = reg.all_agent_ids()
    for div in reg.divisions():
        for agent in div.get("agents", []):
            assert agent in ids, f"본부 {div['key']} 의 미등록 에이전트: {agent}"


def test_kb_dirs_exist_on_disk():
    """active/extra 에이전트가 해석하는 KB 디렉터리는 실재해야 한다."""
    for a in reg._agents():
        if a.get("status") not in {"active", "extra"}:
            continue
        kb_dir = agent_kb_dir(a["id"])
        assert os.path.isdir(kb_dir), f"KB 폴더 없음: {a['id']} → {kb_dir}"


def test_collaboration_contract_agents_registered():
    ids = reg.all_agent_ids()
    div_keys = {d["key"] for d in reg.divisions()} | {"전체"}
    for contract in reg.collaboration_contracts():
        assert contract["from"] in div_keys, f"협업계약 from 미존재 본부: {contract['from']}"
        assert contract["to"] in div_keys, f"협업계약 to 미존재 본부: {contract['to']}"
        for role, agent in contract.get("raci", {}).items():
            assert agent in ids, f"협업계약 {contract['from']}→{contract['to']} 의 미등록 {role}: {agent}"


def test_domain_axes_match_known_domains():
    domains = set(json.loads((CONFIG_DIR / "knowledge_domains.json").read_text(encoding="utf-8"))["domains"])
    for a in reg._agents():
        for axis in a.get("domain_axes", []):
            assert axis in domains, f"알 수 없는 도메인축: {axis} ({a['id']})"
