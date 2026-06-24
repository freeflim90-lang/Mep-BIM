#!/usr/bin/env python3
"""내부 직원 BIM 교육 텔레그램 발송 — 매일 07:00 KST.

대상: LUA BIM LABS 내부 직원 (1yr~20yr 연간 커리큘럼)
언어: 한국어 전용
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
import sys as _sys  # noqa: E402
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import BIM_EDUCATION_DIR  # noqa: E402

EDU_DIR = BIM_EDUCATION_DIR
MESSAGES_DIR = EDU_DIR / "messages"
PROGRESS_FILE = EDU_DIR / "progress.json"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

TRACK_ORDER = [
    "1yr", "2yr", "3yr", "4yr", "5yr",
    "6yr", "7yr", "8yr", "9yr", "10yr",
    "11yr", "12yr", "13yr", "14yr", "15yr",
    "16yr", "17yr", "18yr", "19yr", "20yr",
]

# 내부 직원 목록 (조서희 관리팀 제외)
USERS = [
    {"name": "최정연", "chat_id": "7899169126", "track": "1yr"},
    {"name": "오수빈", "chat_id": "8579787318", "track": "1yr"},
    {"name": "김선정", "chat_id": "8420202032", "track": "1yr"},
    {"name": "허진석", "chat_id": "8721440825", "track": "1yr"},
]


# ---------------------------------------------------------------------------

def load_dotenv() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"users": {}}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def next_track(current: str) -> str | None:
    try:
        idx = TRACK_ORDER.index(current)
    except ValueError:
        return None
    return TRACK_ORDER[idx + 1] if idx + 1 < len(TRACK_ORDER) else None


def get_message(track: str, day: int) -> str | None:
    msg_file = MESSAGES_DIR / track / f"day_{day:03d}.txt"
    return msg_file.read_text(encoding="utf-8").strip() if msg_file.exists() else None


def send_telegram(chat_id: str, text: str) -> bool:
    if not BOT_TOKEN:
        print("  ⚠️  TELEGRAM_BOT_TOKEN 없음")
        return False
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data=payload, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  ✅ 전송 완료 (status={resp.status})")
            return True
    except Exception as e:
        print(f"  ❌ 전송 실패: {e}")
        return False


def main() -> None:
    load_dotenv()
    global BOT_TOKEN
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

    progress = load_progress()
    today = date.today().isoformat()

    for user in USERS:
        name = user["name"]
        chat_id = user["chat_id"]

        user_data = progress.get("users", {}).get(name, {})
        track = user_data.get("track", user["track"])
        current_day = user_data.get("day", 1)
        yr_num = track.replace("yr", "")

        # 같은 날 중복 발송 방지(부팅 catchup 재실행 등으로 하루 2회 도는 사고 차단).
        if user_data.get("last_sent") == today:
            print(f"[{name}] 오늘 이미 발송됨 — 건너뜀")
            continue

        print(f"\n[{name}] {yr_num}년차 커리큘럼 Day {current_day}/365")

        message = get_message(track, current_day)
        if not message:
            print(f"  ⚠️  {track}/day_{current_day:03d}.txt 없음 — generate.py 실행 필요")
            continue

        if send_telegram(chat_id, message):
            if current_day >= 365:
                nxt = next_track(track)
                if nxt:
                    new_track, new_day = nxt, 1
                    print(f"  🎓 {yr_num}년차 완료 → {nxt.replace('yr', '')}년차 승급!")
                else:
                    new_track, new_day = track, current_day
                    print("  🏆 20년차 완주! BIM 그랜드마스터 달성!")
            else:
                new_track, new_day = track, current_day + 1

            progress.setdefault("users", {})[name] = {
                **user_data,
                "name": name,
                "chat_id": chat_id,
                "track": new_track,
                "day": new_day,
                "last_sent": today,
            }

    save_progress(progress)
    print("\n✅ 내부 직원 교육 발송 완료")


if __name__ == "__main__":
    main()
