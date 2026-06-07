#!/usr/bin/env python3
"""오늘의 Qwen 드래프트 아이템 5개를 텔레그램으로 사전 요약 발송."""

from __future__ import annotations

import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
QUEUE_FILE = PROJECT_ROOT / "config" / "qwen_product_draft_queue.json"


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


def send_telegram(text: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("telegram=skipped TELEGRAM 환경변수 없음")
        return False
    MAX = 4000
    chunks = [text[i:i + MAX] for i in range(0, len(text), MAX)]
    ok = True
    for i, chunk in enumerate(chunks):
        payload = urllib.parse.urlencode(
            {"chat_id": chat_id, "text": chunk, "parse_mode": "HTML"}
        ).encode("utf-8")
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload, method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                print(f"  [{i + 1}/{len(chunks)}] status={r.status}")
        except Exception as exc:
            print(f"  [{i + 1}/{len(chunks)}] ERROR: {exc}")
            ok = False
    return ok


def build_message(today: dt.date, tasks: list[dict]) -> str:
    date_id = today.strftime("%Y%m%d")
    today_tasks = [t for t in tasks if t.get("id", "").startswith(f"ADDIN-IDEA-{date_id}-")]

    if not today_tasks:
        return f"[LUA BIM LABS] {today.isoformat()} Qwen 드래프트 아이템 없음"

    lines = [
        f"🛠 <b>오늘의 Qwen Coder 개발 {len(today_tasks)}개 아이템 ({today.isoformat()})</b>",
        "Qwen Coder가 오늘 초안 작업할 Revit/Navisworks Add-in MVP 목록입니다.",
        "",
    ]

    for idx, task in enumerate(today_tasks, start=1):
        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append(f"<b>{'①②③④⑤⑥⑦⑧⑨⑩'[idx-1]} {task['id']}</b>")
        lines.append(f"📦 {task['title']}")
        lines.append(f"🔧 기능: {task.get('deliverable', '-')}")
        lines.append(f"🎯 개발 범위: {task.get('scope', '-')}")
        lines.append("")

    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("📧 이메일 제목 형식: [LUA BIM LABS] 코드 개발 초안 보고 - {아이템ID} {아이템명}")
    return "\n".join(lines)


def main() -> int:
    load_dotenv()
    today = dt.date.today()
    if not QUEUE_FILE.exists():
        print("queue=not_found")
        return 1

    queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    tasks = queue.get("tasks", [])
    msg = build_message(today, tasks)
    print(msg)
    print("\nTelegram 발송 중...")
    send_telegram(msg)
    print("완료.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
