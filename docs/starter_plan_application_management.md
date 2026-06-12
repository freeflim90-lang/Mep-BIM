# Starter Plan Application Management

## Google Sheet

Use this sheet as the first-launch application database:

https://docs.google.com/spreadsheets/d/1v1t5k76mAhKSBx-x19fEw3Kmi7c6heFKMrkIbK_qcFk/edit?usp=sharing

## Operating Rule

The Google Sheet is the source of truth for application intake during the first launch.

PayPal remains the source of truth for payment confirmation.

Obsidian is the source of truth for internal learning and client service notes.

## Daily Admin Workflow

1. Open the Google Sheet.
2. Check new rows.
3. Match `Email used for PayPal payment` with PayPal payment records.
4. Mark `Payment Verified`.
5. Check Telegram username.
6. Register the client with `scripts/starter_plan_onboarding.py`.
7. Ask the client to open the Telegram bot and send `/start`.
8. Record the Telegram `chat_id`.
9. Mark `Telegram Verified`.
10. Set `Client Status`.
11. Create client profile and Obsidian note.
12. Send Telegram welcome message.

## Manual Columns to Add

Add these columns after the form response columns:

```text
Payment Verified
Telegram Verified
Client Status
Start Date
End Date
Obsidian Note
Admin Notes
```

## Local Onboarding Registry

Use the local Starter Plan registry for Telegram delivery:

```text
products/starter_plan/clients.json
```

Detailed onboarding commands:

```text
docs/starter_plan_telegram_onboarding_pipeline.md
```

## Status Values

```text
pending_payment
paid_waiting_telegram
active
expired
cancelled
refund_requested
refunded
```

## Client Status Logic

- `pending_payment`: form submitted, PayPal payment not confirmed.
- `paid_waiting_telegram`: payment confirmed, Telegram connection pending.
- `active`: payment and Telegram connection confirmed, lessons started.
- `expired`: one-month access ended.
- `cancelled`: client stopped before renewal.
- `refund_requested`: client requested refund.
- `refunded`: refund completed.

## Privacy Rule

Do not make the sheet public. Keep sharing limited to the operator account. The public link should not expose customer responses.
