#!/usr/bin/env python3
"""Create and format the LUA BIM LABS Revenue Ledger sheet."""

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
REVENUE_SHEET_TITLE = "Revenue Ledger"

HEADERS = [
    "Month",
    "Payment Date",
    "PayPal Transaction ID",
    "PayPal Payer Email",
    "Customer Email",
    "Customer Country",
    "Product",
    "Currency",
    "Gross Amount",
    "PayPal Fee",
    "Net Amount",
    "Payment Status",
    "Service Status",
    "Operator Registration Status",
    "VAT Review Type",
    "Zero-rate Review",
    "FX Date",
    "FX Source",
    "KRW Revenue Amount",
    "Withdrawal Date",
    "KRW Received",
    "PayPal Statement Saved",
    "Order/Application Evidence Saved",
    "Telegram Activation Evidence Saved",
    "Tax Review Status",
    "Evidence Folder",
    "Business Registration Review",
    "Notes",
]

YES_NO = ["yes", "no"]
PAYMENT_STATUS = ["paid", "refunded", "partially_refunded", "disputed", "cancelled", "needs_review"]
SERVICE_STATUS = ["pending_payment", "paid_waiting_telegram", "active", "expired", "cancelled", "refund_requested", "refunded"]
VAT_REVIEW = ["needs_review", "likely_zero_rate", "domestic_vat_review", "not_zero_rate", "tax_advisor_confirmed"]
OPERATOR_STATUS = ["non_registered_launch", "individual_business_registered", "corporate_registered", "needs_review"]
BUSINESS_REGISTRATION_REVIEW = ["not_needed_yet", "monitor", "review_this_month", "register_soon", "registered"]


def get_service():
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds)


def existing_sheets(service, spreadsheet_id: str) -> dict[str, int]:
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    return {s["properties"]["title"]: s["properties"]["sheetId"] for s in meta["sheets"]}


def ensure_sheet(service, spreadsheet_id: str) -> int:
    sheets = existing_sheets(service, spreadsheet_id)
    if REVENUE_SHEET_TITLE in sheets:
        return sheets[REVENUE_SHEET_TITLE]
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": [{"addSheet": {"properties": {"title": REVENUE_SHEET_TITLE}}}]},
    ).execute()
    return existing_sheets(service, spreadsheet_id)[REVENUE_SHEET_TITLE]


def col_to_a1(index: int) -> str:
    letters = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        letters = chr(65 + remainder) + letters
    return letters


def dropdown(options: list[str]) -> dict:
    return {
        "condition": {
            "type": "ONE_OF_LIST",
            "values": [{"userEnteredValue": option} for option in options],
        },
        "showCustomUi": True,
        "strict": False,
    }


def setup_revenue_sheet(service, spreadsheet_id: str) -> None:
    sheet_id = ensure_sheet(service, spreadsheet_id)
    end_col = col_to_a1(len(HEADERS) - 1)
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{REVENUE_SHEET_TITLE}'!A1:{end_col}1",
        valueInputOption="USER_ENTERED",
        body={"values": [HEADERS]},
    ).execute()

    header_index = {name: idx for idx, name in enumerate(HEADERS)}
    requests: list[dict] = [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {"frozenRowCount": 1, "frozenColumnCount": 3},
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
                        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
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
                    "endIndex": len(HEADERS),
                }
            }
        },
    ]

    for name, options in {
        "Payment Status": PAYMENT_STATUS,
        "Service Status": SERVICE_STATUS,
        "Operator Registration Status": OPERATOR_STATUS,
        "VAT Review Type": VAT_REVIEW,
        "Zero-rate Review": VAT_REVIEW,
        "Tax Review Status": VAT_REVIEW,
        "PayPal Statement Saved": YES_NO,
        "Order/Application Evidence Saved": YES_NO,
        "Telegram Activation Evidence Saved": YES_NO,
        "Business Registration Review": BUSINESS_REGISTRATION_REVIEW,
    }.items():
        col = header_index[name]
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
                    "rule": dropdown(options),
                }
            }
        )

    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": requests}).execute()
    print(f"revenue_sheet=ready title={REVENUE_SHEET_TITLE} columns={len(HEADERS)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Set up Revenue Ledger sheet.")
    parser.add_argument("--spreadsheet-id", default=DEFAULT_SPREADSHEET_ID)
    args = parser.parse_args()

    service = get_service()
    try:
        setup_revenue_sheet(service, args.spreadsheet_id)
    except HttpError as exc:
        details = json.loads(exc.content.decode("utf-8")) if exc.content else {}
        reason = details.get("error", {}).get("message", str(exc))
        raise SystemExit(f"Google Sheets setup failed: {reason}") from exc


if __name__ == "__main__":
    main()
