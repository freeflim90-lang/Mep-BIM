#!/usr/bin/env python3
"""
starter_plan_paypal_verify.py — Starter Plan 결제 수동 확인 + 클라이언트 활성화 도우미

역할:
  1. PayPal 최근 거래 내역 조회 (PayPal REST API)
  2. Google Sheet 신청서 응답과 매칭
  3. 미활성화 클라이언트 자동 감지
  4. clients.json 업데이트 + Telegram 알림 준비

사용법:
  python3 scripts/starter_plan_paypal_verify.py --check    # 미매칭 거래 목록 출력
  python3 scripts/starter_plan_paypal_verify.py --activate <email>  # 특정 이메일 활성화
  python3 scripts/starter_plan_paypal_verify.py --list     # 현재 클라이언트 목록

PayPal API 키 설정 (.env):
  PAYPAL_CLIENT_ID=...
  PAYPAL_CLIENT_SECRET=...
  PAYPAL_ENVIRONMENT=sandbox|live
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
import sys as _sys  # noqa: E402
if str(ROOT) not in _sys.path:
    _sys.path.insert(0, str(ROOT))
from backend.core.paths import STARTER_PLAN_DIR  # noqa: E402

CLIENTS_JSON  = STARTER_PLAN_DIR / "clients.json"
ENV_FILE      = ROOT / ".env"

PAYPAL_LIVE_URL    = "https://api-m.paypal.com"
PAYPAL_SANDBOX_URL = "https://api-m.sandbox.paypal.com"


# ── 환경 변수 로딩 ──────────────────────────────────────────────────

def _load_env() -> None:
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env()
PAYPAL_CLIENT_ID     = os.environ.get("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.environ.get("PAYPAL_CLIENT_SECRET", "")
PAYPAL_ENV           = os.environ.get("PAYPAL_ENVIRONMENT", "live")
BASE_URL = PAYPAL_LIVE_URL if PAYPAL_ENV == "live" else PAYPAL_SANDBOX_URL


# ── PayPal API ─────────────────────────────────────────────────────

def _paypal_token() -> str:
    if not httpx:
        raise RuntimeError("httpx 미설치. pip install httpx")
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        raise RuntimeError("PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET 환경변수 미설정")

    cred = base64.b64encode(f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}".encode()).decode()
    r = httpx.post(
        f"{BASE_URL}/v1/oauth2/token",
        headers={"Authorization": f"Basic {cred}", "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "client_credentials"},
        timeout=10,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def fetch_recent_payments(days: int = 30) -> list[dict]:
    """최근 N일 내 완료된 PayPal 거래 조회."""
    token = _paypal_token()
    start = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT00:00:00Z")
    end   = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    r = httpx.get(
        f"{BASE_URL}/v1/payments/payment",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "start_time": start,
            "end_time": end,
            "count": 100,
            "state": "approved",
        },
        timeout=10,
    )
    r.raise_for_status()
    payments = r.json().get("payments", [])
    result = []
    for p in payments:
        for trans in p.get("transactions", []):
            amount = trans.get("amount", {})
            payer = p.get("payer", {}).get("payer_info", {})
            result.append({
                "payment_id": p.get("id"),
                "create_time": p.get("create_time"),
                "state": p.get("state"),
                "payer_email": payer.get("email"),
                "payer_name": f"{payer.get('first_name','')} {payer.get('last_name','')}".strip(),
                "amount": f"{amount.get('total','')} {amount.get('currency','')}",
            })
    return result


# ── 클라이언트 관리 ────────────────────────────────────────────────

def _load_clients() -> dict:
    if CLIENTS_JSON.exists():
        return json.loads(CLIENTS_JSON.read_text(encoding="utf-8"))
    return {"version": 2, "clients": []}


def _save_clients(data: dict) -> None:
    CLIENTS_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def list_clients() -> None:
    data = _load_clients()
    clients = data.get("clients", [])
    if not clients:
        print("등록된 클라이언트 없음.")
        return
    print(f"{'이메일':<30} {'상태':<12} {'결제':<10} {'시작일':<12} {'공종'}")
    print("-" * 80)
    for c in clients:
        print(f"{c.get('email',''):<30} {c.get('status',''):<12} {c.get('payment_status',''):<10} "
              f"{c.get('start_date',''):<12} {c.get('discipline','')}")


def activate_client(email: str, telegram_id: str = "", discipline: str = "hvac",
                    language: str = "ko", client_name: str = "") -> None:
    data   = _load_clients()
    clients = data.get("clients", [])

    # 이미 존재하면 업데이트, 없으면 신규 추가
    existing = next((c for c in clients if c.get("email") == email), None)
    today = datetime.now().strftime("%Y-%m-%d")
    if existing:
        existing.update({
            "status": "active",
            "payment_status": "paid",
            "start_date": existing.get("start_date") or today,
        })
        print(f"✅ 기존 클라이언트 업데이트: {email}")
    else:
        import uuid
        new_id = f"c{uuid.uuid4().hex[:6]}"
        clients.append({
            "client_id": new_id,
            "name": client_name or email.split("@")[0],
            "email": email,
            "telegram_chat_id": telegram_id,
            "discipline": discipline,
            "language": language,
            "status": "active",
            "payment_status": "paid",
            "start_date": today,
        })
        print(f"✅ 신규 클라이언트 등록: {email} (ID: {new_id})")

    data["clients"] = clients
    _save_clients(data)
    print(f"   → clients.json 저장 완료")
    print(f"   → 다음 단계: Telegram {telegram_id or '[채팅 ID 필요]'} 로 환영 메시지 발송")


def check_unmatched(days: int = 30) -> None:
    """PayPal 거래 중 clients.json에 없는 항목 탐지."""
    data = _load_clients()
    known_emails = {c.get("email", "").lower() for c in data.get("clients", [])}

    print(f"최근 {days}일 PayPal 거래 조회 중...")
    try:
        payments = fetch_recent_payments(days=days)
    except RuntimeError as e:
        print(f"❌ PayPal API 오류: {e}")
        print()
        print("PayPal API 없이 수동 처리 방법:")
        print("  1. PayPal 계정 → Activity → Completed 거래 확인")
        print("  2. 신청서(Google Sheet)에서 PayPal 이메일 매칭")
        print("  3. python3 scripts/starter_plan_paypal_verify.py --activate <email>")
        return

    unmatched = [p for p in payments if p["payer_email"] and
                 p["payer_email"].lower() not in known_emails]

    if not unmatched:
        print("✅ 미매칭 거래 없음. 모든 결제가 클라이언트 목록에 등록됨.")
        return

    print(f"\n⚠  미활성화 결제 {len(unmatched)}건 발견:")
    print(f"{'결제 이메일':<32} {'금액':<18} {'날짜'}")
    print("-" * 70)
    for p in unmatched:
        date = (p.get("create_time") or "")[:10]
        print(f"{p['payer_email']:<32} {p['amount']:<18} {date}")

    print()
    print("활성화 명령어:")
    for p in unmatched:
        print(f"  python3 scripts/starter_plan_paypal_verify.py --activate {p['payer_email']}")


# ── 진입점 ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Starter Plan PayPal 결제 확인 도우미")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check",    action="store_true", help="미매칭 결제 탐지")
    group.add_argument("--activate", metavar="EMAIL",     help="클라이언트 활성화")
    group.add_argument("--list",     action="store_true", help="현재 클라이언트 목록")
    parser.add_argument("--telegram", default="",         help="Telegram Chat ID (--activate 시)")
    parser.add_argument("--discipline", default="hvac",   help="공종 (--activate 시): hvac|piping|plumbing|fire|electrical")
    parser.add_argument("--lang",    default="ko",        help="언어 (--activate 시): ko|en|ja|zh|ar")
    parser.add_argument("--name",    default="",          help="클라이언트 이름 (--activate 시)")
    parser.add_argument("--days",    type=int, default=30, help="조회 기간 (일)")
    args = parser.parse_args()

    if args.list:
        list_clients()
    elif args.check:
        check_unmatched(days=args.days)
    elif args.activate:
        activate_client(
            email=args.activate,
            telegram_id=args.telegram,
            discipline=args.discipline,
            language=args.lang,
            client_name=args.name,
        )


if __name__ == "__main__":
    main()
