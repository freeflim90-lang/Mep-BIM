#!/usr/bin/env python3
"""Gmail 수신함에서 새 문의 이메일을 감지하여 텔레그램으로 알림 전송."""

from __future__ import annotations

import email
import imaplib
import json
import os
import sys
from email.header import decode_header
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.email_notifications import load_local_env

load_local_env()

GMAIL_ADDRESS   = os.environ.get("GMAIL_ADDRESS", "")
GMAIL_PASSWORD  = os.environ.get("GMAIL_APP_PASSWORD", "")
BOT_TOKEN       = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID         = os.environ.get("TELEGRAM_CHAT_ID", "")
SEEN_FILE       = PROJECT_ROOT / "data" / "gmail_inquiry_seen.json"
LOG_FILE        = PROJECT_ROOT / "logs" / "gmail_inquiry_monitor.log"

# 알림 제외 발신자 (내부/자동화 도메인)
SKIP_SENDERS = {
    "noreply", "no-reply", "mailer-daemon", "postmaster",
    "notifications", "alerts", "donotreply",
    "github.com", "cloudflare.com", "anthropic.com",
    "telegram.org", "notion.so",
}


def _decode_str(raw: str | bytes, charset: str | None = None) -> str:
    if isinstance(raw, bytes):
        return raw.decode(charset or "utf-8", errors="replace")
    return raw


def decode_mime_header(value: str) -> str:
    parts = decode_header(value or "")
    return "".join(_decode_str(t, c) for t, c in parts)


def load_seen() -> set[str]:
    if SEEN_FILE.exists():
        try:
            return set(json.loads(SEEN_FILE.read_text()))
        except Exception:
            pass
    return set()


def save_seen(seen: set[str]) -> None:
    SEEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    SEEN_FILE.write_text(json.dumps(sorted(seen), ensure_ascii=False, indent=2))


def should_skip(sender: str) -> bool:
    s = sender.lower()
    return any(kw in s for kw in SKIP_SENDERS) or s.endswith(GMAIL_ADDRESS.lower())


def send_telegram(text: str) -> None:
    import urllib.request, urllib.parse
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode()
    req = urllib.request.Request(url, data=data)
    urllib.request.urlopen(req, timeout=10)


def fetch_new_inquiries() -> list[dict]:
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(GMAIL_ADDRESS, GMAIL_PASSWORD)
    mail.select("INBOX")

    _, data = mail.search(None, "UNSEEN")
    uid_list = data[0].split() if data[0] else []

    seen = load_seen()
    results = []

    for uid in uid_list:
        uid_str = uid.decode()
        if uid_str in seen:
            continue

        _, msg_data = mail.fetch(uid, "(RFC822)")
        raw = msg_data[0][1]
        msg = email.message_from_bytes(raw)

        sender  = decode_mime_header(msg.get("From", ""))
        subject = decode_mime_header(msg.get("Subject", "(제목 없음)"))
        date    = msg.get("Date", "")

        if should_skip(sender):
            seen.add(uid_str)
            continue

        # 본문 미리보기 (최대 200자)
        preview = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    charset = part.get_content_charset() or "utf-8"
                    preview = part.get_payload(decode=True).decode(charset, errors="replace")
                    break
        else:
            charset = msg.get_content_charset() or "utf-8"
            preview = msg.get_payload(decode=True).decode(charset, errors="replace")

        preview = " ".join(preview.split())[:200]

        results.append({
            "uid": uid_str,
            "sender": sender,
            "subject": subject,
            "date": date,
            "preview": preview,
        })
        seen.add(uid_str)

    mail.logout()
    save_seen(seen)
    return results


def main() -> int:
    if not all([GMAIL_ADDRESS, GMAIL_PASSWORD, BOT_TOKEN, CHAT_ID]):
        print("환경변수 누락 (GMAIL_ADDRESS / GMAIL_APP_PASSWORD / TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID)")
        return 1

    try:
        inquiries = fetch_new_inquiries()
    except Exception as e:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LOG_FILE.open("a") as f:
            import datetime
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} ERROR {e}\n")
        return 1

    for inq in inquiries:
        msg = (
            f"📧 새 문의 이메일\n"
            f"From: {inq['sender']}\n"
            f"Subject: {inq['subject']}\n"
            f"Date: {inq['date']}\n\n"
            f"{inq['preview']}{'…' if len(inq['preview']) >= 200 else ''}"
        )
        try:
            send_telegram(msg)
        except Exception as e:
            print(f"텔레그램 전송 실패: {e}")

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a") as f:
        import datetime
        f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} checked, new={len(inquiries)}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
