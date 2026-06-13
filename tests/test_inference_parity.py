"""추론 라우팅 패리티 테스트 — infer_knowledge_agent_from_query 동작 고정.

config 기반 추론(레지스트리)으로 마이그레이션하는 동안 라우팅 결과가
한 건도 바뀌지 않았음을 보장한다. 스냅샷(tests/data/inference_snapshot.json)은
리팩터 *이전* 코드에서 캡처했다. 차이가 나면 테스트가 아니라 규칙 순서를 고친다.

스냅샷 재생성(의도된 동작 변경 시에만):
    PYTHONPATH=. .dev-venv/bin/python /tmp/gen_inference_snapshot.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import backend.server_total as server

_SNAPSHOT_PATH = Path(__file__).parent / "data" / "inference_snapshot.json"
_SNAPSHOT: dict[str, str] = json.loads(_SNAPSHOT_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize("query,expected_agent", sorted(_SNAPSHOT.items()))
def test_inference_parity(query, expected_agent):
    assert server.infer_knowledge_agent_from_query(query) == expected_agent


def test_snapshot_branch_coverage():
    """스냅샷이 충분히 다양한 분기를 덮는지 회귀 방지."""
    assert len(_SNAPSHOT) >= 80
    assert len(set(_SNAPSHOT.values())) >= 30
