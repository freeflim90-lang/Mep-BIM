#!/usr/bin/env python3
"""LUA BIM LABS Starter Plan 텔레그램 발송 — 매일 08:00 KST.

대상: 유료 글로벌 클라이언트 (USD 39/월)
언어: KO·EN·JA·ZH·AR (clients.json의 language 필드 기준, EN fallback)
커리큘럼: 90일 구조화 프로그램
  - Day 01~60: 공통 기초 (MEP BIM 기초·Revit·조정·QA)
  - Day 61~90: 전공별 심화 (hvac·piping·plumbing·fire·electrical)
  - Day 30/60/90: 마일스톤 메시지
  - 매주 금요일: BIM Check Friday 퀴즈
  - Track 완료일: 레퍼런스 카드 PDF 발송
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
from backend.core.paths import BIM_EDUCATION_DIR, STARTER_PLAN_DIR  # noqa: E402

EDU_DIR = BIM_EDUCATION_DIR
PROGRESS_FILE = EDU_DIR / "progress.json"
STARTER_CLIENTS_FILE = STARTER_PLAN_DIR / "clients.json"
STARTER_MESSAGES_DIR = STARTER_PLAN_DIR / "messages"
STARTER_FRIDAY_DIR = STARTER_PLAN_DIR / "friday_quiz"
STARTER_MILESTONE_DIR = STARTER_PLAN_DIR / "milestone_messages"
STARTER_CARDS_DIR = STARTER_PLAN_DIR / "reference_cards"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# 지원 언어: 코드 → 표시명
SUPPORTED_LANGUAGES = {
    "ko": "Korean",
    "en": "English",
    "ja": "Japanese",
    "zh": "Chinese (Simplified)",
    "ar": "Arabic",
}

DISCIPLINE_MAP = {
    "hvac": "hvac",
    "piping": "piping",
    "piping/mechanical": "piping",
    "mechanical": "piping",
    "plumbing": "plumbing",
    "plumbing/sanitary": "plumbing",
    "sanitary": "plumbing",
    "fire protection": "fire",
    "fire": "fire",
    "electrical": "electrical",
}

DISCIPLINE_DISPLAY = {
    "hvac": "HVAC",
    "piping": "Piping",
    "plumbing": "Plumbing",
    "fire": "Fire Protection",
    "electrical": "Electrical",
}

REFERENCE_CARDS = {
    7:  (1, "card_01_roles_lod.pdf",       "Card 1: MEP BIM Key Roles & LOD"),
    14: (2, "card_02_revit_setup.pdf",      "Card 2: Revit MEP Setup Checklist"),
    21: (3, "card_03_drawing_reading.pdf",  "Card 3: MEP Drawing Reading Guide"),
    28: (4, "card_04_model_quality.pdf",    "Card 4: Model Quality Self-Review"),
    38: (5, "card_05_clash_types.pdf",      "Card 5: Clash Types & Priority Matrix"),
    47: (6, "card_06_data_schedule.pdf",    "Card 6: MEP Data & Schedule Reference"),
    54: (7, "card_07_site_readiness.pdf",   "Card 7: Site-Readiness Check Guide"),
    60: (8, "card_08_learning_path.pdf",    "Card 8: BIM Learning Path & Next Steps"),
}

# 영어 fallback 마일스톤 (언어별 파일 없을 때)
MILESTONE_FALLBACK = {
    30: "🎯 30-Day Milestone — Well done!\n\nYou've completed 30 days of the MEP BIM Starter Program.\n\nLUA BIM LABS",
    60: "🏅 60-Day Certificate — Foundation Complete\n\nCongratulations, {name}!\n\nStarting Day 61 → {discipline_name} Deep-Dive\n\nLUA BIM LABS",
    90: "🎓 90 Days Complete — You did it!\n\nCongratulations, {name}!\n\nYou have completed the full 90-Day MEP BIM Starter Program.\n\nThank you for learning with LUA BIM LABS.",
}


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


def normalize_discipline(raw: str) -> str:
    return DISCIPLINE_MAP.get(raw.lower().strip(), "hvac")


def load_active_clients() -> list[dict]:
    if not STARTER_CLIENTS_FILE.exists():
        return []
    try:
        registry = json.loads(STARTER_CLIENTS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  ⚠️  clients.json 오류: {exc}")
        return []

    targets = []
    for client in registry.get("clients", []):
        if client.get("status") != "active":
            continue
        if client.get("payment_status") != "paid":
            continue
        chat_id = str(client.get("telegram_chat_id", "")).strip()
        if not chat_id:
            continue
        targets.append({
            "name": client.get("name", "Starter Client"),
            "chat_id": chat_id,
            "progress_key": f"starter:{client.get('client_id')}",
            "discipline": normalize_discipline(client.get("discipline", "hvac")),
            "language": client.get("language", "en"),
        })
    return targets


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"users": {}}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _lang_fallbacks(language: str) -> list[str]:
    return [language, "en"] if language != "en" else ["en"]


def get_message(day: int, discipline: str, language: str) -> str | None:
    for lang in _lang_fallbacks(language):
        if day >= 61:
            path = STARTER_MESSAGES_DIR / lang / discipline / f"day_{day:03d}.txt"
        else:
            path = STARTER_MESSAGES_DIR / lang / f"day_{day:03d}.txt"
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
    return None


def get_friday_quiz(day: int, language: str) -> str | None:
    week_num = min((day - 1) // 7 + 1, 13)
    for lang in _lang_fallbacks(language):
        path = STARTER_FRIDAY_DIR / lang / f"week_{week_num:02d}.txt"
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
    return None


def get_card_path(filename: str, language: str) -> Path:
    """언어별 레퍼런스 카드 PDF 경로. reference_cards/<lang>/ 우선, 없으면 영어 원본."""
    for lang in _lang_fallbacks(language):
        if lang == "en":
            break  # 영어는 루트(reference_cards/<file>)에 있음
        localized = STARTER_CARDS_DIR / lang / filename
        if localized.exists():
            return localized
    return STARTER_CARDS_DIR / filename


def get_milestone_message(day: int, name: str, discipline: str, language: str) -> str | None:
    discipline_name = DISCIPLINE_DISPLAY.get(discipline, "HVAC")
    for lang in _lang_fallbacks(language):
        path = STARTER_MILESTONE_DIR / lang / f"day_{day:03d}.txt"
        if path.exists():
            template = path.read_text(encoding="utf-8").strip()
            return template.format(name=name, discipline_name=discipline_name)
    template = MILESTONE_FALLBACK.get(day)
    if template:
        return template.format(name=name, discipline_name=discipline_name)
    return None


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


def send_document(chat_id: str, file_path: Path, caption: str = "") -> bool:
    if not BOT_TOKEN or not file_path.exists():
        return False
    boundary = "BIMBotBoundary7734"
    parts: list[bytes] = []

    def field(name: str, value: str) -> bytes:
        return (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n").encode()

    parts.append(field("chat_id", chat_id))
    if caption:
        parts.append(field("caption", caption))
    parts.append(
        (f"--{boundary}\r\nContent-Disposition: form-data; name=\"document\"; filename=\"{file_path.name}\"\r\nContent-Type: application/octet-stream\r\n\r\n").encode()
        + file_path.read_bytes() + b"\r\n"
    )
    parts.append(f"--{boundary}--\r\n".encode())
    body = b"".join(parts)
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data=body, method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"  📎 카드 전송 완료: {file_path.name}")
            return True
    except Exception as e:
        print(f"  ❌ 카드 전송 실패: {e}")
        return False


def process_client(client: dict, user_data: dict, today: str, is_friday: bool) -> dict:
    name = client["name"]
    chat_id = client["chat_id"]
    discipline = client.get("discipline", "hvac")
    language = client.get("language", "en")
    current_day = user_data.get("day", 1)

    lang_display = SUPPORTED_LANGUAGES.get(language, language.upper())
    disc_display = DISCIPLINE_DISPLAY.get(discipline, "HVAC")
    phase = f"Track ({disc_display})" if current_day >= 61 else f"Foundation Day {current_day}/60"
    print(f"\n[{name}] Starter Plan — {phase} [{lang_display}]")

    message = get_message(current_day, discipline, language)
    if not message:
        print(f"  ⚠️  {language}/day_{current_day:03d}.txt 없음 — 번역 파일 생성 필요")
        return user_data

    if not send_telegram(chat_id, message):
        return user_data

    # 금요일 퀴즈
    if is_friday and current_day <= 90:
        quiz = get_friday_quiz(current_day, language)
        if quiz:
            week = min((current_day - 1) // 7 + 1, 13)
            print(f"  📋 BIM Check Friday Week {week} 발송")
            send_telegram(chat_id, quiz)

    # 마일스톤
    milestone = get_milestone_message(current_day, name, discipline, language)
    if milestone:
        print(f"  🎯 Day {current_day} 마일스톤 발송")
        send_telegram(chat_id, milestone)

    # 레퍼런스 카드 (언어별 PDF 우선, 없으면 영어 폴백)
    if current_day in REFERENCE_CARDS:
        card_num, filename, card_title = REFERENCE_CARDS[current_day]
        send_document(chat_id, get_card_path(filename, language),
                      f"📄 Reference Card {card_num}: {card_title}")

    new_day = current_day + 1 if current_day < 90 else 90
    return {**user_data, "name": name, "chat_id": chat_id,
            "day": new_day, "last_sent": today,
            "discipline": discipline, "language": language}


def main() -> None:
    load_dotenv()
    global BOT_TOKEN
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

    clients = load_active_clients()
    if not clients:
        print("활성 Starter 클라이언트 없음.")
        return

    progress = load_progress()
    today = date.today().isoformat()
    is_friday = date.today().weekday() == 4

    if is_friday:
        print("📅 오늘은 금요일 — BIM Check Friday 퀴즈 발송")

    for client in clients:
        key = client["progress_key"]
        user_data = progress.get("users", {}).get(key, {})
        # 같은 날 중복 발송 방지(다른 발송기/재실행과 progress.json 공유).
        if user_data.get("last_sent") == today:
            print(f"  ⏭  {client.get('name', key)}: 오늘 이미 발송됨 — 건너뜀")
            continue
        updated = process_client(client, user_data, today, is_friday)
        progress.setdefault("users", {})[key] = updated

    save_progress(progress)
    print("\n✅ Starter Plan 발송 완료")


if __name__ == "__main__":
    main()
