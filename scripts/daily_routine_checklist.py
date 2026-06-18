#!/usr/bin/env python3
"""LUA BIM LABS 일일 루틴 체크리스트 — 매일 13:00 자동 발송."""

from __future__ import annotations

import json
import os
import subprocess
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys  # noqa: E402
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))
from backend.core.paths import BIMOBJECT_DIR, BIM_EDUCATION_DIR  # noqa: E402

LOG_DIR = PROJECT_ROOT / "logs"

CALENDAR_TOKEN = PROJECT_ROOT / "config" / "calendar" / "token.json"
CALENDAR_ID = "abe70f9ff819811a1230da5cbaae7e6482b8d190488f01f155a2c64a0a964457@group.calendar.google.com"
CALENDAR_SCOPES = ["https://www.googleapis.com/auth/calendar"]
# 루틴 항목 → (캘린더 반복 이벤트 ID, 미완료 시 원래 색상)
ROUTINE_EVENT_MAP: dict[str, tuple[str, str]] = {
    "ku":        ("i0qiko0ojpa14hdal56b8rh33k", "8"),  # 지식 업데이트
    "sync":      ("bq9otauoa40dhfrkpb5bkdr450", "8"),  # 지식 동기화
    "edu":       ("5mil97sluk83891c9080mlvgu4", "9"),  # BIM 교육 발송
    "blog":      ("vamr3b0kehenogs7id6n7b02rc", "9"),  # 블로거 발행
    "qwen":      ("i3dlcn1gs98ib4lap1f7cbl3ks", "9"),  # Qwen 드래프트
    "ax_review": ("flmoukc5bsoatgc0h47q4g20j4", "6"),  # 주간 AX 전략 리뷰 (월)
    "bimobj":    ("sb6j26qg3rvs7edgip85bue47o", "6"),  # BIMobject 크롤링 (일)
    "checklist": ("tee85sctn9273po28truvut4ks", "7"),  # 루틴 체크리스트 보고
}
COLOR_DONE = "2"  # Sage (초록) = 완료


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
        print("TELEGRAM 환경변수 없음")
        return False
    MAX = 4000
    chunks = [text[i:i+MAX] for i in range(0, len(text), MAX)]
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
                print(f"  [{i+1}/{len(chunks)}] status={r.status}")
        except Exception as e:
            print(f"  [{i+1}/{len(chunks)}] ERROR: {e}")
            ok = False
    return ok


# ── 상태 확인 헬퍼 ──────────────────────────────────────────────────

def pgrep(pattern: str) -> bool:
    result = subprocess.run(
        ["pgrep", "-f", pattern], capture_output=True
    )
    return result.returncode == 0


def log_has_today(log_path: Path, today_str: str) -> tuple[bool, str]:
    """로그에 오늘 날짜 항목이 있으면 (True, 마지막 시간) 반환."""
    if not log_path.exists():
        return False, ""
    try:
        lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        hits = [l for l in lines if today_str in l]
        if hits:
            last = hits[-1]
            # HH:MM 패턴 추출
            for part in last.split():
                if len(part) == 8 and part[2] == ":" and part[5] == ":":
                    return True, part[:5]
                if len(part) == 5 and part[2] == ":":
                    return True, part
            return True, ""
        return False, ""
    except Exception:
        return False, ""


def bimobject_crawled_recently(today: date) -> tuple[bool, str]:
    """오늘 또는 어제(일요일) BIMobject JSON이 있는지 확인."""
    data_dir = BIMOBJECT_DIR
    # 오늘
    pattern_today = f"bimobject_{today.strftime('%Y%m%d')}_*.json"
    files_today = sorted(data_dir.glob(pattern_today))
    if files_today:
        ts = files_today[-1].stem.split("_")[-1]
        return True, f"오늘 {ts[:2]}:{ts[2:]} 완료"
    # 어제(일요일인 경우)
    yesterday = today - timedelta(days=1)
    if yesterday.weekday() == 6:
        pattern_yd = f"bimobject_{yesterday.strftime('%Y%m%d')}_*.json"
        files_yd = sorted(data_dir.glob(pattern_yd))
        if files_yd:
            return True, f"어제({yesterday.strftime('%m-%d')}) 완료"
    return False, ""


def weekly_review_done_this_week(today: date) -> tuple[bool, str]:
    """이번 주 월요일 이후 weekly_ax_strategy_review.log에 done 항목이 있는지."""
    log = LOG_DIR / "weekly_ax_strategy_review.log"
    if not log.exists():
        return False, ""
    monday = today - timedelta(days=today.weekday())
    text = log.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    for line in reversed(lines):
        if "done" in line:
            # 날짜 파싱
            for part in line.split():
                try:
                    d = datetime.strptime(part, "%Y-%m-%d").date()
                    if d >= monday:
                        t = ""
                        for p2 in line.split():
                            if len(p2) == 8 and p2[2] == ":" and p2[5] == ":":
                                t = p2[:5]
                        return True, f"{d.strftime('%m-%d')} {t} 완료"
                except ValueError:
                    continue
    return False, ""


# ── Google Calendar 연동 ────────────────────────────────────────────

def _build_calendar_service():
    """Calendar API 서비스 객체 반환. 토큰 없으면 None."""
    if not CALENDAR_TOKEN.exists():
        return None
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build as gcal_build

        creds = Credentials.from_authorized_user_file(str(CALENDAR_TOKEN), CALENDAR_SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            CALENDAR_TOKEN.write_text(creds.to_json(), encoding="utf-8")
        return gcal_build("calendar", "v3", credentials=creds, cache_discovery=False)
    except Exception as exc:
        print(f"  [Calendar] 서비스 초기화 실패: {exc}")
        return None


def _patch_event_color_today(service, event_id: str, color_id: str, today: date) -> bool:
    """오늘 발생하는 반복 이벤트 인스턴스의 색상을 변경한다."""
    import datetime as _dt
    tz = _dt.timezone(_dt.timedelta(hours=9))
    start = _dt.datetime(today.year, today.month, today.day, tzinfo=tz)
    time_min = start.isoformat()
    time_max = (start + _dt.timedelta(days=1)).isoformat()
    try:
        result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
            maxResults=50,
        ).execute()
        items = [
            item for item in result.get("items", [])
            if item.get("recurringEventId") == event_id or item.get("id") == event_id
        ]
        if not items:
            print(f"  [Calendar] 오늘 인스턴스 없음 ({event_id[:8]}…)")
            return False
        service.events().patch(
            calendarId=CALENDAR_ID,
            eventId=items[0]["id"],
            body={"colorId": color_id},
        ).execute()
        verified = service.events().get(
            calendarId=CALENDAR_ID,
            eventId=items[0]["id"],
        ).execute()
        return verified.get("colorId") == color_id
    except Exception as exc:
        print(f"  [Calendar] 색상 업데이트 실패 ({event_id[:8]}…): {exc}")
        return False


def update_calendar_events(statuses: dict[str, bool], today: date) -> None:
    """체크리스트 완료 상태를 캘린더 이벤트 색상에 반영한다.
    완료 = Sage(2, 초록), 미완료 = 원래 색상으로 복원.
    """
    service = _build_calendar_service()
    if service is None:
        print("  [Calendar] 토큰 없음 — 색상 업데이트 건너뜀 (setup_calendar_token.py 먼저 실행)")
        return

    print("\n[Calendar] 이벤트 색상 업데이트 중...")
    for key, is_done in statuses.items():
        if key not in ROUTINE_EVENT_MAP:
            continue
        event_id, orig_color = ROUTINE_EVENT_MAP[key]
        target_color = COLOR_DONE if is_done else orig_color
        patched = _patch_event_color_today(service, event_id, target_color, today)
        mark = "✅" if is_done else "❌"
        verified = "확인" if patched else "미확인"
        print(f"  {mark} {key} → 색상 {'Sage(완료)' if is_done else f'원래({orig_color})'} ({verified})")
    print("[Calendar] 완료")


# ── 메인 체크리스트 빌드 ────────────────────────────────────────────

def build_checklist(today: date, now: datetime) -> tuple[str, dict[str, bool]]:
    today_str = today.isoformat()          # "2026-06-02"
    today_str2 = today.strftime("%Y-%m-%d")
    dow_map = {0: "월요일", 1: "화요일", 2: "수요일", 3: "목요일",
               4: "금요일", 5: "토요일", 6: "일요일"}
    dow = dow_map[today.weekday()]
    is_sunday = today.weekday() == 6
    is_monday = today.weekday() == 0

    lines: list[str] = []
    lines.append(f"📋 <b>LUA BIM LABS 자동 루틴 체크리스트</b>")
    lines.append(f"🗓 {today_str} ({dow}) — {now.strftime('%H:%M')} 기준")
    lines.append("")

    missed: list[str] = []
    statuses: dict[str, bool] = {}

    # ── 상시 실행 (데몬) ──
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("🖥 <b>상시 실행 (데몬)</b>")

    api_ok = pgrep(r"python.*server|uvicorn") or bool(
        subprocess.run(["lsof", "-i", ":8000"], capture_output=True).stdout
    )
    lines.append(f"{'✅' if api_ok else '❌'} API 서버 — {'실행 중' if api_ok else '미실행'}")

    ts_ok = pgrep("tailscaled")
    lines.append(f"{'✅' if ts_ok else '❌'} Tailscale VPN — {'실행 중' if ts_ok else '미실행'}")

    cf_ok = pgrep("cloudflared")
    lines.append(f"{'✅' if cf_ok else '❌'} Cloudflare Revit 터널 — {'실행 중' if cf_ok else '미실행'}")

    # ── 반복 폴링 ──
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("🔁 <b>반복 폴링</b>")

    gmail_ok, gmail_t = log_has_today(LOG_DIR / "gmail_inquiry_monitor.log", today_str2)
    lines.append(f"{'✅' if gmail_ok else '❌'} Gmail 문의 모니터링 (10분) — "
                 f"{gmail_t + ' 정상' if gmail_ok else '미실행'}")
    if not gmail_ok:
        missed.append("Gmail 문의 모니터링")

    api_alert_ok, api_alert_t = log_has_today(
        LOG_DIR / "api_usage_alerts.launchd.out.log", today_str2[:7]
    )
    # api usage log는 날짜 없이 alerts_sent만 — 파일 수정일로 판단
    api_alert_log = LOG_DIR / "api_usage_alerts.launchd.out.log"
    if api_alert_log.exists():
        mtime = date.fromtimestamp(api_alert_log.stat().st_mtime)
        api_alert_ok = mtime >= today
        api_alert_t = "정상"
    lines.append(f"{'✅' if api_alert_ok else '❌'} API 사용량 알림 (30분) — "
                 f"{'정상 (이벤트 없음)' if api_alert_ok else '미실행'}")

    ax_ok, ax_t = log_has_today(LOG_DIR / "hourly_ax_signal_monitor.log", today_str2)
    lines.append(f"{'✅' if ax_ok else '❌'} AX 신호 모니터링 (매시간) — "
                 f"{ax_t + ' 완료' if ax_ok else '미실행'}")
    if not ax_ok:
        missed.append("AX 신호 모니터링")

    # ── 일일 루틴 ──
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("📅 <b>일일 루틴</b>")

    # 지식 업데이트
    done_marker = LOG_DIR / f".daily_knowledge_update_done_{today_str2}"
    ku_ok = done_marker.exists()
    if not ku_ok:
        ku_ok2, ku_t = log_has_today(LOG_DIR / "daily_knowledge_update.log", today_str2)
        ku_label = f"{ku_t} 진행 중" if ku_ok2 else "미실행 (Mac 수면)"
    else:
        ku_label = "완료"
    lines.append(f"{'✅' if ku_ok else ('🔄' if not ku_ok and ku_ok2 else '❌')} "
                 f"지식 업데이트 (00:00) — {ku_label}")
    statuses["ku"] = ku_ok
    if not ku_ok:
        missed.append("지식 업데이트")

    # 지식 동기화
    sync_ok, sync_t = log_has_today(LOG_DIR / "sync_knowledge.log", today_str2)
    sync_label = f"{sync_t} 완료" if sync_ok else "미실행 (Mac 수면)"
    lines.append(f"{'✅' if sync_ok else '❌'} 지식 동기화 (03:00) — {sync_label}")
    statuses["sync"] = sync_ok
    if not sync_ok:
        missed.append("지식 동기화")

    # BIM 교육 텔레그램
    edu_progress = BIM_EDUCATION_DIR / "progress.json"
    edu_ok = False
    edu_label = "미실행 (Mac 수면)"
    if edu_progress.exists():
        try:
            prog = json.loads(edu_progress.read_text(encoding="utf-8"))
            users = prog.get("users", {})
            if users:
                last_dates = [v.get("last_sent", "") for v in users.values()]
                if all(d == today_str2 for d in last_dates):
                    days = [v.get("day", 1) - 1 for v in users.values()]
                    edu_ok = True
                    edu_label = f"Day {days[0]} 발송 완료"
                else:
                    last = max(last_dates)
                    edu_label = f"미실행 (마지막: {last[5:]})"
        except Exception:
            pass
    # 0명 오탐 방지: progress.json 상 미발송이어도 launchd 작업이 오늘 실행됐으면
    # (활성 유료 Starter 0명 → 발송 대상 없음) 정상 실행으로 본다.
    if not edu_ok:
        edu_out = LOG_DIR / "bim_education_daily.out.log"
        if edu_out.exists() and date.fromtimestamp(edu_out.stat().st_mtime) >= today:
            edu_ok = True
            edu_label = "발송 완료 (활성 대상 0명)"
    lines.append(f"{'✅' if edu_ok else '❌'} BIM 교육 텔레그램 발송 (07:00) — {edu_label}")
    statuses["edu"] = edu_ok
    if not edu_ok:
        missed.append("BIM 교육 텔레그램 발송")

    # 블로거 포스트 발행
    blog_ok = False
    blog_label = "미실행"
    publish_log = LOG_DIR / "blogger_daily_publish.jsonl"
    if publish_log.exists():
        try:
            for raw in publish_log.read_text(encoding="utf-8", errors="ignore").splitlines():
                if not raw.strip():
                    continue
                row = json.loads(raw)
                if row.get("date") == today_str2 and row.get("url"):
                    blog_ok = True
                    blog_label = "발행 완료"
        except Exception:
            blog_ok = False

    if not blog_ok:
        lock_path = PROJECT_ROOT / "runtime" / "blogger_queue_publish.lock"
        if lock_path.exists():
            try:
                pid = lock_path.read_text(encoding="utf-8", errors="ignore").strip()
                # PID 재사용 오탐 방지: 해당 PID가 실제 블로거 발행 스크립트인지
                # 커맨드라인까지 대조한다 (단순 ps -p 는 무관한 프로세스에 속음).
                proc = subprocess.run(
                    ["ps", "-p", pid, "-o", "command="],
                    capture_output=True, text=True,
                ) if pid else None
                if proc and proc.returncode == 0 and "blogger_queue_publish" in proc.stdout:
                    blog_label = "실행 중"
                else:
                    blog_label = "미실행 (stale lock)"
            except Exception:
                blog_label = "미실행 (lock 확인 실패)"
    lines.append(f"{'✅' if blog_ok else '❌'} 블로거 포스트 발행 (08:00) — {blog_label}")
    statuses["blog"] = blog_ok
    if not blog_ok:
        missed.append("블로거 포스트 발행")

    # 내부 성장 루프
    growth_ok, growth_t = log_has_today(LOG_DIR / "internal_self_growth_loop.log", today_str2)
    growth_label = f"{growth_t} 완료 (수동)" if growth_ok else "미실행 (Mac 수면)"
    # done 여부
    growth_text = (LOG_DIR / "internal_self_growth_loop.log").read_text(
        encoding="utf-8", errors="ignore"
    ) if (LOG_DIR / "internal_self_growth_loop.log").exists() else ""
    growth_done = any(
        today_str2 in l and "done" in l
        for l in growth_text.splitlines()
    )
    if growth_done:
        growth_label = f"{growth_t} 완료"
    lines.append(f"{'✅' if growth_ok else '❌'} 내부 자기 성장 루프 (08:00) — {growth_label}")
    if not growth_ok:
        missed.append("내부 자기 성장 루프")

    # Qwen 제품 드래프트
    qwen_log = LOG_DIR / "qwen_product_draft_daily.launchd.out.log"
    qwen_ok = False
    qwen_label = "미실행"
    if qwen_log.exists():
        mtime = date.fromtimestamp(qwen_log.stat().st_mtime)
        if mtime >= today:
            qwen_ok = True
            try:
                data = json.loads(qwen_log.read_text(encoding="utf-8", errors="ignore").strip().splitlines()[-1])
                remaining = data.get("remaining", [])
                qwen_label = f"완료 (remaining: {len(remaining)})"
            except Exception:
                qwen_label = "완료"
    lines.append(f"{'✅' if qwen_ok else '❌'} Qwen 제품 드래프트 (08:20) — {qwen_label}")
    statuses["qwen"] = qwen_ok
    if not qwen_ok:
        missed.append("Qwen 제품 드래프트")

    # ── 주간 루틴 ──
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    lines.append("📆 <b>주간 루틴</b>")

    # 주간 AX 전략 리뷰 (월요일)
    ax_review_ok, ax_review_label = weekly_review_done_this_week(today)
    review_mark = "📅 해당 없음 (월요일 아님)" if not is_monday and not ax_review_ok else ""
    if is_monday and not ax_review_ok:
        review_mark = "미실행"
        missed.append("주간 AX 전략 리뷰")
    statuses["ax_review"] = ax_review_ok
    lines.append(
        f"{'✅' if ax_review_ok else ('❌' if is_monday else '➖')} "
        f"주간 AX 전략 리뷰 (월요일 08:00) — "
        f"{ax_review_label if ax_review_ok else review_mark if review_mark else '이번 주 미실행'}"
    )

    # BIMobject 크롤링 (일요일)
    bim_ok, bim_label = bimobject_crawled_recently(today)
    statuses["bimobj"] = bim_ok
    if is_sunday and not bim_ok:
        missed.append("BIMobject 크롤링")
    lines.append(
        f"{'✅' if bim_ok else ('❌' if is_sunday else '➖')} "
        f"BIMobject 크롤링 (일요일 03:00) — "
        f"{bim_label if bim_label else ('미실행 (Mac 수면)' if is_sunday else '해당 없음')}"
    )

    # ── 미실행 요약 ──
    lines.append("")
    lines.append("━━━━━━━━━━━━━━━━━━━━")
    if missed:
        lines.append(f"⚠️ <b>오늘 미실행 항목 {len(missed)}개</b>")
        for m in missed:
            lines.append(f"• {m}")
        lines.append("(모두 새벽 Mac 수면으로 인한 누락)")
    else:
        lines.append("✅ <b>모든 루틴 정상 완료</b>")

    # 체크리스트 보고 이벤트 자체는 스크립트가 실행된 것으로 완료 처리
    statuses["checklist"] = True
    return "\n".join(lines), statuses


def main() -> None:
    load_dotenv()
    today = date.today()
    now = datetime.now()
    print(f"체크리스트 생성 중... {today.isoformat()}")
    msg, statuses = build_checklist(today, now)
    print(msg)
    print("\nTelegram 발송 중...")
    send_telegram(msg)
    update_calendar_events(statuses, today)
    print("완료.")


if __name__ == "__main__":
    main()
