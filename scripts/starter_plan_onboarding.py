#!/usr/bin/env python3
"""Starter Plan client onboarding helper.

This script keeps the first-launch operation intentionally semi-automated:
Google Forms and PayPal are checked by the operator, then verified clients are
registered here for Telegram delivery.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLIENTS_FILE = PROJECT_ROOT / "data" / "starter_plan" / "clients.json"
OBSIDIAN_CLIENT_DIR = (
    PROJECT_ROOT
    / "obsidian_vaults"
    / "lua_bim_lab_global_map"
    / "NAS_Knowledge"
    / "Starter_Plan_Clients"
)


def load_dotenv() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_registry() -> dict:
    if not CLIENTS_FILE.exists():
        return {"version": 1, "clients": []}
    data = json.loads(CLIENTS_FILE.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("clients"), list):
        raise SystemExit(f"Invalid registry format: {CLIENTS_FILE}")
    data.setdefault("version", 1)
    return data


def save_registry(registry: dict) -> None:
    CLIENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CLIENTS_FILE.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def normalize_username(value: str) -> str:
    value = value.strip()
    if value and not value.startswith("@"):
        return f"@{value}"
    return value


def make_client_id(name: str, email: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "client"
    digest = hashlib.sha1(email.strip().lower().encode("utf-8")).hexdigest()[:8]
    return f"starter-{date.today().strftime('%Y%m%d')}-{cleaned[:24]}-{digest}"


def find_client(registry: dict, client_id: str) -> dict:
    for client in registry["clients"]:
        if client.get("client_id") == client_id:
            return client
    raise SystemExit(f"Client not found: {client_id}")


def infer_status(client: dict) -> str:
    paid = client.get("payment_status") == "paid"
    verified_chat = client.get("telegram_status") == "verified" and client.get("telegram_chat_id")
    if paid and verified_chat:
        return "active"
    if paid:
        return "paid_waiting_telegram"
    return "pending_payment"


def add_client(args: argparse.Namespace) -> None:
    registry = load_registry()
    email = args.email.strip().lower()
    for client in registry["clients"]:
        if client.get("email", "").strip().lower() == email:
            raise SystemExit(f"Client already exists for email: {email}")

    client = {
        "client_id": make_client_id(args.name, email),
        "plan_id": "starter",
        "plan_name": "LUA BIM LABS Starter Plan",
        "monthly_price_usd": 39,
        "name": args.name.strip(),
        "email": email,
        "country": args.country.strip(),
        "preferred_language": args.preferred_language.strip(),
        "paypal_email": args.paypal_email.strip().lower(),
        "paypal_transaction_id": args.paypal_transaction_id.strip(),
        "payment_status": "paid" if args.payment_verified else "unverified",
        "payment_verified_at": now_iso() if args.payment_verified else "",
        "telegram_username": normalize_username(args.telegram_username),
        "telegram_display_name": args.telegram_display_name.strip(),
        "telegram_chat_id": args.telegram_chat_id.strip(),
        "telegram_status": "verified" if args.telegram_chat_id else "pending_start",
        "current_bim_level": args.current_bim_level.strip(),
        "main_mep_discipline": args.main_mep_discipline.strip(),
        "learning_goal": args.learning_goal.strip(),
        "biggest_difficulty": args.biggest_difficulty.strip(),
        "start_date": args.start_date.strip(),
        "end_date": args.end_date.strip(),
        "status": "",
        "source": "google_form_manual_entry",
        "application_sheet_row": args.sheet_row.strip(),
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "admin_notes": args.admin_notes.strip(),
        "welcome_sent_at": "",
        "obsidian_note": "",
    }
    if client["payment_status"] == "paid" and not client["start_date"]:
        client["start_date"] = date.today().isoformat()
    if client["payment_status"] == "paid" and not client["end_date"]:
        client["end_date"] = (date.today() + timedelta(days=30)).isoformat()
    client["status"] = infer_status(client)

    registry["clients"].append(client)
    save_registry(registry)
    print(f"created client_id={client['client_id']} status={client['status']}")


def mark_paid(args: argparse.Namespace) -> None:
    registry = load_registry()
    client = find_client(registry, args.client_id)
    client["payment_status"] = "paid"
    client["payment_verified_at"] = now_iso()
    if args.paypal_transaction_id:
        client["paypal_transaction_id"] = args.paypal_transaction_id.strip()
    if args.start_date:
        client["start_date"] = args.start_date
    elif not client.get("start_date"):
        client["start_date"] = date.today().isoformat()
    if args.end_date:
        client["end_date"] = args.end_date
    elif not client.get("end_date"):
        client["end_date"] = (date.fromisoformat(client["start_date"]) + timedelta(days=30)).isoformat()
    client["status"] = infer_status(client)
    client["updated_at"] = now_iso()
    save_registry(registry)
    print(f"updated client_id={client['client_id']} status={client['status']}")

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    admin_chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if token and admin_chat_id:
        msg = (
            f"[Starter] 💰 결제 확인 완료\n"
            f"이름: {client.get('name')}\n"
            f"이메일: {client.get('email')}\n"
            f"Telegram: {client.get('telegram_username')}\n"
            f"PayPal TX: {client.get('paypal_transaction_id') or '미입력'}"
        )
        send_telegram(admin_chat_id, msg)


def set_chat_id(args: argparse.Namespace) -> None:
    registry = load_registry()
    client = find_client(registry, args.client_id)
    client["telegram_chat_id"] = args.chat_id.strip()
    client["telegram_status"] = "verified"
    client["status"] = infer_status(client)
    client["updated_at"] = now_iso()
    save_registry(registry)
    print(f"updated client_id={client['client_id']} status={client['status']}")


def build_welcome_message(client: dict) -> str:
    name = client.get("name", "there")
    start_date = client.get("start_date") or date.today().isoformat()
    return "\n".join(
        [
            f"Hello {name}, welcome to the LUA BIM LABS Starter Plan.",
            "",
            "Your Telegram-based MEP BIM education service is now connected.",
            "",
            f"Plan: Starter Plan, USD 39 / month",
            f"Start date: {start_date}",
            "",
            "What you will receive:",
            "- One practical MEP BIM lesson per day",
            "- Beginner-friendly explanation",
            "- Basic checklist or action item",
            "- Monthly learning direction",
            "",
            "Important scope:",
            "- This service provides general educational content only.",
            "- Please do not send confidential project files, private drawings, contracts, personal data, or materials you do not have permission to share.",
            "- Project file review, Revit model QA, clash report review, engineering verification, code compliance confirmation, and construction approval are not included in the Starter Plan.",
            "",
            "You can ask one short clarification question per week during the launch period.",
        ]
    )


def send_telegram(chat_id: str, text: str) -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN is not configured.")
        return False
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"telegram=sent chat_id={chat_id} status={resp.status}")
            return True
    except Exception as exc:
        print(f"telegram=failed chat_id={chat_id} {type(exc).__name__}: {exc}")
        return False


def fetch_telegram_updates() -> list[dict]:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not configured.")
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/getUpdates")
    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if not payload.get("ok"):
        raise SystemExit(f"Telegram getUpdates failed: {payload}")
    return payload.get("result", [])


def list_telegram_updates(args: argparse.Namespace) -> None:
    wanted = normalize_username(args.username).lstrip("@").lower()
    rows = []
    for update in fetch_telegram_updates():
        message = update.get("message") or update.get("edited_message") or {}
        chat = message.get("chat") or {}
        user = message.get("from") or {}
        username = str(user.get("username", "")).lower()
        if wanted and username != wanted:
            continue
        rows.append(
            {
                "update_id": update.get("update_id", ""),
                "chat_id": chat.get("id", ""),
                "username": f"@{user.get('username', '')}" if user.get("username") else "",
                "name": " ".join(
                    item for item in [user.get("first_name", ""), user.get("last_name", "")] if item
                ),
                "text": str(message.get("text", ""))[:80],
            }
        )
    for row in rows:
        print(
            f"update_id={row['update_id']} chat_id={row['chat_id']} "
            f"username={row['username']} name={row['name']} text={row['text']}"
        )
    print(f"count={len(rows)}")


def connect_telegram(args: argparse.Namespace) -> None:
    registry = load_registry()
    client = find_client(registry, args.client_id)
    wanted = normalize_username(args.username or client.get("telegram_username", "")).lstrip("@").lower()
    if not wanted:
        raise SystemExit("No Telegram username is available.")
    matches = []
    for update in fetch_telegram_updates():
        message = update.get("message") or update.get("edited_message") or {}
        user = message.get("from") or {}
        username = str(user.get("username", "")).lower()
        chat_id = str((message.get("chat") or {}).get("id", "")).strip()
        if username == wanted and chat_id:
            matches.append((update.get("update_id", 0), chat_id))
    if not matches:
        raise SystemExit(f"No Telegram /start or message found for @{wanted}. Ask the client to message the bot first.")
    matches.sort()
    client["telegram_chat_id"] = matches[-1][1]
    client["telegram_status"] = "verified"
    client["status"] = infer_status(client)
    client["updated_at"] = now_iso()
    save_registry(registry)
    print(f"connected client_id={client['client_id']} chat_id={client['telegram_chat_id']} status={client['status']}")


def send_welcome(args: argparse.Namespace) -> None:
    registry = load_registry()
    client = find_client(registry, args.client_id)
    if client.get("status") != "active" and not args.force:
        raise SystemExit("Client is not active. Verify payment and Telegram chat_id first, or use --force.")
    chat_id = client.get("telegram_chat_id", "").strip()
    if not chat_id:
        raise SystemExit("Client has no telegram_chat_id.")

    message = build_welcome_message(client)
    if args.dry_run:
        print(message)
        return
    if send_telegram(chat_id, message):
        client["welcome_sent_at"] = now_iso()
        client["updated_at"] = now_iso()
        save_registry(registry)


def list_clients(args: argparse.Namespace) -> None:
    registry = load_registry()
    wanted = args.status.strip()
    clients = registry.get("clients", [])
    if wanted != "all":
        clients = [client for client in clients if client.get("status") == wanted]
    for client in clients:
        print(
            f"{client.get('client_id')} | {client.get('status')} | "
            f"{client.get('payment_status')} | {client.get('telegram_status')} | "
            f"{client.get('name')} | {client.get('email')} | {client.get('telegram_username')}"
        )
    print(f"count={len(clients)}")


def safe_note_name(client: dict) -> str:
    base = re.sub(r"[^A-Za-z0-9가-힣 _-]+", "", client.get("name", "Client")).strip()
    return f"{client.get('client_id')} - {base or 'Client'}.md"


def render_obsidian_note(client: dict) -> str:
    return "\n".join(
        [
            "---",
            "type: starter-plan-client",
            f"client_id: {client.get('client_id', '')}",
            f"status: {client.get('status', '')}",
            f"plan: {client.get('plan_name', '')}",
            "---",
            "",
            f"# {client.get('name', '')}",
            "",
            "## Service Status",
            f"- Status: {client.get('status', '')}",
            f"- Payment status: {client.get('payment_status', '')}",
            f"- Start date: {client.get('start_date', '')}",
            f"- End date: {client.get('end_date', '')}",
            "",
            "## Contact",
            f"- Email: {client.get('email', '')}",
            f"- PayPal email: {client.get('paypal_email', '')}",
            f"- Telegram username: {client.get('telegram_username', '')}",
            f"- Telegram chat ID: {client.get('telegram_chat_id', '')}",
            "",
            "## Learning Profile",
            f"- Current BIM level: {client.get('current_bim_level', '')}",
            f"- Main MEP discipline: {client.get('main_mep_discipline', '')}",
            f"- Learning goal: {client.get('learning_goal', '')}",
            f"- Biggest difficulty: {client.get('biggest_difficulty', '')}",
            "",
            "## Scope Reminder",
            "- Starter Plan is general MEP BIM educational content only.",
            "- Do not request or store confidential project files, private drawings, contracts, or personal data.",
            "- Project file review, Revit model QA, clash report review, engineering design verification, code compliance confirmation, and construction approval are excluded.",
            "",
            "## Admin Notes",
            client.get("admin_notes", ""),
            "",
        ]
    )


def export_obsidian(args: argparse.Namespace) -> None:
    registry = load_registry()
    targets = registry["clients"] if args.all else [find_client(registry, args.client_id)]
    OBSIDIAN_CLIENT_DIR.mkdir(parents=True, exist_ok=True)
    for client in targets:
        note_path = OBSIDIAN_CLIENT_DIR / safe_note_name(client)
        note_path.write_text(render_obsidian_note(client), encoding="utf-8")
        client["obsidian_note"] = str(note_path.relative_to(PROJECT_ROOT))
        client["updated_at"] = now_iso()
        print(f"obsidian={note_path}")
    save_registry(registry)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Starter Plan onboarding.")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add-client")
    add.add_argument("--name", required=True)
    add.add_argument("--email", required=True)
    add.add_argument("--country", default="")
    add.add_argument("--preferred-language", default="English")
    add.add_argument("--paypal-email", required=True)
    add.add_argument("--paypal-transaction-id", default="")
    add.add_argument("--payment-verified", action="store_true")
    add.add_argument("--telegram-username", required=True)
    add.add_argument("--telegram-display-name", default="")
    add.add_argument("--telegram-chat-id", default="")
    add.add_argument("--current-bim-level", default="")
    add.add_argument("--main-mep-discipline", default="")
    add.add_argument("--learning-goal", default="")
    add.add_argument("--biggest-difficulty", default="")
    add.add_argument("--start-date", default="")
    add.add_argument("--end-date", default="")
    add.add_argument("--sheet-row", default="")
    add.add_argument("--admin-notes", default="")
    add.set_defaults(func=add_client)

    paid = sub.add_parser("mark-paid")
    paid.add_argument("--client-id", required=True)
    paid.add_argument("--paypal-transaction-id", default="")
    paid.add_argument("--start-date", default="")
    paid.add_argument("--end-date", default="")
    paid.set_defaults(func=mark_paid)

    chat = sub.add_parser("set-chat-id")
    chat.add_argument("--client-id", required=True)
    chat.add_argument("--chat-id", required=True)
    chat.set_defaults(func=set_chat_id)

    updates = sub.add_parser("list-telegram-updates")
    updates.add_argument("--username", default="")
    updates.set_defaults(func=list_telegram_updates)

    connect = sub.add_parser("connect-telegram")
    connect.add_argument("--client-id", required=True)
    connect.add_argument("--username", default="")
    connect.set_defaults(func=connect_telegram)

    welcome = sub.add_parser("send-welcome")
    welcome.add_argument("--client-id", required=True)
    welcome.add_argument("--dry-run", action="store_true")
    welcome.add_argument("--force", action="store_true")
    welcome.set_defaults(func=send_welcome)

    listing = sub.add_parser("list")
    listing.add_argument("--status", default="all")
    listing.set_defaults(func=list_clients)

    obsidian = sub.add_parser("export-obsidian")
    obsidian.add_argument("--client-id", default="")
    obsidian.add_argument("--all", action="store_true")
    obsidian.set_defaults(func=export_obsidian)
    return parser


def main() -> None:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()
    if getattr(args, "command", "") == "export-obsidian" and not args.all and not args.client_id:
        parser.error("export-obsidian requires --client-id or --all")
    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
