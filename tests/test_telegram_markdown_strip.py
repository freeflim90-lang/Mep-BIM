"""발송기 send_telegram이 평문 텔레그램용으로 마크다운 '**'를 제거하는지 검증.

배경(2026-06-24): 세 발송기 모두 parse_mode 없이 평문 발송이라 '**굵게**'가
글자 그대로 노출됐음. send_telegram egress에서 '**'를 제거하도록 수정.
이 테스트는 실제로 전송 payload에 '**'가 남지 않는지(그리고 본문은 보존되는지)
urlopen을 가로채 확인한다.
"""

import importlib
import urllib.parse

import pytest

SENDER_NAMES = [
    "scripts.bim_education.send_internal",
    "scripts.bim_education.send_starter",
    "scripts.bim_education.send_daily",
]


class _FakeResp:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


@pytest.mark.parametrize("modname", SENDER_NAMES)
def test_send_telegram_strips_double_asterisk(modname, monkeypatch):
    mod = importlib.import_module(modname)
    captured = {}

    def fake_urlopen(req, *args, **kwargs):
        # urlencode된 POST body에서 text 필드를 복원
        body = req.data.decode("utf-8")
        captured.update(urllib.parse.parse_qs(body))
        return _FakeResp()

    monkeypatch.setattr(mod, "BOT_TOKEN", "TEST_TOKEN")
    monkeypatch.setattr(mod.urllib.request, "urlopen", fake_urlopen)

    raw = "**1. 핵심 개념**\n본문 내용\n**2. 실무 예시**"
    ok = mod.send_telegram("123", raw)

    assert ok is True
    sent = captured["text"][0]
    assert "**" not in sent           # 굵게 마커 제거됨
    assert "1. 핵심 개념" in sent      # 헤더 텍스트는 보존
    assert "본문 내용" in sent          # 본문 보존


@pytest.mark.parametrize("modname", SENDER_NAMES)
def test_send_telegram_returns_false_without_token(modname, monkeypatch):
    mod = importlib.import_module(modname)
    monkeypatch.setattr(mod, "BOT_TOKEN", None)
    assert mod.send_telegram("123", "any") is False
