from __future__ import annotations

import datetime as dt
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

from fastapi import APIRouter, HTTPException

from backend.contract_drafts import validate_project_date, write_contract_draft


def normalize_contact_payload(payload: dict[str, Any]) -> dict[str, str]:
    sender_email = str(payload.get("email", "")).strip()[:200]
    if not sender_email:
        raise HTTPException(status_code=400, detail="email required")

    return {
        "email": sender_email,
        "message": str(payload.get("message", "")).strip()[:2000],
        "company": str(payload.get("company", "")).strip()[:200],
        "phone": str(payload.get("phone", "")).strip()[:50],
        "project": str(payload.get("project", "")).strip()[:200],
        "building_type": str(payload.get("building_type", "")).strip()[:100],
        "area": str(payload.get("area", "")).strip()[:50],
        "budget": str(payload.get("budget", "")).strip()[:100],
        "disciplines": str(payload.get("disciplines", "")).strip()[:200],
        "lod": str(payload.get("lod", "")).strip()[:50],
        "formats": str(payload.get("formats", "")).strip()[:100],
        "start_date": validate_project_date(str(payload.get("start_date", "")).strip()[:20], "start_date"),
        "end_date": validate_project_date(str(payload.get("end_date", "")).strip()[:20], "end_date"),
    }


def build_contact_auto_reply_body(*, contact: dict[str, str], now: str) -> str:
    return f"""안녕하세요, {contact['company'] or '고객'}님.

LUA BIM LABS에 문의해 주셔서 감사합니다.

아래 내용으로 문의가 접수되었습니다.

  프로젝트명 : {contact['project'] or '-'}
  건물 용도  : {contact['building_type'] or '-'}
  연면적     : {(contact['area'] + ' m²') if contact['area'] else '-'}
  요청 공종  : {contact['disciplines'] or '-'}
  착수 희망  : {contact['start_date'] or '-'}

빠른 시일 내에 담당자가 연락드리겠습니다.

감사합니다.
LUA BIM LABS
https://luabimlabs.com
"""


def build_contact_email_body(*, contact: dict[str, str], now: str, contract_label: str) -> str:
    return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LUA BIM LABS — BIM 수행 문의서
접수 일시: {now}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

§ 01  담당자 정보
  성명 / 회사명 : {contact['company']}
  연락처 이메일 : {contact['email']}
  전화번호      : {contact['phone'] or '-'}

§ 02  프로젝트 개요
  프로젝트명    : {contact['project'] or '-'}
  건물 용도     : {contact['building_type'] or '-'}
  연면적        : {(contact['area'] + ' m²') if contact['area'] else '-'}
  희망 예산     : {contact['budget'] or '-'}

§ 03  요청 사항
  요청 공종     : {contact['disciplines'] or '-'}
  LOD 수준      : {contact['lod'] or '-'}
  납품 형식     : {contact['formats'] or '-'}

§ 04  일정
  착수 희망일   : {contact['start_date'] or '-'}
  납품 희망일   : {contact['end_date'] or '-'}

§ 05  추가 요청사항
{contact['message'] or '(없음)'}

§ 06  자동 생성 문서
  계약서 초안   : {contract_label}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""


def send_telegram_contact_notice(*, token: str, chat_id: str | None, text: str) -> tuple[bool, str]:
    if not token or token == "fake-bot-token" or not chat_id:
        return False, "missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID"
    try:
        data = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode()
        urllib.request.urlopen(
            urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data),
            timeout=8,
        )
        return True, ""
    except Exception as exc:  # noqa: BLE001 - contact intake must remain available.
        return False, str(exc)


def append_contact_log(*, path: Path, now: str, email: str, contract_log: str, email_ok: bool, email_err: str, tg_ok: bool, tg_err: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as file:
            file.write(
                f"{now} | from={email} | contract={contract_log} | "
                f"email={'OK' if email_ok else 'FAIL:' + email_err} | "
                f"tg={'OK' if tg_ok else 'FAIL:' + tg_err}\n"
            )
    except OSError:
        return


def create_contact_intake_router(
    *,
    project_root: Path,
    telegram_bot_token: str,
    telegram_chat_id: str | None,
    gmail_settings: Callable[[], dict[str, str]],
    send_gmail: Callable[..., dict[str, Any]],
    now: Callable[[], dt.datetime] = dt.datetime.now,
) -> APIRouter:
    router = APIRouter(tags=["contact-intake"])

    @router.post("/api/contact")
    async def contact_form(payload: dict[str, Any]):
        contact = normalize_contact_payload(payload)
        if contact["start_date"] and contact["end_date"] and contact["start_date"] > contact["end_date"]:
            raise HTTPException(status_code=400, detail="end_date must be on or after start_date")

        received_at = now().strftime("%Y-%m-%d %H:%M")
        contract_path = None
        contract_err = ""
        try:
            contract_path = write_contract_draft(contact, received_at=received_at, project_root=project_root)
        except Exception as exc:  # noqa: BLE001 - do not lose the inbound lead.
            contract_err = str(exc)

        contract_label = str(contract_path.relative_to(project_root)) if contract_path else "생성 실패 - " + contract_err
        body = build_contact_email_body(contact=contact, now=received_at, contract_label=contract_label)

        email_ok = False
        email_err = ""
        try:
            cfg = gmail_settings()
            subject = f"[LUA BIM LABS 문의] {contact['company'] or contact['email']} ({received_at})"
            result = send_gmail(subject=subject, body=body, recipient=cfg["sender"])
            email_ok = bool(result.get("ok", False))
            email_err = str(result.get("reason", ""))
        except Exception as exc:  # noqa: BLE001
            email_err = str(exc)

        contract_summary = f"\n계약서 초안: {contract_path.relative_to(project_root)}" if contract_path else f"\n계약서 초안 생성 실패: {contract_err}"
        tg_summary = (
            f"{contact['company'] or contact['email']} / {contact['project'] or '프로젝트명 미기입'} / "
            f"{contact['building_type'] or '용도 미기입'} / 예산: {contact['budget'] or '미기입'}"
        )
        tg_text = f"웹 문의서 접수\n{tg_summary}\nEmail: {contact['email']}\n일시: {received_at}{contract_summary}"
        tg_ok, tg_err = send_telegram_contact_notice(token=telegram_bot_token, chat_id=telegram_chat_id, text=tg_text)

        auto_reply_ok = False
        try:
            if email_ok:
                reply_subject = f"[LUA BIM LABS] 문의 접수 확인 — {contact['company'] or contact['email']}"
                reply_body = build_contact_auto_reply_body(contact=contact, now=received_at)
                auto_result = send_gmail(subject=reply_subject, body=reply_body, recipient=contact["email"])
                auto_reply_ok = bool(auto_result.get("ok", False))
        except Exception:
            pass

        append_contact_log(
            path=project_root / "logs" / "contact_submissions.log",
            now=received_at,
            email=contact["email"],
            contract_log=str(contract_path.relative_to(project_root)) if contract_path else "FAIL:" + contract_err,
            email_ok=email_ok,
            email_err=email_err,
            tg_ok=tg_ok,
            tg_err=tg_err,
        )

        return {
            "status": "ok",
            "email_sent": email_ok,
            "auto_reply_sent": auto_reply_ok,
            "tg_sent": tg_ok,
            "contract_draft": str(contract_path.relative_to(project_root)) if contract_path else "",
            "contract_error": contract_err,
        }

    return router
