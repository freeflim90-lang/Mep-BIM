"""send_internal.py 중복 발송 방지 가드 회귀 테스트.

배경(2026-06-24): 발송기에 last_sent==today 스킵 가드가 없어, 부팅
routine-catchup 등으로 같은 날 재실행되면 활성 사용자에게 이중 발송+day
2배 증가 위험이 있었음. main()에 가드를 추가. 이 테스트는 '오늘 이미
발송된 사용자는 다시 보내지 않고, 아직이면 보낸다'를 고정한다.
"""

import importlib
from datetime import date

import pytest

si = importlib.import_module("scripts.bim_education.send_internal")


def _run_main_with(monkeypatch, last_sent_value):
    """USERS 전원이 last_sent=last_sent_value 인 progress로 main()을 돌리고,
    send_telegram 호출 횟수와 저장된 progress를 돌려준다."""
    today = date.today().isoformat()
    progress = {"users": {u["name"]: {
        "name": u["name"], "chat_id": u["chat_id"],
        "track": "1yr", "day": 30, "last_sent": last_sent_value,
    } for u in si.USERS}}

    sent = []
    saved = {}
    monkeypatch.setattr(si, "load_dotenv", lambda: None)
    monkeypatch.setattr(si, "BOT_TOKEN", "T", raising=False)
    monkeypatch.setattr(si, "load_progress", lambda: progress)
    monkeypatch.setattr(si, "save_progress", lambda p: saved.update(p))
    monkeypatch.setattr(si, "send_telegram", lambda chat_id, text: sent.append(chat_id) or True)
    # 메시지 파일이 없어도 발송 분기를 타도록 get_message를 고정
    monkeypatch.setattr(si, "get_message", lambda track, day: "📚 테스트 메시지")

    si.main()
    return today, sent, saved


def test_skips_users_already_sent_today(monkeypatch):
    today, sent, saved = _run_main_with(monkeypatch, last_sent_value=date.today().isoformat())
    # 오늘 이미 발송 → 아무에게도 다시 보내지 않음
    assert sent == []
    # day도 그대로(증가 안 함)
    for u in si.USERS:
        assert saved["users"][u["name"]]["day"] == 30


def test_sends_when_not_sent_today(monkeypatch):
    today, sent, saved = _run_main_with(monkeypatch, last_sent_value="2000-01-01")
    # 아직 안 보냄 → 전원 발송 + day 증가 + last_sent 갱신
    assert len(sent) == len(si.USERS)
    for u in si.USERS:
        assert saved["users"][u["name"]]["day"] == 31
        assert saved["users"][u["name"]]["last_sent"] == today
