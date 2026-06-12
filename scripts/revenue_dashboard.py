#!/usr/bin/env python3
"""
revenue_dashboard.py — LUA BIM LABS 매출 및 리드 현황 대시보드

사용법:
  python3 scripts/revenue_dashboard.py
  python3 scripts/revenue_dashboard.py --json
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTBOUND_DB = ROOT / "scripts" / "outbound_sales" / "data" / "companies.db"
CLIENTS_JSON    = ROOT / "data" / "starter_plan" / "clients.json"
EDUCATION_JSON  = ROOT / "data" / "bim_education" / "progress.json"
BUDGET_JSON     = ROOT / "data" / "ai_usage" / "deepseek_monthly_budget.json"


# ── 헬퍼 ───────────────────────────────────────────────────────────

def _db_query(db_path: Path, sql: str, params: tuple = ()) -> list[dict]:
    if not db_path.exists():
        return []
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def _load_json(path: Path) -> dict | list:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── 섹션 수집 ──────────────────────────────────────────────────────

def outbound_sales_stats() -> dict:
    rows = _db_query(OUTBOUND_DB, "SELECT status, COUNT(*) as cnt FROM companies GROUP BY status")
    counts = {r["status"]: r["cnt"] for r in rows}
    total_rows = _db_query(OUTBOUND_DB, "SELECT COUNT(*) as cnt FROM companies")
    email_rows = _db_query(OUTBOUND_DB,
        "SELECT COUNT(*) as cnt FROM companies WHERE email IS NOT NULL AND email != ''")
    followup_due = _db_query(OUTBOUND_DB,
        "SELECT COUNT(*) as cnt FROM companies WHERE status='email_sent' AND next_followup_at IS NOT NULL AND next_followup_at <= ?",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    sent_7d = _db_query(OUTBOUND_DB,
        "SELECT COUNT(*) as cnt FROM email_logs WHERE sent_at >= ?",
        ((datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),))

    return {
        "total_companies": total_rows[0]["cnt"] if total_rows else 0,
        "with_email": email_rows[0]["cnt"] if email_rows else 0,
        "new": counts.get("new", 0),
        "email_sent": counts.get("email_sent", 0),
        "followup_done": counts.get("followup_done", 0),
        "followup_due_now": followup_due[0]["cnt"] if followup_due else 0,
        "emails_sent_last_7d": sent_7d[0]["cnt"] if sent_7d else 0,
    }


def starter_plan_stats() -> dict:
    data = _load_json(CLIENTS_JSON)
    clients = data.get("clients", []) if isinstance(data, dict) else []
    active   = [c for c in clients if c.get("status") == "active"]
    paid     = [c for c in clients if c.get("payment_status") == "paid"]
    mrr_usd  = len(active) * 39
    return {
        "total_clients": len(clients),
        "active": len(active),
        "paid": len(paid),
        "mrr_usd": mrr_usd,
        "arr_usd": mrr_usd * 12,
    }


def ai_cost_stats() -> dict:
    data = _load_json(BUDGET_JSON)
    budget = data.get("monthly_budget_usd", 50)
    now_month = datetime.now().strftime("%Y-%m")
    month_data = data.get("months", {}).get(now_month, {})
    spent = month_data.get("estimated_spend_usd", 0)
    calls = len(month_data.get("calls", []))
    return {
        "budget_usd": budget,
        "spent_usd": round(spent, 2),
        "remaining_usd": round(budget - spent, 2),
        "calls_this_month": calls,
        "utilization_pct": round(spent / budget * 100, 1) if budget else 0,
    }


def education_stats() -> dict:
    data = _load_json(EDUCATION_JSON)
    users = data.get("users", {}) if isinstance(data, dict) else {}
    today = datetime.now().strftime("%Y-%m-%d")
    active_today = [u for u in users.values() if u.get("last_sent") == today]
    return {
        "total_users": len(users),
        "active_today": len(active_today),
        "users": [
            {"name": u.get("name", k), "day": u.get("day", 0), "track": u.get("track", "")}
            for k, u in users.items()
        ],
    }


def bcc_addin_status() -> dict:
    """BCC Add-in 스토어 출시 상태 (하드코딩 — PRODUCT_RECORD.md 기준)."""
    return {
        "strategy": "ready",
        "store_docs": "draft_ready",
        "entitlement_scaffold": "ready",
        "windows_build": "PENDING_OWNER",
        "qa_evidence": "PENDING_OWNER",
        "store_app_id": "PENDING_OWNER",
        "store_upload": "manual_step_pending",
        "blockers": ["windows_build", "qa_evidence", "store_app_id"],
    }


# ── 출력 ───────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
GRAY   = "\033[90m"


def _color(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"


def _status_icon(val) -> str:
    if val in ("ready", "draft_ready"):
        return _color("✓", GREEN)
    if val in ("PENDING_OWNER", "manual_step_pending"):
        return _color("✗", RED)
    return _color("~", YELLOW)


def print_dashboard(data: dict) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print()
    print(_color("=" * 60, CYAN))
    print(_color(f"  LUA BIM LABS 매출 현황 대시보드  —  {now}", BOLD))
    print(_color("=" * 60, CYAN))

    # ── Starter Plan MRR ──
    sp = data["starter_plan"]
    mrr = sp["mrr_usd"]
    mrr_color = GREEN if mrr > 0 else RED
    print()
    print(_color("  📦 Starter Plan (MEP BIM 교육)", BOLD))
    print(f"     MRR        : {_color(f'USD {mrr:,}', mrr_color)}")
    print(f"     ARR        : USD {sp['arr_usd']:,}")
    print(f"     활성 클라이언트: {_color(str(sp['active']), mrr_color)}명")
    print(f"     전체 등록   : {sp['total_clients']}명")
    if mrr == 0:
        print(_color("     ⚠  아직 유료 클라이언트 0명. 첫 결제 유입이 최우선 과제.", YELLOW))

    # ── 내부 교육 ──
    edu = data["education"]
    edu_color = GREEN if edu["active_today"] > 0 else GRAY
    print()
    print(_color("  🎓 내부 BIM 교육 현황", BOLD))
    print(f"     등록 인원   : {edu['total_users']}명")
    print(f"     오늘 발송   : {_color(str(edu['active_today']), edu_color)}명")
    for u in edu["users"]:
        print(f"       - {u['name']}: Day {u['day']} ({u['track']} 트랙)")

    # ── 아웃바운드 영업 ──
    ob = data["outbound_sales"]
    sent = ob["email_sent"]
    sent_color = GREEN if sent > 0 else RED
    print()
    print(_color("  📧 아웃바운드 영업 파이프라인", BOLD))
    print(f"     수집 업체   : {ob['total_companies']:,}개")
    print(f"     이메일 보유 : {ob['with_email']:,}개")
    print(f"     발송 완료   : {_color(str(sent), sent_color)}개")
    print(f"     발송 대기   : {_color(str(ob['new']), YELLOW if ob['new'] > 0 else GRAY)}개")
    print(f"     팔로업 예정 : {_color(str(ob['followup_due_now']), YELLOW if ob['followup_due_now'] > 0 else GRAY)}개")
    print(f"     최근 7일 발송: {ob['emails_sent_last_7d']}건")
    if ob["new"] > 0 and sent == 0:
        print(_color(f"     📋  {ob['with_email']}개 이메일 확보 완료. 발송 시점은 별도 결정 예정.", GRAY))
    if ob["followup_due_now"] > 0:
        print(_color(f"     ⚠  팔로업 대기 {ob['followup_due_now']}개. 즉시 실행:", YELLOW))
        print(_color("         → python3 scripts/outbound_sales/main.py followup --dry-run", GRAY))

    # ── BCC Add-in ──
    bcc = data["bcc_addin"]
    print()
    print(_color("  🔧 BCC Add-in (Autodesk Store)", BOLD))
    fields = [
        ("전략·문서", bcc["strategy"]),
        ("Store 문서", bcc["store_docs"]),
        ("Entitlement", bcc["entitlement_scaffold"]),
        ("Windows 빌드", bcc["windows_build"]),
        ("QA Evidence", bcc["qa_evidence"]),
        ("Store App ID", bcc["store_app_id"]),
    ]
    for label, val in fields:
        icon = _status_icon(val)
        disp = val.replace("_", " ")
        print(f"     {icon}  {label:<16} {_color(disp, GRAY)}")
    if bcc["blockers"]:
        print(_color(f"     블로커: {', '.join(bcc['blockers'])}", RED))
        print(_color("     → Windows 환경에서 Revit 빌드 완료 후 QA 스크린샷 촬영 필요", GRAY))

    # ── AI 비용 ──
    ai = data["ai_cost"]
    util_color = GREEN if ai["utilization_pct"] < 60 else YELLOW
    print()
    print(_color("  🤖 AI 운영 비용 (DeepSeek)", BOLD))
    print(f"     이번 달 지출: USD {ai['spent_usd']} / {ai['budget_usd']}")
    util_pct_str = f"{ai['utilization_pct']}%"
    print(f"     예산 소진율 : {_color(util_pct_str, util_color)}")
    print(f"     잔여 예산   : USD {ai['remaining_usd']}")
    print(f"     이번 달 호출: {ai['calls_this_month']}회")

    # ── 다음 실행 액션 ──
    print()
    print(_color("  🎯 지금 당장 해야 할 액션 (우선순위 순)", BOLD))
    actions = []
    if ob["followup_due_now"] > 0:
        actions.append(("HIGH", f"팔로업 이메일 발송 ({ob['followup_due_now']}개 대기 중)"))
    if mrr == 0:
        actions.append(("HIGH", "Starter Plan 결제 유도 — 블로그 CTA, SNS, 지인 소개 강화"))
    if "windows_build" in bcc["blockers"]:
        actions.append(("MED", "Windows 환경에서 BCC Add-in 빌드 → QA 스크린샷 → App Store 제출"))
    actions.append(("LOW", "웹사이트 배포 (website/ 변경사항 → deploy_website.sh 실행)"))

    for level, desc in actions:
        level_color = RED if level == "HIGH" else YELLOW if level == "MED" else GRAY
        print(f"     [{_color(level, level_color)}] {desc}")

    print()
    print(_color("=" * 60, CYAN))
    print()


# ── 진입점 ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="LUA BIM LABS 매출 현황 대시보드")
    parser.add_argument("--json", action="store_true", help="JSON 형식으로 출력")
    args = parser.parse_args()

    data = {
        "generated_at": datetime.now().isoformat(),
        "starter_plan": starter_plan_stats(),
        "education": education_stats(),
        "outbound_sales": outbound_sales_stats(),
        "bcc_addin": bcc_addin_status(),
        "ai_cost": ai_cost_stats(),
    }

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_dashboard(data)


if __name__ == "__main__":
    main()
