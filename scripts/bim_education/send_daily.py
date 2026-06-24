#!/usr/bin/env python3
"""BIM 일일 교육 텔레그램 발송 — 매일 8시 KST LaunchAgent가 실행.

Starter Plan (90일) + 내부 직원 연간 커리큘럼 지원.
- Day 61+ : 클라이언트 discipline별 Track 9 레슨 발송
- Day 30/60/90 : 마일스톤 메시지 자동 발송
- 매주 금요일 : BIM Check Friday 퀴즈 추가 발송
- Track 완료일 : 레퍼런스 카드 PDF 발송
- 다국어 지원 : 클라이언트 언어(language 필드)에 따라 메시지 선택, 영어 fallback
"""

from __future__ import annotations

import json
import os
import sys
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
MESSAGES_DIR = EDU_DIR / "messages"
PROGRESS_FILE = EDU_DIR / "progress.json"
STARTER_CLIENTS_FILE = STARTER_PLAN_DIR / "clients.json"
STARTER_MESSAGES_DIR = STARTER_PLAN_DIR / "messages"
STARTER_FRIDAY_DIR = STARTER_PLAN_DIR / "friday_quiz"
STARTER_MILESTONE_DIR = STARTER_PLAN_DIR / "milestone_messages"
STARTER_CARDS_DIR = STARTER_PLAN_DIR / "reference_cards"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

TRACK_ORDER = ["1yr", "2yr", "3yr", "4yr", "5yr", "6yr", "7yr", "8yr", "9yr", "10yr"]

# Supported languages: code → display name
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

# Track 완료일 → 레퍼런스 카드 번호 및 파일명
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

# English milestone messages (fallback if language-specific file not found)
MILESTONE_MESSAGES = {
    30: """🎯 30-Day Milestone — Well done!

You've completed 30 days of the MEP BIM Starter Program.

So far you've covered:
✓ MEP BIM orientation and roles
✓ Revit MEP setup and modeling basics
✓ MEP drawing and system reading
✓ Model quality fundamentals

Keep going — you're one third of the way through the Foundation curriculum.

Day 31 begins the Clash Coordination module.

LUA BIM LABS""",

    60: """🏅 60-Day Certificate — Foundation Complete

Congratulations, {name}!

You have completed the 60-Day MEP BIM Foundation Program.

Your 60-day completion certificate has been issued separately.

Starting Day 61, your lessons shift to your chosen discipline:
→ {discipline_name} Deep-Dive

This specialist track continues through Day 90.

LUA BIM LABS""",

    90: """🎓 90 Days Complete — You did it!

Congratulations, {name}!

You have completed the full 90-Day MEP BIM Starter Program.

You've built a solid foundation across:
✓ MEP BIM orientation and workflows
✓ Revit MEP basics and model quality
✓ Clash coordination fundamentals
✓ Data and schedule management
✓ Site-readiness thinking
✓ {discipline_name} discipline deep-dive

Your 90-day completion certificate has been issued separately.

What's next:

Personal Tutor — USD 119/month
- Personalized level diagnosis
- Custom daily lessons matched to your level
- Monthly written progress report
- Level check and advancement tracking
- Discipline-specific scenario lessons
- Coming Soon

Reply here if you're interested in continuing with Personal Tutor.

Thank you for learning with LUA BIM LABS.""",
}

# 내부 직원 교육은 send_internal.py (internal-education-daily LaunchAgent)가 전담.
# 이 스크립트는 Starter 클라이언트 전용.


# ---------------------------------------------------------------------------
# 환경 로딩
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


# ---------------------------------------------------------------------------
# 클라이언트 로딩
# ---------------------------------------------------------------------------

def normalize_discipline(raw: str) -> str:
    return DISCIPLINE_MAP.get(raw.lower().strip(), "hvac")


def load_active_starter_clients() -> list[dict]:
    if not STARTER_CLIENTS_FILE.exists():
        return []
    try:
        registry = json.loads(STARTER_CLIENTS_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"  ⚠️  Starter client registry 오류: {exc}")
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
        raw_discipline = client.get("discipline", "hvac")
        targets.append({
            "name": client.get("name", "Starter Client"),
            "chat_id": chat_id,
            "track": "starter",
            "progress_key": f"starter:{client.get('client_id')}",
            "discipline": normalize_discipline(raw_discipline),
            "language": client.get("language", "en"),
        })
    return targets


# ---------------------------------------------------------------------------
# 진도 관리
# ---------------------------------------------------------------------------

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text(encoding="utf-8"))
    return {"users": {}}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def next_track(current: str) -> str | None:
    idx = TRACK_ORDER.index(current)
    return TRACK_ORDER[idx + 1] if idx + 1 < len(TRACK_ORDER) else None


# ---------------------------------------------------------------------------
# 메시지 조회 (다국어 지원)
# ---------------------------------------------------------------------------

def _lang_fallbacks(language: str) -> list[str]:
    """Try requested language first, then English."""
    return [language, "en"] if language != "en" else ["en"]


def get_message(track: str, day: int, discipline: str = "hvac", language: str = "en") -> str | None:
    if track != "starter":
        # 내부 직원 트랙은 언어 구분 없이 기존 경로 사용 (한국어)
        msg_file = MESSAGES_DIR / track / f"day_{day:03d}.txt"
        return msg_file.read_text(encoding="utf-8").strip() if msg_file.exists() else None

    for lang in _lang_fallbacks(language):
        if day >= 61:
            msg_file = STARTER_MESSAGES_DIR / lang / discipline / f"day_{day:03d}.txt"
        else:
            msg_file = STARTER_MESSAGES_DIR / lang / f"day_{day:03d}.txt"
        if msg_file.exists():
            return msg_file.read_text(encoding="utf-8").strip()
    return None


def get_friday_quiz(current_day: int, language: str = "en") -> str | None:
    week_num = min((current_day - 1) // 7 + 1, 13)
    for lang in _lang_fallbacks(language):
        quiz_file = STARTER_FRIDAY_DIR / lang / f"week_{week_num:02d}.txt"
        if quiz_file.exists():
            return quiz_file.read_text(encoding="utf-8").strip()
    return None


def get_card_path(filename: str, language: str = "en") -> Path:
    """언어별 레퍼런스 카드 PDF 경로. reference_cards/<lang>/ 우선, 없으면 영어 원본."""
    for lang in _lang_fallbacks(language):
        if lang == "en":
            break  # 영어는 루트(reference_cards/<file>)에 있음
        localized = STARTER_CARDS_DIR / lang / filename
        if localized.exists():
            return localized
    return STARTER_CARDS_DIR / filename


def get_milestone_message(day: int, name: str, discipline: str, language: str = "en") -> str | None:
    """언어별 마일스톤 파일 로드, 없으면 영어 fallback."""
    discipline_name = DISCIPLINE_DISPLAY.get(discipline, "HVAC")

    for lang in _lang_fallbacks(language):
        msg_file = STARTER_MILESTONE_DIR / lang / f"day_{day:03d}.txt"
        if msg_file.exists():
            template = msg_file.read_text(encoding="utf-8").strip()
            return template.format(name=name, discipline_name=discipline_name)

    # 파일이 없을 경우 코드 내 영어 fallback
    template = MILESTONE_MESSAGES.get(day)
    if not template:
        return None
    return template.format(name=name, discipline_name=discipline_name)


# ---------------------------------------------------------------------------
# Telegram API
# ---------------------------------------------------------------------------

def send_telegram(chat_id: str, text: str) -> bool:
    if not BOT_TOKEN:
        print("  ⚠️  TELEGRAM_BOT_TOKEN 없음")
        return False
    # 평문 발송(parse_mode 미사용)이라 마크다운 '**'가 글자 그대로 노출됨 → 제거.
    text = text.replace("**", "")
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
    if not BOT_TOKEN:
        return False
    if not file_path.exists():
        print(f"  ⚠️  파일 없음 (PDF 미생성): {file_path.name}")
        return False

    boundary = "BIMBotBoundary7734"
    body_parts: list[bytes] = []

    def field(name: str, value: str) -> bytes:
        return (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n"
        ).encode("utf-8")

    body_parts.append(field("chat_id", chat_id))
    if caption:
        body_parts.append(field("caption", caption))

    file_bytes = file_path.read_bytes()
    body_parts.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="document"; filename="{file_path.name}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode("utf-8")
        + file_bytes
        + b"\r\n"
    )
    body_parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(body_parts)

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"  📎 카드 전송 완료: {file_path.name} (status={resp.status})")
            return True
    except Exception as e:
        print(f"  ❌ 카드 전송 실패: {e}")
        return False


# ---------------------------------------------------------------------------
# Starter 클라이언트 처리
# ---------------------------------------------------------------------------

def process_starter_client(
    user: dict,
    user_data: dict,
    progress: dict,
    today: str,
    is_friday_today: bool,
) -> dict:
    name = user["name"]
    chat_id = user["chat_id"]
    progress_key = user["progress_key"]
    discipline = user.get("discipline", "hvac")
    language = user.get("language", "en")

    track = user_data.get("track", "starter")
    current_day = user_data.get("day", 1)

    disc_display = DISCIPLINE_DISPLAY.get(discipline, "HVAC")
    track_label = f"Track 9 ({disc_display})" if current_day >= 61 else f"Day {current_day}/60"
    lang_display = SUPPORTED_LANGUAGES.get(language, language.upper())
    print(f"\n[{name}] Starter Plan {track_label} — Day {current_day} [{lang_display}]")

    # 레슨 발송
    message = get_message(track, current_day, discipline, language)
    if not message:
        if current_day >= 61:
            print(f"  ⚠️  {language}/track9/{discipline}/day_{current_day:03d}.txt 없음 — 번역 생성 필요")
        else:
            print(f"  ⚠️  {language}/day_{current_day:03d}.txt 없음 — 번역 생성 필요")
        return user_data

    sent = send_telegram(chat_id, message)
    if not sent:
        return user_data

    # BIM Check Friday 추가 발송
    if is_friday_today and current_day <= 90:
        quiz = get_friday_quiz(current_day, language)
        if quiz:
            print(f"  📋 BIM Check Friday 발송 (Week {min((current_day - 1) // 7 + 1, 13)})")
            send_telegram(chat_id, quiz)
        else:
            print(f"  ⚠️  BIM Check Friday 퀴즈 없음 ({language}/week_{min((current_day - 1) // 7 + 1, 13):02d}.txt)")

    # 마일스톤 메시지 발송
    milestone_msg = get_milestone_message(current_day, name, discipline, language)
    if milestone_msg:
        print(f"  🎯 Day {current_day} 마일스톤 메시지 발송")
        send_telegram(chat_id, milestone_msg)

    # 레퍼런스 카드 발송 (언어별 PDF 우선, 없으면 영어 폴백)
    if current_day in REFERENCE_CARDS:
        card_num, filename, card_title = REFERENCE_CARDS[current_day]
        card_path = get_card_path(filename, language)
        caption = f"📄 Quick Reference Card {card_num}: {card_title}"
        print(f"  📎 레퍼런스 카드 {card_num} 발송 시도")
        send_document(chat_id, card_path, caption)

    # 진도 업데이트
    new_day = current_day + 1 if current_day < 90 else 90
    return {
        **user_data,
        "name": name,
        "chat_id": chat_id,
        "track": track,
        "day": new_day,
        "last_sent": today,
        "discipline": discipline,
        "language": language,
    }


# ---------------------------------------------------------------------------
# 메인
# ---------------------------------------------------------------------------

def main() -> None:
    load_dotenv()
    global BOT_TOKEN
    BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

    progress = load_progress()
    today = date.today().isoformat()
    is_friday_today = date.today().weekday() == 4

    if is_friday_today:
        print("📅 오늘은 금요일 — BIM Check Friday 퀴즈 자동 발송")

    users = load_active_starter_clients()

    if not users:
        # 내부 직원 교육은 send_internal.py 가 전담하므로, 활성 유료 Starter
        # 클라이언트가 없으면 이 스크립트는 발송할 대상이 없다. 수동 실행 시
        # "발송 완료"로 오인하지 않도록 명시한다.
        print("ℹ️  활성 유료 Starter 클라이언트 없음 — 발송 대상 0명 "
              "(내부 직원 교육은 send_internal.py 담당)")
        return

    for user in users:
        name = user["name"]
        progress_key = user.get("progress_key", name)

        user_data = progress.get("users", {}).get(progress_key, {})
        # 같은 날 중복 발송 방지(send_starter.py와 progress.json·키 공유).
        if user_data.get("last_sent") == today:
            print(f"  ⏭  {name}: 오늘 이미 발송됨 — 건너뜀")
            continue

        updated = process_starter_client(user, user_data, progress, today, is_friday_today)
        progress.setdefault("users", {})[progress_key] = updated

    save_progress(progress)
    print("\n✅ 발송 완료")


if __name__ == "__main__":
    main()
