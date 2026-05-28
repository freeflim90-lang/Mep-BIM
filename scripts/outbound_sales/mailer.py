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

TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "proposal_email.html")


def _load_template() -> str:
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _render(template: str, company: dict) -> str:
    """{{변수}} 형태의 플레이스홀더 치환"""
    return (template
        .replace("{{COMPANY_NAME}}", company.get("name", "귀사"))
        .replace("{{CATEGORY}}",     company.get("category", "BIM"))
        .replace("{{ADDRESS}}",      company.get("address", ""))
    )


def send_proposal(company: dict, dry_run: bool = False) -> bool:
    """
    단일 업체에게 제안 이메일 발송.
    dry_run=True 이면 실제 발송 없이 내용만 출력.
    """
    to_email = company.get("email", "").strip()
    if not to_email:
        print(f"  [SKIP] 이메일 없음: {company['name']}")
        return False

    template = _load_template()
    html_body = _render(template, company)
    subject   = f"[LUA BIM LABS] MEP BIM 협업 제안 — {company['name']} 귀중"

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
        print(f"  ✅ 발송 완료: {company['name']} <{to_email}>")
        return True
    except Exception as e:
        print(f"  ❌ 발송 실패: {company['name']} — {e}")
        return False


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
