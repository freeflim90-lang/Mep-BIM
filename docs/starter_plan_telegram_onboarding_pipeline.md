# Starter Plan Telegram Onboarding Pipeline

## Goal

Connect Google Form applications, PayPal payment confirmation, and Telegram lesson delivery without creating misunderstanding about the service scope.

## Source of Truth

- Google Form / Sheet: application intake and learning profile
- PayPal: payment confirmation
- `data/starter_plan/clients.json`: local service delivery registry
- Telegram: daily education delivery channel
- Obsidian: internal client learning and service notes

## Client Flow

1. Client opens the Google Form.
2. Client pays through PayPal.
3. Client submits the form with PayPal payment email and Telegram username.
4. Operator checks the Google Sheet and PayPal transaction.
5. Operator marks `Payment Verified` as `yes`.
6. Client opens the Telegram bot and sends `/start`.
7. Telegram sync script records the client's Telegram `chat_id` in Google Sheets.
8. Paid + Telegram-verified rows are mirrored into the local delivery registry.
9. Operator sends the welcome message.
10. Daily education script sends lessons only to active, paid, Telegram-verified clients.

## Telegram Rule

A Telegram bot generally cannot message a person first by username. The client must open the bot and send `/start` before the bot can send education messages.

Recommended form/onboarding text:

```text
After payment and form submission, please open the LUA BIM LABS Telegram bot and send /start.
Your service can begin only after PayPal payment is verified and Telegram connection is confirmed.
```

## Operator Commands

Recommended Telegram sync after clients send `/start`:

```bash
python3 scripts/starter_plan_sync_telegram_sheet.py
```

The same sync can run every 10 minutes through LaunchAgent:

```bash
~/Library/LaunchAgents/com.luabimlab.starter-telegram-sheet-sync.plist
```

This updates the Google Sheet:

- `Telegram Start Confirmed`
- `Telegram Chat ID`
- `Telegram Verified`
- `Client ID`
- `Client Status`
- `Start Date` and `End Date` when payment is verified
- `Next Action`

If `Payment Verified` is `yes`, the client is also mirrored into `data/starter_plan/clients.json` for daily lesson delivery.

Register a form submission:

```bash
python3 scripts/starter_plan_onboarding.py add-client \
  --name "Client Name" \
  --email "client@example.com" \
  --country "Country" \
  --preferred-language "English" \
  --paypal-email "paypal@example.com" \
  --telegram-username "@clientusername" \
  --current-bim-level "Beginner" \
  --main-mep-discipline "HVAC" \
  --learning-goal "Learn MEP BIM basics"
```

After PayPal verification:

```bash
python3 scripts/starter_plan_onboarding.py mark-paid \
  --client-id "starter-YYYYMMDD-client-xxxxxxxx" \
  --paypal-transaction-id "PAYPAL-TRANSACTION-ID"
```

After the client sends `/start`, record the Telegram chat ID:

```bash
python3 scripts/starter_plan_onboarding.py list-telegram-updates \
  --username "@clientusername"
```

Then either connect automatically from the latest matching update:

```bash
python3 scripts/starter_plan_onboarding.py connect-telegram \
  --client-id "starter-YYYYMMDD-client-xxxxxxxx"
```

Or set the chat ID manually:

```bash
python3 scripts/starter_plan_onboarding.py set-chat-id \
  --client-id "starter-YYYYMMDD-client-xxxxxxxx" \
  --chat-id "123456789"
```

Send onboarding message:

```bash
python3 scripts/starter_plan_onboarding.py send-welcome \
  --client-id "starter-YYYYMMDD-client-xxxxxxxx"
```

Create or update Obsidian client notes:

```bash
python3 scripts/starter_plan_onboarding.py export-obsidian --all
```

List current clients:

```bash
python3 scripts/starter_plan_onboarding.py list --status all
python3 scripts/starter_plan_onboarding.py list --status active
```

## Google Sheet Status Mapping

Use these values in the manual columns:

```text
pending_payment
paid_waiting_telegram
active
expired
cancelled
refund_requested
refunded
```

When the local script prints a status, copy that status back to the Google Sheet `Client Status` column.

## Daily Sending

The daily Telegram sender now reads:

- internal education users from the existing script
- active Starter clients from `data/starter_plan/clients.json`

A Starter client receives daily lessons only when all are true:

- `status` is `active`
- `payment_status` is `paid`
- `telegram_chat_id` exists

## Scope Protection

Keep these messages in the form, welcome message, and service page:

- The Starter Plan is general MEP BIM educational content only.
- Do not submit confidential project files, private drawings, contracts, personal data, or materials without permission.
- Project file review, Revit model QA, clash report review, engineering design verification, code compliance confirmation, and construction approval are not included.
