from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CODE_DEV_RECIPIENT = "jycomapany90@naver.com"


def load_local_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def gmail_settings() -> dict[str, str]:
    load_local_env()
    sender = (
        os.environ.get("CODE_DEV_GMAIL_FROM")
        or os.environ.get("GMAIL_ADDRESS")
        or os.environ.get("GMAIL_USER")
        or ""
    )
    password = (
        os.environ.get("CODE_DEV_GMAIL_APP_PASSWORD")
        or os.environ.get("GMAIL_APP_PASSWORD")
        or os.environ.get("GMAIL_PASSWORD")
        or ""
    )
    recipient = (
        os.environ.get("CODE_DEV_GMAIL_TO")
        or os.environ.get("GMAIL_TO")
        or DEFAULT_CODE_DEV_RECIPIENT
    )
    return {
        "enabled": os.environ.get("CODE_DEV_GMAIL_ENABLED", "true").lower(),
        "sender": sender,
        "password": password,
        "recipient": recipient,
        "smtp_host": os.environ.get("GMAIL_SMTP_HOST", "smtp.gmail.com"),
        "smtp_port": os.environ.get("GMAIL_SMTP_PORT", "587"),
    }


def can_send_gmail() -> tuple[bool, str]:
    settings = gmail_settings()
    if settings["enabled"] in {"0", "false", "no", "off"}:
        return False, "CODE_DEV_GMAIL_ENABLED=false"
    if not settings["sender"]:
        return False, "missing GMAIL_ADDRESS or CODE_DEV_GMAIL_FROM"
    if not settings["password"]:
        return False, "missing Gmail app password"
    if not settings["recipient"]:
        return False, "missing CODE_DEV_GMAIL_TO or GMAIL_TO"
    return True, "ok"


def send_gmail(subject: str, body: str, attachments: list[Path] | None = None) -> dict[str, str | bool]:
    ok, reason = can_send_gmail()
    settings = gmail_settings()
    if not ok:
        return {"ok": False, "reason": reason}

    msg = EmailMessage()
    msg["Subject"] = subject[:240]
    msg["From"] = settings["sender"]
    msg["To"] = settings["recipient"]
    msg.set_content(body)

    for path in attachments or []:
        if not path.exists() or not path.is_file():
            continue
        data = path.read_bytes()
        msg.add_attachment(
            data,
            maintype="application",
            subtype="octet-stream",
            filename=path.name,
        )

    with smtplib.SMTP(settings["smtp_host"], int(settings["smtp_port"]), timeout=20) as server:
        server.ehlo()
        server.starttls()
        server.login(settings["sender"], settings["password"])
        server.send_message(msg)
    return {"ok": True, "reason": "sent"}
