# ================================================================
# mailer.py — 제안 이메일 발송
# ================================================================
import smtplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import (
    SMTP_SERVER, SMTP_PORT,
    SENDER_EMAIL, SENDER_PASSWORD, SENDER_NAME,
    EMAIL_SEND_DELAY,
    BASE_DIR,
)

TEMPLATE_PATH   = os.path.join(BASE_DIR, "templates", "proposal_email.html")
FOLLOWUP1_PATH  = os.path.join(BASE_DIR, "templates", "followup1_email.html")
FOLLOWUP2_PATH  = os.path.join(BASE_DIR, "templates", "followup2_email.html")


def _load_template(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _render(template: str, company: dict) -> str:
    """{{변수}} 형태의 플레이스홀더 치환"""
    return (template
        .replace("{{COMPANY_NAME}}", company.get("name", "귀사"))
        .replace("{{CATEGORY}}",     company.get("category", "BIM"))
        .replace("{{ADDRESS}}",      company.get("address", ""))
        .replace("{{SENDER_EMAIL}}", SENDER_EMAIL)
    )


def _send_email(to_email: str, subject: str, html_body: str, dry_run: bool = False, label: str = "") -> bool:
    """단일 이메일 발송 공통 함수."""
    if dry_run:
        print(f"  [DRY RUN] To: {to_email} | Subject: {subject}")
        return True

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"]      = to_email
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        print(f"  ✅ 발송 완료{label}: {to_email}")
        return True
    except Exception as e:
        print(f"  ❌ 발송 실패{label}: {to_email} — {e}")
        return False


def send_proposal(company: dict, dry_run: bool = False) -> bool:
    """단일 업체에게 최초 제안 이메일 발송."""
    to_email = company.get("email", "").strip()
    if not to_email:
        print(f"  [SKIP] 이메일 없음: {company['name']}")
        return False

    html_body = _render(_load_template(TEMPLATE_PATH), company)
    subject   = f"[LUA BIM LABS] MEP BIM 협업 제안 — {company['name']} 귀중"
    return _send_email(to_email, subject, html_body, dry_run=dry_run, label=f" [{company['name']}]")


def send_followup(company: dict, followup_count: int, dry_run: bool = False) -> bool:
    """팔로업 이메일 발송 (1차: D+3, 2차: D+10)."""
    to_email = company.get("email", "").strip()
    if not to_email:
        return False

    template_path = FOLLOWUP1_PATH if followup_count == 1 else FOLLOWUP2_PATH
    html_body = _render(_load_template(template_path), company)
    subject   = f"[LUA BIM LABS] MEP BIM 협업 제안 ({followup_count}차 팔로업) — {company['name']} 귀중"
    return _send_email(to_email, subject, html_body, dry_run=dry_run, label=f" [{company['name']} F{followup_count}]")


def send_bulk(companies: list[dict], dry_run: bool = False) -> dict:
    """여러 업체에 순차 발송. 결과 반환."""
    success, fail, skip = 0, 0, 0

    for company in companies:
        result = send_proposal(company, dry_run=dry_run)
        if result is True:
            success += 1
        elif result is False and company.get("email"):
            fail += 1
        else:
            skip += 1

        if not dry_run:
            time.sleep(EMAIL_SEND_DELAY)

    return {"success": success, "fail": fail, "skip": skip}


def send_followup_bulk(companies: list[dict], dry_run: bool = False) -> dict:
    """팔로업 대상 업체에 순차 발송."""
    success, fail = 0, 0

    for company in companies:
        fc = (company.get("followup_count") or 0) + 1
        result = send_followup(company, followup_count=fc, dry_run=dry_run)
        if result:
            success += 1
        else:
            fail += 1

        if not dry_run:
            time.sleep(EMAIL_SEND_DELAY)

    return {"success": success, "fail": fail}
