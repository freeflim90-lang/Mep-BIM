"""지식 검색 스모크 테스트 — 재구성 후 대표 질의가 올바른 에이전트 KB 를 찾는지 고정.

파일 트리 재구성(knowledge/10_agents 팀 폴더화)이나 카탈로그(FILE_MAP) 변경이
검색 품질을 깨뜨리면 여기서 잡힌다.
"""
from __future__ import annotations

import pytest

import backend.server_total as server

CASES = [
    ("revit api transaction 처리 기준", "Revit_Addin"),
    ("냉각수 cws 배관 유체 종류", "공조배관"),
    ("스프링클러 헤드 살수반경", "소방기계"),
    ("ifc4 openbim 속성셋", "IFC_OpenBIM"),
    ("교육 커리큘럼 온보딩", "교육컨설팅"),
]


@pytest.mark.parametrize("query,expected_agent", CASES)
def test_inferred_agent(query, expected_agent):
    assert server.infer_knowledge_agent_from_query(query) == expected_agent


@pytest.mark.parametrize("query,expected_stem", [
    ("냉각수 cws 배관 유체 종류", "공조배관"),
    ("스프링클러 헤드 살수반경", "소방기계"),
    ("revit api transaction 처리 기준", "Revit_Addin"),
])
def test_search_top_match(query, expected_stem):
    matches = server.search_local_knowledge(query, limit=3)
    assert matches, f"no matches for: {query}"
    top = matches[0]
    assert top["path"].stem == expected_stem
    assert top["score"] >= 18
