#!/usr/bin/env python3
"""Configure the Starter Plan Google Sheet for application management."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "scripts" / "outbound_sales" / "data" / "service_account.json"
DEFAULT_SPREADSHEET_ID = "1v1t5k76mAhKSBx-x19fEw3Kmi7c6heFKMrkIbK_qcFk"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

ADMIN_COLUMNS = [
    "Payment Verified",
    "Payment Verified At",
    "PayPal Amount USD",
    "PayPal Transaction ID Confirmed",
    "Telegram Start Confirmed",
    "Telegram Chat ID",
    "Telegram Verified",
    "Client ID",
    "Client Status",
    "Start Date",
    "End Date",
    "Welcome Sent",
    "Obsidian Note",
    "Last Lesson Sent",
    "Next Action",
    "Admin Notes",
]

STATUS_OPTIONS = [
    "pending_payment",
    "paid_waiting_telegram",
    "active",
    "expired",
    "cancelled",
    "refund_requested",
    "refunded",
]

YES_NO_OPTIONS = ["yes", "no"]


def col_to_a1(index: int) -> str:
    letters = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def get_service():
    if not SERVICE_ACCOUNT_FILE.exists():
        raise SystemExit(f"Missing service account file: {SERVICE_ACCOUNT_FILE}")
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


def get_first_sheet(service, spreadsheet_id: str) -> tuple[dict, list[str]]:
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet = meta["sheets"][0]
    title = sheet["properties"]["title"]
    values = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=f"{title}!1:1")
        .execute()
        .get("values", [[]])
    )
    headers = values[0] if values else []
    return sheet, headers


def ensure_admin_columns(service, spreadsheet_id: str, sheet: dict, headers: list[str]) -> list[str]:
    title = sheet["properties"]["title"]
    missing = [column for column in ADMIN_COLUMNS if column not in headers]
    if not missing:
        print("admin_columns=already_present")
        return headers

    start_col = len(headers)
    end_col = start_col + len(missing) - 1
    range_name = f"{title}!{col_to_a1(start_col)}1:{col_to_a1(end_col)}1"
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body={"values": [missing]},
    ).execute()
    print(f"admin_columns=added count={len(missing)} columns={', '.join(missing)}")
    return [*headers, *missing]


def make_dropdown_rule(options: list[str]) -> dict:
    return {
        "condition": {
            "type": "ONE_OF_LIST",
            "values": [{"userEnteredValue": option} for option in options],
        },
        "showCustomUi": True,
        "strict": False,
    }


def format_sheet(service, spreadsheet_id: str, sheet: dict, headers: list[str]) -> None:
    sheet_id = sheet["properties"]["sheetId"]
    requests: list[dict] = [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {
                        "frozenRowCount": 1,
                        "frozenColumnCount": 1,
                    },
                },
                "fields": "gridProperties.frozenRowCount,gridProperties.frozenColumnCount",
            }
        },
        {
            "repeatCell": {
                "range": {"sheetId": sheet_id, "startRowIndex": 0, "endRowIndex": 1},
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.07, "green": 0.1, "blue": 0.16},
                        "textFormat": {
                            "bold": True,
                            "foregroundColor": {"red": 1, "green": 1, "blue": 1},
                        },
                        "horizontalAlignment": "CENTER",
                    }
                },
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
            }
        },
        {
            "autoResizeDimensions": {
                "dimensions": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": 0,
                    "endIndex": len(headers),
                }
            }
        },
    ]

    header_index = {name: idx for idx, name in enumerate(headers)}
    status_col = header_index.get("Client Status")
    if status_col is not None:
        requests.append(
            {
                "setDataValidation": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": 1000,
                        "startColumnIndex": status_col,
                        "endColumnIndex": status_col + 1,
                    },
                    "rule": make_dropdown_rule(STATUS_OPTIONS),
                }
            }
        )

    for name in ["Payment Verified", "Telegram Start Confirmed", "Telegram Verified", "Welcome Sent"]:
        col = header_index.get(name)
        if col is None:
            continue
        requests.append(
            {
                "setDataValidation": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": 1000,
                        "startColumnIndex": col,
                        "endColumnIndex": col + 1,
                    },
                    "rule": make_dropdown_rule(YES_NO_OPTIONS),
                }
            }
        )

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": requests},
    ).execute()
    print("format=applied")


def write_status_reference(service, spreadsheet_id: str) -> None:
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = meta["sheets"]
    existing = {item["properties"]["title"]: item["properties"]["sheetId"] for item in sheets}
    if "Status Reference" not in existing:
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": [{"addSheet": {"properties": {"title": "Status Reference"}}}]},
        ).execute()

    values = [
        ["Field", "Allowed Value", "Meaning"],
        ["Client Status", "pending_payment", "Form submitted, PayPal payment not confirmed"],
        ["Client Status", "paid_waiting_telegram", "Payment confirmed, Telegram /start or chat ID pending"],
        ["Client Status", "active", "Payment and Telegram connection confirmed"],
        ["Client Status", "expired", "One-month access ended"],
        ["Client Status", "cancelled", "Client stopped before renewal"],
        ["Client Status", "refund_requested", "Refund requested"],
        ["Client Status", "refunded", "Refund completed"],
        ["yes/no", "yes", "Confirmed"],
        ["yes/no", "no", "Not confirmed or not yet done"],
    ]
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range="'Status Reference'!A1:C10",
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()
    print("status_reference=updated")


def main() -> None:
    parser = argparse.ArgumentParser(description="Set up Starter Plan Google Sheet admin columns.")
    parser.add_argument("--spreadsheet-id", default=DEFAULT_SPREADSHEET_ID)
    parser.add_argument("--no-status-reference", action="store_true")
    args = parser.parse_args()

    service = get_service()
    try:
        sheet, headers = get_first_sheet(service, args.spreadsheet_id)
        updated_headers = ensure_admin_columns(service, args.spreadsheet_id, sheet, headers)
        format_sheet(service, args.spreadsheet_id, sheet, updated_headers)
        if not args.no_status_reference:
            write_status_reference(service, args.spreadsheet_id)
    except HttpError as exc:
        details = json.loads(exc.content.decode("utf-8")) if exc.content else {}
        reason = details.get("error", {}).get("message", str(exc))
        if exc.resp.status in {403, 404}:
            sa_email = json.loads(SERVICE_ACCOUNT_FILE.read_text(encoding="utf-8")).get("client_email", "")
            raise SystemExit(
                "Google Sheet access failed.\n"
                f"Share the sheet with this service account as Editor, then rerun:\n{sa_email}\n"
                f"Reason: {reason}"
            ) from exc
        raise


if __name__ == "__main__":
    main()
