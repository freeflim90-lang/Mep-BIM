"""
LUA BIM LAND — 서버 사이드 게임 엔진

담당 연산:
  - BIM 밀도(D_BIM) → 영토 등급
  - XP 산정 (연면적 × 기여도 × 등급 승수 × Shadow Strike 승수)
  - Shadow Strike 감지 (이직 후 동일 프로젝트 재참여)
  - 동기화 로그 영속화 (data/bim_land/territory_logs.json)
"""

from __future__ import annotations

import json
import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel

# ── 데이터 저장 경로 ────────────────────────────────────────────────────────────
_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "bim_land"
_LOGS_FILE              = _DATA_DIR / "territory_logs.json"
_TERRITORIES_FILE       = _DATA_DIR / "territories.json"
_PROJECTS_FILE          = _DATA_DIR / "projects.json"
_CLAIMS_FILE            = _DATA_DIR / "participation_claims.json"
_LOCATION_REQ_FILE      = _DATA_DIR / "location_change_requests.json"

FT2_TO_M2 = 0.092903  # 1 ft² = 0.092903 m²
GFA_SUSPICIOUS_M2 = 1_500_000  # 150만 m² 초과 시 자동 승인 유보

# ── Pydantic 모델 ───────────────────────────────────────────────────────────────

class SyncRequest(BaseModel):
    project_code: str
    project_name: str
    user_email: str
    total_elements: int
    gross_floor_area_ft2: float = 0.0   # 0이면 요소 수 기반 추정
    central_path_hash: str = ""
    central_path: str = ""      # Revit 파일 전체 경로
    rvt_file_name: str = ""     # Revit 파일명 (basename)
    sync_at: Optional[datetime.datetime] = None
    client_version: str = "LuaBimLand-v1"
    source: str = "revit-addin"
    latitude: float = 0.0               # 현장 위도 (지도 표시용, 선택)
    longitude: float = 0.0              # 현장 경도


class SyncResult(BaseModel):
    status: str
    bim_density: float
    territory_grade: str
    grade_multiplier: float
    xp_earned: float
    shadow_strike: bool
    shadow_strike_multiplier: float
    message: str
    # 신고된 사용자: 연락처 제출 요청
    requires_verification: bool = False
    pending_report_id: str = ""
    # 참여 이력 미등록 사용자
    participation_required: bool = False


# ── 영토 등급 ───────────────────────────────────────────────────────────────────

_GRADES: list[tuple[float, str, float]] = [
    # (D_BIM 하한, 등급명, 승수)
    (3.0, "Legendary", 3.0),
    (1.5, "Epic",      2.0),
    (0.5, "Rare",      1.5),
    (0.0, "Normal",    1.0),
]


def _grade(density: float) -> tuple[str, float]:
    for threshold, name, multiplier in _GRADES:
        if density >= threshold:
            return name, multiplier
    return "Normal", 1.0


# ── Shadow Strike 감지 ──────────────────────────────────────────────────────────

def _check_shadow_strike(project_code: str, user_email: str, current_team: str) -> float:
    """
    동일 프로젝트에서 다른 팀으로 기록된 과거 이력이 있으면 Shadow Strike 발동.
    이직 인원 1명 → ×1.3 / 2명 이상 → ×1.5
    """
    logs = _load_logs()
    past_teams = {
        entry["user_team"]
        for entry in logs
        if entry.get("project_code") == project_code
        and entry.get("user_email") == user_email
        and entry.get("user_team") != current_team
    }
    if len(past_teams) == 0:
        return 1.0
    if len(past_teams) == 1:
        return 1.3
    return 1.5


# ── 핵심 연산 ───────────────────────────────────────────────────────────────────

def process_sync(req: SyncRequest) -> SyncResult:
    _ensure_data_dir()

    # 차단된 사용자는 즉시 거부
    if is_blocked(req.user_email):
        return SyncResult(
            status="blocked",
            bim_density=0, territory_grade="", grade_multiplier=1.0,
            xp_earned=0, shadow_strike=False, shadow_strike_multiplier=1.0,
            message=f"⛔ {req.user_email} 계정은 관리자에 의해 차단되었습니다.",
        )

    # 관리자 등록 프로젝트: 승인된 참여 이력 없으면 보류
    if _is_registered_project(req.project_code) and not _has_approved_participation(req.user_email, req.project_code):
        return SyncResult(
            status="participation_required",
            bim_density=0, territory_grade="", grade_multiplier=1.0,
            xp_earned=0, shadow_strike=False, shadow_strike_multiplier=1.0,
            message=(
                "📋 이 프로젝트는 참여 이력 등록이 필요합니다.\n"
                "Revit Add-in의 [프로젝트 참여 등록] 버튼에서\n"
                "이력서 형식으로 참여 정보를 제출해주세요."
            ),
            participation_required=True,
        )

    # 신고된 사용자: 연락처 미제출 시 동기화 보류
    pending = _get_pending_report_for(req.user_email)
    if pending and not pending.get("contact_phone"):
        return SyncResult(
            status="verification_required",
            bim_density=0, territory_grade="", grade_multiplier=1.0,
            xp_earned=0, shadow_strike=False, shadow_strike_multiplier=1.0,
            message=(
                "📋 귀하에 대한 부정 사용 신고가 접수되었습니다.\n"
                "LUA BIM LAND 연속 사용을 위해 연락처를 제출하고 "
                "관리자의 확인을 받아야 합니다.\n"
                f"신고 ID: {pending['report_id']}"
            ),
            requires_verification=True,
            pending_report_id=pending["report_id"],
        )

    gross_m2 = req.gross_floor_area_ft2 * FT2_TO_M2

    # BIM 밀도: 연면적이 0이면 요소 수 기반 추정 (100 elements ≈ 1m² proxy)
    if gross_m2 > 0:
        density = req.total_elements / gross_m2
    else:
        density = req.total_elements / 1000.0  # 연면적 미등록 시 완화 추정

    grade_name, grade_mult = _grade(density)

    # Shadow Strike: 현재 팀은 user_email 도메인으로 간이 추정
    current_team = _team_from_email(req.user_email)
    ss_mult = _check_shadow_strike(req.project_code, req.user_email, current_team)
    shadow_strike = ss_mult > 1.0

    # XP = max(연면적_m², 요소수 / 100) × 등급 승수 × Shadow Strike 승수
    base_area = gross_m2 if gross_m2 > 0 else req.total_elements / 100.0
    xp = round(base_area * grade_mult * ss_mult, 2)

    # 로그 영속화
    _append_log({
        "project_code":     req.project_code,
        "project_name":     req.project_name,
        "user_email":       req.user_email,
        "user_team":        current_team,
        "total_elements":   req.total_elements,
        "gross_floor_m2":   round(gross_m2, 2),
        "bim_density":      round(density, 4),
        "territory_grade":  grade_name,
        "xp_earned":        xp,
        "shadow_strike":    shadow_strike,
        "ss_multiplier":    ss_mult,
        "sync_at":          (req.sync_at or datetime.datetime.utcnow()).isoformat(),
        "central_path_hash": req.central_path_hash,
        "central_path":     req.central_path,
        "rvt_file_name":    req.rvt_file_name,
    })

    # 영토 소유권 갱신 (좌표 + 연면적 + 파일명 포함)
    _update_territory(
        req.project_code, req.project_name, current_team,
        grade_name, xp, req.latitude, req.longitude, gross_m2,
        req.rvt_file_name, req.central_path,
    )

    message = _build_message(grade_name, xp, shadow_strike, ss_mult)

    return SyncResult(
        status="ok",
        bim_density=round(density, 4),
        territory_grade=grade_name,
        grade_multiplier=grade_mult,
        xp_earned=xp,
        shadow_strike=shadow_strike,
        shadow_strike_multiplier=ss_mult,
        message=message,
    )


# ── 메시지 생성 ─────────────────────────────────────────────────────────────────

def _build_message(grade: str, xp: float, shadow_strike: bool, ss_mult: float) -> str:
    grade_emoji = {"Normal": "🟢", "Rare": "🔵", "Epic": "🟣", "Legendary": "🟠"}.get(grade, "⚪")
    msg = f"{grade_emoji} [{grade}] 영토 동기화 완료 — +{xp:,.1f} XP 획득"
    if shadow_strike:
        msg += f"\n⚡ Shadow Strike 발동! 공격력 ×{ss_mult} 적용됨"
    return msg


# ── 영속화 유틸 ─────────────────────────────────────────────────────────────────

def _team_from_email(email: str) -> str:
    """이메일 도메인을 팀 식별자로 사용 (예: user@luabim.com → luabim.com)."""
    if "@" in email:
        return email.split("@")[-1].lower()
    return email.lower() or "unknown"


def _ensure_data_dir() -> None:
    _DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_logs() -> list[dict]:
    if not _LOGS_FILE.exists():
        return []
    try:
        return json.loads(_LOGS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _append_log(entry: dict) -> None:
    logs = _load_logs()
    logs.append(entry)
    _LOGS_FILE.write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_territories() -> dict:
    if not _TERRITORIES_FILE.exists():
        return {}
    try:
        return json.loads(_TERRITORIES_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _update_territory(
    project_code: str,
    project_name: str,
    team: str,
    grade: str,
    xp: float,
    lat: float = 0.0,
    lng: float = 0.0,
    gross_floor_m2: float = 0.0,
    rvt_file_name: str = "",
    central_path: str = "",
) -> None:
    territories = _load_territories()
    existing = territories.get(project_code, {})
    entry: dict = {
        "project_name":   project_name,
        "owner_team":     team,
        "grade":          grade,
        "total_xp":       round(existing.get("total_xp", 0) + xp, 2),
        "last_sync_at":   datetime.datetime.utcnow().isoformat(),
        "status":         "STABLE",
    }
    # 좌표·연면적은 한 번이라도 제공됐으면 유지 (더 큰 값 우선)
    resolved_lat = lat  if lat  != 0.0 else existing.get("latitude",  0.0)
    resolved_lng = lng  if lng  != 0.0 else existing.get("longitude", 0.0)
    entry["latitude"]       = resolved_lat
    entry["longitude"]      = resolved_lng
    entry["gross_floor_m2"] = max(gross_floor_m2, existing.get("gross_floor_m2", 0.0))
    entry["location_pending"] = (resolved_lat == 0.0 and resolved_lng == 0.0)
    # 동기화 파일 정보 (비어있으면 기존 값 유지)
    if rvt_file_name:
        entry["last_sync_file"] = rvt_file_name
    else:
        entry.setdefault("last_sync_file", existing.get("last_sync_file", ""))
    if central_path:
        entry["last_sync_path"] = central_path
    else:
        entry.setdefault("last_sync_path", existing.get("last_sync_path", ""))
    territories[project_code] = entry
    _TERRITORIES_FILE.write_text(
        json.dumps(territories, ensure_ascii=False, indent=2), encoding="utf-8"
    )


# ── 조회 API ────────────────────────────────────────────────────────────────────

def get_all_territories() -> dict:
    return _load_territories()


def get_territory(project_code: str) -> dict | None:
    return _load_territories().get(project_code)


def get_leaderboard(top_n: int = 10) -> list[dict]:
    """팀별 누적 XP 합산 순위."""
    territories = _load_territories()
    team_xp: dict[str, float] = {}
    for t in territories.values():
        team = t.get("owner_team", "unknown")
        team_xp[team] = team_xp.get(team, 0) + t.get("total_xp", 0)
    ranked = sorted(team_xp.items(), key=lambda x: x[1], reverse=True)
    return [{"rank": i + 1, "team": team, "total_xp": round(xp, 2)}
            for i, (team, xp) in enumerate(ranked[:top_n])]


# =============================================================================
# 어드민: 차단 사용자 관리
# =============================================================================

_BLOCKED_FILE  = _DATA_DIR / "blocked_users.json"
_REPORTS_FILE  = _DATA_DIR / "reports.json"


def _load_blocked() -> dict:
    if not _BLOCKED_FILE.exists():
        return {}
    try:
        return json.loads(_BLOCKED_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def is_blocked(email: str) -> bool:
    return email.lower() in _load_blocked()


def block_user(email: str, reason: str, blocked_by: str = "admin") -> dict:
    _ensure_data_dir()
    blocked = _load_blocked()
    key = email.lower()
    if key in blocked:
        return {"status": "already_blocked", "email": key}
    blocked[key] = {
        "email":      key,
        "reason":     reason,
        "blocked_by": blocked_by,
        "blocked_at": datetime.datetime.utcnow().isoformat(),
    }
    _BLOCKED_FILE.write_text(json.dumps(blocked, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "blocked", "email": key}


def unblock_user(email: str) -> dict:
    blocked = _load_blocked()
    key = email.lower()
    if key not in blocked:
        return {"status": "not_found", "email": key}
    del blocked[key]
    _BLOCKED_FILE.write_text(json.dumps(blocked, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "unblocked", "email": key}


def get_blocked_users() -> list[dict]:
    return list(_load_blocked().values())


# =============================================================================
# 신고 시스템
# =============================================================================

def _load_reports() -> list[dict]:
    if not _REPORTS_FILE.exists():
        return []
    try:
        return json.loads(_REPORTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _get_pending_report_for(email: str) -> dict | None:
    """해당 이메일에 대한 미결 신고가 있으면 반환."""
    for r in _load_reports():
        if r.get("reported_email", "").lower() == email.lower() and r.get("status") == "pending":
            return r
    return None


def submit_contact(report_id: str, email: str, phone: str) -> dict:
    """피신고자가 연락처를 제출 — reported_phone 필드에 저장."""
    reports = _load_reports()
    for r in reports:
        if r["report_id"] == report_id and r.get("reported_email", "").lower() == email.lower():
            if r["status"] != "pending":
                return {"status": "already_resolved"}
            r["reported_phone"] = phone
            r["reported_phone_submitted_at"] = datetime.datetime.utcnow().isoformat()
            _REPORTS_FILE.write_text(
                json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            return {"status": "submitted", "report_id": report_id,
                    "message": "연락처가 제출되었습니다. 관리자 확인 후 결과를 알려드립니다."}
    return {"status": "not_found"}


def file_report(
    reporter_email: str,
    reported_email: str,
    project_code: str,
    reason: str,
    reporter_phone: str = "",
) -> dict:
    _ensure_data_dir()
    reports = _load_reports()
    report_id = f"RPT-{len(reports) + 1:04d}"
    entry = {
        "report_id":      report_id,
        "reporter_email": reporter_email,
        "reporter_phone": reporter_phone,          # 신고자 연락처
        "reported_email": reported_email,
        "reported_phone": "",                      # 피신고자 연락처 (submit_contact로 제출)
        "project_code":   project_code,
        "reason":         reason,
        "status":         "pending",
        "resolved_by":    None,
        "resolved_at":    None,
        "filed_at":       datetime.datetime.utcnow().isoformat(),
    }
    reports.append(entry)
    _REPORTS_FILE.write_text(json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"status": "filed", "report_id": report_id}


def get_reports(status_filter: str = "all") -> list[dict]:
    reports = _load_reports()
    if status_filter == "all":
        return sorted(reports, key=lambda x: x["filed_at"], reverse=True)
    return [r for r in reports if r.get("status") == status_filter]


def resolve_report(report_id: str, action: str, resolved_by: str = "admin") -> dict:
    """
    action: 'block' → 신고 대상 차단 + 상태 resolved_blocked
            'dismiss' → 신고 기각, 상태 resolved_dismissed
    """
    reports = _load_reports()
    for r in reports:
        if r["report_id"] == report_id:
            if r["status"] != "pending":
                return {"status": "already_resolved", "report_id": report_id}
            r["resolved_by"] = resolved_by
            r["resolved_at"] = datetime.datetime.utcnow().isoformat()
            if action == "block":
                block_user(r["reported_email"], f"신고 처리: {r['reason']}", resolved_by)
                r["status"] = "resolved_blocked"
            else:
                r["status"] = "resolved_dismissed"
            _REPORTS_FILE.write_text(
                json.dumps(reports, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            return {"status": "resolved", "action": action, "report_id": report_id}
    return {"status": "not_found", "report_id": report_id}


# =============================================================================
# 프로젝트 레지스트리 (관리자 등록 전용)
# =============================================================================

def _load_projects() -> dict:
    if not _PROJECTS_FILE.exists():
        return {}
    try:
        return json.loads(_PROJECTS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _is_registered_project(project_code: str) -> bool:
    return project_code in _load_projects()


def _gfa_review_status(gfa: float) -> str:
    """연면적 값에 따른 초기 검토 상태 결정."""
    if gfa <= 0:
        return "unset"
    if gfa > GFA_SUSPICIOUS_M2:
        return "suspended"   # 과도 의심 → 자동 유보
    return "pending"         # 정상 범위 → 검토 대기


_CHO_TO_EN: dict[int, str] = {
    0: 'G', 1: 'K', 2: 'N', 3: 'D', 4: 'T', 5: 'R',
    6: 'M', 7: 'B', 8: 'P', 9: 'S', 10: 'S', 11: '',
    12: 'J', 13: 'J', 14: 'C', 15: 'K', 16: 'T', 17: 'P', 18: 'H',
}
# ㅇ 초성(묵음)일 때 모음으로 대체 (연→Y, 이→I, 아→A 등)
_JUNG_TO_EN: dict[int, str] = {
    0: 'A', 1: 'A', 2: 'Y', 3: 'Y', 4: 'E', 5: 'E',
    6: 'Y', 7: 'Y', 8: 'O', 9: 'W', 10: 'W', 11: 'W',
    12: 'Y', 13: 'U', 14: 'W', 15: 'W', 16: 'W',
    17: 'Y', 18: 'E', 19: 'E', 20: 'I',
}


def _hangul_initial(ch: str) -> str:
    """한글 한 글자의 초성 → 영문 대문자. ㅇ 초성이면 모음으로 대체."""
    code = ord(ch)
    if not (0xAC00 <= code <= 0xD7A3):
        return ch.upper() if ch.isascii() and ch.isalpha() else ''
    offset = code - 0xAC00
    cho = offset // 588
    en = _CHO_TO_EN.get(cho, '')
    if en == '':  # ㅇ 초성(묵음) → 모음으로 대체
        jung = (offset % 588) // 28
        en = _JUNG_TO_EN.get(jung, '')
    return en


def _abbrev_from_team(team_name: str) -> str:
    """팀명 → 대문자 약어 (2~4자).
    첫 단어가 짧은 ASCII(≤5자)이면 그대로 사용 (LUA, LG, SK …).
    아니면 공백 기준 각 단어 첫 글자 추출.
    단어 1개일 때 결과가 1자 이하면 앞 3음절 초성 사용.
    """
    parts = [p for p in team_name.strip().split() if p]
    if not parts:
        return "PRJ"
    first = parts[0]
    # 첫 단어가 짧고 순수 ASCII 알파벳이면 브랜드명으로 직접 사용
    if first.isascii() and first.isalpha() and len(first) <= 5:
        return first.upper()[:4]
    # 각 단어의 첫 글자 추출
    letters = [_hangul_initial(p[0]) for p in parts[:4]]
    abbrev = ''.join(filter(None, letters))
    # 단어 1개이고 1자 이하면 앞 3음절까지 확장
    if len(abbrev) <= 1 and len(parts) == 1:
        for ch in parts[0][1:3]:
            en = _hangul_initial(ch)
            if en:
                abbrev += en
            if len(abbrev) >= 3:
                break
    return (abbrev or "PRJ")[:4]


def _initials_from_name(person_name: str) -> str:
    """사람 이름 → 이니셜 (2~3자).
    각 글자의 초성→영문 변환 (최정연 → CJY, 이민준 → IMJ).
    """
    name = person_name.strip()
    if not name:
        return "USR"
    letters = []
    for ch in name:
        if ch == ' ':
            continue
        en = _hangul_initial(ch)
        if en:
            letters.append(en)
        if len(letters) >= 3:
            break
    return (''.join(letters) or "USR")[:3]


def _auto_project_code(team_name: str = "", person_name: str = "") -> str:
    """팀명 약어 + 이름 이니셜 기반 코드 자동 생성: {TEAM}-{INITIALS}-{SEQ:03d}."""
    team_part   = _abbrev_from_team(team_name)   if team_name   else "PRJ"
    person_part = _initials_from_name(person_name) if person_name else "USR"
    projects    = _load_projects()
    prefix = f"{team_part}-{person_part}-"
    max_n = 0
    for code in projects:
        if code.startswith(prefix):
            try:
                max_n = max(max_n, int(code[len(prefix):]))
            except ValueError:
                pass
    n = max_n + 1
    while True:
        code = f"{prefix}{n:03d}"
        if code not in projects:
            return code
        n += 1


def admin_register_project(
    project_code: str,
    project_name: str,
    team_name: str = "",
    person_name: str = "",
    address: str = "",
    lat: float = 0.0,
    lng: float = 0.0,
    gross_floor_area_m2: float = 0.0,
    disciplines: list[str] = [],
    start_date: str = "",
    end_date: str = "",
    description: str = "",
    registered_by: str = "admin",
) -> dict:
    _ensure_data_dir()
    if not project_code:
        project_code = _auto_project_code(team_name, person_name)
    projects = _load_projects()
    if project_code in projects:
        return {"status": "already_exists", "project_code": project_code}
    projects[project_code] = {
        "project_code":        project_code,
        "project_name":        project_name,
        "team_name":           team_name,
        "person_name":         person_name,
        "address":             address,
        "latitude":            lat,
        "longitude":           lng,
        "gross_floor_area_m2": gross_floor_area_m2,
        "gfa_review_status":   _gfa_review_status(gross_floor_area_m2),
        "gfa_reviewed_by":     None,
        "gfa_reviewed_at":     None,
        "disciplines":         disciplines,
        "start_date":          start_date,
        "end_date":            end_date,
        "description":         description,
        "registered_by":       registered_by,
        "registered_at":       datetime.datetime.utcnow().isoformat(),
        "participation_required": True,
    }
    _PROJECTS_FILE.write_text(
        json.dumps(projects, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {"status": "registered", "project_code": project_code}


def admin_update_project(project_code: str, updates: dict) -> dict:
    projects = _load_projects()
    if project_code not in projects:
        return {"status": "not_found"}
    # 연면적이 변경되면 검토 상태 초기화
    if "gross_floor_area_m2" in updates:
        new_gfa = updates["gross_floor_area_m2"]
        updates.setdefault("gfa_review_status", _gfa_review_status(new_gfa))
        updates["gfa_reviewed_by"] = None
        updates["gfa_reviewed_at"] = None
    projects[project_code].update(updates)
    projects[project_code]["updated_at"] = datetime.datetime.utcnow().isoformat()
    _PROJECTS_FILE.write_text(
        json.dumps(projects, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {"status": "updated", "project_code": project_code}


def admin_transfer_team(
    project_code: str,
    new_team_name: str,
    transferred_by: str = "admin",
    reason: str = "",
) -> dict:
    """이직으로 인한 팀명 변경 처리.
    - projects.json: team_name 갱신
    - territories.json: owner_team 갱신 (Shadow Strike 로그는 보존)
    """
    projects = _load_projects()
    if project_code not in projects:
        return {"status": "not_found"}
    old_team = projects[project_code].get("team_name", "")
    projects[project_code]["team_name"]        = new_team_name
    projects[project_code]["team_transferred_from"] = old_team
    projects[project_code]["team_transferred_by"]   = transferred_by
    projects[project_code]["team_transferred_at"]   = datetime.datetime.utcnow().isoformat()
    if reason:
        projects[project_code]["team_transfer_reason"] = reason
    projects[project_code]["updated_at"] = datetime.datetime.utcnow().isoformat()
    _PROJECTS_FILE.write_text(
        json.dumps(projects, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # 영토 owner_team도 갱신
    territories = _load_territories()
    if project_code in territories:
        territories[project_code]["owner_team"]            = new_team_name
        territories[project_code]["team_transferred_from"] = old_team
        territories[project_code]["last_sync_at"]          = datetime.datetime.utcnow().isoformat()
        _TERRITORIES_FILE.write_text(
            json.dumps(territories, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return {"status": "transferred", "project_code": project_code,
            "old_team": old_team, "new_team": new_team_name}


def review_gfa(
    project_code: str,
    action: str,          # "approve" | "suspend"
    reviewer: str = "admin",
    reason: str = "",
) -> dict:
    """연면적 검토 승인 또는 유보 처리."""
    projects = _load_projects()
    if project_code not in projects:
        return {"status": "not_found"}
    p = projects[project_code]
    if p.get("gfa_review_status") == "unset":
        return {"status": "error", "message": "연면적이 입력되지 않았습니다."}
    p["gfa_review_status"] = "approved" if action == "approve" else "suspended"
    p["gfa_reviewed_by"]   = reviewer
    p["gfa_reviewed_at"]   = datetime.datetime.utcnow().isoformat()
    if reason:
        p["gfa_review_reason"] = reason
    p["updated_at"] = datetime.datetime.utcnow().isoformat()
    _PROJECTS_FILE.write_text(
        json.dumps(projects, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {"status": p["gfa_review_status"], "project_code": project_code}


def get_gfa_review_queue(status_filter: str = "all") -> list[dict]:
    """연면적 검토가 필요한 프로젝트 목록."""
    projects = list(_load_projects().values())
    if status_filter != "all":
        projects = [p for p in projects if p.get("gfa_review_status") == status_filter]
    return sorted(projects, key=lambda p: p.get("registered_at", ""), reverse=True)


def admin_delete_project(project_code: str) -> dict:
    projects = _load_projects()
    if project_code not in projects:
        return {"status": "not_found"}
    del projects[project_code]
    _PROJECTS_FILE.write_text(
        json.dumps(projects, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {"status": "deleted", "project_code": project_code}


def get_projects() -> list[dict]:
    return list(_load_projects().values())


def get_project(project_code: str) -> dict | None:
    return _load_projects().get(project_code)


# =============================================================================
# 참여 이력 신청 (일반 사용자 — Add-in 에서 제출)
# =============================================================================

def _load_claims() -> list[dict]:
    if not _CLAIMS_FILE.exists():
        return []
    try:
        return json.loads(_CLAIMS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def _has_approved_participation(user_email: str, project_code: str) -> bool:
    for c in _load_claims():
        if (c.get("user_email", "").lower() == user_email.lower()
                and c.get("project_code") == project_code
                and c.get("status") == "approved"):
            return True
    return False


def submit_participation_claim(
    user_email: str,
    project_code: str,
    role: str,
    discipline: str,
    start_date: str,
    end_date: str,
    description: str,
    user_phone: str = "",
    company: str = "",
) -> dict:
    _ensure_data_dir()
    claims = _load_claims()

    # 동일 이메일+프로젝트 중복 대기 신청 방지
    for c in claims:
        if (c.get("user_email", "").lower() == user_email.lower()
                and c.get("project_code") == project_code
                and c.get("status") == "pending"):
            return {"status": "already_pending", "claim_id": c["claim_id"]}

    claim_id = f"CLM-{len(claims) + 1:04d}"
    entry = {
        "claim_id":     claim_id,
        "user_email":   user_email,
        "user_phone":   user_phone,
        "company":      company,
        "project_code": project_code,
        "role":         role,          # 직책 (예: BIM 코디네이터)
        "discipline":   discipline,    # 공종 (예: MEP)
        "start_date":   start_date,
        "end_date":     end_date,
        "description":  description,   # 자유 기술 (이력서 내용)
        "status":       "pending",     # pending | approved | rejected
        "reviewed_by":  None,
        "reviewed_at":  None,
        "submitted_at": datetime.datetime.utcnow().isoformat(),
    }
    claims.append(entry)
    _CLAIMS_FILE.write_text(
        json.dumps(claims, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {"status": "submitted", "claim_id": claim_id}


def get_participation_claims(
    project_code: str = "",
    status_filter: str = "all",
) -> list[dict]:
    claims = _load_claims()
    if project_code:
        claims = [c for c in claims if c.get("project_code") == project_code]
    if status_filter != "all":
        claims = [c for c in claims if c.get("status") == status_filter]
    return sorted(claims, key=lambda x: x.get("submitted_at", ""), reverse=True)


def resolve_participation_claim(
    claim_id: str,
    action: str,         # 'approve' | 'reject'
    reviewed_by: str = "admin",
) -> dict:
    claims = _load_claims()
    for c in claims:
        if c["claim_id"] == claim_id:
            if c["status"] != "pending":
                return {"status": "already_resolved", "claim_id": claim_id}
            c["status"]      = "approved" if action == "approve" else "rejected"
            c["reviewed_by"] = reviewed_by
            c["reviewed_at"] = datetime.datetime.utcnow().isoformat()
            _CLAIMS_FILE.write_text(
                json.dumps(claims, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            return {"status": c["status"], "claim_id": claim_id}
    return {"status": "not_found", "claim_id": claim_id}


# ── 위치 변경 요청 ───────────────────────────────────────────────────────────────

def _load_location_requests() -> list[dict]:
    if not _LOCATION_REQ_FILE.exists():
        return []
    try:
        return json.loads(_LOCATION_REQ_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def submit_location_change_request(
    project_code: str,
    new_lat: float,
    new_lng: float,
    requester: str = "admin",
    reason: str = "",
) -> dict:
    _ensure_data_dir()
    project = get_project(project_code)
    if not project:
        return {"status": "not_found"}

    reqs = _load_location_requests()

    # 동일 프로젝트 대기 중 요청이 있으면 중복 방지
    for r in reqs:
        if r.get("project_code") == project_code and r.get("status") == "pending":
            return {"status": "already_pending", "request_id": r["request_id"]}

    request_id = f"LOC-{len(reqs) + 1:04d}"
    entry = {
        "request_id":   request_id,
        "project_code": project_code,
        "project_name": project.get("project_name", ""),
        "prev_lat":     project.get("latitude", 0.0),
        "prev_lng":     project.get("longitude", 0.0),
        "new_lat":      new_lat,
        "new_lng":      new_lng,
        "requester":    requester,
        "reason":       reason,
        "status":       "pending",
        "reviewed_by":  None,
        "reviewed_at":  None,
        "submitted_at": datetime.datetime.utcnow().isoformat(),
    }
    reqs.append(entry)
    _LOCATION_REQ_FILE.write_text(
        json.dumps(reqs, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return {"status": "submitted", "request_id": request_id}


def get_location_change_requests(status_filter: str = "all") -> list[dict]:
    reqs = _load_location_requests()
    if status_filter != "all":
        reqs = [r for r in reqs if r.get("status") == status_filter]
    return sorted(reqs, key=lambda x: x.get("submitted_at", ""), reverse=True)


def resolve_location_change_request(
    request_id: str,
    action: str,          # 'approve' | 'reject'
    reviewed_by: str = "admin",
) -> dict:
    reqs = _load_location_requests()
    for r in reqs:
        if r["request_id"] == request_id:
            if r["status"] != "pending":
                return {"status": "already_resolved", "request_id": request_id}
            r["status"]      = "approved" if action == "approve" else "rejected"
            r["reviewed_by"] = reviewed_by
            r["reviewed_at"] = datetime.datetime.utcnow().isoformat()
            _LOCATION_REQ_FILE.write_text(
                json.dumps(reqs, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            # 승인 시 프로젝트 좌표 실제 반영
            if r["status"] == "approved":
                admin_update_project(r["project_code"], {
                    "latitude":  r["new_lat"],
                    "longitude": r["new_lng"],
                })
            return {"status": r["status"], "request_id": request_id}
    return {"status": "not_found", "request_id": request_id}
