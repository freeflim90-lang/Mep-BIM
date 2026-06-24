"""번역/생성 백엔드 폴백 감지 회귀 테스트.

배경(2026-06-24): _is_exhaustion류 검사가 401/인증 오류를 폴백 트리거로
잡지 못해, 무효 ANTHROPIC_API_KEY 상황에서 매 항목이 죽고 다음 백엔드로
강등되지 않던 버그가 translate_starter·generate·translate_starter_messages
세 곳에 있었다. 이 테스트는 인증 오류·한도 초과가 폴백을 트리거하도록 고정한다.
"""

import importlib

import pytest

translate_starter = importlib.import_module("scripts.bim_education.translate_starter")
generate = importlib.import_module("scripts.bim_education.generate")

# 폴백을 트리거해야 하는 오류 메시지(실제 SDK/HTTP 오류 문구 표본)
TRIGGER_ERRORS = [
    "Error code: 401 - invalid x-api-key",
    "authentication_error",
    "permission denied",
    "Error code: 429 - rate limit exceeded",
    "Error code: 402 - insufficient balance",
    "your credit balance is too low",
    "quota exceeded",
    "overloaded",
]

# 폴백이 아니라 즉시 표면화(raise)해야 하는 진짜 버그성 오류
NON_TRIGGER_ERRORS = [
    "JSONDecodeError: expecting value",
    "connection refused",
    "KeyError: 'choices'",
]


@pytest.mark.parametrize("msg", TRIGGER_ERRORS)
def test_is_exhaustion_triggers_on_auth_and_limit(msg):
    assert translate_starter._is_exhaustion(msg) is True
    assert any(k in msg.lower() for k in generate._FALLBACK_KEYWORDS)


@pytest.mark.parametrize("msg", NON_TRIGGER_ERRORS)
def test_is_exhaustion_ignores_real_bugs(msg):
    assert translate_starter._is_exhaustion(msg) is False
    assert not any(k in msg.lower() for k in generate._FALLBACK_KEYWORDS)


def test_401_specifically_triggers_fallback():
    # 원래 버그의 정확한 재발 방지: 401/invalid x-api-key 가 폴백을 타야 함.
    assert translate_starter._is_exhaustion("Error code: 401 - invalid x-api-key")
    assert "401" in generate._FALLBACK_KEYWORDS
    assert "invalid x-api-key" in generate._FALLBACK_KEYWORDS
