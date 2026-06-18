#!/usr/bin/env python3
"""부팅 시 누락 루틴 따라잡기.

Mac이 일일 루틴 예약 시각(00:00~13:00)에 꺼져 있거나 잠들어 있어 launchd가
건너뛴 경우, 맥이 다시 켜질 때(로그인) 이 스크립트가 RunAtLoad로 실행되어
'예약 시각이 이미 지났는데 오늘 실행 흔적이 없는' 루틴을 골라 수동 실행한다.

판정은 각 루틴의 산출물(완료 마커 / 발행 로그 / launchd out.log mtime)을 보고
'오늘 실행됐는가'를 확인하므로, 이미 정상 실행된 루틴은 다시 돌리지 않는다(멱등).

com.luabimlab.routine-catchup LaunchAgent(RunAtLoad)가 실행한다.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys  # noqa: E402
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import BIM_EDUCATION_DIR  # noqa: E402

LOG_DIR = PROJECT_ROOT / "logs"
CATCHUP_LOG = LOG_DIR / "routine_catchup.log"

# 부팅 직후 네트워크/데몬(tailscale, cloudflared 등)이 올라올 시간을 준다.
STARTUP_DELAY_SEC = 45
# 작업 루틴 kickstart 후 체크리스트 발송까지 대기(다른 루틴이 어느 정도 진행되도록).
CHECKLIST_DELAY_SEC = 120


# ── 공통 헬퍼 ──────────────────────────────────────────────────────

def _log(msg: str) -> None:
    line = f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}"
    print(line, flush=True)
    try:
        with CATCHUP_LOG.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


def load_dotenv() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _ran_today_mtime(path: Path, today: date) -> bool:
    """launchd out.log 등 산출 파일이 오늘 갱신됐으면 True."""
    if not path.exists():
        return False
    return date.fromtimestamp(path.stat().st_mtime) >= today


def _log_has_today(path: Path, today_str: str) -> bool:
    if not path.exists():
        return False
    try:
        return today_str in path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False


# ── 루틴별 '오늘 완료됐는가' 판정 ───────────────────────────────────

def _done_ku(today: date, today_str: str) -> bool:
    marker = LOG_DIR / f".daily_knowledge_update_done_{today_str}"
    return marker.exists() or _ran_today_mtime(
        LOG_DIR / "daily_knowledge_update.launchd.out.log", today
    )


def _done_sync(today: date, today_str: str) -> bool:
    return _log_has_today(LOG_DIR / "sync_knowledge.log", today_str)


def _done_edu(today: date, today_str: str) -> bool:
    # Starter(유료) 교육: launchd가 오늘 실행했으면 완료(대상 0명이어도 정상 실행).
    return _ran_today_mtime(LOG_DIR / "bim_education_daily.out.log", today)


def _done_internal_edu(today: date, today_str: str) -> bool:
    # 내부 직원 교육: progress.json 전원 오늘 발송 또는 launchd 오늘 실행.
    prog = BIM_EDUCATION_DIR / "progress.json"
    if prog.exists():
        try:
            users = json.loads(prog.read_text(encoding="utf-8")).get("users", {})
            if users and all(v.get("last_sent") == today_str for v in users.values()):
                return True
        except Exception:
            pass
    return _ran_today_mtime(LOG_DIR / "internal_education_daily.out.log", today)


def _done_blog(today: date, today_str: str) -> bool:
    publish_log = LOG_DIR / "blogger_daily_publish.jsonl"
    if not publish_log.exists():
        return False
    try:
        for raw in publish_log.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not raw.strip():
                continue
            row = json.loads(raw)
            if row.get("date") == today_str and row.get("url"):
                return True
    except Exception:
        return False
    return False


def _done_growth(today: date, today_str: str) -> bool:
    return _log_has_today(LOG_DIR / "internal_self_growth_loop.log", today_str)


def _done_qwen(today: date, today_str: str) -> bool:
    return _ran_today_mtime(LOG_DIR / "qwen_product_draft_daily.launchd.out.log", today)


def _done_checklist(today: date, today_str: str) -> bool:
    return _ran_today_mtime(LOG_DIR / "daily_routine_checklist.out.log", today)


# key, 표시명, 라벨, (hour, minute), 완료판정, 체크리스트여부
ROUTINES = [
    ("ku",       "지식 업데이트",        "com.luabimlab.daily-knowledge-update",   (0, 0),  _done_ku,           False),
    ("sync",     "지식 동기화",          "com.luabimlabs.sync-knowledge",          (3, 0),  _done_sync,         False),
    ("edu",      "BIM 교육(Starter)",    "com.luabimlab.bim-education-daily",       (7, 0),  _done_edu,          False),
    ("internal", "BIM 교육(내부직원)",   "com.luabimlab.internal-education-daily",  (7, 0),  _done_internal_edu, False),
    ("blog",     "블로거 포스트 발행",   "com.luabimlab.daily-blogger-post",        (8, 0),  _done_blog,         False),
    ("growth",   "내부 자기 성장 루프",  "com.luabimlab.internal-self-growth-loop", (8, 0),  _done_growth,       False),
    ("qwen",     "Qwen 제품 드래프트",   "com.luabimlab.qwen-product-draft-daily",  (8, 20), _done_qwen,         False),
    ("checklist","루틴 체크리스트 발송", "com.luabimlab.daily-routine-checklist",   (13, 0), _done_checklist,    True),
]


def kickstart(label: str) -> bool:
    uid = os.getuid()
    result = subprocess.run(
        ["launchctl", "kickstart", f"gui/{uid}/{label}"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        return True
    _log(f"  ⚠️ kickstart 실패 {label}: rc={result.returncode} {result.stderr.strip()}")
    return False


def send_telegram(text: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return
    payload = urllib.parse.urlencode(
        {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    ).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage", data=payload, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            _log(f"  텔레그램 status={r.status}")
    except Exception as exc:
        _log(f"  텔레그램 발송 실패: {exc}")


def main() -> None:
    load_dotenv()
    _log("=== 부팅 따라잡기 시작 ===")
    if STARTUP_DELAY_SEC:
        time.sleep(STARTUP_DELAY_SEC)

    today = date.today()
    today_str = today.isoformat()
    now = datetime.now()

    caught: list[str] = []
    checklist_pending = False

    for key, name, label, (hh, mm), done_fn, is_checklist in ROUTINES:
        scheduled = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
        if now < scheduled:
            continue  # 아직 예약 시각 전 → launchd가 정시에 실행. 건드리지 않음.
        try:
            if done_fn(today, today_str):
                continue  # 이미 오늘 실행됨.
        except Exception as exc:
            _log(f"  판정 오류 {key}: {exc} → 건너뜀")
            continue

        if is_checklist:
            checklist_pending = True  # 체크리스트는 마지막에 따로 처리.
            continue

        _log(f"  ▶ 누락 감지 → 수동 실행: {name} ({label})")
        if kickstart(label):
            caught.append(name)

    # 작업 루틴을 어느 정도 진행시킨 뒤 체크리스트 발송(누락이었던 경우).
    if caught:
        _log(f"따라잡기 {len(caught)}건 실행, 체크리스트 발송까지 {CHECKLIST_DELAY_SEC}s 대기")
        time.sleep(CHECKLIST_DELAY_SEC)

    if checklist_pending:
        _log("  ▶ 체크리스트 발송 따라잡기")
        kickstart("com.luabimlab.daily-routine-checklist")

    if caught:
        body = "🔁 <b>부팅 따라잡기</b> — 누락 루틴 수동 실행\n" + "\n".join(
            f"• {n}" for n in caught
        )
        send_telegram(body)
    else:
        _log("누락 루틴 없음 — 따라잡기 불필요")

    _log("=== 부팅 따라잡기 종료 ===")


if __name__ == "__main__":
    main()
