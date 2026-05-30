#!/usr/bin/env python3
"""Sync Telegram /start chat IDs into the Starter Plan Google Sheet.

Recommended first-launch automation:
- client submits Google Form
- client pays through PayPal
- client opens Telegram bot and sends /start
- this script matches Telegram username to the sheet and writes chat_id
- paid + Telegram-verified rows are mirrored to local delivery registry
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path
from urllib.error import HTTPError

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "scripts" / "outbound_sales" / "data" / "service_account.json"
CLIENTS_FILE = PROJECT_ROOT / "data" / "starter_plan" / "clients.json"
DEFAULT_SPREADSHEET_ID = "1v1t5k76mAhKSBx-x19fEw3Kmi7c6heFKMrkIbK_qcFk"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

HEADER_ALIASES = {
    "name": ["Full name", "Name"],
    "email": ["Email adress", "Email address", "Email"],
    "country": ["Country"],
    "language": ["Preferred language"],
    "paypal_email": ["Paypal Payment Email", "PayPal Payment Email", "Email used for PayPal payment"],
    "paypal_transaction": ["PayPal transaction ID or receipt ID", "PayPal Transaction ID"],
    "telegram_username": ["Telegram username", "Telegram username (Please include @. Example: @yourname)"],
    "telegram_display_name": ["Telegram display name"],
    "current_bim_level": ["Current BIM level"],
    "main_mep_discipline": ["Main MEP discipline"],
    "payment_verified": ["Payment Verified"],
    "payment_verified_at": ["Payment Verified At"],
    "amount": ["PayPal Amount USD"],
    "transaction_confirmed": ["PayPal Transaction ID Confirmed"],
    "telegram_start_confirmed": ["Telegram Start Confirmed"],
    "telegram_chat_id": ["Telegram Chat ID"],
    "telegram_verified": ["Telegram Verified"],
    "client_id": ["Client ID"],
    "client_status": ["Client Status"],
    "start_date": ["Start Date"],
    "end_date": ["End Date"],
    "next_action": ["Next Action"],
    "admin_notes": ["Admin Notes"],
}


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


def normalize_username(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("@"):
        value = value[1:]
    return value.lower()


def truthy(value: str) -> bool:
    return value.strip().lower() in {"yes", "y", "true", "paid", "verified", "확인", "완료"}


def col_to_a1(index: int) -> str:
    letters = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def get_service():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


def send_admin_notification(token: str, chat_id: str, text: str) -> None:
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as exc:
        print(f"admin_notify=failed {type(exc).__name__}: {exc}")


def fetch_telegram_updates() -> dict[str, dict]:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not configured.")
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/getUpdates")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        if exc.code == 409:
            print("telegram_updates=skipped reason=conflict")
            return {}
        raise
    if not payload.get("ok"):
        raise SystemExit(f"Telegram getUpdates failed: {payload}")

    matched: dict[str, dict] = {}
    for update in payload.get("result", []):
        message = update.get("message") or update.get("edited_message") or {}
        user = message.get("from") or {}
        chat = message.get("chat") or {}
        username = normalize_username(str(user.get("username", "")))
        chat_id = str(chat.get("id", "")).strip()
        if not username or not chat_id:
            continue
        matched[username] = {
            "update_id": update.get("update_id", 0),
            "chat_id": chat_id,
            "display_name": " ".join(
                item for item in [user.get("first_name", ""), user.get("last_name", "")] if item
            ).strip(),
            "text": str(message.get("text", ""))[:80],
        }
    return matched


def get_first_sheet(service, spreadsheet_id: str) -> tuple[str, list[list[str]]]:
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    title = meta["sheets"][0]["properties"]["title"]
    values = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=f"{title}!A:AB")
        .execute()
        .get("values", [])
    )
    return title, values


def build_column_map(headers: list[str]) -> dict[str, int]:
    normalized = {header.strip().lower(): idx for idx, header in enumerate(headers)}
    columns: dict[str, int] = {}
    for key, aliases in HEADER_ALIASES.items():
        for alias in aliases:
            idx = normalized.get(alias.strip().lower())
            if idx is not None:
                columns[key] = idx
                break
        if key not in columns:
            for idx, header in enumerate(headers):
                if aliases[0].strip().lower() in header.strip().lower():
                    columns[key] = idx
                    break
    required = ["telegram_username", "telegram_chat_id", "telegram_start_confirmed", "telegram_verified", "client_status"]
    missing = [key for key in required if key not in columns]
    if missing:
        raise SystemExit(f"Missing required sheet columns: {', '.join(missing)}")
    return columns


def row_get(row: list[str], columns: dict[str, int], key: str) -> str:
    idx = columns.get(key)
    if idx is None or idx >= len(row):
        return ""
    return row[idx].strip()


def make_client_id(row_number: int, name: str, email: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or f"row-{row_number}"
    digest = hashlib.sha1((email or str(row_number)).strip().lower().encode("utf-8")).hexdigest()[:8]
    return f"starter-{date.today().strftime('%Y%m%d')}-{cleaned[:20]}-{digest}"


def load_clients() -> dict:
    if not CLIENTS_FILE.exists():
        return {"version": 1, "clients": []}
    return json.loads(CLIENTS_FILE.read_text(encoding="utf-8"))


def save_clients(registry: dict) -> None:
    CLIENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CLIENTS_FILE.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def upsert_local_client(row: list[str], columns: dict[str, int], row_number: int, client_id: str) -> None:
    registry = load_clients()
    clients = registry.setdefault("clients", [])
    existing = next((client for client in clients if client.get("client_id") == client_id), None)
    if existing is None:
        existing = {"client_id": client_id}
        clients.append(existing)

    start_date = row_get(row, columns, "start_date") or date.today().isoformat()
    end_date = row_get(row, columns, "end_date") or (date.fromisoformat(start_date) + timedelta(days=30)).isoformat()
    existing.update(
        {
            "plan_id": "starter",
            "plan_name": "LUA BIM LABS Starter Plan",
            "monthly_price_usd": 39,
            "name": row_get(row, columns, "name"),
            "email": row_get(row, columns, "email").lower(),
            "country": row_get(row, columns, "country"),
            "preferred_language": row_get(row, columns, "language") or "English",
            "paypal_email": row_get(row, columns, "paypal_email").lower(),
            "paypal_transaction_id": row_get(row, columns, "paypal_transaction"),
            "payment_status": "paid",
            "telegram_username": "@" + normalize_username(row_get(row, columns, "telegram_username")),
            "telegram_display_name": row_get(row, columns, "telegram_display_name"),
            "telegram_chat_id": row_get(row, columns, "telegram_chat_id"),
            "telegram_status": "verified",
            "current_bim_level": row_get(row, columns, "current_bim_level"),
            "main_mep_discipline": row_get(row, columns, "main_mep_discipline"),
            "start_date": start_date,
            "end_date": end_date,
            "status": "active",
            "source": "google_sheet_telegram_sync",
            "application_sheet_row": str(row_number),
            "updated_at": date.today().isoformat(),
        }
    )
    save_clients(registry)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync Telegram chat IDs into the Starter Plan Google Sheet.")
    parser.add_argument("--spreadsheet-id", default=DEFAULT_SPREADSHEET_ID)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-local-registry", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    admin_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")

    updates = fetch_telegram_updates()
    service = get_service()
    sheet_title, values = get_first_sheet(service, args.spreadsheet_id)
    if not values:
        raise SystemExit("Sheet is empty.")
    headers = values[0]
    columns = build_column_map(headers)

    today = date.today().isoformat()
    batch_values = []
    local_sync_count = 0
    matched_count = 0

    # Notify admin of new Google Form submissions (rows without client_id)
    if bot_token and admin_chat_id and not args.dry_run:
        for offset, row in enumerate(values[1:], start=2):
            name = row_get(row, columns, "name")
            email = row_get(row, columns, "email")
            existing_client_id = row_get(row, columns, "client_id") if "client_id" in columns else ""
            if name and email and not existing_client_id:
                msg = (
                    f"[Starter] 📋 신규 신청\n"
                    f"이름: {name}\n"
                    f"이메일: {email}\n"
                    f"Telegram: {row_get(row, columns, 'telegram_username')}"
                )
                send_admin_notification(bot_token, admin_chat_id, msg)

    for offset, row in enumerate(values[1:], start=2):
        username = normalize_username(row_get(row, columns, "telegram_username"))
        if not username or username not in updates:
            continue

        matched_count += 1
        update = updates[username]
        row_extended = [*row, *[""] * (len(headers) - len(row))]
        row_extended[columns["telegram_start_confirmed"]] = "yes"
        row_extended[columns["telegram_chat_id"]] = update["chat_id"]
        row_extended[columns["telegram_verified"]] = "yes"

        client_id = row_get(row_extended, columns, "client_id")
        if not client_id:
            client_id = make_client_id(
                offset,
                row_get(row_extended, columns, "name"),
                row_get(row_extended, columns, "email"),
            )
            row_extended[columns["client_id"]] = client_id

        payment_ok = truthy(row_get(row_extended, columns, "payment_verified"))
        prev_status = row_get(row, columns, "client_status") if "client_status" in columns else ""
        if payment_ok:
            row_extended[columns["client_status"]] = "active"
            if "start_date" in columns and not row_get(row_extended, columns, "start_date"):
                row_extended[columns["start_date"]] = today
            if "end_date" in columns and not row_get(row_extended, columns, "end_date"):
                row_extended[columns["end_date"]] = (date.today() + timedelta(days=30)).isoformat()
            if "next_action" in columns:
                row_extended[columns["next_action"]] = "Active - daily lessons enabled"
            if not args.no_local_registry:
                upsert_local_client(row_extended, columns, offset, client_id)
                local_sync_count += 1
            # Notify admin when a client is newly activated
            if bot_token and admin_chat_id and prev_status != "active" and not args.dry_run:
                name = row_get(row_extended, columns, "name")
                tg = row_get(row_extended, columns, "telegram_username")
                msg = (
                    f"[Starter] 💰 결제 확인 + 활성화\n"
                    f"이름: {name}\n"
                    f"Telegram: @{tg}\n"
                    f"chat_id: {update['chat_id']}"
                )
                send_admin_notification(bot_token, admin_chat_id, msg)
        else:
            row_extended[columns["client_status"]] = "pending_payment"
            if "next_action" in columns:
                row_extended[columns["next_action"]] = "Verify PayPal payment"

        start_col = min(
            columns["telegram_start_confirmed"],
            columns["telegram_chat_id"],
            columns["telegram_verified"],
            columns["client_id"],
            columns["client_status"],
        )
        end_col = max(
            columns["telegram_start_confirmed"],
            columns["telegram_chat_id"],
            columns["telegram_verified"],
            columns["client_id"],
            columns["client_status"],
            columns.get("start_date", 0),
            columns.get("end_date", 0),
            columns.get("next_action", 0),
        )
        batch_values.append(
            {
                "range": f"{sheet_title}!{col_to_a1(start_col)}{offset}:{col_to_a1(end_col)}{offset}",
                "values": [row_extended[start_col : end_col + 1]],
            }
        )

    if args.dry_run:
        print(f"dry_run=true matched_rows={matched_count} local_registry_candidates={local_sync_count}")
        return

    if batch_values:
        service.spreadsheets().values().batchUpdate(
            spreadsheetId=args.spreadsheet_id,
            body={"valueInputOption": "USER_ENTERED", "data": batch_values},
        ).execute()
    print(f"matched_rows={matched_count} sheet_rows_updated={len(batch_values)} local_clients_synced={local_sync_count}")


if __name__ == "__main__":
    main()
